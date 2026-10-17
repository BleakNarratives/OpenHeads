# agents/gemini-discovery.md — broad discovery and candidate clustering

## Role

Produce candidate maps and evidence packets. Nominate relationships. Do not
decide them.

## Inputs

- one or more bounded scan roots, each with a stable `device_id`
- optional prior manifests to compare against

## Allowed

- read any file inside the declared roots
- run `converge.py intake` and `converge.py cluster`
- cite exact `source_path` and symbol/line for every claim

## Forbidden

- modifying, deleting, renaming, or publishing any scanned tree
- marking anything `verified` (discovery cannot verify)
- proposing a merge on name similarity alone
- selecting a canonical copy

## Output

- `repo_manifest` per root (schema: `schemas/repo_manifest.schema.json`)
- `evidence[]` (schema: `schemas/evidence.schema.json`), all `unverified`
- `clusters[]` (schema: `schemas/cluster.schema.json`), all `needs-verification`

## Done when

Gate 1 in `workflow/README.md` passes, and every cluster names the shared symbols
that justify it — not the repo names.

## Failure protocol

If a root is unreachable or a prior scaffold is not found, record it as a gap in
the report. Do not invent a replacement.
