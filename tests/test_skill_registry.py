#!/usr/bin/env python3
"""Tests for the manifest-backed published Skill registry."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skill_registry import RegistryError, load_registry  # noqa: E402


PRIMARY_ROUTES = {
    "tiguan-source-to-practice",
    "tiguan-practice-knowledge-base",
    "tiguan-service-ops",
    "tiguan-post-session-questioning",
    "tiguan-business-review",
}


class SkillRegistryTest(unittest.TestCase):
    def test_manifest_is_the_single_source_for_published_skills(self) -> None:
        registry = load_registry(ROOT)

        self.assertEqual(registry.primary_route_ids, frozenset(PRIMARY_ROUTES))
        self.assertIn("tiguan-assessment-session-design", registry.published_skill_ids)
        self.assertNotIn(
            "tiguan-assessment-session-design", registry.primary_route_ids
        )
        for skill_id in registry.published_skill_ids:
            self.assertTrue((ROOT / "skills" / skill_id).is_dir(), skill_id)
            self.assertTrue((ROOT / "skills" / skill_id / "SKILL.md").is_file(), skill_id)

    def test_duplicate_missing_and_undeclared_primary_routes_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            plugin_dir = temporary_root / ".claude-plugin"
            plugin_dir.mkdir()

            def write_manifest(skills: list[str], primary_routes: list[str]) -> None:
                (plugin_dir / "plugin.json").write_text(
                    json.dumps({"skills": skills, "primaryRoutes": primary_routes}),
                    encoding="utf-8",
                )

            write_manifest(
                ["./skills/one", "./skills/one"], ["one"]
            )
            with self.assertRaisesRegex(RegistryError, "duplicate"):
                load_registry(temporary_root)

            write_manifest(["./skills/one"], ["missing"])
            with self.assertRaisesRegex(RegistryError, "undeclared"):
                load_registry(temporary_root)

            write_manifest(["./skills/one"], [])
            with self.assertRaisesRegex(RegistryError, "exactly five"):
                load_registry(temporary_root)


if __name__ == "__main__":
    unittest.main()
