#!/usr/bin/env python3
"""Minimal dependency-free validator for public SKILL.md packages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def validate(skill_dir: Path) -> None:
    if not skill_dir.is_dir():
        raise ValueError(f"skill directory not found: {skill_dir}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise ValueError(f"missing {skill_md}")

    fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if set(fields) != {"name", "description"}:
        raise ValueError("frontmatter must contain only name and description")
    name = fields["name"]
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        raise ValueError(f"invalid skill name: {name!r}")
    if name != skill_dir.name:
        raise ValueError(f"skill name {name!r} does not match folder {skill_dir.name!r}")
    if not fields["description"]:
        raise ValueError("description must not be empty")
    if not (skill_dir / "agents/openai.yaml").is_file():
        raise ValueError("missing agents/openai.yaml")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    try:
        validate(args.skill_dir.resolve())
    except ValueError as exc:
        parser.error(str(exc))
    print(f"valid skill: {args.skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
