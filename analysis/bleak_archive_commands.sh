#!/usr/bin/env bash
# Archive the 26 empty BleakNarratives repos.
#
#   ./bleak_archive_commands.sh          # dry run - prints what would happen
#   ./bleak_archive_commands.sh --apply  # actually archives
#
# Archiving is reversible (unarchive from the repo's Settings page or via
# `gh api -X PATCH repos/BleakNarratives/NAME -f archived=false`), which is why
# this archives rather than deletes. Delete only after you are satisfied.
#
# Requires: gh, authenticated as BleakNarratives.

set -u

OWNER="BleakNarratives"
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

EMPTY=(
  Akasha
  Apex-Recovery
  Automation-DNA
  CodeMentor-MVP
  DevIDE
  ModMind-Hub
  ModMind-Rapper2.0
  Mrs-Higgins-Front-Desk-Lady
  Mrs-Higgins-SaaS
  New-SaaS-Launchpad
  Pattern-Atlas
  Print-Hello-Work
  ProjectCentral
  Ship-Or-Skip
  ShipWrekD-OS
  ShipWrekD-OS-Syntax-AI-Driven-IDE-Version-2.0
  This-Shit
  Tracer
  benefinder
  bleak-core-toolbox
  bleak-datacampus
  boa_bundle
  foxwoodacademy
  motherbrain
  root_2025
  whorl-nexus
)

if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

if [ "$APPLY" -eq 0 ]; then
  echo "DRY RUN - nothing will change. Re-run with --apply to archive."
  echo
fi

ok=0
fail=0
for repo in "${EMPTY[@]}"; do
  # Guard: refuse to touch anything that is not actually empty.
  size=$(gh api "repos/$OWNER/$repo" --jq '.size' 2>/dev/null || echo "?")
  if [ "$size" != "0" ]; then
    printf '  SKIP  %-48s size=%s (not empty)\n' "$repo" "$size"
    fail=$((fail + 1))
    continue
  fi
  if [ "$APPLY" -eq 0 ]; then
    printf '  WOULD ARCHIVE  %s\n' "$repo"
    ok=$((ok + 1))
    continue
  fi
  if gh api -X PATCH "repos/$OWNER/$repo" -f archived=true >/dev/null 2>&1; then
    printf '  ARCHIVED  %s\n' "$repo"
    ok=$((ok + 1))
  else
    printf '  FAILED    %s\n' "$repo"
    fail=$((fail + 1))
  fi
done

echo
echo "done: $ok ok, $fail skipped/failed"
[ "$APPLY" -eq 0 ] && echo "(dry run - use --apply to execute)"
exit 0
