# Handoff — Gemini CLI

Gemini CLI has a large context window and is good at reading broadly then
summarizing. Use it for survey-and-report jobs where reading everything matters
more than writing code.

---

## Kickdown prompt — verify the pass-1 analysis

```
Read ~/OpenHeads/SESSION_CONTEXT.md, then
~/OpenHeads/analysis/BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md.

You are working on the BleakNarratives consolidation.

TASK: Verify the pass-1 analysis against the live repos, and correct anything
that is wrong.

The pass-1 scan claimed:
- 116 public repos, 26 completely empty (zero files, zero bytes)
- 708 blob groups byte-identical across 2+ repos
- 17 repos are clones of one React/Vite scaffold
- mrs-higgins family: 4 repos, 460 files, 210 distinct blobs

Method:
1. For each of the 26 repos claimed empty, confirm via the GitHub API that
   size == 0. Report any that are NOT empty.
2. Spot-check 10 of the 17 scaffold repos: is tsconfig.json really identical?
3. Spot-check the mrs-higgins claim: are the READMEs really byte-identical?
4. Report every correction in analysis/CORRECTIONS.md.

Do not push. Do not edit the roadmap. Report findings only.

Rules: no scope expansion, no feature suggestions, no naming commentary.
If a claim is wrong, say so plainly with the evidence.
```

---

## Why this shape

The pass-1 numbers drive real decisions (which repos to archive). They should be
independently verified before anything is deleted. Gemini's context window makes
it good at holding the whole account in view at once.

## Second session — stress-test the money list

```
Read ~/OpenHeads/SESSION_CONTEXT.md and
~/OpenHeads/bootstrap/ACCOUNT_MRD.txt section 6 (the money list).

TASK: Stress-test the money list. For each ranked path, find the specific,
current, real-world obstacles the operator would hit, and what it actually takes
to clear each one.

For each path report:
- the exact signup / eligibility requirement
- whether it needs KYC identity documents (this is the binding constraint)
- realistic time to first dollar
- the single most likely reason it fails

Be blunt. The operator is homeless and needs accurate information more than
encouragement. Do not pad the list with paths that do not actually work without
identity documents.
```

---

## Third session — map the swarm core

```
Read ~/OpenHeads/bootstrap/dist/bleak-whorl/QRD.md and ROADMAP.md.

TASK: Map the actual module surface of Whorl and the five repos queued for
absorption (Vigil, SyntaxIntelligence, Swarmulacrum, core_framework,
propagated_node, Concierge).

For each: list every importable module, its public functions, and whether it has
tests. Then report overlaps - functions that exist in more than one repo.

Output a table to bleak-whorl/docs/ABSORPTION_MAP.md.

Do not push. Do not refactor anything. This is reconnaissance only.
```
