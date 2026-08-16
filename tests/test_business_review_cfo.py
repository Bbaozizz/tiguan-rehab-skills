#!/usr/bin/env python3
"""Behavior tests for the CFO extension of the business-review calculator."""

from __future__ import annotations

import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tiguan-business-review/scripts/analyze_business.py"


class BusinessReviewCfoTest(unittest.TestCase):
    def run_case(self, payload: dict) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.json"
            input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                ["python3", str(SCRIPT), "--input", str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )
        parsed = json.loads(result.stdout) if result.stdout else {}
        return result, parsed

    def with_metadata(self, payload: dict) -> dict:
        fields = [key for key, value in payload.items() if isinstance(value, (int, float))]
        return {
            "period": "2026-08",
            "source_note": "synthetic monthly example; no client-level data",
            "metric_definitions": {field: f"definition for {field}" for field in fields},
            **payload,
        }

    def test_solo_shop_calculates_three_lines_and_capacity_gate(self) -> None:
        payload = self.with_metadata(
            {
                "business_type": "solo_shop",
                "average_revenue_per_session": 320,
                "variable_cost_per_session": 20,
                "fixed_operating_cost": 3500,
                "owner_target_wage": 8000,
                "fixed_staff_cost": 0,
                "reserve_target": 2000,
                "realistic_monthly_capacity": 64.5,
                "planned_utilization_rate": 0.7,
                "average_sessions_per_active_client": 3,
            }
        )
        result, output = self.run_case(payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        model = output["operating_model"]
        self.assertEqual(model["survival_line_sessions"], 12)
        self.assertEqual(model["owner_wage_line_sessions"], 39)
        self.assertEqual(model["healthy_line_sessions"], 45)
        self.assertAlmostEqual(model["effective_capacity_sessions"], 45.15)
        self.assertTrue(model["healthy_capacity_feasible"])
        self.assertEqual(model["healthy_required_active_clients"], 15)

    def test_cash_only_does_not_claim_business_health(self) -> None:
        result, output = self.run_case(
            self.with_metadata({"cash_collected": 20000})
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["operating_model"]["status"], "unknown")
        self.assertEqual(output["priority"]["code"], "collect_data")
        self.assertIn("delivered_revenue", output["unknown_fields"]["current_period"])

    def test_prepaid_delivery_risk_blocks_expansion_advice(self) -> None:
        payload = self.with_metadata(
            {
                "cash_collected": 20000,
                "delivered_revenue": 10500,
                "prepaid_remaining_liability": 28000,
                "prepaid_clients_with_future_booking": 8,
                "prepaid_clients_without_future_booking": 12,
                "fixed_operating_cost": 4000,
                "owner_target_wage": 8000,
                "fixed_staff_cost": 0,
            }
        )
        result, output = self.run_case(payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["priority"]["code"], "prepaid_delivery_risk")
        self.assertAlmostEqual(
            output["cash_and_obligation"]["prepaid_unbooked_client_rate"], 0.6
        )
        self.assertEqual(output["current_delivery"]["owner_wage_coverage_gap"], -1500)

    def test_non_finite_cfo_value_is_rejected_as_standard_json(self) -> None:
        for value in [math.nan, math.inf, -math.inf]:
            result, output = self.run_case(
                self.with_metadata({"average_revenue_per_session": value})
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output["status"], "invalid")
            self.assertNotIn("NaN", result.stdout)
            self.assertNotIn("Infinity", result.stdout)

    def test_builtin_verification_covers_three_business_forms(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--verify"],
            check=False,
            capture_output=True,
            text=True,
        )
        output = json.loads(result.stdout) if result.stdout else {}
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["status"], "ok")
        self.assertEqual(set(output["checks"]), {"freelance", "solo_shop", "small_studio"})


if __name__ == "__main__":
    unittest.main()
