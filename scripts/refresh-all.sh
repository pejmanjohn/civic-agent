#!/bin/bash
# The Monday-coffee command: attempt the four cheap snapshot refreshes locally,
# then remind about the review checklist. Deliberate and manual by design.
set -uo pipefail
cd "$(dirname "$0")/.."

for src in washington.fit_filed_actuals washington.dor_property_tax_levies \
           washington.ofm_population washington.revenue_by_biennium; do
  echo ""
  echo "########## $src"
  python3 scripts/refresh.py "$src" || echo "!! $src refresh needs attention"
done

echo ""
echo "Done. If anything changed: review the diff per each refresh's checklist,"
echo "sync cards/benchmarks as needed, then: bash scripts/gates.sh"
