# ROADMAP — bleak-whorl

**Cluster:** E - Swarm core
**Canonical:** This repo IS canonical. Absorbing: `Vigil`, `SyntaxIntelligence`,
`Swarmulacrum`, `core_framework`, `propagated_node`, `Concierge`.

Note that `core_framework` states in its own README that it contains
**no copied source code** - every file is a pointer into canonical trees.
It is a documentation repo wearing a code repo's clothes.
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One swarm core. Every other swarm-shaped repo folds in here or is archived.

## Current state

Whorl is healthy and modular. Six repos queued for absorption.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. The module set already in Whorl: scouts, forge, hotseat, loom, agents, tailor, nostr, slice, core
2. Vigil's integrity/geometry/fabrication as whorl/scouts/ substrate
3. SyntaxIntelligence's tier ladder as whorl/governance/
4. SQLite persistence and offline operation

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| Web UI | The CLI is the interface. A web UI is a second front end. |
| Plugin registry | Modules are plugins already. |
| Distributed multi-node | propagated_node exists but single-node is not finished. |
| Renaming modules for consistency | Churn without function. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Seed bleak-whorl from Whorl** — Clean tree, no history rewrite.
- [ ] **Add whorl/scouts/integrity + geometry + fabrication** — Port from Vigil, keep the HMAC signing and quadratic dispersion logic intact.
- [ ] **Add whorl/governance/tiers** — Port the 6-tier ladder from SyntaxIntelligence.
- [ ] **Move core_framework's pointer table into docs/ORCHESTRATION.md** — It is documentation. Treat it as documentation.
- [ ] **Reconcile the duplicate core_framework/** — It also exists inside a9-codex-grapher. One of them is stale.
- [ ] **Archive the absorbed repos** — With pointer READMEs.

## Milestones

| Milestone | Meaning | Status |
|---|---|---|
| M1 — Runs | It executes without crashing on the target device | not started |
| M2 — Works | It does the actual job end to end | not started |
| M3 — Shippable | Someone else could use it from the README alone | not started |
| M4 — Paid | Someone has paid money for it | not started |

## Dependencies on other repos

| Repo | What we need from it | Status |
|---|---|---|
| Vigil | integrity.py, geometry.py, fabrication.py (to absorb) |
| SyntaxIntelligence | tier ladder (to absorb) |
| Agentic-Almanac | supplies docs/AGENT_ALMANAC.json to whorl/src/skill/scout.py (exists) |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Absorbing too much at once | Nothing works and nothing is testable | Absorb one repo per pass, verify imports after each |
| Whorl's own tests are thin | Regressions go unnoticed | Add an import smoke test for every module first |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

Whorl (canonical), Vigil, SyntaxIntelligence, Swarmulacrum, core_framework, propagated_node, Concierge

If this repo is being merged **into** another, the merge plan is:

1. Seed bleak-whorl from Whorl
2. Absorb Vigil as whorl/scouts/{integrity,geometry,fabrication}.py
3. Absorb SyntaxIntelligence tiers as whorl/governance/tiers.py
4. core_framework pointer table becomes docs/ORCHESTRATION.md
5. Archive Vigil, SyntaxIntelligence, Swarmulacrum, core_framework, propagated_node, Concierge
