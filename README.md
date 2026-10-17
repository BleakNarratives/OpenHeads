# OpenHeads — Session Bootstrap Hub

**This repo is the handshake.** Any agent, in any CLI, on any device, starts here.

If you are an AI agent reading this at the start of a session: read
[`SESSION_CONTEXT.md`](SESSION_CONTEXT.md) next, then the `bootstrap/dist/<repo>/QRD.md`
for whichever repo you are working in.

If you are the operator: run `bash install_bootstrap.sh` once on the device, then
every new session in any CLI picks this up automatically.

---

## What is in here

| Path | What it is |
|---|---|
| `SESSION_CONTEXT.md` | The universal context block. Every agent reads this first. |
| `analysis/` | Pass-1 account scan: 116 repos, clusters, duplication evidence. |
| `bootstrap/dist/` | Ready-to-create repo kits. Each has QRD/MRD/ROADMAP/TODO. |
| `bootstrap/templates/` | The four doc templates, for future repos. |
| `bootstrap/generate.py` | Regenerates `dist/` from cluster definitions. |
| `bootstrap/create_repos.sh` | One-shot script that creates and pushes the repos. |
| `install_bootstrap.sh` | Wires this repo into every CLI agent on the device. |
| `handoffs/` | Per-CLI kickdown prompts. One file per agent. |

---

## Quick start (operator)

```bash
# 1. Clone this repo somewhere permanent
git clone https://github.com/BleakNarratives/OpenHeads.git ~/OpenHeads

# 2. Install the session bootstrap into every CLI agent you use
cd ~/OpenHeads && bash install_bootstrap.sh

# 3. Create the consolidation repos (dry run first, always)
cd ~/OpenHeads/bootstrap && bash create_repos.sh --dry-run
bash create_repos.sh --apply
```

---

## The document system

Four docs per repo, four distinct jobs. Do not merge them.

| File | Audience | Job |
|---|---|---|
| `QRD.md` | The next **agent** | Handoff. Intent, state, guardrails, scope limits. |
| `MRD.txt` | The **human** | Only work a body must do. Nothing delegable. |
| `ROADMAP.md` | Both | Ordered plan, scope, and the parked-ideas list. |
| `TODO.md` | Both | One-line tasks tagged `[A]`gent / `[H]`uman / `[B]`locked. |

**QRD** = Quick Rundown. Carries intent between models so nothing is lost in
translation. **MRD** = Meatsuit Rundown. The human-only list. It exists because
a solo operator's scarcest resource is their own attention.

---

## Rules that apply to every agent in every repo

1. **Never narrate work you did not do.** Run it, or mark it unverified. This
   account builds tooling whose whole premise is that agents claim "done"
   without proof.
2. **Prefer deleting to adding.** The problem here is too much, not too little.
3. **Defer scope, never execute it.** New idea goes in `ROADMAP.md` section
   "Out of scope / deferred" with one sentence. Then stop.
4. **Runtime targets are Termux and Crostini.** No Docker, no GPU, no paid
   cloud, no desktop-only dependencies.
5. **Do not comment on naming, language, or tone.** The operator is aware and
   did not ask for that.
6. **Keep the MRD honest.** If a task goes in it, it must genuinely need a human.

---

## Account state

116 public repos, target ~60. 26 are completely empty. 708 blob groups are
byte-identical across repos. 17 repos are clones of one React/Vite scaffold.

Full detail in [`analysis/BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md`](analysis/BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md).
Machine-readable in [`analysis/bleak_unification_catalog.json`](analysis/bleak_unification_catalog.json).
