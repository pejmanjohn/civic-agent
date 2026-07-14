#!/bin/bash
# All local quality gates in one shot. Run before pushing (the pre-push hook
# installed by scripts/install-hooks.sh does this automatically).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== tests =="
python3 -m unittest discover -s tests

echo "== plugin package =="
python3 scripts/package_plugin.py --check

echo "== coverage matrix =="
python3 scripts/coverage.py --check

echo "== WA-20 scoreboard =="
python3 scripts/wa20.py --check

echo "== WA-20 expectation ratchet =="
if git rev-parse --verify -q origin/main >/dev/null; then
  BASE="origin/main"
else
  BASE="main"
fi
python3 scripts/wa20.py --ratchet-check "$BASE"

echo ""
echo "All gates green."
