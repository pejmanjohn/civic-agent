#!/bin/bash
# Daily local drift check (loaded via launchd; see CONTRIBUTING.md Local Ops).
# Runs ONE probe sweep, logs the ledger to ~/.civic-agent/drift.log, and
# raises a macOS notification only when a source drifted or errored.
set -uo pipefail
cd "$(dirname "$0")/.."
LOG_DIR="$HOME/.civic-agent"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/drift.log"

echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
REPORT="$(python3 scripts/drift.py --status --json 2>>"$LOG")" || {
  echo "drift.py failed to run" >> "$LOG"
  osascript -e 'display notification "drift.py failed to run - see ~/.civic-agent/drift.log" with title "Civic Agent drift"' 2>/dev/null || true
  exit 0
}

SUMMARY="$(printf '%s' "$REPORT" | python3 -c "
import json, sys
report = json.load(sys.stdin)
summary = report['summary']
for entry in report['results']:
    fresh = entry.get('freshness', {})
    print('%-44s %-8s %s' % (entry['source_id'], entry['status'], fresh.get('state', 'unknown')))
print('SUMMARY ok=%(ok)s drift=%(drift)s error=%(error)s skipped=%(skipped)s' % summary)
")"
printf '%s\n' "$SUMMARY" >> "$LOG"

DRIFT=$(printf '%s' "$SUMMARY" | sed -n 's/.*drift=\([0-9]*\).*/\1/p')
ERRS=$(printf '%s' "$SUMMARY" | sed -n 's/.*error=\([0-9]*\).*/\1/p')
OKS=$(printf '%s' "$SUMMARY" | sed -n 's/.*ok=\([0-9]*\).*/\1/p')
if [ "${OKS:-0}" -eq 0 ] && [ "${DRIFT:-0}" -eq 0 ] && [ "${ERRS:-0}" -gt 0 ]; then
  # Every probe failed and nothing succeeded: almost certainly local network,
  # not eight simultaneous endpoint failures. Log it; no alarm.
  echo "all probes errored - likely local network outage; no notification" >> "$LOG"
elif [ "${DRIFT:-0}" -gt 0 ] || [ "${ERRS:-0}" -gt 0 ]; then
  osascript -e "display notification \"drift=$DRIFT error=$ERRS - run: python3 scripts/drift.py --status\" with title \"Civic Agent drift\"" 2>/dev/null || true
fi
