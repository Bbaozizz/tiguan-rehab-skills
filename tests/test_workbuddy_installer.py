#!/usr/bin/env python3
"""Behavior tests for the WorkBuddy one-command installer."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools/install-workbuddy.sh"
sys.path.insert(0, str(ROOT / "tools"))
from skill_registry import load_registry  # noqa: E402


class WorkBuddyInstallerTest(unittest.TestCase):
    def run_installer(self, workbuddy_home: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "bash",
                str(INSTALLER),
                "--source-dir",
                str(ROOT),
                "--workbuddy-home",
                str(workbuddy_home),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_installs_all_public_skills_into_workbuddy_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workbuddy_home = Path(temp_dir) / ".workbuddy"

            result = self.run_installer(workbuddy_home)

            self.assertEqual(result.returncode, 0, result.stderr)
            for name in load_registry(ROOT).published_skill_ids:
                installed = workbuddy_home / "skills" / name / "SKILL.md"
                self.assertTrue(installed.is_file(), name)
                self.assertEqual(
                    installed.read_text(encoding="utf-8"),
                    (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8"),
                )

    def test_reinstall_replaces_managed_skills_and_preserves_other_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workbuddy_home = Path(temp_dir) / ".workbuddy"
            skills_home = workbuddy_home / "skills"
            unrelated = skills_home / "my-private-skill" / "SKILL.md"
            stale = skills_home / "tiguan-rehab" / "stale.txt"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("keep me", encoding="utf-8")
            stale.parent.mkdir(parents=True)
            stale.write_text("old", encoding="utf-8")

            result = self.run_installer(workbuddy_home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep me")
            self.assertFalse(stale.exists())

    def test_installer_reads_the_source_manifest_instead_of_a_shell_list(self) -> None:
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertIn(".claude-plugin/plugin.json", script)

    def test_invalid_source_does_not_replace_existing_installation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            workbuddy_home = temp_root / ".workbuddy"
            existing = workbuddy_home / "skills" / "tiguan-rehab" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing installation", encoding="utf-8")

            result = subprocess.run(
                [
                    "bash",
                    str(INSTALLER),
                    "--source-dir",
                    str(temp_root / "missing-source"),
                    "--workbuddy-home",
                    str(workbuddy_home),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(
                existing.read_text(encoding="utf-8"), "existing installation"
            )


if __name__ == "__main__":
    unittest.main()
