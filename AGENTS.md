# AGENTS.md — repository context

## What this workspace is

This workspace is the **analysis seat** for the BleakNarratives GitHub account
(`github.com/BleakNarratives`). There is no application source here. Work
products are analysis, catalogs, and automation scripts, delivered as files.

The operator works from a **Chromebook** and cannot access this container's
filesystem directly. See "Delivery" below.

## Account facts (verified 2026-10-16)

- 116 public repos, 0 private, 0 archived, 2 forks.
- ~0.39 GB total. `Skin-Deep` (257 MB) + `sprint-ralphy` (89 MB) = 89% of bytes.
- **26 repos are completely empty** (zero files, zero bytes).
- 708 blob groups are byte-identical across 2+ repos.
- 17 repos are clones of the same React/Vite scaffold.

## Known repo clusters

Full detail in `BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md`; machine-readable in
`bleak_unification_catalog.json`. Summary:

| Cluster | Canonical | Members |
|---|---|---|
| A mrs-higgins | `mrs-higgins-chromebook` | mrs-higgins, -a9, -moto (fork-per-device) |
| B live-wrappers | NEW `live-wrappers` | riffusion/claude/gemini/copilot-live-wrapper |
| C react-scaffolds | NEW `bleak-ui-kit` | 17 Vite apps, identical tsconfig/vite.config |
| D verification | `tribunal` | ConstraintOps, Praudit, EquiLex, MemGuard |
| E swarm-core | `Whorl` | Vigil, SyntaxIntelligence, Swarmulacrum, core_framework, propagated_node, Concierge |
| F code-city | `Code-City-Apocalypse` | PivotCity, modmind-shell, EquiNex-Universal-Dashboard, Vertical-AI-V4 |
| G vertical-ai | `Official-Vertical-AI-Boardroom` | Vertical-AI, -V4, -Notebook-LM, Vert-AI-Studio-Fromtend, vertical_local |
| H outreach | `Pytch` | passive_income_swarm, Product-Launch-Engine, askhole-cli, Negotiator, Kindred |
| J legal | `OutcLaw` | EquiLex, OpenClaw-CLI-But-Better, OutClaw-Integration |
| K android-ports | keep as-is | zeroclaw-android, crown-jules, Hermes, goose-mobile |
| L zip-dumps | extract then delete | claudio_jr, Rampage-Refactor, ChAImeleon |
| M scouts | NEW `scouts-lab` | ChronoScouts, Kronos-Scouts |
| N stubs | delete | Smell-Scan, Meatwatch, nesting_bestie, hotseat |

Recurring root cause of sprawl: **one repo per device, per provider, per
scaffold** instead of one repo with profiles/adapters/templates inside it.

## Delivery — the drive bridge

The operator's Chromebook can reach this container over HTTPS. Two lanes:

- `https://work-1-hlucqceaikkyoewj.prod-runtime.all-hands.dev/` (port 12000)
- `https://work-2-hlucqceaikkyoewj.prod-runtime.all-hands.dev/` (port 12001)

`/workspace/bridge/bridge_server.py` (stdlib only) serves `/outbox` for download
and accepts uploads into `/workspace/bridge/inbox`.

Start it:

```bash
cd /workspace/bridge && nohup python3 bridge_server.py > /tmp/bridge.log 2>&1 &
```

Publish a deliverable:

```bash
cp <file> /workspace/bridge/outbox/
```

The operator pulls with:

```bash
curl -sS <LANE>/outbox/<file> -o ~/<file>
```

**Security:** the lane is open to anyone holding the URL while running. Never
place secrets, keys, or personal-data dumps in `outbox/`. Prefer the operator's
own `cat << 'EOF'` terminal paste for anything sensitive. Check
`/workspace/bridge/inbox/` at the start of a session for files they pushed up.

## Environment notes

- GitHub access via `$GITHUB_TOKEN` (authenticated as BleakNarratives). Use the
  REST API; `gh` is installed but not logged in.
- There is no working `git` remote in `/workspace/project` (empty repo, no
  commits). Do not push unless the operator asks.
- Useful pattern for scanning: fetch `git/trees/<branch>?recursive=1` for every
  repo and index blobs by SHA — that is how the duplication numbers above were
  measured, and it beats reading names.

## Working style

The operator prefers concrete artifacts over discussion, and wants items
knocked off a checklist one at a time. When asked to proceed on consolidation,
pick the top unfinished item from the roadmap's punch list and complete it
end to end rather than re-summarizing.
