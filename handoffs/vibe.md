# Handoff — Vibe CLI

Vibe is the exploratory one. Use it for the work where you want an agent to
wander through the tree and come back with something you did not think to ask
for — but bounded, so it does not scopesplode.

---

## Kickdown prompt — find what is actually reusable

```
Read ~/OpenHeads/SESSION_CONTEXT.md and
~/OpenHeads/analysis/bleak_unification_catalog.json.

You are working on the BleakNarratives consolidation.

TASK: Find the genuinely reusable code hiding in the repos we plan to archive.

We are about to archive or absorb roughly 50 repos. Some of them contain small
pieces of real value that would be lost. Find them.

Method:
1. Take the repos tagged "archive-empty" and "delete" in the catalog.
2. For each non-empty one, read the code and identify anything genuinely useful:
   a working algorithm, a clever adapter, a well-formed data structure, a
   tested utility.
3. For each find, report: the file, what it does, and which surviving repo
   should receive it.
4. Write the results to analysis/SALVAGE_LIST.md, ranked by value.

Be selective. "It has a function" is not value. Only flag things that would
actually be missed.

Do not move any files. This is a survey. Do not push.
```

---

## Why this shape

Vibe is good at the open-ended "look around and tell me what you notice" job.
Bounding it to the archive list keeps it from wandering into the whole account.

## Second session — the naming archaeology

```
Read ~/OpenHeads/SESSION_CONTEXT.md.

TASK: Build a plain-language glossary of the account's own vocabulary.

The account uses a lot of invented terminology (MikeySwarm, Whorl, Molt,
Synt City, Vertical AI, Hotseat, AskHole, Kindred, Meridian, Predicase, Implore,
Veritas, LWM, Code City, and more). New agents and models have no idea what any
of it means, and the operator has to re-explain it every session.

1. Search the account for each term.
2. Write a one-paragraph definition of each, in plain language, based on how it
   is actually used in the code and docs.
3. Note which terms refer to the same thing, and which are genuinely distinct.
4. Output to analysis/GLOSSARY.md.

This is documentation, not renaming. Do not propose new names.
Do not push.
```
