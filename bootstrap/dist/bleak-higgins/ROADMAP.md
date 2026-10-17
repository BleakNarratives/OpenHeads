# ROADMAP — bleak-higgins

**Cluster:** A - Mrs. Higgins pipeline
**Canonical:** This repo IS canonical. Three sibling repos are absorbed into it:
`mrs-higgins`, `mrs-higgins-a9`, `mrs-higgins-moto`.

They were never different projects. They are the same pipeline pointed
at different device paths. The shared README is byte-identical across all
four, as are setup.sh, mrs_higgins.sh, the static assets, the templates,
and all ~50 saas_packages/*.json files.
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One canonical Mrs-Higgins pipeline, device-agnostic, with a profile per target device.

## Current state

4 repos to be merged into 1. Porting not yet started.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. The pipeline loop: load packages, route, invoice, follow up, reconcile, report
2. Device profiles for Termux, Crostini, and moto targets
3. Lightning payments via Voltage
4. Ollama-powered copy generation
5. The saas_packages catalogue

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| Web dashboard | The CLI briefing already answers the question. A dashboard is a second way to do something that works. |
| Multi-user support | One operator. There is no second user. |
| Cloud sync | Offline-first is a requirement, not a limitation to fix. |
| Plugin system | Nothing needs plugins yet. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Create the canonical repo** — Push mrs-higgins-chromebook's tree as the initial commit of bleak-higgins.
- [ ] **Port 20 unique blobs from a9** — Diff against canonical, copy in what is genuinely new.
- [ ] **Port 17 unique blobs from moto** — Same process.
- [ ] **Port 3 unique blobs from mrs-higgins** — Same process.
- [ ] **Add device-profiles/** — Extract the hardcoded device paths into profiles: termux.yaml, crostini.yaml, moto.yaml.
- [ ] **Archive the three siblings** — With a redirect note in each README.
- [ ] **First real run** — Execute the loop on the Chromebook and record what actually happens.

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
| payment_system | Lightning + Monero + Stripe + license keys (exists, not wired) |
| passive_income_swarm | FastAPI gateway if a network face is needed (exists, separate) |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Voltage API changes | Payment loop breaks | Wrap in one adapter module so only one file changes |
| Device paths hardcoded | Runs on one device only | device-profiles/ is the fix; do it in pass 2 |
| No tests | Cannot tell working from broken | Add one smoke test that runs the briefing command |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

mrs-higgins, mrs-higgins-a9, mrs-higgins-chromebook (canonical), mrs-higgins-moto, The-Werkz (carries a 5th copy)

If this repo is being merged **into** another, the merge plan is:

1. Seed new repo from mrs-higgins-chromebook tree
2. Port unique blobs from a9, moto, mrs-higgins
3. Introduce device-profiles/, refactor path references to read from them
4. Archive the three siblings with a pointer README
