#!/usr/bin/env bash
# bootstrap_everything.sh - one shot. Creates the consolidation repos, pushes
# the doc kits, and wires the session context into every CLI agent.
#
#   bash bootstrap_everything.sh              # dry run (default)
#   bash bootstrap_everything.sh --apply      # do it
#   bash bootstrap_everything.sh --apply --skip-repos   # context only
#   bash bootstrap_everything.sh --apply --skip-context # repos only
#
# Requires: git, gh (authenticated as BleakNarratives), python3.
# Safe to re-run: existing repos are skipped, not overwritten.

set -u

SELF="$(cd "$(dirname "$0")" && pwd)"
OWNER="BleakNarratives"
APPLY=0
SKIP_REPOS=0
SKIP_CTX=0

for arg in "$@"; do
  case "$arg" in
    --apply)        APPLY=1 ;;
    --skip-repos)   SKIP_REPOS=1 ;;
    --skip-context) SKIP_CTX=1 ;;
    -h|--help)      sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

hr() { printf '%s\n' "------------------------------------------------------------"; }
step() { echo; hr; echo "$*"; hr; }

# ---------------------------------------------------------------------------
step "0. Preflight"
# ---------------------------------------------------------------------------
missing=0
for c in git gh python3; do
  if command -v "$c" >/dev/null 2>&1; then
    printf '  ok      %s\n' "$c"
  else
    printf '  MISSING %s\n' "$c"; missing=1
  fi
done
if [ "$missing" -eq 1 ]; then
  echo; echo "Install the missing tools first. On Debian/Crostini:" >&2
  echo "  sudo apt update && sudo apt install -y git python3 gh" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo; echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi
printf '  ok      gh authenticated as %s\n' "$(gh api user --jq .login 2>/dev/null || echo '?')"

if [ "$APPLY" -eq 0 ]; then
  echo
  echo "DRY RUN. Nothing will be created or modified."
  echo "Re-run with --apply to execute."
fi

# ---------------------------------------------------------------------------
if [ "$SKIP_REPOS" -eq 0 ]; then
  step "1. Repo kits"
  if [ ! -d "$SELF/bootstrap/dist" ]; then
    echo "  bootstrap/dist missing. Regenerating from definitions..."
    ( cd "$SELF/bootstrap" && python3 generate.py ) || exit 1
  fi

  if [ "$APPLY" -eq 0 ]; then
    echo "  would create / push:"
    for d in "$SELF"/bootstrap/dist/bleak-*; do
      [ -d "$d" ] || continue
      printf '    %s\n' "$(basename "$d")"
    done
  else
    # Stage each kit into a temp git repo and push.
    for d in "$SELF"/bootstrap/dist/bleak-*; do
      [ -d "$d" ] || continue
      repo="$(basename "$d")"
      if gh repo view "$OWNER/$repo" >/dev/null 2>&1; then
        printf '  EXISTS   %s (skipping)\n' "$repo"
        continue
      fi
      tmp="$(mktemp -d)"
      cp -r "$d"/. "$tmp"/
      (
        cd "$tmp" || exit 1
        git init -q
        git add -A
        git -c user.name=openhands -c user.email=openhands@all-hands.dev \
            commit -qm "Bootstrap: QRD, MRD, ROADMAP, TODO"
        gh repo create "$OWNER/$repo" --public --source=. --remote=origin --push >/dev/null 2>&1
      )
      if [ $? -eq 0 ]; then
        printf '  CREATED  %s\n' "$repo"
      else
        printf '  FAILED   %s\n' "$repo"
      fi
      rm -rf "$tmp"
    done
  fi
fi

# ---------------------------------------------------------------------------
if [ "$SKIP_CTX" -eq 0 ]; then
  step "2. Session context (all CLI agents)"
  if [ "$APPLY" -eq 0 ]; then
    echo "  would run: bash $SELF/install_bootstrap.sh"
    echo "  targets:  ~/AGENTS.md, ~/.codex, ~/.gemini, ~/.aider.conf.md,"
    echo "            ~/.kilo, ~/.vibe, ~/.copilot, ~/.claude, ~/.config/opencode"
    echo "            plus a pointer block in ~/.bashrc and ~/.zshrc"
    echo "  freebuffy: deliberately NOT touched"
  else
    bash "$SELF/install_bootstrap.sh" || exit 1
  fi
fi

# ---------------------------------------------------------------------------
step "3. Summary"
# ---------------------------------------------------------------------------
if [ "$APPLY" -eq 0 ]; then
  cat <<'EOF'
  Dry run complete. To execute:

      bash bootstrap_everything.sh --apply

  Then, in a new shell:

      oh                 # print the session context block
      oh repos           # list the repo kits
      oh qrd bleak-whorl # a repo's handoff
      oh-run codex       # launch codex with context piped in

  The repo kits are also in bootstrap/dist/ if you would rather copy them
  by hand.
EOF
else
  cat <<'EOF'
  Done.

  Next:
    1. source ~/.bashrc        (or open a new shell)
    2. oh                      (confirm the context loads)
    3. Pick a repo kit and hand its QRD to whichever agent you want.
       Kickdown prompts for each CLI are in handoffs/.

  Reminder: the repos are created but EMPTY of code. They hold the docs and
  the plan. Populating them is the next work session.
EOF
fi
