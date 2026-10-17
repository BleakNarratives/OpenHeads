# Handoff — GitHub Copilot

Copilot is IDE-side and best at in-editor completion, refactors, and explaining
existing code. Use it for the "help me understand this file" jobs.

---

## Kickdown prompt — triage the legal toolkit

```
Read ~/OpenHeads/SESSION_CONTEXT.md, then open
~/OpenHeads/bootstrap/dist/bleak-outclaw/QRD.md.

You are working on the BleakNarratives consolidation, legal toolkit cluster.

TASK: Triage OutcLaw's 305 files and produce a map of what is real.

OutcLaw is a pro se legal AI toolkit: citation extraction, citation fraud
detection, IRAC argument generation, FOIA requests, judicial complaints.
97 Python files, 78 txt, 43 md, plus PDFs and DOCX.

Method:
1. Read the entry points first (LAUNCH_ME.py, app.py, __init__.py).
2. Classify every Python file: CORE (the actual product), SUPPORT (helpers),
   EXPERIMENT (superseded or dead), or BINARY-ADJACENT (wrappers around data).
3. Flag the stray '=' directory and the duplicate OutClaw_Judicial_Complaints
   directories - what are they?
4. Output the map to docs/FILE_TRIAGE.md.

Do not delete anything. Do not refactor. Report only.

Rules: do not comment on naming. Do not propose a restructure yet. Just tell us
what is there.
```

---

## Second session — explain the citation pipeline

```
Read ~/OpenHeads/bootstrap/dist/bleak-outclaw/docs/FILE_TRIAGE.md.

TASK: Explain outclaw_arch.py and outclaw_semantic.py in plain language.

For each:
- what it takes as input
- what it produces as output
- the actual algorithm, step by step
- what could go wrong (false positives, missed citations, edge cases)

Write it to docs/PIPELINE_EXPLAINED.md so a future agent does not have to
reverse-engineer it again.

Do not modify the code. Do not push.
```

---

## Why this shape

Copilot's in-editor context makes it good at reading a large unfamiliar codebase
and reporting back. 305 files is more than anyone wants to read by hand, and
this is exactly the kind of survey work that should be delegated.
