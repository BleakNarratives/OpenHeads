# Convergence Starter Pack

A small, reusable workflow that lets three agents cooperate against real
repositories and produce **comparable, provenance-linked evidence** — without
anyone silently merging anything.

It exists because the failure mode is not "too few tools". It is sequencing: a
scanner runs, a report looks impressive, and nothing is verified. This pack makes
the verification step a real, runnable artifact.

## What it does

Three bounded stages, each writing JSON the next one reads:

| Stage | Command | Output |
|---|---|---|
| intake | `converge.py intake --device-id ID --root PATH --out FILE` | `repo_manifest` — identity, provenance, per-file sha256 |
| analyze | `converge.py analyze --manifest FILE --out FILE` | `evidence[]` — claims tied to symbols/lines |
| cluster | `converge.py cluster --manifests FILE ... --out FILE` | `clusters[]` + unique symbols |
| report | `converge.py report --manifests FILE ... --out FILE` | full report + proposed tasks (`apply: false`) |

Stdlib only. No database, no dispatcher, no framework. Python 3.9+.

## Setup

Nothing to install:

```bash
python3 -m unittest discover -s tests -v      # 15 tests
```

Artifacts can be checked against the schemas with the bundled stdlib validator
(no `jsonschema` install needed):

```bash
python3 bin/validate.py --schema schemas/evidence.schema.json --data reports/evidence.json
```

## One working example

```bash
python3 fixture/make_fixture.py
python3 bin/converge.py intake  --device-id deviceA --root fixture/deviceA --out reports/a.json
python3 bin/converge.py intake  --device-id deviceB --root fixture/deviceB --out reports/b.json
python3 bin/converge.py report  --manifests reports/a.json reports/b.json --out reports/report.json
```

On the bundled fixture this reports 2 overlapping clusters (`normalize_path`,
`join_root`), 3 unique symbols, and 1 stub (`promised_but_absent`), and emits two
proposed tasks with `apply: false`. See `reports/convergence_report.json`.

## What it deliberately does not do

- It does not modify, delete, rename, or publish any scanned tree.
- It does not select a canonical copy.
- It does not treat a name match as a merge. Every cluster is `needs-verification`.
- It does not emit "merge now". The strongest recommendation is a task for a human.

## Layout

```
bin/converge.py              the pipeline (stdlib only)
bin/validate.py              minimal JSON Schema validator (stdlib only)
schemas/                     repo_manifest / evidence / cluster JSON Schemas
agents/                      the three agent role contracts
workflow/README.md           orchestration, handoff contract, validation gates
tests/test_pipeline.py       end-to-end pipeline tests
tests/test_schemas.py        schema conformance + negative controls
fixture/                     the bounded two-device test fixture
reports/                     generated output (never written into source repos)
```

## Known limits

- Only Python files are analysed (`ast`); other languages are hashed but not
  symbol-extracted.
- Symbol overlap is *lexical*. Two identical names can be unrelated, and two
  different names can be the same behaviour. That is exactly why clustering
  stops at `needs-verification`.
- The scan bounds (`--max-files/--max-depth/--max-seconds`) are conservative by
  default and record truncation rather than hiding it.
