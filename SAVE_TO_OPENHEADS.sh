#!/usr/bin/env bash
# SAVE_TO_OPENHEADS.sh
#
# Run this ON YOUR CHROMEBOOK, from inside the unpacked openheads-kit directory.
#
#   tar -xzf openheads-kit.tar.gz -C ~/OpenHeads-kit
#   cd ~/OpenHeads-kit
#   bash SAVE_TO_OPENHEADS.sh
#
# It pushes everything to github.com/BleakNarratives/OpenHeads using YOUR gh
# credentials (the agent's token is read-only, so it cannot do this itself).
#
# Then, optionally, it creates the 7 consolidation repos.
#
#   bash SAVE_TO_OPENHEADS.sh --repos      # also create the repo kits
#
# Safe to re-run.

set -u

OWNER="BleakNarratives"
REPO="OpenHeads"
SELF="$(cd "$(dirname "$0")" && pwd)"
DO_REPOS=0
[ "${1:-}" = "--repos" ] && DO_REPOS=1

hr() { printf '%s\n' "============================================================"; }

hr
echo "OpenHeads bootstrap push"
hr

# --- preflight -------------------------------------------------------------
if ! command -v gh >/dev/null 2>&1; then
  echo "gh not found. Install it:" >&2
  echo "  (Debian/Crostini) sudo apt update && sudo apt install -y gh" >&2
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run:" >&2
  echo "  gh auth login" >&2
  echo >&2
  echo "Choose HTTPS, and make sure the token has 'repo' scope so it can push." >&2
  exit 1
fi
echo "  gh:      ok ($(gh api user --jq .login 2>/dev/null))"
echo "  source:  $SELF"
echo

# --- init and push ---------------------------------------------------------
cd "$SELF" || exit 1
if [ ! -d .git ]; then
  git init -q
fi
git config user.name  >/dev/null 2>&1 || git config user.name  "BleakNarratives"
git config user.email >/dev/null 2>&1 || git config user.email "bleaknarratives@users.noreply.github.com"

git add -A
if git diff --cached --quiet 2>/dev/null; then
  echo "  nothing new to commit"
else
  git commit -q -m "Bootstrap: session context, repo kits, CLI handoffs

Pass-1 consolidation work plus the agent handshake.

- SESSION_CONTEXT.md: universal context block every agent reads first
- analysis/: pass-1 scan of 116 repos, clusters, duplication evidence
- bootstrap/dist/: 7 repo kits, each with QRD/MRD/ROADMAP/TODO
- install_bootstrap.sh: wires context into every CLI agent
- bootstrap_everything.sh: one-shot create + wire
- handoffs/: per-CLI kickdown prompts

Co-authored-by: openhands <openhands@all-hands.dev>"
  echo "  committed"
fi

# Use gh's credential helper so we never handle the token by hand.
git remote remove origin >/dev/null 2>&1
git remote add origin "https://github.com/$OWNER/$REPO.git"

echo "  pushing to $OWNER/$REPO ..."
if git push -u origin main 2>&1 | tail -4; then
  echo
  echo "  PUSHED. https://github.com/$OWNER/$REPO"
else
  echo
  echo "  push failed. If it says 'denied', your gh token lacks repo write scope." >&2
  echo "  Fix: gh auth refresh -h github.com -s repo" >&2
  echo "  Then re-run this script." >&2
  exit 1
fi

# --- optionally create the repo kits --------------------------------------
if [ "$DO_REPOS" -eq 1 ]; then
  hr
  echo "Creating the 7 consolidation repos"
  hr
  for d in "$SELF"/bootstrap/dist/bleak-*; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    if gh repo view "$OWNER/$name" >/dev/null 2>&1; then
      printf '  EXISTS   %s\n' "$name"
      continue
    fi
    tmp="$(mktemp -d)"
    cp -r "$d"/. "$tmp"/
    (
      cd "$tmp" || exit 1
      git init -q
      git config user.name "BleakNarratives"
      git config user.email "bleaknarratives@users.noreply.github.com"
      git add -A
      git commit -qm "Bootstrap: QRD, MRD, ROADMAP, TODO"
      gh repo create "$OWNER/$name" --public --source=. --remote=origin --push >/dev/null 2>&1
    )
    if [ $? -eq 0 ]; then printf '  CREATED  %s\n' "$name"; else printf '  FAILED   %s\n' "$name"; fi
    rm -rf "$tmp"
  done
  echo
  echo "  Note: the new repos hold docs and plan only. Populating them with code"
  echo "  is the next work session."
fi

# --- wire the session context ---------------------------------------------
hr
echo "Wiring session context into your CLI agents"
hr
bash "$SELF/install_bootstrap.sh"

hr
cat <<'EOF'
Done.

Next:
  1. source ~/.bashrc
  2. oh                  # confirm the context block prints
  3. oh repos            # list the repo kits
  4. Pick a kit, hand its QRD to whichever agent you want.
     Kickdown prompts are in handoffs/ - one per CLI.
EOF
