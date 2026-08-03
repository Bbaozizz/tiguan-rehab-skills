#!/usr/bin/env python3
"""Block public builds when the repository contract or safety boundary drifts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "tiguan-rehab",
    "tiguan-assessment-session-design",
    "tiguan-source-to-practice",
    "tiguan-practice-knowledge-base",
    "tiguan-service-ops",
    "tiguan-post-session-questioning",
    "tiguan-business-review",
}
FORBIDDEN = (
    "/Users/apple/",
    "tiguan-studio-db",
    "studio.sqlite",
    "clients/by-name",
    "appSecret",
    "access_token",
)


def fail(errors: list[str]) -> None:
    print("公开发布门禁失败：", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    errors: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        errors.append(f"VERSION 不是语义化版本：{version!r}")

    plugin = json.loads(
        (ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(
        (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
    )
    plugin_names = {Path(item).name for item in plugin.get("skills", [])}
    if plugin_names != EXPECTED_SKILLS:
        errors.append(f"plugin.json Skills 不一致：{sorted(plugin_names)}")
    market_items = marketplace.get("plugins", [])
    if marketplace.get("metadata", {}).get("version") != version:
        errors.append("marketplace metadata.version 与 VERSION 不一致")
    if {item.get("name") for item in market_items} != EXPECTED_SKILLS:
        errors.append("marketplace 插件集与已发布 Skills 不一致")
    if any(item.get("version") != version for item in market_items):
        errors.append("marketplace 存在与 VERSION 不一致的插件")

    for name in sorted(EXPECTED_SKILLS):
        skill_dir = ROOT / "skills" / name
        skill_md = skill_dir / "SKILL.md"
        agent_yaml = skill_dir / "agents/openai.yaml"
        if not skill_md.is_file():
            errors.append(f"缺少 {skill_md.relative_to(ROOT)}")
            continue
        if not agent_yaml.is_file():
            errors.append(f"缺少 {agent_yaml.relative_to(ROOT)}")
        text = skill_md.read_text(encoding="utf-8")
        if f"name: {name}" not in text:
            errors.append(f"{skill_md.relative_to(ROOT)} name 与目录不一致")
        if "TODO" in text:
            errors.append(f"{skill_md.relative_to(ROOT)} 仍有 TODO")

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
        for token in FORBIDDEN:
            if token.lower() in text.lower():
                errors.append(f"{path.relative_to(ROOT)} 含禁止公开内容：{token}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    badge = re.search(r"version-([0-9.]+)-", readme)
    if badge is None or badge.group(1) != version:
        errors.append("README 版本 Badge 与 VERSION 不一致")

    if errors:
        fail(errors)
    print(
        f"公开发布门禁通过：v{version}，"
        f"{len(EXPECTED_SKILLS)} 个已实现 Skill，未发现私有运行时路径。"
    )


if __name__ == "__main__":
    main()
