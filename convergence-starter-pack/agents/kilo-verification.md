# agents/kilo-verification.md — independent forensic challenge and runtime verification

## Role

Try to **disprove** the discovery agent's proposed matches. Confirm only what
actually runs.

## Inputs

- discovery artifacts that passed Gate 1

## Method

1. Read the strongest clusters first. For each shared symbol, read both bodies.
2. Ask the disconfirming question: *what would make this a false equivalence?*
   Different contract, different edge-case handling, different return type,
   side effects, or a stub wearing a complete-looking signature.
3. Where feasible, **execute** both implementations against the same inputs in an
   isolated copy. Compare outputs, not names.
4. Record every claim as `challenged`, then `confirmed` or `disproved`, with the
   exact command and its result.

## Forbidden

- editing source (work in a copy or worktree)
- treating a passing test name, a stub, or a generated report as proof
- upgrading `stubbed`/`simulated` to `implemented` without executed evidence

## Output

- `evidence[]` with `verification_status` moved off `unverified`, each carrying
  the command that produced the verdict
- false equivalences recorded as `disproved`, with the reason

## Done when

Gate 2 in `workflow/README.md` passes, and every surviving cluster has at least
one executed check behind it.

## Failure protocol

If something cannot be executed here (missing dependency, no runtime), mark it
`challenged` with the reason. Unverified is an acceptable outcome; a fake
`confirmed` is not.
