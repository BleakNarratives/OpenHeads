# Handoff — Kilo

Kilo is good for multi-file coordinated edits. Use it for migrations that touch
many files but follow one pattern.

---

## Kickdown prompt — extract the shared UI starter

```
Read ~/OpenHeads/SESSION_CONTEXT.md and
~/OpenHeads/bootstrap/dist/bleak-ui-kit/QRD.md and ROADMAP.md.

You are working on the BleakNarratives consolidation, React scaffold cluster.

CONTEXT: 17 repos are clones of one Vite/React scaffold. tsconfig.json is
byte-identical in 15 of them. vite.config.ts is identical in 12. We are building
one shared starter (bleak-ui-kit) and re-pointing the survivors at it.

TASK: Extract the canonical config set and prove it on one real app.

1. Pull tsconfig.json, vite.config.ts, index.html, and metadata.json from
   EquiNex-Universal-Dashboard (the richest scaffold).
2. Create the starter layout:
     bleak-ui-kit/
       tsconfig.json
       vite.config.ts
       index.html
       package.json
       src/App.tsx          (minimal shell)
       README.md            (how to consume it)
3. Do NOT publish to npm. Local consumption only.
4. Document the migration steps in README.md.

Do not push. Do not migrate any app yet - extraction only.

Rules: do not add a component library. This is a starter, not a design system.
Do not add Storybook. Do not generalize for cases nobody has.
```

---

## Second session — migrate the first consumer

```
Read ~/OpenHeads/bootstrap/dist/bleak-ui-kit/README.md.

TASK: Migrate EquiNex-Universal-Dashboard to consume bleak-ui-kit.

1. Delete its local tsconfig.json and vite.config.ts.
2. Point it at the shared config (extend, do not copy).
3. Keep every existing component and service exactly as-is.
4. Verify it still builds.
5. Report any file that could not be migrated and why.

Do not push. One app only. If it breaks, stop and report - do not "fix" it by
inventing a new config.
```

---

## Why this shape

The risk in this cluster is breaking working apps while chasing tidiness. The
prompt front-loads extraction (safe and reversible) and isolates migration to a
single app so a failure is contained and visible.
