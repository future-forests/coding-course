#!/usr/bin/env bash
# Sync shared course updates from main into the solution branch.
# Run this ONLY on the solution branch, after editing main (README, pixi.toml, etc.).
set -euo pipefail

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "solution" ]]; then
  echo "Error: switch to the solution branch first (you are on '$current_branch')."
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Error: commit or stash your changes before syncing."
  exit 1
fi

echo "Fetching latest main..."
git fetch origin main

echo "Merging origin/main into solution..."
if git merge origin/main -m "Sync main into solution"; then
  echo "Done — no conflicts."
  exit 0
fi

echo
echo "Conflicts detected — applying the usual resolution for this repo:"
echo "  • shared files (README, etc.) → take main's version"
echo "  • solution/ folder            → keep solution branch version"
echo

# During 'git merge main' on solution: --theirs = main, --ours = solution
git checkout --theirs README.md 2>/dev/null || true
git checkout HEAD -- solution/ 2>/dev/null || true

git add README.md solution/ 2>/dev/null || true

if git diff --name-only --diff-filter=U | grep -q .; then
  echo
  echo "Some conflicts remain — resolve manually, then:"
  echo "  git add <resolved-files>"
  echo "  git commit"
  exit 1
fi

git commit --no-edit
echo "Merge complete."
