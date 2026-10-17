# QRD — Quick Rundown

> Handoff document. Written for the **next agent/model**, not for the human.
> Read this first, before touching anything. Update it last, before you stop.

**Repo:** bleak-tools
**Cluster:** H + N - Operator toolbelt and stubs
**Status:** NEW - absorbs 8 small repos
**Last agent pass:** 2026-10-17 — OpenHands (Claude)
**Consolidation pass:** 1 of the BleakNarratives unification effort

---

## 1. What this is (60 seconds)

One home for the account's small, genuinely useful command-line tools.
Each is 2-10 files. Individually too small to justify a repo; together they
are a real toolbelt.

Absorbs: bin-scripts (74 files, 28 Python, 20 shell), askhole-cli,
Negotiator, Kindred, Concierge, propagated_node, Gemini-CLI-Bridge,
pattern_journal.

## 2. Why it exists

Eight repos averaging under 15 KB each. Each one costs a full repo's
overhead - a README, a license, a CI config, a place in the mental model -
for a single script. Consolidating them removes 7 repos from the account
and makes the tools actually findable.

## 3. Canonical or not

This repo is NEW and IS canonical for small tools.

`bin-scripts` is the backbone - it is already an operator toolbelt with a
description that reads '~/bin operator toolbelt'. The others attach to it.

If this repo is **not** canonical, it is scheduled to be absorbed. Do not add new
features here. Add them to the canonical repo named above.

## 4. Where the intent lives

The operator's original words carry information that summaries lose. Preserve
them. Before editing anything, read:

- `MRD.txt` — what only a human can do (hard blocker list)
- `ROADMAP.md` — the ordered plan and current state
- `TODO.md` — the actionable checklist

Do **not** rewrite the operator's phrasing in these files. Add to them. If you
must reword, keep the original in a blockquote beneath your version.

## 5. State of the code (verified)

bin-scripts: 74 files (28 Python, 20 shell) - vault tools, agentfork,
boot_heal, cache_guard, ecosystem_sync, err_watch, freebuff_doctor,
hook_server, llama-serve, market_scan.

Plus: askhole-cli (2 files), Negotiator (7), Kindred (16),
Concierge (2), propagated_node (27), Gemini-CLI-Bridge (3),
pattern_journal (8).

## 6. Known good / known broken

| | |
|---|---|
| Works | bin-scripts is in daily use per its own description. |
| Broken | Unknown for the absorbed tools. |
| Unverified | Everything else. |

Anything marked **Unverified** has not been run. Do not describe it as working.
This project's whole thesis is that agents narrate fiction as fact — do not
become the thing we are building a defense against.

## 7. Constraints you must respect

- **Runtime target:** Termux / Crostini shell + Python — Termux / Crostini / Android aarch64 are the
  primary targets. Anything requiring a desktop, a GPU, Docker, or a paid cloud
  service is out of scope unless the operator says otherwise.
- **Offline-first:** the core loop must work with no network.
- **No new heavy dependencies** without operator sign-off.
- **The operator is solo, homeless, and time-constrained.** Every "nice to have"
  you add is a thing a human now has to maintain alone. Prefer deleting to adding.

## 8. Scope creep — the guardrail

This project was scoped once. The scope is in `ROADMAP.md` section "In scope".

**If you believe new work is needed, do not do it. Write it in
`ROADMAP.md` section "Out of scope / deferred" with one sentence of
justification, and leave it.** The operator has explicitly asked for help
narrowing scope. Adding features is the failure mode, not the success mode.

Signs you are scopesploding:

- You are adding a second way to do something that already works.
- You are generalizing for a use case nobody has asked for.
- You are building a config system for something with one config.
- You are renaming things to be "cleaner" without a functional reason.
- Your diff is larger than the problem.

## 9. What the last pass did

Pass 1 was analysis only. The account was scanned, all 116 repos were
content-hashed, and the duplication clusters were identified. No code in
this cluster was executed or modified.

## 10. What the next pass should do

1. Seed bleak-tools from bin-scripts
2. Move askhole-cli and Negotiator in as tools/
3. Write the one-line-per-tool index

## 11. Open questions for the operator

Questions an agent cannot answer alone. The operator reads this section.

- Which bin-scripts entries do you actually run regularly? Those get documentation first.

## 12. Handoff hygiene

Before you end your session:

- [ ] Ran whatever tests exist; recorded actual results (not intentions)
- [ ] Updated `ROADMAP.md` with real progress, not narrated progress
- [ ] Updated this QRD (sections 9 and 10)
- [ ] Did not add scope; deferred anything new to "Out of scope"
- [ ] Left the repo in a state where the next agent can start in under 5 minutes

---

## Template usage notes (delete this section once the repo is live)

**QRD** = Quick Rundown. It is a baton, not a README. Its job is to make the
next agent effective in five minutes and to stop intent from being lost in
translation between models. Write it in plain, direct sentences. No marketing.

Keep it under ~150 lines. If it grows past that, the overflow belongs in
`ROADMAP.md` or `docs/`.
