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
        self.assertNotIn("GitHub Pages", readme)

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

    def test_skill_packages_follow_public_skill_contract(self) -> None:
        for name in SKILL_NAMES:
            skill_dir = ROOT / "skills" / name
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), name)
            self.assertTrue((skill_dir / "agents/openai.yaml").is_file(), name)
            text = skill_md.read_text(encoding="utf-8")
            self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")
            self.assertIn("description:", text)

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
