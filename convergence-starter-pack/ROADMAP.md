# ROADMAP — convergence-starter-pack

**Cluster:** tooling (not part of a consolidation cluster; this is the pipeline
that the clusters get run through)
**Canonical:** yes — new work, no prior canonical copy exists
**Updated:** 2026-10-17 (pass 1)

---

## Purpose

Give three agents (Gemini discovers, Kilo verifies, OpenHands implements) a shared
contract so that repository convergence produces **comparable, provenance-linked
evidence** instead of another indiscriminate scan report. The deliverable is a
small reusable starter pack, not a new giant scanner.

## Current state

Built and verified in this session. Location: `/workspace/convergence-starter-pack`.

- `bin/converge.py` — 3 stages (intake / analyze / cluster / report), stdlib only.
- `bin/validate.py` — minimal JSON Schema validator, stdlib only.
- `schemas/` — repo_manifest, evidence, cluster.
- `agents/` — the three role contracts.
- `workflow/README.md` — handoff contract and three validation gates.
- `tests/` — **15 tests, all passing** (`python3 -m unittest discover -s tests`).
- Fixture reproduces all five required cases; the demo report emits 2 clusters,
  3 unique symbols, 1 stub, 2 proposed tasks with `apply: false`.

The prior DeepSeek scaffold was searched for and **not found** (local fs, OpenHeads
cache, all 124 account repos, GitHub code search). This pack is a from-scratch
replacement only after that search came up empty.

## In scope

The scope was decided once. It does not grow without the operator saying so out
loud. If a line here feels too narrow, that is the point.

- Bounded scanning of declared roots into `repo_manifest` artifacts (device
  provenance + per-file sha256 preserved).
- Evidence extraction for Python via `ast`, with stub detection.
- Symbol-overlap clustering that stops at `needs-verification`.
- A report that proposes tasks with `apply: false`.
- Schema conformance tests and negative controls.
- The three agent role contracts and the handoff gates.

## Out of scope / deferred

Ideas that came up and were deliberately parked. Not rejected — parked. Adding
to this list is a success, not a failure. It means scope held.

| Idea | Why deferred |
|---|---|
| Semantic / behavioural clustering (beyond symbol names) | Kilo's verification stage is the honest place for judgement; a similarity score would invite auto-merging |
| Multi-language symbol extraction (JS/TS, Go, etc.) | Only Python is extractable with stdlib `ast`; adding parsers means dependencies |
| `--from-list device_id=path` batch intake | Convenient, but one root per invocation is clearer and keeps provenance explicit |
| Auto-apply of merged results | Explicitly forbidden by the design; a human decides |
| Web UI / dashboard | Not needed; the artifacts are the interface |
| Fartographer proper | **Shelved by operator 2026-10-17.** Likely merges with Tailor, ModMind, and Syntax General Intelligence rather than being its own thing |
| Recovering the exact DeepSeek scaffold | Search came up empty; recreating it would risk "Turd Merger number seventeen" |

## Ordered plan

Work top-down. Do not start item N+1 while item N is open unless item N is
blocked on the operator (in which case note the block and move on).

1. ~~Build the pipeline + schemas + tests + fixture~~ (**done**, 15 tests green).
2. ~~Write the OH cluster prompt~~ (**done** — `workflow/cluster-prompt.md`).
3. Run the pipeline against the real device material once the operator gathers it
   (blocked on operator: material is on the three devices, not reachable here).
4. Add a `quarantine` path for manifests that fail hash verification on re-read.
5. Hand the first real cluster to Kilo and record whether the challenge held.

## Milestones

| Milestone | Meaning | Status |
|---|---|---|
| M1 — Runs | It executes without crashing on the target device | **Met** — runs on stdlib Python |
| M2 — Works | It does the actual job end to end | **Met on the fixture**; not yet on real device material |
| M3 — Shippable | Someone else could use it from the README alone | Partial — README written, not yet exercised by a second person |
| M4 — Paid | Someone has paid money for it | Not applicable |

## Dependencies on other repos

| Repo | What we need from it | Status |
|---|---|---|
| `a9-codex-grapher` | Reuse its manifest/digest ideas; do **not** duplicate its scanner | Reviewed, real, 71 tests pass; scanner not reused yet |
| `OpenHeads` | Bootstrap context, the four-doc system, `oh` helper | Available in plugin cache |
| `bridge_server.py` | Moving artifacts between the container and the Chromebook | Working, stdlib only |
| The three devices | The actual A9 / Moto 4 / cloud material to converge | **Blocked on operator** — not mounted here |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Symbol overlap is lexical, so false positives are certain | A wrong cluster wastes Kilo's time | Clusters stop at `needs-verification`; Kilo must disprove before anything proceeds |
| Partial scans mistaken for complete ones | Silent under-coverage | Bounds are recorded in `truncated` and travel with the artifact |
| Rebuilding what already exists | The exact sprawl this account is trying to reduce | Existing tools inspected first; `a9-codex-grapher` not duplicated |
| Python-only extraction | Other languages unanalysed | Stated in README "Known limits"; they are hashed, not analysed |

---

## Consolidation context

This repo is the **tooling** for the 116-repo consolidation effort, not a member
of a cluster. It is the thing the cluster packs get run through.

Related repos in this cluster:

- `a9-codex-grapher` — the existing scan/manifest layer (reuse, don't duplicate)
- `Whorl` — has an `agents/` directory; possible future home for the role contracts
- `OpenHeads` — session bootstrap and the four-doc system

If this repo is being merged **into** another, the merge plan is:

Not scheduled. If it is ever absorbed, `Whorl` is the likeliest home (it already
has an `agents/` tree), and the role contracts in `agents/` would move there while
`bin/` stays a standalone CLI.
