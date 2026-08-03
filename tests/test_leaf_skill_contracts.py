#!/usr/bin/env python3
"""Contracts that keep each Day-0 leaf safe and independently usable."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_LEAVES = {
    "tiguan-source-to-practice",
    "tiguan-practice-knowledge-base",
    "tiguan-service-ops",
    "tiguan-post-session-questioning",
    "tiguan-business-review",
}


class LeafSkillContractTest(unittest.TestCase):
    def test_each_leaf_has_a_safe_first_success_and_return_boundary(self) -> None:
        for skill_id in PRIMARY_LEAVES:
            text = (ROOT / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
            evals = json.loads(
                (ROOT / "skills" / skill_id / "evals/evals.json").read_text(encoding="utf-8")
            )
            for marker in [
                "任务契约",
                "第一个可复核输出",
                "只使用当前对话、附件和用户明确点名",
                "未知",
                "## 返回入口",
                "返回 `/tiguan-rehab`",
                "不得直接路由到另一个叶子 Skill",
            ]:
                self.assertIn(marker, text, f"{skill_id}: {marker}")
            self.assertGreaterEqual(len(evals), 2, skill_id)
            self.assertEqual({item["kind"] for item in evals}, {"positive", "near_miss"})

    def test_source_to_practice_never_turns_unconfirmed_sources_into_prescriptions(self) -> None:
        text = (ROOT / "skills/tiguan-source-to-practice/SKILL.md").read_text(encoding="utf-8")
        for marker in ["合成、非个体化或未确认", "不得生成个体化动作、剂量、频率、排课或处方"]:
            self.assertIn(marker, text)

    def test_source_to_practice_asks_for_the_users_model_before_teaching(self) -> None:
        text = (ROOT / "skills/tiguan-source-to-practice/SKILL.md").read_text(encoding="utf-8")
        for marker in [
            "先问后教",
            "不要先总结资料或告诉用户怎么用",
            "请先用你自己的话说说",
            "理解一致",
            "遗漏",
            "误解",
            "过度推断",
        ]:
            self.assertIn(marker, text)

    def test_knowledge_base_separates_source_observation_and_verification(self) -> None:
        text = (ROOT / "skills/tiguan-practice-knowledge-base/SKILL.md").read_text(encoding="utf-8")
        for marker in ["来源事实", "当事人观察", "已验证必须指向真实使用结果"]:
            self.assertIn(marker, text)
        self.assertIn("个人知识库不是其他 Skill 的使用前提", text)
        self.assertIn("没有现成知识库", text)

    def test_service_ops_requires_preview_authorization_adapter_and_readback(self) -> None:
        text = (ROOT / "skills/tiguan-service-ops/SKILL.md").read_text(encoding="utf-8")
        for marker in ["preview -> confirm -> apply -> readback", "明确授权", "已配置适配器", "独立回读"]:
            self.assertIn(marker, text)

    def test_service_ops_has_a_useful_zero_adapter_draft_mode(self) -> None:
        text = (ROOT / "skills/tiguan-service-ops/SKILL.md").read_text(encoding="utf-8")
        for marker in [
            "没有客户档案或适配器",
            "一次服务的脱敏口述",
            "专业记录草稿",
            "客户回家说明",
            "下次关注点",
            "不得把便于理解的补充写成已确认内容",
            "AI 建议待治疗师确认",
            "不得把描述性观察改写成改善、有效、进步或因果结论",
            "未知项只写缺少的字段",
            "治疗师已确认的下次关注点",
            "没有明确计划时写“未提供”",
        ]:
            self.assertIn(marker, text)

    def test_post_session_questioning_preserves_record_gaps_as_questions(self) -> None:
        text = (ROOT / "skills/tiguan-post-session-questioning/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("档案没写不等于现场没做", text)
        self.assertIn("现场待追问", text)
        self.assertIn("没有现成档案", text)
        self.assertIn("事后新陈述", text)

    def test_business_review_keeps_missing_data_unknown(self) -> None:
        text = (ROOT / "skills/tiguan-business-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("未检查不能记0", text)
        self.assertIn("缺失业务数据保持 `unknown`", text)

    def test_business_review_owns_the_zero_data_collection_path(self) -> None:
        text = (ROOT / "skills/tiguan-business-review/SKILL.md").read_text(encoding="utf-8")
        for marker in [
            "没有标准表格也能开始",
            "零数据模式",
            "7 天最小采集表",
            "数据记录在哪里",
            "不能把“请补数据”当作本次交付",
        ]:
            self.assertIn(marker, text)
        template = ROOT / "skills/tiguan-business-review/assets/minimum-7-day-collection.csv"
        self.assertTrue(template.is_file())
        header = template.read_text(encoding="utf-8").splitlines()[0]
        for field in ["date", "inquiries", "booked_first_sessions", "scheduled_sessions", "completed_sessions"]:
            self.assertIn(field, header)


if __name__ == "__main__":
    unittest.main()
