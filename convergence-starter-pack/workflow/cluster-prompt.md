# OH cluster prompt — hand this to an OpenHands session

Self-contained. A fresh OpenHands session with no prior context should be able to
run this end to end. Copy everything between the rules below into the new session
as the first message.

---

## MISSION

You are the **implementation agent** for one bounded repository-convergence
cluster. You will run a small existing pipeline, verify its output honestly, and
produce a reviewable proposal. You will **not** merge anything.

## CONTEXT

- Pipeline location: `/workspace/convergence-starter-pack` (stdlib only, Python 3.9+).
- Read first, in this order:
  1. `/workspace/convergence-starter-pack/AGENTS.md` — the safety rules. They bind you.
  2. `/workspace/convergence-starter-pack/workflow/README.md` — handoff gates.
  3. `/workspace/convergence-starter-pack/README.md` — what the tool does.
- The three stages: `intake` → `analyze` → `cluster` → `report`.

## INPUTS YOU MUST BE GIVEN

Do not start without these. If any is missing, stop and ask — do not guess.

- `DEVICE_ID` — stable id of the producing device (e.g. `moto-4-5g-2024`).
- `ROOT` — the absolute path of the bounded tree to scan.
- `CLUSTER_HINT` — optional: what the operator believes overlaps, and with what.

## DO

1. Confirm the tree exists and note its size. If `ROOT` is not reachable, stop
   and report that — do not scan something else and call it the same thing.
2. Run, in order, and keep the real output:
   ```bash
   cd /workspace/convergence-starter-pack
   python3 -m unittest discover -s tests          # must be green before you trust the tool
   python3 bin/converge.py intake  --device-id "$DEVICE_ID" --root "$ROOT" \
       --out reports/manifest.json
   python3 bin/converge.py analyze --manifest reports/manifest.json \
       --out reports/evidence.json
   python3 bin/converge.py report  --manifests reports/manifest.json \
       --out reports/report.json
   ```
3. Read `reports/report.json`. For each cluster, open the cited `source_path`s and
   judge whether the shared symbol really is the same behaviour. Record your
   verdict per cluster: `confirmed` or `disproved`, with the reason.
4. Produce `reports/proposal.md` containing:
   - what was scanned (device, root, revision, file count, `truncated` yes/no)
   - the clusters, each with your verdict and the source lines you read
   - the unique symbols (these must **not** be proposed for merging)
   - the stubs, labelled as stubs
   - at most **one** bounded task, with acceptance criteria, a diff if you made
     one, the test command and its real output, unresolved risks, and rollback steps
   - `apply: false` — always.

## DO NOT

- Do not modify, delete, rename, or publish anything inside `ROOT`.
- Do not commit or push to any primary branch. Work in a worktree or a copy.
- Do not report a task as done without the command and its actual output.
- Do not upgrade `stubbed` or `simulated` to `implemented` without executing it.
- Do not propose merging because names or structures look alike.
- Do not invent a "recovered" scaffold if a search comes up empty — say it is absent.

## DONE WHEN

- Tests ran, and you have their real output.
- `reports/report.json` and `reports/proposal.md` exist.
- Every cluster carries a verdict with a reason.
- At most one bounded task is proposed, with `apply: false`.
- You can state, in one sentence, what you actually ran versus what you inferred.

## REPORT BACK

Post, in this order: (1) exact commands run, (2) their actual results, (3) what
failed or is unimplemented, (4) the proposal path. Not a summary of what you
intended — what happened.
