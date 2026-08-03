#!/usr/bin/env python3
"""Contract tests for the public Tguan rehabilitation Skills repository."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = {
    "tiguan-rehab",
    "tiguan-assessment-session-design",
    "tiguan-source-to-practice",
    "tiguan-practice-knowledge-base",
    "tiguan-service-ops",
    "tiguan-post-session-questioning",
    "tiguan-business-review",
}


class PublicRepoContractTest(unittest.TestCase):
    def test_required_public_entrypoints_exist(self) -> None:
        required = [
            "README.md",
            "README.en.md",
            "VERSION",
            "LICENSE",
            "docs/getting-started.md",
            "docs/skill-map.svg",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            "tools/build-skills.sh",
            "tools/check-publication-readiness.py",
            "tools/quick_validate_skill.py",
            "tools/install-workbuddy.sh",
            "tools/install-workbuddy.ps1",
        ]
        for relative_path in required:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_ci_uses_a_repository_owned_skill_validator(self) -> None:
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("tools/quick_validate_skill.py", workflow)
        self.assertIn("claude plugin validate .", workflow)
        self.assertNotIn("/tmp/quick_validate.py", workflow)

    def test_readme_covers_the_complete_user_journey(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        required_headings = [
            "## 这套 Skills 解决什么问题",
            "## 快速开始",
            "## 能力一览",
            "## 安装",
            "## 它怎样工作",
            "## 隐私与临床边界",
            "## 开源路线图",
            "## 项目结构",
            "## 许可证",
        ]
        for heading in required_headings:
            self.assertIn(heading, readme)
        self.assertIn("/tiguan-rehab", readme)
        self.assertIn("/tiguan-assessment-session-design", readme)
        self.assertIn("npx -y skills add", readme)
        self.assertIn("### 更新", readme)
        self.assertIn("更新体观康复 Skills", readme)
        self.assertIn("https://github.com/Bbaozizz/tiguan-rehab-skills/releases", readme)
        self.assertIn("### WorkBuddy 一键安装", readme)
        self.assertIn(
            "raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/"
            "tools/install-workbuddy.sh",
            readme,
        )
        self.assertIn("~/.workbuddy/skills", readme)
        self.assertIn("#### Windows", readme)
        self.assertIn(
            "raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/"
            "tools/install-workbuddy.ps1",
            readme,
        )
        for capability in [
            "实践认知校准",
            "可验证服务设计",
            "专业价值可见化",
            "执业系统诊断",
        ]:
            self.assertIn(capability, readme)
        self.assertIn("规划中的能力不等于已经可安装", readme)
        self.assertNotIn("GitHub Pages", readme)

    def test_public_surfaces_lead_with_the_five_path_first_run(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8")
        for text in [readme, guide]:
            self.assertIn("/tiguan-rehab", text)
            self.assertIn("五条", text)
            self.assertIn("附加的直接调用能力", text)
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("plugin.json", ci)
        self.assertIn("dist/skills/*.zip", release)

    def test_public_surfaces_explain_zero_infrastructure_first_success(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8")
        for text in [readme, guide]:
            self.assertIn("不需要先有知识库、客户档案、标准经营表或系统接口", text)
            self.assertIn("先让你讲出自己的理解", text)
            self.assertIn("7 天最小采集表", text)

    def test_public_guide_and_map_share_the_capability_framework(self) -> None:
        guide = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8")
        skill_map = (ROOT / "docs/skill-map.svg").read_text(encoding="utf-8")
        for capability in [
            "实践认知校准",
            "可验证服务设计",
            "专业价值可见化",
            "执业系统诊断",
        ]:
            self.assertIn(capability, guide)
            self.assertIn(capability, skill_map)
        self.assertIn("当前安装包包含 7 个已发布 Skill", guide)
        self.assertIn("只路由已发布能力", skill_map)
        self.assertIn("/tiguan-post-session-questioning", skill_map)
        self.assertIn("/tiguan-business-review", skill_map)

    def test_license_is_noncommercial_and_attribution_required(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("CC BY-NC 4.0", license_text)
        self.assertIn("Attribution", license_text)
        self.assertIn("NonCommercial", license_text)

    def test_relative_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in ROOT.rglob("*.md"):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(text):
                target = raw_target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                file_target = unquote(target.split("#", 1)[0])
                self.assertTrue(
                    (path.parent / file_target).resolve().exists(),
                    f"{path.relative_to(ROOT)} -> {target}",
                )

    def test_version_and_plugin_manifests_are_consistent(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

        plugin = json.loads(
            (ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )

        plugin_names = {Path(path).name for path in plugin["skills"]}
        self.assertEqual(plugin_names, SKILL_NAMES)
        self.assertEqual(marketplace["metadata"]["version"], version)
        self.assertEqual(
            {item["name"] for item in marketplace["plugins"]}, SKILL_NAMES
        )
        self.assertTrue(
            all(item["version"] == version for item in marketplace["plugins"])
        )

    def test_manifest_declares_the_five_day_zero_routes(self) -> None:
        plugin = json.loads(
            (ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            set(plugin["primaryRoutes"]),
            {
                "tiguan-source-to-practice",
                "tiguan-practice-knowledge-base",
                "tiguan-service-ops",
                "tiguan-post-session-questioning",
                "tiguan-business-review",
            },
        )

    def test_skill_packages_follow_public_skill_contract(self) -> None:
        for name in SKILL_NAMES:
            skill_dir = ROOT / "skills" / name
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), name)
            self.assertTrue((skill_dir / "agents/openai.yaml").is_file(), name)
            text = skill_md.read_text(encoding="utf-8")
            self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")
            self.assertIn("description:", text)

    def test_five_new_skills_have_distinct_first_success_contracts(self) -> None:
        expected_markers = {
            "tiguan-source-to-practice": [
                "不以“总结完资料”为成功",
                "来源事实",
                "最小实践动作",
                "验证标准",
            ],
            "tiguan-practice-knowledge-base": [
                "不以“收藏了多少资料”为成功",
                "来源指针",
                "已验证",
                "待验证",
            ],
            "tiguan-service-ops": [
                "preview -> confirm -> apply -> readback",
                "预约",
                "正式记录",
                "消课",
                "家庭作业卡",
            ],
            "tiguan-post-session-questioning": [
                "这是一场多轮追问",
                "一次只深挖一条",
                "档案没写不等于现场没做",
            ],
            "tiguan-business-review": [
                "未检查不能记0",
                "引流效率",
                "预约转化",
                "交付效率",
                "消课闭环",
            ],
        }
        for name, markers in expected_markers.items():
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, text, f"{name}: {marker}")

    def test_router_only_routes_released_capabilities(self) -> None:
        router = (ROOT / "skills/tiguan-rehab/SKILL.md").read_text(encoding="utf-8")
        for name in SKILL_NAMES - {"tiguan-rehab"}:
            self.assertIn(f"/{name}", router)
        self.assertNotIn("当前公开包尚未发布对应 Skill", router)

    def test_router_discovers_need_and_material_before_routing(self) -> None:
        router = (ROOT / "skills/tiguan-rehab/SKILL.md").read_text(encoding="utf-8")
        for marker in [
            "一次只问一个问题",
            "最想先解决",
            "已经有什么**脱敏或可公开**的材料",
            "最高需求相关性",
            "最短可复核反馈",
            "不要重复询问",
        ]:
            self.assertIn(marker, router, marker)

    def test_router_continues_into_first_success_without_reentry(self) -> None:
        router = (ROOT / "skills/tiguan-rehab/SKILL.md").read_text(encoding="utf-8")
        for marker in [
            "不要要求用户再输入 slash 命令",
            "立即开始叶子 Skill 的第一项实质动作",
            "最高需求：",
            "选中路由：",
            "选择一条路径",
            "现在开始",
        ]:
            self.assertIn(marker, router, marker)

        example = ROOT / "skills/tiguan-rehab/examples/guided-first-run.md"
        self.assertTrue(example.is_file())
        example_text = example.read_text(encoding="utf-8")
        self.assertIn("WorkBuddy", example_text)
        self.assertIn("第一轮只问", example_text)
        self.assertIn("/tiguan-rehab", example_text)

    def test_service_ops_keeps_business_states_separate(self) -> None:
        text = (ROOT / "skills/tiguan-service-ops/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("生成草稿不等于已写入", text)
        self.assertIn("正式记录写入不等于已消课", text)
        self.assertIn("消课不等于已发送客户提醒", text)
        self.assertIn("没有已配置适配器", text)

    def test_each_new_skill_has_a_synthetic_first_run(self) -> None:
        for name in SKILL_NAMES - {"tiguan-rehab", "tiguan-assessment-session-design"}:
            example = ROOT / "skills" / name / "examples/first-run.md"
            self.assertTrue(example.is_file(), name)
            text = example.read_text(encoding="utf-8")
            self.assertIn("合成", text, name)
            self.assertIn("第一次", text, name)

    def test_assessment_skill_treats_the_ten_question_form_as_a_starter(self) -> None:
        skill_dir = ROOT / "skills/tiguan-assessment-session-design"
        questionnaire = (skill_dir / "assets/intake-questionnaire-template.md").read_text(
            encoding="utf-8"
        )
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(
            re.findall(r"(?m)^## Q\d{2}\uff5c", questionnaire),
            [f"## Q{index:02d}\uff5c" for index in range(1, 11)],
        )
        self.assertIn("每题最多 6 个选项", questionnaire)
        self.assertIn("可多选，最多选择 2 项", questionnaire)
        self.assertIn("为了让康复师提前准备，你还有哪些资料可以提供？", questionnaire)
        self.assertNotIn("你之前尝试过什么？", questionnaire)
        self.assertIn("内置起步模板", questionnaire)
        self.assertIn("不要要求用户把自己的问卷改写成 Q01–Q10", skill_text)
        self.assertIn("自己的问卷优先", skill_text)

    def test_assessment_skill_separates_setup_prep_and_optional_post_session(self) -> None:
        skill_dir = ROOT / "skills/tiguan-assessment-session-design"
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

        for mode in ["问卷设置模式", "课前准备模式", "课后可选模式"]:
            self.assertIn(mode, skill_text)
        self.assertIn("保留原题号和问题原文", skill_text)
        self.assertIn("没有现场事实时停在课前准备", skill_text)

        pre_session_output = re.search(
            r"## 课前准备默认输出\n\n```text\n(?P<body>.*?)\n```",
            skill_text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(pre_session_output)
        body = pre_session_output.group("body")
        self.assertIn("脱敏答卷事实卡", body)
        self.assertIn("现场待追问", body)
        self.assertNotIn("客户提醒", body)
        self.assertNotIn("报告", body)
        self.assertNotIn("PDF", body)

    def test_public_guide_leads_with_questionnaire_setup_and_pre_session_prep(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8")
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")

        for text in [readme, guide]:
            self.assertIn("上传自己的问卷", text)
            self.assertIn("问卷答案", text)
            self.assertIn("课前准备", text)
            self.assertIn("PDF 是可选项", text)
        self.assertIn("upload your own questionnaire", english)
        self.assertIn("pre-session preparation", english)

    def test_assessment_skill_includes_first_success_examples(self) -> None:
        examples = ROOT / "skills/tiguan-assessment-session-design/examples"
        setup = examples / "questionnaire-setup-prompt.md"
        prep = examples / "custom-questionnaire-answers.md"

        self.assertTrue(setup.is_file())
        self.assertTrue(prep.is_file())
        self.assertIn("上传自己的问卷", setup.read_text(encoding="utf-8"))
        prep_text = prep.read_text(encoding="utf-8")
        self.assertIn("脱敏问卷答案", prep_text)
        self.assertIn("课前准备", prep_text)
        self.assertNotIn("Q01", prep_text)

    def test_public_files_do_not_leak_private_runtime_details(self) -> None:
        forbidden_patterns = [
            r"/Users/apple/",
            r"tiguan-studio-db",
            r"studio\.sqlite",
            r"appSecret",
            r"access[_-]?token",
            r"clients/by-name",
            r"feishu",
        ]
        public_suffixes = {
            ".md",
            ".html",
            ".json",
            ".yaml",
            ".yml",
            ".svg",
            ".py",
            ".sh",
        }
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in public_suffixes:
                continue
            if "tests" in path.parts or path.name == "check-publication-readiness.py":
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                self.assertIsNone(
                    re.search(pattern, text, flags=re.IGNORECASE),
                    f"{path.relative_to(ROOT)} matched {pattern}",
                )

    def test_assessment_renderer_escapes_input_and_creates_printable_html(self) -> None:
        input_data = {
            "client_label": "合成案例 <script>alert(1)</script>",
            "assessment_date": "2026-07-31",
            "primary_goal": "连续办公时更自在地转头",
            "baseline": ["转头到右侧约 45° 出现熟悉不适"],
            "session_findings": ["短时处理后动作范围有变化，需继续复测"],
            "life_action": "不适通常出现前起身，重新调整桌椅与前臂支撑",
            "next_retest": "在相同坐姿与时段重复转头基线",
            "boundaries": ["当次变化不等于长期疗效"],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.json"
            output_path = Path(temp_dir) / "report.html"
            input_path.write_text(
                json.dumps(input_data, ensure_ascii=False), encoding="utf-8"
            )
            result = subprocess.run(
                [
                    "python3",
                    str(
                        ROOT
                        / "skills/tiguan-assessment-session-design/scripts/render_report.py"
                    ),
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output_path.read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", html.lower())
            self.assertIn('rel="icon"', html)
            self.assertIn("window.print()", html)
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
            self.assertNotIn("<script>alert(1)</script>", html)


if __name__ == "__main__":
    unittest.main()
