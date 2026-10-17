# AGENTS.md — shared safety and execution rules

These rules apply to every agent in this pipeline. They are enforced by the code
where enforcement is possible, and by review where it is not.

## Non-negotiable

1. **Never narrate work you did not do.** Run it, or mark it unverified. A
   printed PASS, a stub, a generated report, or a simulated result is not proof
   of working behavior.
2. **Preserve provenance.** Every claim carries the `manifest_id` and
   `source_path` it came from. A claim without a source location is not evidence.
3. **Never silently select a canonical copy.** Choosing a winner is a human
   decision recorded in a report, never an automatic side effect.
4. **Never delete, overwrite, publish, or merge a candidate during discovery.**
5. **No integration is accepted because names, comments, APIs, or directory
   structures resemble one another.** Resemblance is a hypothesis.
6. **Keep unique implementations.** A symbol present in one source only is
   reported as unique and is never proposed for merging.
7. **Every source-changing action is reviewable and reversible.** The pipeline
   produces a diff and rollback instructions; it never applies them itself.
8. **Bound every scan** by explicit roots, file counts, depth, and time, and
   report truncation.
9. **Do not include credentials, keys, tokens, or sensitive environment files**
   in reports or bundles.

## Evidence vocabulary (use exactly)

- `implemented` / `partial` / `stubbed` / `simulated` / `undocumented` — describe
  the **source**.
- `tested` / `verified` — require an **executed** check. Not a claim.
- `verification_status`: `unverified` → `challenged` → `confirmed` | `disproved`.
  Only an executed check moves this off `unverified`.

## Stage boundaries

- Discovery may read anything in scope and writes nothing to source.
- Verification may execute code in an isolated copy; it never edits source.
- Implementation may edit only inside an isolated worktree or branch, and only
  against an approved task packet.

## Escalate instead of guessing

If a scan root is unreachable, a device is not mounted, or a prior scaffold
cannot be located, say so and stop. Do not fabricate a replacement and call it
recovered work.
