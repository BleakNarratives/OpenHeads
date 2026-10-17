#!/usr/bin/env bash
# install_bootstrap.sh - wire the OpenHeads session context into every CLI agent.
#
#   bash install_bootstrap.sh          # install
#   bash install_bootstrap.sh --uninstall
#
# Idempotent. Safe to re-run. Writes only inside the paths listed below.
#
# What it does:
#   - copies SESSION_CONTEXT.md into each agent's native context location
#   - appends a short pointer to shell rc files (does NOT replace them)
#   - creates an `oh` helper command that prints the context block
#   - never touches freebuffy (operator asked to leave it alone)

set -u

SELF="$(cd "$(dirname "$0")" && pwd)"
CTX="$SELF/SESSION_CONTEXT.md"
MARK="# >>> OpenHeads session bootstrap >>>"
MARK_END="# <<< OpenHeads session bootstrap <<<"
UNINSTALL=0
[ "${1:-}" = "--uninstall" ] && UNINSTALL=1

if [ ! -f "$CTX" ]; then
  echo "ERROR: SESSION_CONTEXT.md not found next to this script." >&2
  echo "Run this from inside a clone of BleakNarratives/OpenHeads." >&2
  exit 1
fi

say() { printf '  %s\n' "$*"; }

# ---------------------------------------------------------------------------
# 1. Agent-native context files
# ---------------------------------------------------------------------------
# Each CLI reads instructions from a different filename. We write the same
# content to all of them. AGENTS.md is the emerging cross-tool standard; the
# rest are tool-specific.

install_agent_file() {
  local path="$1" name="$2"
  local dir
  dir="$(dirname "$path")"
  if [ ! -d "$dir" ]; then
    return 1
  fi
  if [ "$UNINSTALL" -eq 1 ]; then
    [ -f "$path" ] && rm -f "$path" && say "removed $path"
    return 0
  fi
  {
    echo "<!-- OpenHeads bootstrap: generated from $SELF/SESSION_CONTEXT.md -->"
    echo "<!-- Edit SESSION_CONTEXT.md in the OpenHeads repo, not this file. -->"
    echo
    cat "$CTX"
  } > "$path"
  say "wrote $path ($name)"
}

if [ "$UNINSTALL" -eq 0 ]; then
  echo "Installing agent context files:"
  # Home-level (applies to every project)
  install_agent_file "$HOME/AGENTS.md"          "generic / cross-tool"
  install_agent_file "$HOME/.codex/AGENTS.md"   "codex"
  install_agent_file "$HOME/.gemini/AGENTS.md"  "gemini-cli"
  install_agent_file "$HOME/.aider.conf.md"     "aider"
  install_agent_file "$HOME/.kilo/AGENTS.md"    "kilo"
  install_agent_file "$HOME/.vibe/AGENTS.md"    "vibe"
  install_agent_file "$HOME/.copilot/AGENTS.md" "copilot"
  install_agent_file "$HOME/.claude/CLAUDE.md"  "claude"
  install_agent_file "$HOME/.config/opencode/AGENTS.md" "opencode"
  echo
  echo "  (skipped any tool whose config directory does not exist)"
  echo "  (freebuffy deliberately untouched)"
  echo
else
  echo "Removing agent context files:"
  install_agent_file "$HOME/AGENTS.md"          "generic"
  install_agent_file "$HOME/.codex/AGENTS.md"   "codex"
  install_agent_file "$HOME/.gemini/AGENTS.md"  "gemini-cli"
  install_agent_file "$HOME/.aider.conf.md"     "aider"
  install_agent_file "$HOME/.kilo/AGENTS.md"    "kilo"
  install_agent_file "$HOME/.vibe/AGENTS.md"    "vibe"
  install_agent_file "$HOME/.copilot/AGENTS.md" "copilot"
  install_agent_file "$HOME/.claude/CLAUDE.md"  "claude"
  install_agent_file "$HOME/.config/opencode/AGENTS.md" "opencode"
  echo
fi

