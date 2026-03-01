#!/usr/bin/env bash
# vet-install.sh — Safe skill installation wrapper
# SOP Reference: 6.1, Step 2
#
# Delegates to skillvet's safe-install.sh after verifying the scanner exists.
# Usage: bash scripts/vet-install.sh <skill-slug>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLVET_DIR="${REPO_ROOT}/skills/skillvet"
SAFE_INSTALL="${SKILLVET_DIR}/scripts/safe-install.sh"

if [ $# -lt 1 ]; then
    echo "ERROR: No skill slug provided."
    echo "Usage: bash scripts/vet-install.sh <skill-slug>"
    exit 1
fi

SKILL_SLUG="$1"

if [ ! -d "$SKILLVET_DIR" ]; then
    echo "ERROR: skillvet scanner not found at ${SKILLVET_DIR}"
    echo "Install it first (T-3.1): clone the skillvet repository into skills/skillvet/"
    exit 1
fi

if [ ! -f "$SAFE_INSTALL" ]; then
    echo "ERROR: safe-install.sh not found at ${SAFE_INSTALL}"
    exit 1
fi

echo "=== Vetting skill: ${SKILL_SLUG} ==="
echo "Scanner: ${SAFE_INSTALL}"
echo ""

bash "$SAFE_INSTALL" "$SKILL_SLUG"
