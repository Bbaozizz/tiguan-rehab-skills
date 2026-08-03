#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-"$ROOT_DIR/dist/skills"}"
VERSION="$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")"

python3 "$ROOT_DIR/tools/check-publication-readiness.py"
mkdir -p "$OUT_DIR"
find "$OUT_DIR" -maxdepth 1 -type f \( -name 'tiguan-*.zip' -o -name 'tiguan-rehab-skills-*.zip' \) -delete

STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGE_DIR"' EXIT

python3 - "$ROOT_DIR" "$OUT_DIR" "$STAGE_DIR" "$VERSION" <<'PY'
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
stage = Path(sys.argv[3])
version = sys.argv[4]
skill_names = (
    "tiguan-rehab",
    "tiguan-assessment-session-design",
    "tiguan-source-to-practice",
    "tiguan-practice-knowledge-base",
    "tiguan-service-ops",
    "tiguan-post-session-questioning",
    "tiguan-business-review",
)

for name in skill_names:
    source = root / "skills" / name
    archive_path = out / f"{name}.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, path.relative_to(source))
    shutil.copy2(archive_path, stage / archive_path.name)

(stage / "README.md").write_text(
    f"# 体观康复 Skills {version}\n\n"
    "每个 zip 都是独立 Skill，解压后根目录为 SKILL.md。\n\n"
    "- tiguan-rehab.zip：统一入口与路由。\n"
    "- tiguan-assessment-session-design.zip：问卷设置、答卷课前准备、合成案例与可选报告。\n\n"
    "- tiguan-source-to-practice.zip：资料到可验证实践。\n"
    "- tiguan-practice-knowledge-base.zip：个人工作知识库。\n"
    "- tiguan-service-ops.zip：客户服务运营预览与安全执行。\n"
    "- tiguan-post-session-questioning.zip：证据驱动的课后质询。\n"
    "- tiguan-business-review.zip：脱敏经营漏斗分析。\n\n"
    "使用脱敏输入；AI 不替代临床判断与责任。\n",
    encoding="utf-8",
)

bundle = out / f"tiguan-rehab-skills-{version}.zip"
with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(stage.iterdir()):
        archive.write(path, path.name)
print(f"built: {bundle}")
PY