# ---------------------------------------------------------------------------
# 2. Shell rc pointer + the `oh` helper
# ---------------------------------------------------------------------------

RC_FILES="$HOME/.bashrc"
[ -f "$HOME/.zshrc" ] && RC_FILES="$RC_FILES $HOME/.zshrc"

if [ "$UNINSTALL" -eq 1 ]; then
  for rc in $RC_FILES; do
    [ -f "$rc" ] || continue
    if grep -qF "$MARK" "$rc"; then
      python3 - "$rc" "$MARK" "$MARK_END" <<'PYEOF'
import sys
path, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(path).read().splitlines(True)
out, skip = [], False
for line in lines:
    if line.strip() == start:
        skip = True
        continue
    if line.strip() == end:
        skip = False
        continue
    if not skip:
        out.append(line)
open(path, "w").writelines(out)
PYEOF
      say "cleaned $rc"
    fi
  done
  echo
  echo "Uninstalled. Your other rc content was not touched."
  exit 0
fi

BLOCK="
$MARK
# OpenHeads session bootstrap - see $SELF
export OPENHEADS_HOME=\"$SELF\"

# Print the agent context block, or pipe it into a CLI.
oh() {
  case \"\${1:-}\" in
    ''|ctx|context)  cat \"\$OPENHEADS_HOME/SESSION_CONTEXT.md\" ;;
    readme)          cat \"\$OPENHEADS_HOME/README.md\" ;;
    qrd)             cat \"\$OPENHEADS_HOME/bootstrap/dist/\${2:-bleak-higgins}/QRD.md\" ;;
    mrd)             cat \"\$OPENHEADS_HOME/bootstrap/dist/\${2:-bleak-higgins}/MRD.txt\" ;;
    todo)            cat \"\$OPENHEADS_HOME/bootstrap/dist/\${2:-bleak-higgins}/TODO.md\" ;;
    roadmap)         cat \"\$OPENHEADS_HOME/bootstrap/dist/\${2:-bleak-higgins}/ROADMAP.md\" ;;
    repos)           ls \"\$OPENHEADS_HOME/bootstrap/dist\" ;;
    handoff)         cat \"\$OPENHEADS_HOME/handoffs/\${2:-generic}.md\" ;;
    status)          git -C \"\$OPENHEADS_HOME\" --no-pager log --oneline -5 2>/dev/null || echo 'not a git repo' ;;
    *)               echo 'usage: oh [ctx|readme|qrd|mrd|todo|roadmap|repos|handoff|status] [repo]' ;;
  esac
}

# Start any CLI agent with the context preloaded.
#   oh-run codex            -> codex with context on stdin
#   oh-run gemini           -> gemini with context on stdin
oh-run() {
  local cli=\"\${1:-\$1}\"
  if [ -z \"\$cli\" ]; then echo 'usage: oh-run <cli> [args...]'; return 1; fi
  shift
  if ! command -v \"\$cli\" >/dev/null 2>&1; then
    echo \"\$cli not found on PATH\"; return 1
  fi
  echo \"[openheads] launching \$cli with session context\" >&2
  { echo '=== SESSION CONTEXT (OpenHeads) ==='; cat \"\$OPENHEADS_HOME/SESSION_CONTEXT.md\";
    echo; echo '=== BEGIN ==='; } | \"\$cli\" \"\$@\"
}

alias ohctx='cat \"\$OPENHEADS_HOME/SESSION_CONTEXT.md\"'
$MARK_END
"

for rc in $RC_FILES; do
  [ -f "$rc" ] || touch "$rc"
  if grep -qF "$MARK" "$rc"; then
    say "already installed in $rc (skipping)"
  else
    printf '%s\n' "$BLOCK" >> "$rc"
    say "appended to $rc"
  fi
done

echo
echo "Done. Open a new shell, or run:  source ~/.bashrc"
echo
echo "Try:"
echo "  oh                 # print the context block"
echo "  oh repos           # list the repo kits"
echo "  oh qrd bleak-whorl # that repo's handoff"
echo "  oh-run codex       # launch codex with context piped in"
