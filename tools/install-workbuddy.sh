#!/usr/bin/env bash
set -Eeuo pipefail

REPOSITORY="${TIGUAN_SKILLS_REPOSITORY:-Bbaozizz/tiguan-rehab-skills}"
REF="${TIGUAN_SKILLS_REF:-main}"
SOURCE_DIR="${TIGUAN_SKILLS_SOURCE_DIR:-}"
WORKBUDDY_HOME="${WORKBUDDY_HOME:-${HOME}/.workbuddy}"

usage() {
  cat <<'EOF'
Install Tguan Rehabilitation Skills for WorkBuddy.

Usage:
  bash install-workbuddy.sh [options]

Options:
  --workbuddy-home PATH  Override the WorkBuddy data directory.
  --source-dir PATH      Install from a local repository checkout.
  --ref REF              Install a Git branch, tag, or commit (default: main).
  --repository OWNER/REPO
                         Override the GitHub repository.
  -h, --help             Show this help.
EOF
}

while (($#)); do
  case "$1" in
    --workbuddy-home)
      [[ $# -ge 2 ]] || { echo "Missing value for --workbuddy-home" >&2; exit 2; }
      WORKBUDDY_HOME="$2"
      shift 2
      ;;
    --source-dir)
      [[ $# -ge 2 ]] || { echo "Missing value for --source-dir" >&2; exit 2; }
      SOURCE_DIR="$2"
      shift 2
      ;;
    --ref)
      [[ $# -ge 2 ]] || { echo "Missing value for --ref" >&2; exit 2; }
      REF="$2"
      shift 2
      ;;
    --repository)
      [[ $# -ge 2 ]] || { echo "Missing value for --repository" >&2; exit 2; }
      REPOSITORY="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

TEMP_SOURCE=""
STAGE_DIR=""
REGISTRY_OUTPUT=""

cleanup() {
  if [[ -n "$STAGE_DIR" && -d "$STAGE_DIR" ]]; then
    rm -rf -- "$STAGE_DIR"
  fi
  if [[ -n "$TEMP_SOURCE" && -d "$TEMP_SOURCE" ]]; then
    rm -rf -- "$TEMP_SOURCE"
  fi
  if [[ -n "$REGISTRY_OUTPUT" && -f "$REGISTRY_OUTPUT" ]]; then
    rm -f -- "$REGISTRY_OUTPUT"
  fi
}
trap cleanup EXIT

if [[ -n "$SOURCE_DIR" ]]; then
  if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Source directory does not exist: $SOURCE_DIR" >&2
    exit 1
  fi
  REPO_ROOT="$(cd "$SOURCE_DIR" && pwd)"
else
  command -v curl >/dev/null 2>&1 || {
    echo "curl is required to download the Skills package." >&2
    exit 1
  }
  command -v tar >/dev/null 2>&1 || {
    echo "tar is required to unpack the Skills package." >&2
    exit 1
  }

  TEMP_SOURCE="$(mktemp -d "${TMPDIR:-/tmp}/tiguan-workbuddy-source.XXXXXX")"
  ARCHIVE="$TEMP_SOURCE/source.tar.gz"
  EXTRACTED="$TEMP_SOURCE/extracted"
  mkdir -p "$EXTRACTED"

  echo "Downloading $REPOSITORY@$REF ..."
  curl -fsSL \
    "https://codeload.github.com/$REPOSITORY/tar.gz/$REF" \
    -o "$ARCHIVE"
  tar -xzf "$ARCHIVE" -C "$EXTRACTED"

  shopt -s nullglob
  EXTRACTED_ENTRIES=("$EXTRACTED"/*)
  shopt -u nullglob
  if [[ ${#EXTRACTED_ENTRIES[@]} -ne 1 || ! -d "${EXTRACTED_ENTRIES[0]}" ]]; then
    echo "Downloaded archive has an unexpected layout." >&2
    exit 1
  fi
  REPO_ROOT="${EXTRACTED_ENTRIES[0]}"
fi

command -v python3 >/dev/null 2>&1 || {
  echo "python3 is required to install Tguan Skills on macOS/Linux." >&2
  exit 1
}

SKILL_NAMES=()
REGISTRY_OUTPUT="$(mktemp "${TMPDIR:-/tmp}/tiguan-skill-registry.XXXXXX")"
if ! python3 "$REPO_ROOT/tools/skill_registry.py" \
  --repo-root "$REPO_ROOT" --published-skill-ids > "$REGISTRY_OUTPUT"; then
  echo "Invalid package: strict skill registry validation failed" >&2
  exit 1
fi
while IFS= read -r skill_name; do
  [[ -n "$skill_name" ]] && SKILL_NAMES+=("$skill_name")
done < "$REGISTRY_OUTPUT"

if [[ ${#SKILL_NAMES[@]} -eq 0 ]]; then
  echo "Invalid package: .claude-plugin/plugin.json declares no skills" >&2
  exit 1
fi

for name in "${SKILL_NAMES[@]}"; do
  if [[ ! -f "$REPO_ROOT/skills/$name/SKILL.md" ]]; then
    echo "Invalid package: missing skills/$name/SKILL.md" >&2
    exit 1
  fi
done

TARGET_ROOT="$WORKBUDDY_HOME/skills"
mkdir -p "$TARGET_ROOT"
TARGET_ROOT="$(cd "$TARGET_ROOT" && pwd -P)"

assert_target_within_skills_root() {
  python3 - "$TARGET_ROOT" "$1" <<'PY'
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve(strict=False)
try:
    target.relative_to(root)
except ValueError:
    raise SystemExit(f"Refusing target outside Skills root: {target}")
PY
}

STAGE_DIR="$(mktemp -d "$TARGET_ROOT/.tiguan-install.XXXXXX")"
mkdir -p "$STAGE_DIR/new" "$STAGE_DIR/backup"

for name in "${SKILL_NAMES[@]}"; do
  assert_target_within_skills_root "$TARGET_ROOT/$name"
  cp -R "$REPO_ROOT/skills/$name" "$STAGE_DIR/new/$name"
done

INSTALLED_NAMES=()
INSTALL_FAILED=0
rollback_install() {
  echo "Installation failed. Restoring the previous WorkBuddy Skills." >&2
  for installed_name in "${INSTALLED_NAMES[@]}"; do
    installed_target="$TARGET_ROOT/$installed_name"
    if [[ -e "$installed_target" || -L "$installed_target" ]]; then
      rm -rf -- "$installed_target"
    fi
  done
  for managed_name in "${SKILL_NAMES[@]}"; do
    managed_backup="$STAGE_DIR/backup/$managed_name"
    if [[ -e "$managed_backup" || -L "$managed_backup" ]]; then
      mv "$managed_backup" "$TARGET_ROOT/$managed_name"
    fi
  done
}
for name in "${SKILL_NAMES[@]}"; do
  target="$TARGET_ROOT/$name"
  assert_target_within_skills_root "$target"
  if [[ -e "$target" || -L "$target" ]]; then
    if ! mv "$target" "$STAGE_DIR/backup/$name"; then
      INSTALL_FAILED=1
      break
    fi
  fi
  if ! mv "$STAGE_DIR/new/$name" "$target"; then
    INSTALL_FAILED=1
    break
  fi
  INSTALLED_NAMES+=("$name")
done

if [[ $INSTALL_FAILED -ne 0 ]]; then
  rollback_install
  exit 1
fi

if [[ "${TIGUAN_INSTALLER_TEST_FAIL_VERIFICATION:-}" == "1" ]]; then
  rm -f -- "$TARGET_ROOT/tiguan-rehab/SKILL.md"
fi
for name in "${SKILL_NAMES[@]}"; do
  if [[ ! -f "$TARGET_ROOT/$name/SKILL.md" ]]; then
    echo "Installation verification failed: $name" >&2
    rollback_install
    exit 1
  fi
done

echo
echo "Installed Tguan Rehabilitation Skills for WorkBuddy:"
for name in "${SKILL_NAMES[@]}"; do
  echo "- $name"
done
echo "Location: $TARGET_ROOT"
echo "Next: refresh or restart WorkBuddy, then run /tiguan-rehab 新手入门"
