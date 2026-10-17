# Handoff — Aider

Aider is best at tight, reviewable, commit-per-change edits inside a git repo.
Use it for surgical fixes where you want every change to be a clean commit.

---

## Kickdown prompt

```
Read ~/OpenHeads/SESSION_CONTEXT.md and
~/OpenHeads/bootstrap/dist/bleak-verification/QRD.md.

You are working on the BleakNarratives consolidation, in the verification
cluster (tribunal + ConstraintOps).

TASK: Produce one honest end-to-end demo of the claim detector.

The product's thesis: an AI coding agent claims "done" or "all tests pass"
without evidence, and this tool catches it.

Method:
1. Create demos/claim_detector/ with a minimal harness:
   - a fake agent transcript that contains 3 claims, 2 unbacked and 1 backed
   - the detector run against it
   - output showing which claims were flagged and why
2. Keep it runnable with: python3 demos/claim_detector/run.py
3. No new dependencies. Stdlib only.
4. One commit per file, clear messages.

Do not push. Do not refactor tribunal's existing modules. Build only the demo.

Rules: no scope expansion. If you think the demo needs more, write the idea in
ROADMAP.md under "Out of scope" and continue with the small version.
```

---

## Why this shape

The demo is the product. Everything else in the verification cluster is
supporting material. Aider's commit-per-change workflow keeps it reviewable.

## Second session — wire the guards

```
Read ~/OpenHeads/bootstrap/dist/bleak-verification/ROADMAP.md.

TASK: Move EquiLex and MemGuard into guards/ as two self-contained modules.

1. guards/compliance.py  <- from EquiLex (compliance monitor)
2. guards/memory.py      <- from MemGuard (PSI-driven OOM defense)
3. Each must import cleanly with no third-party dependencies.
4. Add guards/__init__.py exposing both.
5. Add one test per guard that runs without network.

One commit per guard. Do not modify tribunal's existing code.
Do not push.
```
