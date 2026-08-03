#!/usr/bin/env python3
"""Tests for deterministic published-Skill routing contract checks."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check-routing-contract.py"


class RoutingContractToolTest(unittest.TestCase):
    def run_checker(self, repo_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(CHECKER), "--repo-root", str(repo_root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_repository_passes(self) -> None:
        result = self.run_checker(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_missing_return_direct_leaf_route_and_broad_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "repo"
            shutil.copytree(ROOT, clone)
            leaf = clone / "skills/tiguan-source-to-practice/SKILL.md"
            leaf.write_text(
                leaf.read_text(encoding="utf-8")
                .replace("返回 `/tiguan-rehab`", "返回入口")
                .replace("不得直接路由到另一个叶子 Skill", "请直接路由到 /tiguan-business-review")
                + "\n扫描当前工作目录获取资料。\n完成后立即路由到 /tiguan-business-review。\n",
                encoding="utf-8",
            )
            result = self.run_checker(clone)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("return", result.stderr.lower())
            self.assertIn("direct", result.stderr.lower())
            self.assertIn("broad", result.stderr.lower())
            self.assertIn("primary leaf", result.stderr.lower())

    def test_rejects_an_undeclared_published_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone = Path(temp_dir) / "repo"
            shutil.copytree(ROOT, clone)
            rogue = clone / "skills/rogue/SKILL.md"
            rogue.parent.mkdir()
            rogue.write_text("---\nname: rogue\ndescription: x\n---\n", encoding="utf-8")
            result = self.run_checker(clone)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("undeclared", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
