# ROADMAP — bleak-verification

**Cluster:** D - Verification and adversarial review
**Canonical:** This repo IS canonical. Absorbing: `ConstraintOps` (product, pricing,
docs), `Praudit` (shim wrappers), `EquiLex` (compliance monitor),
`MemGuard` (OOM defense).

`tribunal` is the engine. `ConstraintOps` is the commercial face. The
other three are runtime guards with the same verdict-bus shape.
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One verification product: engine, guards, and a sellable service around it.

## Current state

Engine and product docs exist separately. Not yet joined.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. Claim detection: catch 'done' / 'verified' / 'tests pass' without evidence
2. Evidence checking against actual filesystem and test state
3. The ConstraintOps service offering and its pricing tiers
4. Runtime guards: OOM pressure and compliance checks

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| Supporting every CLI agent | Start with one. Gemini CLI or Codex CLI, whichever is actually used. |
| A hosted SaaS version | Local first. Hosting is a second business. |
| The VSCode extension | CLI proves the concept; the extension is distribution later. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Seed bleak-verification from tribunal** — Engine first.
- [ ] **Bring ConstraintOps docs into docs/service/** — Positioning, pricing, client forms, outreach.
- [ ] **Fold Praudit shims into wrapper/** — They are integration adapters.
- [ ] **Fold EquiLex and MemGuard into guards/** — Both produce verdicts on runtime state.
- [ ] **Write one end-to-end demo** — An agent claims done; the tool catches it. That demo is the product.
- [ ] **Archive the four absorbed repos** — With pointer READMEs.

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
| Official-Vertical-AI-Boardroom | Tribunal cites it as the source methodology (exists) |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Scope: supporting all agents | Nothing ships | One agent integration first, proven end to end |
| Overlap with Code City | Two places to maintain verification | Code City consumes this; it does not reimplement it |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

tribunal (canonical), ConstraintOps, Praudit, EquiLex, MemGuard

If this repo is being merged **into** another, the merge plan is:

1. Seed bleak-verification from tribunal
2. ConstraintOps docs -> docs/service/
3. Praudit shims -> wrapper/
4. EquiLex + MemGuard -> guards/
5. Archive all four
