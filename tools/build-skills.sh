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

sys.path.insert(0, str(Path(sys.argv[1]) / "tools"))
from skill_registry import load_registry

root = Path(sys.argv[1])
out = Path(sys.argv[2])
stage = Path(sys.argv[3])
version = sys.argv[4]
skill_names = sorted(load_registry(root).published_skill_ids)

for name in skill_names:
    source = root / "skills" / name
    archive_path = out / f"{name}.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, path.relative_to(source))
    shutil.copy2(archive_path, stage / archive_path.name)

(stage / "README.md").write_text(
    f"# 体观康复 Skills {version}\n\n每个 zip 都是独立 Skill，解压后根目录为 SKILL.md。\n\n"
    + "".join(f"- {name}.zip\n" for name in skill_names)
    + "\n使用脱敏输入；AI 不替代临床判断与责任。\n",
    encoding="utf-8",
)

bundle = out / f"tiguan-rehab-skills-{version}.zip"
with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(stage.iterdir()):
        archive.write(path, path.name)
print(f"built: {bundle}")
PY
