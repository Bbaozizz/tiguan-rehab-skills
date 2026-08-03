#!/usr/bin/env python3
"""Static and CI contracts for the native Windows WorkBuddy installer."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools/install-workbuddy.ps1"
CI_WORKFLOW = ROOT / ".github/workflows/ci.yml"


class WorkBuddyWindowsContractTest(unittest.TestCase):
    def test_powershell_installer_manages_only_the_public_skills(self) -> None:
        script = INSTALLER.read_text(encoding="utf-8")

        self.assertIn('"tiguan-rehab"', script)
        self.assertIn('"tiguan-assessment-session-design"', script)
        self.assertIn('"tiguan-source-to-practice"', script)
        self.assertIn('"tiguan-practice-knowledge-base"', script)
        self.assertIn('"tiguan-service-ops"', script)
        self.assertIn('"tiguan-post-session-questioning"', script)
        self.assertIn('"tiguan-business-review"', script)
        self.assertIn(".workbuddy", script)
        self.assertIn("SKILL.md", script)
        self.assertNotIn("Remove-Item $WorkBuddyHome", script)
        self.assertNotIn("Remove-Item $TargetRoot", script)

    def test_ci_executes_installer_on_a_real_windows_runner(self) -> None:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("windows-latest", workflow)
        self.assertIn("tools/install-workbuddy.ps1", workflow)
        self.assertIn("tiguan-assessment-session-design", workflow)
        self.assertIn("my-private-skill", workflow)


if __name__ == "__main__":
    unittest.main()
