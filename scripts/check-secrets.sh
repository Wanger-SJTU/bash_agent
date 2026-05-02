#!/bin/bash
# Pre-commit hook to prevent committing sensitive information

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

ERRORS=0

# Check for API keys in staged files
echo "Checking for sensitive information..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Patterns to check
PATTERNS=(
    "sk-ant-[a-zA-Z0-9_-]{20,}"  # Anthropic API keys
    "sk-[a-zA-Z0-9_-]{20,}"        # OpenAI API keys
    "ANTHROPIC_API_KEY\s*=\s*['\"]?[sk-]"  # API key assignments
    "OPENAI_API_KEY\s*=\s*['\"]?[sk-]"     # API key assignments
    "api_key\s*[:=]\s*['\"]?[sk-]"         # Config API keys
)

for FILE in $STAGED_FILES; do
    if [ ! -f "$FILE" ]; then
        continue
    fi

    # Skip certain file types
    if [[ "$FILE" == *.png ]] || [[ "$FILE" == *.jpg ]] || [[ "$FILE" == *.gif ]]; then
        continue
    fi

    # Skip documentation files that contain examples
    if [[ "$FILE" == *.md ]] || [[ "$FILE" == *.txt ]] || [[ "$FILE" == *.example ]]; then
        # For docs, only warn if it looks like a real key (not placeholders)
        if grep -qE "sk-(ant-)?[a-zA-Z0-9_-]{30,}" "$FILE" 2>/dev/null; then
            # Check if it contains example/placeholder indicators
            if ! grep -qE "(your-key-here|placeholder|example|dummy|test|fake)" "$FILE" 2>/dev/null; then
                echo -e "${RED}✗ Possible real API key in documentation: $FILE${NC}"
                echo -e "${YELLOW}  Documentation should use placeholders like 'sk-ant-your-key-here'${NC}"
                ERRORS=$((ERRORS + 1))
            fi
        fi
        continue
    fi

    for PATTERN in "${PATTERNS[@]}"; do
        if grep -qE "$PATTERN" "$FILE" 2>/dev/null; then
            echo -e "${RED}✗ Potential API key found in: $FILE${NC}"
            echo -e "${YELLOW}  Pattern: $PATTERN${NC}"
            echo -e "${YELLOW}  Please remove the API key before committing.${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    done
done

# Check for config files that shouldn't be committed
CONFIG_PATTERNS=(
    "bashagnet\.yaml"
    "\.env$"
    "\.env\.local"
    "config\.yaml"
)

for FILE in $STAGED_FILES; do
    for PATTERN in "${CONFIG_PATTERNS[@]}"; do
        if echo "$FILE" | grep -qE "$PATTERN"; then
            echo -e "${RED}✗ Config file should not be committed: $FILE${NC}"
            echo -e "${YELLOW}  Add it to .gitignore if needed${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    done
done

if [ $ERRORS -gt 0 ]; then
    echo -e "\n${RED}❌ Pre-commit check failed: $ERRORS error(s) found${NC}"
    echo -e "${YELLOW}💡 To bypass (unsafe): git commit --no-verify${NC}"
    exit 1
fi

echo -e "${GREEN}✓ No sensitive information found${NC}"
exit 0
