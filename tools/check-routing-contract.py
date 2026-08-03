#!/usr/bin/env python3
"""Validate explicit public routing contracts; never infer user intent."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skill_registry import RegistryError, load_registry


FORBIDDEN_DISCOVERY = ("扫描当前工作目录", "扫描工作区", "broad workspace discovery")
RETURN_MARKER = "返回 `/tiguan-rehab`"
DIRECT_LEAF_MARKER = "不得直接路由到另一个叶子 Skill"


def check(repo_root: Path) -> list[str]:
    try:
        registry = load_registry(repo_root)
    except RegistryError as error:
        return [str(error)]
    errors: list[str] = []
    published_dirs = {
        path.name for path in (repo_root / "skills").iterdir() if path.is_dir()
    }
    undeclared = published_dirs - set(registry.published_skill_ids)
    if undeclared:
        errors.append(f"undeclared published Skill directories: {sorted(undeclared)}")
    for skill_id in registry.published_skill_ids:
        skill_md = repo_root / "skills" / skill_id / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"missing published SKILL.md: {skill_id}")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if any(marker in text for marker in FORBIDDEN_DISCOVERY):
            errors.append(f"broad discovery instruction: {skill_id}")
        if skill_id in registry.primary_route_ids:
            if RETURN_MARKER not in text:
                errors.append(f"missing return footer: {skill_id}")
            if DIRECT_LEAF_MARKER not in text:
                errors.append(f"missing direct-route prohibition: {skill_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.repo_root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("routing contract: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
