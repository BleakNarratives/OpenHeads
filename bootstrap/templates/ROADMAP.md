# ROADMAP — {{REPO}}

**Cluster:** {{CLUSTER}}
**Canonical:** {{CANONICAL_STATUS}}
**Updated:** {{DATE}} (pass {{PASS}})

---

## Purpose

{{PURPOSE}}

## Current state

{{CURRENT_STATE}}

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

{{IN_SCOPE_LIST}}

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
{{DEFERRED_TABLE}}

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

{{PLAN_LIST}}

## Milestones

| Milestone | Meaning | Status |
|---|---|---|
| M1 — Runs | It executes without crashing on the target device | {{M1}} |
| M2 — Works | It does the actual job end to end | {{M2}} |
| M3 — Shippable | Someone else could use it from the README alone | {{M3}} |
| M4 — Paid | Someone has paid money for it | {{M4}} |

## Dependencies on other repos

| Repo | What we need from it | Status |
|---|---|---|
{{DEPS_TABLE}}

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
{{RISKS_TABLE}}

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

{{CLUSTER_MEMBERS}}

If this repo is being merged **into** another, the merge plan is:

{{MERGE_PLAN}}
