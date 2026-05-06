#!/usr/bin/env sh
# AKOS template — pre-commit hook for {{REPO_SLUG}}.
# Rendered by bless into <repo>/.husky/pre-commit (when stack=node).

. "$(dirname -- "$0")/_/husky.sh"

# Runs only on files staged for commit; fast and developer-friendly.
npx lint-staged

# Brand-jargon scan on staged external-facing prose (non-blocking warning).
if [ -f scripts/lint-jargon.ts ] || [ -f scripts/lint-jargon.js ]; then
  npm run lint:jargon --if-present || {
    echo "warn(brand-jargon): forbidden tokens detected in external-facing prose; review before pushing."
  }
fi
