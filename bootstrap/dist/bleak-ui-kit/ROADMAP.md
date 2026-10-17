# ROADMAP — bleak-ui-kit

**Cluster:** C - React/Vite scaffold sprawl
**Canonical:** This repo is NEW and IS canonical for scaffolding. The 17 scaffold repos
either consume it or get archived.

Triage recommendation: archive `another-flop`, `are_n_dee`,
`Tentative-Title`, `reverse_filter`, `homeless_mike_tarot` outright - the
names indicate experiments. Keep the rest for feature extraction.
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One starter. Every front end consumes it. No more scaffold copies.

## Current state

17 parallel scaffolds. Consolidation not started.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. Vite + React + TypeScript starter with the account's shared config
2. Shared components: layout, theming, the metadata.json convention
3. A documented way to consume it

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| A component library | A starter, not a design system. Components come from real apps. |
| Storybook | Heavy dependency, no current user. |
| Publishing to npm | Local consumption first. npm is distribution later. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Extract the canonical config set** — tsconfig.json, vite.config.ts, index.html, metadata.json.
- [ ] **Triage the 17 repos** — Which are products, which are experiments.
- [ ] **Build the starter** — Config plus a minimal App shell plus README.
- [ ] **Re-point the survivors** — Consume the starter, delete local config copies.
- [ ] **Archive the experiments** — The five named above, unless told otherwise.

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
| EquiNex-Universal-Dashboard | richest scaffold, best extraction source (exists) |
| odds-of-the-gods | largest at 156 files, has real components (exists) |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Breaking a working app | Lost work | Extract first, migrate one app at a time |
| Nobody adopts it | 18 scaffolds instead of 17 | Migrate one real app end to end as proof |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

17 scaffold repos listed in section 5, plus Code-City-Apocalypse and Skin-Deep which also carry scaffolds

If this repo is being merged **into** another, the merge plan is:

1. Extract shared config into bleak-ui-kit
2. Migrate one real app (EquiNex-Universal-Dashboard) as proof
3. Migrate the survivors one at a time
4. Archive the experiments
