#!/usr/bin/env python3
"""Behavior tests for the deterministic business-review calculator."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tiguan-business-review/scripts/analyze_business.py"


class BusinessReviewTest(unittest.TestCase):
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

    def test_missing_fields_stay_unknown_instead_of_becoming_zero(self) -> None:
        result, output = self.run_case({"period": "2026-07"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(output["metrics"]["inquiry_to_booking"]["value"])
        self.assertEqual(output["metrics"]["inquiry_to_booking"]["status"], "unknown")
        self.assertEqual(output["priority"]["code"], "collect_data")

    def test_lowest_actionable_stage_becomes_current_priority(self) -> None:
        payload = {
            "period": "2026-07",
            "inquiries": 100,
            "booked_first_sessions": 20,
            "scheduled_sessions": 50,
            "completed_sessions": 45,
            "checked_out_sessions": 45,
            "sold_sessions": 80,
            "delivered_sold_sessions": 24,
        }
        result, output = self.run_case(payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["priority"]["code"], "booking_conversion")
        self.assertAlmostEqual(output["metrics"]["inquiry_to_booking"]["value"], 0.2)
        self.assertAlmostEqual(output["metrics"]["delivery_efficiency"]["value"], 0.3)

    def test_impossible_funnel_is_rejected(self) -> None:
        result, output = self.run_case(
            {"period": "2026-07", "inquiries": 3, "booked_first_sessions": 4}
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output["status"], "invalid")
        self.assertIn("booked_first_sessions", output["errors"][0])


if __name__ == "__main__":
    unittest.main()
