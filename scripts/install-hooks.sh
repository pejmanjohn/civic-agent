#!/bin/bash
# Install the local git hooks (currently: pre-push runs scripts/gates.sh).
set -euo pipefail
cd "$(dirname "$0")/.."
HOOK=.git/hooks/pre-push
cat > "$HOOK" <<'EOF'
#!/bin/bash
# Auto-installed by scripts/install-hooks.sh - all gates must pass to push.
exec bash "$(git rev-parse --show-toplevel)/scripts/gates.sh"
EOF
chmod +x "$HOOK"
echo "Installed $HOOK"
