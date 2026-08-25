#!/usr/bin/env bash
set -euo pipefail
student_id="${1:-}"
safe_id="$(printf '%s' "$student_id" | tr '[:lower:]' '[:upper:]' | tr -cd 'A-Z0-9_-')"
if [ -z "$safe_id" ]; then echo "Usage: bash scripts/create_member_workspace.sh STUDENT_ID"; exit 1; fi
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
target="$repo_root/04_active_workspaces/${safe_id}_current_working_folder"
mkdir -p "$target"/{notes,notebooks,code,evidence,scratch}
printf 'Member workspace ready: %s\n' "$target"
printf 'Copy the student current working folder contents here, then create a member branch.\n'
