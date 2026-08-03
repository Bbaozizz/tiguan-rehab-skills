#!/usr/bin/env python3
"""Manifest-backed registry for the Skills published by this repository."""

from __future__ import annotations

import json
import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet


class RegistryError(ValueError):
    """Raised when the public package manifest cannot define a safe registry."""


@dataclass(frozen=True)
class SkillRegistry:
    published_skill_ids: FrozenSet[str]
    primary_route_ids: FrozenSet[str]


def _skill_id(value: object) -> str:
    if not isinstance(value, str) or not value.startswith("./skills/"):
        raise RegistryError("published Skill path must start with ./skills/")
    skill_id = value.removeprefix("./skills/")
    if not skill_id or "/" in skill_id or skill_id in {".", ".."}:
        raise RegistryError("published Skill path must name one Skill directory")
    return skill_id


def _route_id(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise RegistryError("primary route ID must be a non-empty string")
    return value


def load_registry(repo_root: Path) -> SkillRegistry:
    """Load the complete published Skill and primary-route sets from plugin.json."""
    manifest_path = repo_root / ".claude-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RegistryError(f"cannot load skill registry: {error}") from error
    if not isinstance(manifest, dict):
        raise RegistryError("skill registry manifest must be a JSON object")

    skills = manifest.get("skills")
    primary_routes = manifest.get("primaryRoutes")
    if not isinstance(skills, list) or not isinstance(primary_routes, list):
        raise RegistryError("skill registry requires skills and primaryRoutes lists")

    published_ids = [_skill_id(value) for value in skills]
    route_ids = [_route_id(value) for value in primary_routes]
    if len(published_ids) != len(set(published_ids)):
        raise RegistryError("duplicate published Skill ID")
    if len(route_ids) != len(set(route_ids)):
        raise RegistryError("duplicate primary route ID")
    undeclared = set(route_ids) - set(published_ids)
    if undeclared:
        raise RegistryError(f"undeclared primary route IDs: {sorted(undeclared)}")
    if len(route_ids) != 5:
        raise RegistryError("primaryRoutes must contain exactly five route IDs")

    return SkillRegistry(frozenset(published_ids), frozenset(route_ids))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--published-skill-ids", action="store_true")
    args = parser.parse_args()
    if not args.published_skill_ids:
        parser.error("--published-skill-ids is required")
    try:
        registry = load_registry(args.repo_root)
    except RegistryError as error:
        print(f"invalid skill registry: {error}", file=sys.stderr)
        return 1
    print("\n".join(sorted(registry.published_skill_ids)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
