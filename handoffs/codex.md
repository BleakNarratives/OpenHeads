# Handoff — Codex CLI

Copy the block below into Codex at session start. Tuned for Codex's strengths:
long autonomous runs, careful diffs, strong at mechanical refactors.

---

## Kickdown prompt

```
Read ~/OpenHeads/SESSION_CONTEXT.md first. Then read
~/OpenHeads/bootstrap/dist/bleak-higgins/QRD.md and TODO.md.

You are working on the BleakNarratives consolidation. Your job this session:

TASK: Seed bleak-higgins from the mrs-higgins-chromebook tree, then port the
40 unique blobs from the three sibling repos (mrs-higgins, mrs-higgins-a9,
mrs-higgins-moto).

Constraints:
- Do not add features. This is a merge, not a rewrite.
- Do not rename anything.
- Do not comment on code style or naming.
- Offline-friendly: no Docker, no GPU, no cloud services.
- Every claim you make must be backed by a command you actually ran.

Method:
1. Clone mrs-higgins-chromebook into a working directory.
2. For each sibling, compare content (not just paths) against canonical and
   identify blobs that do not exist in canonical.
3. Copy in only the genuinely new files.
4. Record what you moved in a MIGRATION.md.
5. Do NOT push anywhere. Leave the tree for the operator to review.

Report back with: files added, files skipped and why, and anything that needed
a human decision.
```

---

## Why this shape

Codex is strong at mechanical diff-and-port work. The prompt gives it a bounded,
verifiable job with an explicit "do not push" so nothing lands unreviewed.

## Follow-up session (after the merge is reviewed)

```
Read ~/OpenHeads/bootstrap/dist/bleak-higgins/QRD.md.

TASK: Extract hardcoded device paths into device-profiles/.

1. Find every hardcoded path in the Higgins tree (grep for /storage/, /data/,
   /sdcard/, and any absolute paths).
2. Design a profile format: device-profiles/{termux,crostini,moto}.yaml with a
   single paths: mapping.
3. Refactor the code to read from the active profile.
4. Keep backward compatibility: with no profile set, behave as before.
5. Add a test that loads each profile.

Do not push. If more than 15 files are affected, report the plan first.
```
