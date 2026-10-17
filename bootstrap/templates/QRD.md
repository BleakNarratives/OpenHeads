# QRD — Quick Rundown

> Handoff document. Written for the **next agent/model**, not for the human.
> Read this first, before touching anything. Update it last, before you stop.

**Repo:** {{REPO}}
**Cluster:** {{CLUSTER}}
**Status:** {{STATUS}}
**Last agent pass:** {{DATE}} — {{MODEL_OR_AGENT}}
**Consolidation pass:** {{PASS}} of the BleakNarratives unification effort

---

## 1. What this is (60 seconds)

{{WHAT_THIS_IS}}

## 2. Why it exists

{{WHY}}

## 3. Canonical or not

{{CANONICAL_STATUS}}

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

{{CODE_STATE}}

## 6. Known good / known broken

| | |
|---|---|
| Works | {{WORKS}} |
| Broken | {{BROKEN}} |
| Unverified | {{UNVERIFIED}} |

Anything marked **Unverified** has not been run. Do not describe it as working.
This project's whole thesis is that agents narrate fiction as fact — do not
become the thing we are building a defense against.

## 7. Constraints you must respect

- **Runtime target:** {{RUNTIME}} — Termux / Crostini / Android aarch64 are the
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

{{LAST_PASS}}

## 10. What the next pass should do

{{NEXT_LIST}}

## 11. Open questions for the operator

Questions an agent cannot answer alone. The operator reads this section.

- {{QUESTION_1}}

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
