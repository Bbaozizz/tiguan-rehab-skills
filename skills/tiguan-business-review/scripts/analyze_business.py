#!/usr/bin/env python3
"""Calculate a small, auditable service-business funnel from de-identified JSON."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


METRICS = (
    ("inquiry_to_booking", "booked_first_sessions", "inquiries", 0.35),
    ("appointment_completion", "completed_sessions", "scheduled_sessions", 0.80),
    ("delivery_efficiency", "delivered_sold_sessions", "sold_sessions", 0.65),
    ("checkout_closure", "checked_out_sessions", "completed_sessions", 0.95),
)

PRIORITIES = {
    "inquiry_to_booking": {
        "code": "booking_conversion",
        "label": "先提升预约转化",
    },
    "appointment_completion": {
        "code": "appointment_completion",
        "label": "先降低预约流失",
    },
    "delivery_efficiency": {
        "code": "delivery_efficiency",
        "label": "先提升已售课交付效率",
    },
    "checkout_closure": {
        "code": "checkout_closure",
        "label": "先补齐消课闭环",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to the input JSON")
    return parser.parse_args()


def read_number(payload: Dict[str, Any], field: str, errors: List[str]) -> Optional[float]:
    if field not in payload or payload[field] is None:
        return None
    value = payload[field]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{field} must be a non-negative number")
        return None
    if not math.isfinite(value) or value < 0:
        errors.append(f"{field} must be a non-negative number")
        return None
    return float(value)


def calculate_metric(
    payload: Dict[str, Any],
    name: str,
    numerator_field: str,
    denominator_field: str,
    threshold: float,
    errors: List[str],
) -> Dict[str, Any]:
    numerator = read_number(payload, numerator_field, errors)
    denominator = read_number(payload, denominator_field, errors)
    result: Dict[str, Any] = {
        "value": None,
        "status": "unknown",
        "numerator_field": numerator_field,
        "denominator_field": denominator_field,
        "numerator": numerator,
        "denominator": denominator,
        "threshold": threshold,
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
    result["value"] = round(value, 6)
    result["status"] = "below_threshold" if value < threshold else "ok"
    return result


def choose_priority(metrics: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    for metric_name, _, _, _ in METRICS:
        if metrics[metric_name]["status"] == "below_threshold":
            priority = dict(PRIORITIES[metric_name])
            priority["trigger_metric"] = metric_name
            return priority
    if all(metrics[name]["status"] == "ok" for name, _, _, _ in METRICS):
        return {
            "code": "acquisition_scale",
            "label": "当前基础漏斗无明显断点，再验证有效引流",
            "trigger_metric": "all_core_metrics",
        }
    return {
        "code": "collect_data",
        "label": "先补齐最小经营数据",
        "trigger_metric": "insufficient_data",
    }


def provenance_conflicts(payload: Dict[str, Any]) -> List[str]:
    """Return explicit metadata conflicts without inventing missing provenance."""
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
    for _, numerator, denominator, _ in METRICS:
        for field in (numerator, denominator):
            definition = definitions.get(field)
            if payload.get(field) is not None and (
                not isinstance(definition, str) or not definition.strip()
            ):
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


def main() -> int:
    args = parse_args()
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

    errors: List[str] = []
    metrics = {
        name: calculate_metric(
            payload, name, numerator, denominator, threshold, errors
        )
        for name, numerator, denominator, threshold in METRICS
    }
    if errors:
        print(json.dumps({"status": "invalid", "errors": errors}, ensure_ascii=False))
        return 2

    output = {
        "status": "ok",
        "period": payload.get("period"),
        "metrics": metrics,
        "priority": choose_priority(metrics),
        "unknown_fields": sorted(
            {
                field
                for _, numerator, denominator, _ in METRICS
                for field in (numerator, denominator)
                if field not in payload or payload[field] is None
            }
        ),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
