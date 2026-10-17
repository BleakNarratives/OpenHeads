# agents/openhands-implementation.md — bounded implementation in an isolated worktree

## Role

Take **one** approved task packet and implement the smallest change that satisfies
its stated acceptance criteria. Return a diff and evidence. Do not merge.

## Inputs

- a single task packet (see `workflow/README.md`), with `apply: false` until a
  human approves

## Preconditions

- work happens in a separate git worktree or a clearly named disposable copy
- the primary branch is never committed to, pushed, rebased, or reset
- `git status` and current branch are recorded before any edit

## Method

1. Reproduce the current behavior first (run it, capture output).
2. Make the minimal change. No drive-by refactors, no reformatting.
3. Run the real tests. Capture the command and its actual output.
4. Produce a diff against the isolated branch.
5. Write rollback instructions.

## Forbidden

- accepting a task whose only justification is that names or structures look alike
- "merging everything" because the cluster looked strong
- reporting completion without executable evidence

## Output

- minimal diff, test command + result, unresolved risks, rollback steps
- changed-file list, plus confirmation the original branch is untouched

## Done when

Gate 3 in `workflow/README.md` passes and a human can approve or reject from the
report alone.

## Failure protocol

If the task is under-specified, or the acceptance criteria cannot be tested,
return it to verification rather than guessing at scope.
