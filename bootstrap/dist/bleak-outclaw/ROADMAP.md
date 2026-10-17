# ROADMAP — bleak-outclaw

**Cluster:** J - Legal toolkit
**Canonical:** This repo IS canonical. Absorbing: `EquiLex` (compliance monitor),
`OpenClaw-CLI-But-Better` (ENDEMPTS docs + dashboard),
`OutClaw-Integration` (6.8 MB of docs, zero code).
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One legal toolkit. Citation analysis, argument generation, filing support.

## Current state

305 files exist. Not consolidated, not verified.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. Citation extraction and classification
2. IRAC argument generation
3. FOIA request generation
4. Judicial complaint drafting
5. Local-only operation

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| A web interface | CLI first. |
| Supporting non-federal jurisdictions | Federal first, proven. |
| Fine-tuning a legal model | Prompt the existing model until that stops working. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Seed bleak-outclaw from OutcLaw** — 305 files as the base.
- [ ] **Clean the stray '=' directory and duplicate dirs** — OutClaw_Judicial_Complaints and its (1) twin.
- [ ] **Fold EquiLex in as compliance/** — It is a compliance monitor; same domain.
- [ ] **Move ENDEMPTS docs to docs/endempts/** — From OpenClaw-CLI-But-Better.
- [ ] **Reduce OutClaw-Integration to docs/deployment/** — It is 6.8 MB of markdown and 3 images, no code.
- [ ] **Verify one real pipeline** — Feed a real document, get a real citation analysis.

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
| OllamaWrapper | already inside OutcLaw (exists) |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Legal accuracy | Bad output harms a real litigant | Never present output as legal advice; it is a drafting aid |
| Repo size | 2.4 MB plus PDFs and DOCX | Move binaries out of git if they grow |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

OutcLaw (canonical), EquiLex, OpenClaw-CLI-But-Better, OutClaw-Integration

If this repo is being merged **into** another, the merge plan is:

1. Seed bleak-outclaw from OutcLaw
2. Clean stray directories
3. EquiLex -> compliance/
4. ENDEMPTS docs -> docs/endempts/
5. OutClaw-Integration -> docs/deployment/
6. Archive the three
