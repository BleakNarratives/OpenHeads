# workflow/ — orchestration, handoff contract, validation gates

The three agents never call each other directly. They exchange **artifacts** that
conform to the schemas in `../schemas/`. That is what makes their findings
comparable.

## Pipeline

```
        ┌──────────────┐   repo_manifest + evidence[]   ┌──────────────┐
roots → │  discovery   │ ─────────────────────────────► │ verification │
        │  (Gemini)    │                                │   (Kilo)     │
        └──────────────┘                                └──────┬───────┘
                                                               │ challenged evidence
                                                               ▼
                                                      ┌──────────────────┐
                                                      │  implementation  │
                                                      │   (OpenHands)    │
                                                      └──────────────────┘
                                                               │ diff + tests
                                                               ▼
                                                        human decision
```

`bin/converge.py` performs discovery and clustering mechanically. The agent role
files in `../agents/` describe the judgement each agent adds on top.

## Handoff contract

A stage may hand work to the next only when its artifact passes the gate below.
Each artifact is a single JSON file; paths are relative to the artifact.

### Gate 1 — discovery → verification

- [ ] every manifest has `device_id`, `source_root`, `revision`, and a sha256 per file
- [ ] `truncated` is recorded for every bounded scan
- [ ] every evidence packet has a `source_path` and a `location`
- [ ] no evidence packet is marked `verified` (discovery cannot verify)
- [ ] clusters use `confidence_basis`; `name-only` clusters are marked `not-mergeable`

### Gate 2 — verification → implementation

- [ ] each claimed cluster has at least one `challenged` evidence entry
- [ ] each confirmed match names the command that was actually run and its result
- [ ] stubs and simulations are labelled, not upgraded
- [ ] false equivalences are recorded as `disproved`, with the reason

### Gate 3 — implementation → human

- [ ] exactly one bounded task, with stated acceptance criteria
- [ ] a minimal diff against an isolated branch or worktree
- [ ] real test output (command + result), not a summary
- [ ] unresolved risks listed
- [ ] rollback instructions included
- [ ] `apply` is `false` until a human approves

## Task packet (the only thing implementation accepts)

```json
{
  "task_id": "cl-7cebc4fd6c",
  "kind": "verify-then-consider",
  "targets": ["overlap_b.py", "overlap_a.py"],
  "acceptance": "both implementations agree on the shared symbol's contract, proven by a run",
  "apply": false
}
```

`converge.py report` emits these automatically from clusters.

## Safe failure

- Unreachable root, unmounted device, or missing prior scaffold → report and stop.
- Digest/parse failure on a manifest → that manifest is quarantined; others proceed.
- Any bound hit → `truncated: true`; the stage still completes, and the truncation
  travels with the artifact so no downstream agent mistakes a partial scan for a full one.
