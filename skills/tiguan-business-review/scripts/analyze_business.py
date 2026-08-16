#!/usr/bin/env python3
"""Calculate an auditable operating model for a small health service business."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


FUNNEL_METRICS = (
    ("inquiry_to_booking", "booked_first_sessions", "inquiries", 0.35),
    ("appointment_completion", "completed_sessions", "scheduled_sessions", 0.80),
    ("delivery_efficiency", "delivered_sold_sessions", "sold_sessions", 0.65),
    ("checkout_closure", "checked_out_sessions", "completed_sessions", 0.95),
)

FUNNEL_PRIORITIES = {
    "inquiry_to_booking": ("booking_conversion", "先检查咨询到首次预约的转化"),
    "appointment_completion": ("appointment_completion", "先降低预约后的到店流失"),
    "delivery_efficiency": ("delivery_efficiency", "先检查已售服务的交付节奏"),
    "checkout_closure": ("checkout_closure", "先补齐服务完成后的消课闭环"),
}

BUSINESS_TYPES = {"freelance", "solo_shop", "small_studio"}

NUMBER_FIELDS = {
    "cash_collected",
    "delivered_revenue",
    "prepaid_remaining_liability",
    "prepaid_clients_with_future_booking",
    "prepaid_clients_without_future_booking",
    "average_revenue_per_session",
    "variable_cost_per_session",
    "fixed_operating_cost",
    "owner_target_wage",
    "fixed_staff_cost",
    "reserve_target",
    "realistic_monthly_capacity",
    "planned_utilization_rate",
    "average_sessions_per_active_client",
    "inquiries",
    "booked_first_sessions",
    "scheduled_sessions",
    "completed_sessions",
    "sold_sessions",
    "delivered_sold_sessions",
    "checked_out_sessions",
}

CFO_MODEL_FIELDS = (
    "average_revenue_per_session",
    "variable_cost_per_session",
    "fixed_operating_cost",
    "owner_target_wage",
    "fixed_staff_cost",
    "reserve_target",
    "realistic_monthly_capacity",
    "planned_utilization_rate",
)

CURRENT_PERIOD_FIELDS = (
    "cash_collected",
    "delivered_revenue",
    "prepaid_remaining_liability",
    "prepaid_clients_with_future_booking",
    "prepaid_clients_without_future_booking",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Path to a de-identified input JSON")
    group.add_argument("--verify", action="store_true", help="Run built-in checks")
    return parser.parse_args()


def rounded(value: float) -> float:
    return round(value, 6)


def parse_numbers(payload: Dict[str, Any], errors: List[str]) -> Dict[str, Optional[float]]:
    numbers: Dict[str, Optional[float]] = {}
    for field in NUMBER_FIELDS:
        if field not in payload or payload[field] is None:
            numbers[field] = None
            continue
        value = payload[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be a non-negative number")
            numbers[field] = None
            continue
        if not math.isfinite(value) or value < 0:
            errors.append(f"{field} must be a non-negative number")
            numbers[field] = None
            continue
        numbers[field] = float(value)
    rate = numbers["planned_utilization_rate"]
    if rate is not None and rate > 1:
        errors.append("planned_utilization_rate must be between 0 and 1")
    return numbers


def provenance_conflicts(payload: Dict[str, Any]) -> List[str]:
    """Validate period, source and definitions without inventing provenance."""
    conflicts: List[str] = []
    period = payload.get("period")
    source_note = payload.get("source_note")
    definitions = payload.get("metric_definitions")
    if not isinstance(period, str) or not period.strip():
        conflicts.append("missing period metadata")
    if not isinstance(source_note, str) or not source_note.strip():
        conflicts.append("missing source_note metadata")
    if not isinstance(definitions, dict):
        conflicts.append("missing metric_definitions metadata")
        definitions = {}
    for field in sorted(NUMBER_FIELDS):
        if payload.get(field) is None:
            continue
        definition = definitions.get(field)
        if not isinstance(definition, str) or not definition.strip():
            conflicts.append(f"missing metric definition: {field}")
    declared = payload.get("metadata")
    if declared is not None:
        if not isinstance(declared, dict):
            conflicts.append("metadata must be an object")
        else:
            if "period" in declared and declared["period"] != period:
                conflicts.append("contradictory period metadata")
            if "source_note" in declared and declared["source_note"] != source_note:
                conflicts.append("contradictory source metadata")
    return conflicts


def missing(numbers: Dict[str, Optional[float]], fields: Tuple[str, ...]) -> List[str]:
    return [field for field in fields if numbers[field] is None]


def calculate_funnel_metric(
    numbers: Dict[str, Optional[float]],
    name: str,
    numerator_field: str,
    denominator_field: str,
    threshold: float,
    errors: List[str],
) -> Dict[str, Any]:
    numerator = numbers[numerator_field]
    denominator = numbers[denominator_field]
    result: Dict[str, Any] = {
        "value": None,
        "status": "unknown",
        "numerator_field": numerator_field,
        "denominator_field": denominator_field,
        "numerator": numerator,
        "denominator": denominator,
        "default_threshold": threshold,
    }
    if numerator is None or denominator is None:
        result["reason"] = "missing numerator or denominator"
        return result
    if numerator > denominator:
        errors.append(
            f"{numerator_field} ({numerator:g}) cannot exceed "
            f"{denominator_field} ({denominator:g})"
        )
        result["status"] = "invalid"
        return result
    if denominator == 0:
        result["reason"] = "denominator is zero"
        return result
    value = numerator / denominator
    result["value"] = rounded(value)
    result["status"] = "below_default_threshold" if value < threshold else "ok"
    return result


def calculate_operating_model(
    numbers: Dict[str, Optional[float]], errors: List[str]
) -> Dict[str, Any]:
    p = numbers["average_revenue_per_session"]
    v = numbers["variable_cost_per_session"]
    f = numbers["fixed_operating_cost"]
    w = numbers["owner_target_wage"]
    labor = numbers["fixed_staff_cost"]
    reserve = numbers["reserve_target"]
    capacity = numbers["realistic_monthly_capacity"]
    utilization = numbers["planned_utilization_rate"]
    sessions_per_client = numbers["average_sessions_per_active_client"]

    result: Dict[str, Any] = {
        "status": "unknown",
        "unit_contribution": None,
        "survival_line_sessions": None,
        "owner_wage_line_sessions": None,
        "healthy_line_sessions": None,
        "effective_capacity_sessions": None,
        "healthy_capacity_gap_sessions": None,
        "healthy_capacity_feasible": None,
        "healthy_required_active_clients": None,
    }

    if p is not None and v is not None:
        if p <= v:
            errors.append(
                "average_revenue_per_session must be greater than variable_cost_per_session"
            )
            return result
        contribution = p - v
        result["unit_contribution"] = rounded(contribution)

        if f is not None and labor is not None:
            result["survival_line_sessions"] = math.ceil((f + labor) / contribution)
            if w is not None:
                result["owner_wage_line_sessions"] = math.ceil(
                    (f + labor + w) / contribution
                )
                if reserve is not None:
                    result["healthy_line_sessions"] = math.ceil(
                        (f + labor + w + reserve) / contribution
                    )

    if capacity is not None and utilization is not None:
        result["effective_capacity_sessions"] = rounded(capacity * utilization)

    healthy_line = result["healthy_line_sessions"]
    effective_capacity = result["effective_capacity_sessions"]
    if healthy_line is not None and effective_capacity is not None:
        gap = effective_capacity - healthy_line
        result["healthy_capacity_gap_sessions"] = rounded(gap)
        result["healthy_capacity_feasible"] = gap >= 0

    if healthy_line is not None and sessions_per_client is not None:
        if sessions_per_client == 0:
            errors.append("average_sessions_per_active_client must be greater than 0")
        else:
            result["healthy_required_active_clients"] = math.ceil(
                healthy_line / sessions_per_client
            )

    known = sum(
        result[field] is not None
        for field in (
            "unit_contribution",
            "survival_line_sessions",
            "owner_wage_line_sessions",
            "healthy_line_sessions",
            "effective_capacity_sessions",
        )
    )
    result["status"] = "complete" if known == 5 else ("partial" if known else "unknown")
    return result


def calculate_current_delivery(numbers: Dict[str, Optional[float]]) -> Dict[str, Any]:
    delivered = numbers["delivered_revenue"]
    f = numbers["fixed_operating_cost"]
    w = numbers["owner_target_wage"]
    labor = numbers["fixed_staff_cost"]
    reserve = numbers["reserve_target"]
    completed = numbers["completed_sessions"]
    variable = numbers["variable_cost_per_session"]

    result: Dict[str, Any] = {
        "basis": "unknown",
        "known_variable_cost": None,
        "owner_wage_coverage_gap": None,
        "healthy_coverage_gap": None,
    }
    if delivered is None or f is None or w is None or labor is None:
        return result

    contribution = delivered
    result["basis"] = "before_variable_costs"
    if completed is not None and variable is not None:
        known_variable_cost = completed * variable
        result["known_variable_cost"] = rounded(known_variable_cost)
        contribution -= known_variable_cost
        result["basis"] = "after_known_variable_costs"

    result["owner_wage_coverage_gap"] = rounded(contribution - f - labor - w)
    if reserve is not None:
        result["healthy_coverage_gap"] = rounded(contribution - f - labor - w - reserve)
    return result


def calculate_cash_and_obligation(numbers: Dict[str, Optional[float]]) -> Dict[str, Any]:
    cash = numbers["cash_collected"]
    delivered = numbers["delivered_revenue"]
    liability = numbers["prepaid_remaining_liability"]
    booked = numbers["prepaid_clients_with_future_booking"]
    unbooked = numbers["prepaid_clients_without_future_booking"]
    result: Dict[str, Any] = {
        "cash_minus_delivered_revenue": None,
        "prepaid_remaining_liability": liability,
        "prepaid_booking_coverage_rate": None,
        "prepaid_unbooked_client_rate": None,
        "majority_without_future_booking": None,
    }
    if cash is not None and delivered is not None:
        result["cash_minus_delivered_revenue"] = rounded(cash - delivered)
    if booked is not None and unbooked is not None:
        total = booked + unbooked
        if total > 0:
            result["prepaid_booking_coverage_rate"] = rounded(booked / total)
            result["prepaid_unbooked_client_rate"] = rounded(unbooked / total)
            result["majority_without_future_booking"] = unbooked > booked
    return result


def choose_priority(
    operating: Dict[str, Any],
    current_delivery: Dict[str, Any],
    cash_and_obligation: Dict[str, Any],
    funnel: Dict[str, Dict[str, Any]],
) -> Dict[str, str]:
    if operating["healthy_capacity_feasible"] is False:
        return {
            "code": "structural_capacity_gap",
            "label": "先修正价格、成本、服务结构或产能，当前健康目标超过现实产能",
            "trigger": "healthy_capacity_feasible",
        }

    liability = cash_and_obligation["prepaid_remaining_liability"]
    majority_unbooked = cash_and_obligation["majority_without_future_booking"]
    if liability is not None and liability > 0 and majority_unbooked is True:
        return {
            "code": "prepaid_delivery_risk",
            "label": "先检查剩课客户节奏与未来预约，不继续放大待交付责任",
            "trigger": "majority_without_future_booking",
        }

    for metric_name, _, _, _ in FUNNEL_METRICS:
        if funnel[metric_name]["status"] == "below_default_threshold":
            code, label = FUNNEL_PRIORITIES[metric_name]
            return {"code": code, "label": label, "trigger": metric_name}

    owner_gap = current_delivery["owner_wage_coverage_gap"]
    if owner_gap is not None and owner_gap < 0:
        return {
            "code": "owner_wage_gap",
            "label": "本期已交付收入尚未覆盖经营成本与老板目标工资，先定位收入缺口来自哪一环",
            "trigger": "owner_wage_coverage_gap",
        }

    if operating["status"] != "complete":
        return {
            "code": "collect_data",
            "label": "先补齐最小 CFO 数据，不用现金流水直接判断经营健康",
            "trigger": "incomplete_operating_model",
        }

    if all(funnel[name]["status"] == "ok" for name, _, _, _ in FUNNEL_METRICS):
        return {
            "code": "hold_and_review",
            "label": "当前模型与基础漏斗无明显结构性断点，保持同口径并做一周复查",
            "trigger": "all_checked_metrics",
        }

    return {
        "code": "collect_current_period",
        "label": "经营模型已可计算，下一步补本期交付、剩课与漏斗事实",
        "trigger": "insufficient_current_period_data",
    }


def analyze_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    business_type = payload.get("business_type")
    if business_type is not None and business_type not in BUSINESS_TYPES:
        errors.append(
            "business_type must be one of freelance, solo_shop, small_studio"
        )

    numbers = parse_numbers(payload, errors)
    operating = calculate_operating_model(numbers, errors)
    funnel = {
        name: calculate_funnel_metric(
            numbers, name, numerator, denominator, threshold, errors
        )
        for name, numerator, denominator, threshold in FUNNEL_METRICS
    }
    if errors:
        return {"status": "invalid", "errors": errors}

    current_delivery = calculate_current_delivery(numbers)
    cash_and_obligation = calculate_cash_and_obligation(numbers)
    warnings: List[str] = []
    if cash_and_obligation["cash_minus_delivered_revenue"] is not None:
        warnings.append(
            "cash_minus_delivered_revenue is a timing difference, not profit or the change in prepaid liability"
        )
    if current_delivery["basis"] == "before_variable_costs":
        warnings.append(
            "current delivery gaps are before variable costs because completed_sessions or variable_cost_per_session is unknown"
        )
    if cash_and_obligation["majority_without_future_booking"] is True:
        warnings.append(
            "more prepaid clients lack a future booking than have one; inspect service rhythm and delivery capacity"
        )

    return {
        "status": "ok",
        "period": payload.get("period"),
        "business_type": business_type,
        "source_note": payload.get("source_note"),
        "facts": {
            "cash_collected": numbers["cash_collected"],
            "delivered_revenue": numbers["delivered_revenue"],
            "prepaid_remaining_liability": numbers["prepaid_remaining_liability"],
        },
        "operating_model": operating,
        "current_delivery": current_delivery,
        "cash_and_obligation": cash_and_obligation,
        "metrics": funnel,
        "funnel_metrics": funnel,
        "priority": choose_priority(
            operating, current_delivery, cash_and_obligation, funnel
        ),
        "unknown_fields": {
            "cfo_model": missing(numbers, CFO_MODEL_FIELDS),
            "current_period": missing(numbers, CURRENT_PERIOD_FIELDS),
            "funnel": sorted(
                {
                    field
                    for _, numerator, denominator, _ in FUNNEL_METRICS
                    for field in (numerator, denominator)
                    if numbers[field] is None
                }
            ),
        },
        "warnings": warnings,
    }


def verify_calculator() -> Dict[str, Any]:
    cases = {
        "freelance": (
            {
                "business_type": "freelance",
                "average_revenue_per_session": 320,
                "variable_cost_per_session": 100,
                "fixed_operating_cost": 800,
                "owner_target_wage": 8000,
                "fixed_staff_cost": 0,
                "reserve_target": 2000,
                "realistic_monthly_capacity": 86,
                "planned_utilization_rate": 0.60,
            },
            50,
            51.6,
        ),
        "solo_shop": (
            {
                "business_type": "solo_shop",
                "average_revenue_per_session": 320,
                "variable_cost_per_session": 20,
                "fixed_operating_cost": 3500,
                "owner_target_wage": 8000,
                "fixed_staff_cost": 0,
                "reserve_target": 2000,
                "realistic_monthly_capacity": 64.5,
                "planned_utilization_rate": 0.70,
                "average_sessions_per_active_client": 3,
            },
            45,
            45.15,
        ),
        "small_studio": (
            {
                "business_type": "small_studio",
                "average_revenue_per_session": 380,
                "variable_cost_per_session": 150,
                "fixed_operating_cost": 6000,
                "owner_target_wage": 8000,
                "fixed_staff_cost": 3000,
                "reserve_target": 3000,
                "realistic_monthly_capacity": 129,
                "planned_utilization_rate": 0.70,
            },
            87,
            90.3,
        ),
    }
    checks: Dict[str, Any] = {}
    for name, (payload, expected_line, expected_capacity) in cases.items():
        output = analyze_payload(payload)
        actual_line = output["operating_model"]["healthy_line_sessions"]
        actual_capacity = output["operating_model"]["effective_capacity_sessions"]
        passed = (
            output["status"] == "ok"
            and actual_line == expected_line
            and abs(actual_capacity - expected_capacity) < 1e-9
        )
        checks[name] = {
            "passed": passed,
            "healthy_line_sessions": actual_line,
            "effective_capacity_sessions": actual_capacity,
        }
    return {
        "status": "ok"
        if all(item["passed"] for item in checks.values())
        else "failed",
        "checks": checks,
    }


def main() -> int:
    args = parse_args()
    if args.verify:
        output = verify_calculator()
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if output["status"] == "ok" else 1

    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    if not isinstance(payload, dict):
        print(
            json.dumps(
                {"status": "invalid", "errors": ["input root must be an object"]},
                ensure_ascii=False,
            )
        )
        return 2

    metadata_conflicts = provenance_conflicts(payload)
    if metadata_conflicts:
        print(
            json.dumps(
                {
                    "status": "invalid",
                    "errors": ["invalid metric provenance metadata"],
                    "metadata_conflicts": metadata_conflicts,
                },
                ensure_ascii=False,
            )
        )
        return 2

    output = analyze_payload(payload)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
