# ROADMAP — bleak-vertical-ai

**Cluster:** G - Vertical AI / Boardroom
**Canonical:** This repo IS canonical. Absorbing: `Vertical-AI`, `Vertical-AI-V4`,
`Vertical-AI-Notebook-LM`, `Vert-AI-AI-Studio-Fromtend`, `vertical_local`.

Six repos share one product name. Three are front ends for the same engine.
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One boardroom engine with multiple front ends, and a clear product offering.

## Current state

Six repos, one concept, no consolidation.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. The boardroom engine: personas, debate, debrief
2. The chairman / adjudication logic
3. One front end (CLI)

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| Three separate front ends | One CLI until the engine is proven. |
| The Notebook-LM audio deep dive | A different product wearing the same name. |
| Codebase evolution daemon | Ambitious, unrelated to the boardroom's core job. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Seed bleak-vertical-ai from Official-Vertical-AI-Boardroom** — The real engine.
- [ ] **Verify the boardroom runs** — One question in, one debrief out.
- [ ] **Move MarketScout.zip out of git** — Binaries do not belong in the tree.
- [ ] **Absorb the front ends as ui/** — Or archive them, if the CLI is enough.
- [ ] **Decide the Notebook-LM's fate** — It may be its own product.

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
| payment_system | README says it was built for the Boardroom (exists) |
| tribunal | cites Boardroom as its methodology source (related) |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Six repos, one name | Nobody knows which is current | One canonical, explicit archives |
| Log files and zips in git | Bloats the repo | Gitignore and remove |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

Official-Vertical-AI-Boardroom (canonical), Vertical-AI, Vertical-AI-V4, Vertical-AI-Notebook-LM, Vert-AI-AI-Studio-Fromtend, vertical_local

If this repo is being merged **into** another, the merge plan is:

1. Seed bleak-vertical-ai from Official-Vertical-AI-Boardroom
2. Verify one boardroom run end to end
3. Front ends -> ui/, or archive
4. vertical_local docs -> docs/
5. Archive the absorbed repos
