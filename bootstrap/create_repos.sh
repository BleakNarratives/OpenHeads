#!/usr/bin/env bash
# Create and push the BleakNarratives consolidation repos.
#
#   bash create_repos.sh --dry-run   # preview (default)
#   bash create_repos.sh --apply     # create + push
#
# Requires gh, authenticated as BleakNarratives.
set -u
OWNER="BleakNarratives"
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
cd "$(dirname "$0")" || exit 1

if ! gh auth status >/dev/null 2>&1; then echo "gh not authenticated"; exit 1; fi

declare -A DESC=(
  [bleak-higgins]="Local autonomous SaaS routing pipeline. Canonical home for the Mrs-Higgins family."
  [bleak-whorl]="Field intelligence and agent deployment workbench. Canonical swarm core."
  [bleak-verification]="Catch AI agents that narrate work they did not do. Engine plus commercial face."
  [bleak-ui-kit]="Shared React/Vite starter. Replaces 17 near-identical scaffold repos."
  [bleak-tools]="The operator toolbelt. Small CLI tools, shims, and utilities in one place."
  [bleak-outclaw]="Pro se legal AI toolkit. Citation fraud detection, IRAC arguments, FOIA, judicial complaints."
  [bleak-vertical-ai]="AI expert model boardroom. Multi-persona analysis and adversarial review."
)

for repo in "${!DESC[@]}"; do
  if [ ! -d "dist/$repo" ]; then echo "  MISSING dist/$repo"; continue; fi
  if gh repo view "$OWNER/$repo" >/dev/null 2>&1; then
    printf "  EXISTS   %s\n" "$repo"; continue
  fi
  if [ "$APPLY" -eq 0 ]; then
    printf "  WOULD CREATE  %-22s %s\n" "$repo" "${DESC[$repo]}"
    continue
  fi
  if gh repo create "$OWNER/$repo" --public --description "${DESC[$repo]}" \
       --source="dist/$repo" --remote=origin --push >/dev/null 2>&1; then
    printf "  CREATED  %s\n" "$repo"
  else
    printf "  FAILED   %s\n" "$repo"
  fi
done

echo
echo "Account-level docs are in dist/_account/ - push them to the repo you want as the account hub:"
echo "  cd dist/bleak-verification && cp ../_account/* . && git add . && git commit -m 'Add account-level QRD and MRD' && git push"
