# ROADMAP — bleak-tools

**Cluster:** H + N - Operator toolbelt and stubs
**Canonical:** This repo is NEW and IS canonical for small tools.

`bin-scripts` is the backbone - it is already an operator toolbelt with a
description that reads '~/bin operator toolbelt'. The others attach to it.
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

One toolbelt. Every small tool lives here and is documented in one index.

## Current state

bin-scripts exists and works. Seven repos to absorb.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

1. bin-scripts as the base, with an indexed README
2. The small CLI tools: askhole, Negotiator, Kindred, Concierge
3. Gemini-CLI-Bridge, pattern_journal

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| Unifying the CLI interface | They are separate tools. A wrapper is a second way to call them. |
| Packaging as a pip install | Local use first. |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

- [ ] **Seed bleak-tools from bin-scripts** — It is the base.
- [ ] **Add tools/ per absorbed tool** — One directory each, preserving the original file.
- [ ] **Write the tool index** — One line per tool in the README so they are findable.
- [ ] **Archive the 7 absorbed repos** — With pointer READMEs.

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
| none | - | - |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Tools rot unmaintained | Toolbelt becomes a graveyard | The README index names what is actually used vs parked |

---

## Consolidation context

This repo is part of a 116-repo consolidation effort. See the cluster table in
the account-level roadmap. Related repos in this cluster:

bin-scripts (base), askhole-cli, Negotiator, Kindred, Concierge, propagated_node, Gemini-CLI-Bridge, pattern_journal

If this repo is being merged **into** another, the merge plan is:

1. Seed bleak-tools from bin-scripts
2. tools/<name>/ per absorbed tool
3. Indexed README
4. Archive the 7
