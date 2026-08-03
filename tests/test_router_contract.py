#!/usr/bin/env python3
"""Static contract tests for the single-path public router."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from skill_registry import load_registry  # noqa: E402


class RouterContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.router = (ROOT / "skills/tiguan-rehab/SKILL.md").read_text(encoding="utf-8")
        self.contract = (
            ROOT / "skills/tiguan-rehab/references/task-contract.md"
        ).read_text(encoding="utf-8")

    def test_router_uses_exactly_the_five_manifest_primary_routes(self) -> None:
        registry = load_registry(ROOT)
        for route_id in registry.primary_route_ids:
            self.assertIn(f"/{route_id}", self.router)
        self.assertEqual(len(registry.primary_route_ids), 5)

    def test_router_refuses_broad_discovery_menus_and_multi_skill_plans(self) -> None:
        forbidden = ["扫描当前工作目录", "扫描工作区", "浏览工作区", "五个高频场景先列"]
        for marker in forbidden:
            self.assertNotIn(marker, self.router, marker)
        for marker in ["不得列出五条路径作为菜单", "不得预排多 Skill 链"]:
            self.assertIn(marker, self.router)

    def test_router_declares_the_six_field_contract_and_same_turn_handoff(self) -> None:
        for field in [
            "最高需求",
            "安全的已提供材料",
            "最小未知",
            "选中路由",
            "第一个可复核输出",
            "硬边界",
        ]:
            self.assertIn(field, self.contract)
        self.assertIn("同一对话", self.router)
        self.assertIn("立即开始叶子 Skill 的第一项实质动作", self.router)

    def test_assessment_is_direct_additional_capability_not_primary_route(self) -> None:
        self.assertIn("附加的直接调用能力", self.router)
        self.assertIn("/tiguan-assessment-session-design", self.router)
        self.assertNotIn(
            "| 设置自己的问卷，或用脱敏答卷做课前准备 | /tiguan-assessment-session-design",
            self.router,
        )

    def test_synthetic_cases_cover_ten_profiles_and_fixture_boundaries(self) -> None:
        cases = json.loads((ROOT / "evals/router/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 10)
        self.assertEqual({case["id"] for case in cases}, {f"P{i:02d}" for i in range(1, 11)})
        for case in cases:
            for field in ["expected_route", "first_success", "forbidden_behaviors", "hard_failures"]:
                self.assertIn(field, case, case["id"])
        p02 = next(case for case in cases if case["id"] == "P02")
        self.assertIn("个体化动作剂量", p02["forbidden_behaviors"])
        self.assertIn("临床处方", p02["hard_failures"])
        for profile_id in ["P03", "P09"]:
            case = next(case for case in cases if case["id"] == profile_id)
            self.assertIn("仅可使用明确提供的合成 fixture", case["hard_failures"])


if __name__ == "__main__":
    unittest.main()
