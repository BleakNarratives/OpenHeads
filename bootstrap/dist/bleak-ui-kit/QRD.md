# QRD — Quick Rundown

> Handoff document. Written for the **next agent/model**, not for the human.
> Read this first, before touching anything. Update it last, before you stop.

**Repo:** bleak-ui-kit
**Cluster:** C - React/Vite scaffold sprawl
**Status:** NEW - replaces 17 scaffold repos
**Last agent pass:** 2026-10-17 — OpenHands (Claude)
**Consolidation pass:** 1 of the BleakNarratives unification effort

---

## 1. What this is (60 seconds)

One Vite + React + TypeScript starter that the account's front-end work
consumes instead of copying.

Seventeen repos in this account are clones of the same scaffold. Their
tsconfig.json is byte-identical in 15 of them. vite.config.ts is identical
in 12. The differences are almost entirely in App.tsx.

## 2. Why it exists

Seventeen copies of one config file is 17 places for the same bug to live
and 17 upgrades to perform by hand. A shared starter converts that into one
place. It is the cheapest large win in the account.

## 3. Canonical or not

This repo is NEW and IS canonical for scaffolding. The 17 scaffold repos
either consume it or get archived.

Triage recommendation: archive `another-flop`, `are_n_dee`,
`Tentative-Title`, `reverse_filter`, `homeless_mike_tarot` outright - the
names indicate experiments. Keep the rest for feature extraction.

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

17 repos, 656 files total, 580 distinct blobs. Only 10 blobs are shared
by 3+ repos, which means the duplication is in config, not in features.

Scaffold repos: ShipWrekD-OS-Syntax-AI-Driven-IDE, Vertical-AI,
Vert-AI-AI-Studio-Fromtend, ModMind-GlassRing-and-Company,
ModMind-Identity-Utility, Kick-Rock, another-flop, are_n_dee,
reverse_filter, Eww, Tentative-Title, homeless_mike_tarot,
nesting_bestie_taylor_demo, odds-of-the-gods, fd_cohort,
EquiNex-Universal-Dashboard, Pivot

## 6. Known good / known broken

| | |
|---|---|
| Works | Each scaffold presumably runs. None verified by an agent. |
| Broken | Unknown. |
| Unverified | Which of the 17 contain real features worth extracting. |

Anything marked **Unverified** has not been run. Do not describe it as working.
This project's whole thesis is that agents narrate fiction as fact — do not
become the thing we are building a defense against.

## 7. Constraints you must respect

- **Runtime target:** Node/Vite. Build output is static, so it deploys anywhere. — Termux / Crostini / Android aarch64 are the
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

1. Extract the canonical tsconfig/vite.config/index.html set
2. Triage the 17: product, experiment, or already dead
3. Migrate EquiNex-Universal-Dashboard as the first consumer

## 11. Open questions for the operator

Questions an agent cannot answer alone. The operator reads this section.

- Which of the 17 scaffolds are you still actively working on?

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
