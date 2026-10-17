# QRD — Quick Rundown

> Handoff document. Written for the **next agent/model**, not for the human.
> Read this first, before touching anything. Update it last, before you stop.

**Repo:** bleak-higgins
**Cluster:** A - Mrs. Higgins pipeline
**Status:** canonical (merging in 3 repos)
**Last agent pass:** 2026-10-17 — OpenHands (Claude)
**Consolidation pass:** 1 of the BleakNarratives unification effort

---

## 1. What this is (60 seconds)

A fully local, offline-capable SaaS routing pipeline that runs on an
Android phone under Termux. It loads product packages, generates
platform-specific listings, creates Lightning invoices, follows up on
unpaid leads, reconciles payments, and reports what is actually working.

The crew of scripts (front_desk_lady, bookkeeper, the_closer, copywriter,
scout, the_ledger, briefing) is the product. One shell command runs it.

## 2. Why it exists

It is the closest thing in this account to a revenue loop that needs no
KYC, no cloud, and no team. Lightning is the only payment rail that does
not require identity documents, and this pipeline already integrates it.
That makes it the fastest available path to a first dollar given the
operator's current constraints.

## 3. Canonical or not

This repo IS canonical. Three sibling repos are absorbed into it:
`mrs-higgins`, `mrs-higgins-a9`, `mrs-higgins-moto`.

They were never different projects. They are the same pipeline pointed
at different device paths. The shared README is byte-identical across all
four, as are setup.sh, mrs_higgins.sh, the static assets, the templates,
and all ~50 saas_packages/*.json files.

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

Four repos, 460 files total, collapsing to ~210 distinct blobs.

| Repo | Files | Unique blobs |
|---|---|---|
| mrs-higgins | 21 | 3 |
| mrs-higgins-a9 | 76 | 20 |
| mrs-higgins-moto | 26 | 17 |
| mrs-higgins-chromebook | 337 | 109 (canonical) |

40 unique blobs need to be ported in from the three siblings.

## 6. Known good / known broken

| | |
|---|---|
| Works | Not verified by an agent yet. Operator reports the loop runs end to end. |
| Broken | Unknown - no test suite exists. |
| Unverified | Everything. Pass 1 was analysis only; no code was executed. |

Anything marked **Unverified** has not been run. Do not describe it as working.
This project's whole thesis is that agents narrate fiction as fact — do not
become the thing we are building a defense against.

## 7. Constraints you must respect

- **Runtime target:** Termux / Android aarch64 primary; Crostini secondary — Termux / Crostini / Android aarch64 are the
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

1. Seed bleak-higgins from mrs-higgins-chromebook
2. Diff and port the 40 unique blobs from the three siblings
3. Write device-profiles/ and refactor path references

## 11. Open questions for the operator

Questions an agent cannot answer alone. The operator reads this section.

- Which device is the actual production target - the moto or the Chromebook?

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
