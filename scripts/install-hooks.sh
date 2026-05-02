#!/bin/bash
# Install git hooks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$SCRIPT_DIR/../.git/hooks"
CHECK_SECRETS="$SCRIPT_DIR/check-secrets.sh"

echo "Installing git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Install pre-commit hook
ln -sf "$CHECK_SECRETS" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

echo "✓ Pre-commit hook installed"
echo ""
echo "The hook will check for:"
echo "  - API keys (sk-ant-*, sk-*)"
echo "  - Config files with keys"
echo "  - .env files"
echo ""
echo "To bypass: git commit --no-verify"
