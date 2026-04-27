#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "$script_dir/.." && pwd)"

cd "$script_dir"

uv run --project "$repo_dir/backend/src" --with pyinstaller pyinstaller \
  --onefile \
  --noconsole \
  --name LarpCheck \
  --add-data "$repo_dir/backend/src/ransomware/resources/problems:resources/problems" \
  --add-data "$repo_dir/backend/src/problem_bank/testcases:testcases" \
  --add-data "$repo_dir/sandbox_backup:sandbox_backup" \
  "$repo_dir/backend/src/ransomware/__main__.py"

echo "Done. dist/LarpCheck ready."
