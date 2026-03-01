#!/usr/bin/env bash
# scan-skill.sh — Automated supply chain security scanner for Claude skills
#
# Usage: bash scan-skill.sh <path-to-skill-dir-or-file>
#
# Exit codes:
#   0 = clean (no suspicious patterns found)
#   1 = FAILED (one or more suspicious patterns detected)
#   2 = usage error

set -euo pipefail

# ─── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: bash scan-skill.sh <path-to-skill-dir-or-file>"
  exit 2
fi

if [[ ! -e "$TARGET" ]]; then
  echo -e "${RED}Error: '$TARGET' does not exist.${RESET}"
  exit 2
fi

echo -e "${BOLD}${CYAN}=== Xomware Skill Security Scanner ===${RESET}"
echo -e "Target: ${TARGET}"
echo ""

FINDINGS=0

# ─── Helper ───────────────────────────────────────────────────────────────────
check_pattern() {
  local description="$1"
  local pattern="$2"
  local severity="${3:-HIGH}"

  if grep -rn --include="*.js" --include="*.ts" --include="*.sh" \
              --include="*.md" --include="*.json" --include="*.py" \
              -E "$pattern" "$TARGET" 2>/dev/null | grep -v "^Binary"; then
    echo -e "  ${RED}[${severity}]${RESET} ${description}"
    FINDINGS=$((FINDINGS + 1))
    echo ""
  fi
}

# ─── Checks ───────────────────────────────────────────────────────────────────

echo -e "${BOLD}[1/7] Checking for HTTP fetch() calls to non-Xomware domains...${RESET}"
# Flag any fetch() that doesn't point to xomware.com
if grep -rn --include="*.js" --include="*.ts" --include="*.sh" --include="*.md" \
            -E "fetch\(" "$TARGET" 2>/dev/null \
    | grep -v "xomware\.com" \
    | grep -v "^Binary"; then
  echo -e "  ${RED}[HIGH]${RESET} fetch() call to non-Xomware domain detected"
  FINDINGS=$((FINDINGS + 1))
fi
echo ""

echo -e "${BOLD}[2/7] Checking for Node.js HTTP/HTTPS module usage...${RESET}"
check_pattern \
  "require('http') or require('https') — direct HTTP client" \
  "require\(['\"]https?['\"]" \
  "HIGH"

echo -e "${BOLD}[3/7] Checking for sensitive path access (~/.ssh, ~/.aws, ~/.env)...${RESET}"
check_pattern \
  "Reading from ~/.ssh/ — SSH key exfiltration risk" \
  "~/\.ssh" \
  "CRITICAL"
check_pattern \
  "Reading from ~/.aws/ — AWS credential exfiltration risk" \
  "~/\.aws" \
  "CRITICAL"
check_pattern \
  "Reading .env files — environment secret exfiltration risk" \
  "~/\.env|/\.env[^a-zA-Z]|\bprocess\.env\b" \
  "HIGH"

echo -e "${BOLD}[4/7] Checking for security hook overrides...${RESET}"
check_pattern \
  "PreToolUse / PostToolUse hook manipulation" \
  "(PreToolUse|PostToolUse|hooks.*override|removeHook|clearHooks)" \
  "CRITICAL"

echo -e "${BOLD}[5/7] Checking for Base64-encoded payloads...${RESET}"
# Look for long base64 strings (≥40 chars of base64 alphabet)
if grep -rn --include="*.js" --include="*.ts" --include="*.sh" --include="*.md" \
            --include="*.json" --include="*.py" \
            -E "[A-Za-z0-9+/]{40,}={0,2}" "$TARGET" 2>/dev/null \
    | grep -v "^Binary" \
    | grep -v "node_modules"; then
  echo -e "  ${YELLOW}[MEDIUM]${RESET} Long Base64-like string found — may be encoded payload (review manually)"
  FINDINGS=$((FINDINGS + 1))
fi
echo ""

echo -e "${BOLD}[6/7] Checking for dynamic eval() / exec() calls...${RESET}"
check_pattern \
  "eval() — dynamic code execution" \
  "\beval\s*\(" \
  "CRITICAL"
check_pattern \
  "exec() — shell command injection risk" \
  "\bexec\s*\(" \
  "HIGH"
check_pattern \
  "execSync() — synchronous shell command injection" \
  "\bexecSync\s*\(" \
  "HIGH"
check_pattern \
  "child_process usage" \
  "require\(['\"]child_process['\"]" \
  "HIGH"

echo -e "${BOLD}[7/7] Checking for auto_reject_patterns from registry.json...${RESET}"
REGISTRY_DIR="$(dirname "$0")/../registry/registry.json"
if [[ -f "$REGISTRY_DIR" ]]; then
  patterns=$(python3 -c "
import json, sys
with open('$REGISTRY_DIR') as f:
    data = json.load(f)
for p in data.get('auto_reject_patterns', []):
    print(p)
" 2>/dev/null || true)
  while IFS= read -r pat; do
    [[ -z "$pat" ]] && continue
    if grep -rn --include="*.js" --include="*.ts" --include="*.sh" \
                --include="*.md" --include="*.json" --include="*.py" \
                -F "$pat" "$TARGET" 2>/dev/null | grep -v "^Binary" | grep -v "scan-skill.sh"; then
      echo -e "  ${RED}[AUTO-REJECT]${RESET} Pattern matched: ${BOLD}${pat}${RESET}"
      FINDINGS=$((FINDINGS + 1))
    fi
  done <<< "$patterns"
fi
echo ""

# ─── Summary ──────────────────────────────────────────────────────────────────
echo -e "${BOLD}=== Scan Complete ===${RESET}"
if [[ "$FINDINGS" -eq 0 ]]; then
  echo -e "${GREEN}✅ CLEAN — No suspicious patterns found.${RESET}"
  echo -e "   Proceed to manual review checklist before registry approval."
  exit 0
else
  echo -e "${RED}🚫 FAILED — ${FINDINGS} suspicious pattern(s) detected.${RESET}"
  echo -e "   This skill is AUTO-REJECTED. Do not install without explicit Dom approval."
  exit 1
fi
