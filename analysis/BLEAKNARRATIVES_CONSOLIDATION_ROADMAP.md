# BleakNarratives — Unification & Downsizing Roadmap

**Generated:** 2026-10-16
**Scope:** all 116 public repositories under `github.com/BleakNarratives`
**Method:** full recursive file-tree scan of every repo, content-hash (blob SHA)
matching to find genuinely duplicated files, plus README and structure reads.

This is a working checklist, not a report. Tick items off as they land.

---

## 1. What I can see from here

I have authenticated read access to your GitHub account as `BleakNarratives`
(116 public repos, 0 private, 0 archived, 2 forks). I scanned every repo's
complete file tree and content-hashed every blob, so the "duplication" numbers
below are measured, not guessed.

What I do **not** have: access to your Chromebook filesystem. Section 6 fixes
that with a live bridge that is already running.

### Headline numbers

| Metric | Value |
|---|---|
| Repositories | 116 |
| Completely empty (zero files, zero bytes) | **26** |
| Total bytes across all repos | ~0.39 GB |
| Duplicated blob groups (same content in 2+ repos) | **708** |
| Repos that are a React/Vite scaffold clone | 17 |
| Single-file / license-only repos | 3 |
| Repos that are nothing but a `.zip` dump | 3 |

### The two biggest single items

- `Skin-Deep` — 257 MB (65% of your entire account's bytes)
- `sprint-ralphy` — 89 MB (contains 165 markdown files and 39 XSD schema files)

Those two are 89% of your storage. Everything else combined is ~43 MB.

---

## 2. The 26 empty repos — delete or archive today

These have **zero files and zero bytes**. Nothing is lost. Two of them
(`motherbrain`, `whorl-nexus`) hold a single commit with no tree, so archive
rather than delete if you want to keep the URL.

```
Akasha                                  Mrs-Higgins-SaaS
Apex-Recovery                           New-SaaS-Launchpad
Automation-DNA                          Pattern-Atlas
CodeMentor-MVP                          Print-Hello-Work
DevIDE                                  ProjectCentral
ModHub  (ModMind-Hub)                   Ship-Or-Skip
ModMind-Rapper2.0                       ShipWrekD-OS
Mrs-Higgins-Front-Desk-Lady             ShipWrekD-OS-Syntax-AI-Driven-IDE-Version-2.0
This-Shit                               bleak-core-toolbox
Tracer                                  bleak-datacampus
benefinder                              boa_bundle
foxwoodacademy                          motherbrain
root_2025                               whorl-nexus
```

That is an instant **22% cut** in repo count with zero content risk.
`bleak_archive_commands.sh` in this repo does it in one pass.

---

## 3. Real duplication, by cluster

Each cluster below is a set of repos that share actual file content, with the
measured overlap. These are your merge candidates.

### Cluster A — Mrs. Higgins pipeline (4 → 1) ★ highest confidence

`mrs-higgins` · `mrs-higgins-a9` · `mrs-higgins-chromebook` · `mrs-higgins-moto`

**Evidence:** all four carry a **byte-identical README** (5,222 B), identical
`setup.sh`, identical `mrs_higgins.sh`, identical `static/css/style.css`,
`templates/index.html`, `static/js/app.js`, and **all ~50 `saas_packages/*.json`
files**. `The-Werkz` carries the same files a fifth time.

| Repo | Files | Size | Unique blobs | Last push |
|---|---|---|---|---|
| mrs-higgins | 21 | 143 KB | 3 | 2026-08-05 |
| mrs-higgins-a9 | 76 | 176 KB | 20 | 2026-10-16 |
| mrs-higgins-chromebook | 337 | 266 KB | 109 | 2026-10-16 |
| mrs-higgins-moto | 26 | 34 KB | 17 | 2026-10-16 |
| **combined** | **460** | — | **210 distinct** | — |

**Action:** `mrs-higgins-chromebook` is canonical (newest, most complete). Port
the 37 unique blobs from `a9` + `moto` into it, then archive the other three.
The 460 files collapse to ~210.

> Note: this is your "platform-agnostic, env-aware" case in miniature — the four
> repos differ almost entirely by *target device path* (`/storage/ED7B-AD5A/...`,
> Termux, Crostini). One repo with a `device-profiles/` directory removes the
> whole fork-per-device pattern.

### Cluster B — Live wrapper family (4 → 1) ★ highest confidence

`riffusion-live-wrapper` · `claude-live-wrapper` · `gemini-live-wrapper` ·
`copilot-live-wrapper`

**Evidence:** identical skeleton — `GOVERNANCE.md`, `METRICS.md`,
`PITCH_DECK_OUTLINE.md`, `PITCH_SLIDES.txt`, `TIMELINE.md`,
`VIEWER_INTERFACE.md`, `SUBMISSION_EMAIL.txt`, `CONTEXT_HANDOFF.md`,
`demos/sound_check_demo.py`, `run_green_room.sh`, `requirements.txt`,
`src/vivx_monitor.py`, `src/lyria_adapter.py`. **The only real difference is
`src/<provider>_sdk/`.**

**Action:** one repo, `live-wrappers`, with `src/{claude,gemini,riffusion,copilot}_sdk/`
and the shared green-room core lifted to `src/core/`. 77 files → ~60, and the
four READMEs/governance docs stop drifting apart.

### Cluster C — React/Vite scaffold sprawl (17 → 1 template)

`ShipWrekD-OS-Syntax-AI-Driven-IDE` · `Vertical-AI` · `Vert-AI-AI-Studio-Fromtend` ·
`ModMind-GlassRing-and-Company` · `ModMind-Identity-Utility` · `Kick-Rock` ·
`another-flop` · `are_n_dee` · `reverse_filter` · `Eww` · `Tentative-Title` ·
`homeless_mike_tarot` · `nesting_bestie_taylor_demo` · `odds-of-the-gods` ·
`fd_cohort` · `EquiNex-Universal-Dashboard` · `Pivot`

**Evidence:** `tsconfig.json` is byte-identical across **15** of them;
`vite.config.ts` across **12**; 10 scaffold blobs appear in 3+ repos.
656 files total, only 580 distinct — and most of the difference is `App.tsx`.

**Action:** one `bleak-ui-kit` starter repo. Each surviving app keeps only its
`src/`, `components/`, `services/` and consumes the kit. Then triage: several of
these (`another-flop`, `are_n_dee`, `Tentative-Title`, `reverse_filter`,
`homeless_mike_tarot`) are experiments, not products — archive them outright.

### Cluster D — Verification / adversarial-review family (5 → 2)

`tribunal` · `ConstraintOps` · `Praudit` · `EquiLex` · `MemGuard`

**Evidence:** all five are "catch the agent lying / keep the machine honest"
tools. `tribunal` (adversarial review of agent claims) is the engine;
`ConstraintOps` (forensic audits, 49 markdown files, priced service tiers) is the
commercial face; `Praudit` is a shim/wrapper set (`openclaw_shim.py`,
`molt_shim.py`, `vibe_skill_shim.py`); `EquiLex` is an Android compliance monitor;
`MemGuard` is OOM defense.

**Action:** keep `tribunal` (engine) + `ConstraintOps` (product/docs/pricing).
Fold `Praudit`'s shims into `tribunal/wrapper/`. Fold `EquiLex` and `MemGuard`
in as `tribunal/guards/` — they are both runtime guards with the same
verdict-bus shape.

### Cluster E — Swarm / orchestration core (6 → 1)

`Whorl` · `Vigil` · `SyntaxIntelligence` · `Swarmulacrum` · `core_framework` ·
`propagated_node` · `Concierge`

**Evidence:**
- `Whorl` already *is* the modular ecosystem (scouts / forge / hotseat / loom /
  agents / tailor / nostr / slice / core) and is Termux-native, SQLite + Ollama.
- `Vigil` is the scout integrity + geometry + fabrication layer
  (`integrity.py`, `geometry.py`, `fabrication.py`) that Whorl's `scouts` module
  needs. It's the substrate, not a rival.
- `SyntaxIntelligence` supplies the 6-tier governance ladder (Recruit →
  Council) — i.e. the *permission* model.
- `Swarmulacrum` is the audit/white-paper + `core` + `bin`.
- `core_framework` — **its own README says it "contains no copied source code —
  every file here is a pointer into the canonical trees."** It is a
  documentation repo wearing a code repo's clothes.

**Action:** `Whorl` is canonical. Add `whorl/scouts/integrity` (from Vigil),
`whorl/governance/tiers` (from SyntaxIntelligence), and move
`core_framework`'s pointer table into `whorl/docs/ORCHESTRATION.md`. Then
archive `core_framework`, `Swarmulacrum`, `propagated_node`, `Concierge`.

> ⚠️ `a9-codex-grapher` also contains a `core_framework/` directory. So
> `core_framework` exists in two places already. Worth reconciling.

### Cluster F — Code City bench (7 → 2)

`Code-City-Apocalypse` · `PivotCity` · `modmind-shell` · `ModMind-Hub` (empty) ·
`EquiNex-Universal-Dashboard` · `Vertical-AI-V4` · `Official-Vertical-AI-Boardroom`

**Evidence:** `Code-City-Apocalypse` is already a monorepo — 1,463 files holding
`Code_City/`, `Code_City_Unified/`, `SCOUT_CONTAINER/`, `registry/`, `plugins/`,
`ui/`, `frontend/rampage-refactor/`. It also **vendors a 351-file
`SCOUT_CONTAINER/Syntax-AI-Unified/` subtree** that is its own project, and
`Code_City_Unified/modmind_unified/` at 150 files.

**Action:**
1. Extract `SCOUT_CONTAINER/Syntax-AI-Unified/` into its own repo — it is a
   standalone stack being carried as luggage.
2. `Code-City-Apocalypse` stays the bench monorepo; `PivotCity`, `modmind-shell`,
   `EquiNex-Universal-Dashboard`, `Vertical-AI-V4` fold in as modules.

### Cluster G — Vertical AI / Boardroom (6 → 1)

`Official-Vertical-AI-Boardroom` · `Vertical-AI` · `Vertical-AI-V4` ·
`Vertical-AI-Notebook-LM` · `Vert-AI-AI-Studio-Fromtend` · `vertical_local`

**Evidence:** six repos with the same product name and overlapping frontends.
`boardroom.py`, `boardroom_bridge.py`, `chairman.py`, `board_debrief.py` are the
real engine. `vertical_local` is 4 files of docs (MRD/QRD/ROADMAP).

**Action:** `Official-Vertical-AI-Boardroom` is canonical. Fold the three
frontends in as `ui/` variants; move `vertical_local`'s docs into `docs/`.

### Cluster H — Outreach & commerce (7 → 3)

`Pytch` · `passive_income_swarm` · `Product-Launch-Engine` · `askhole-cli` ·
`Negotiator` · `Kindred` · `Poncho-Villa`

**Evidence:** `Pytch` is the outreach engine (pitch → deploy → follow-up).
`passive_income_swarm` is the FastAPI gateway + agent marketplace + Nostr DVM
worker. These two are the real system. `askhole-cli` (2 files) and `Negotiator`
(7 files) are single-script tools that belong in `bin-scripts`.

**Action:** keep `Pytch` + `passive_income_swarm`. Move `askhole-cli`,
`Negotiator`, `Kindred` into `bin-scripts` (or `Pytch/tools/`).
`Product-Launch-Engine` folds into `Pytch`.

### Cluster I — Payments (2 → 1)

`payment_system` · `saas_packages/lightning_payment_integration.json` (in the
Higgins repos)

**Evidence:** `payment_system` already implements Bitcoin on-chain + Lightning +
Monero + Stripe + license keys, Docker-ready, and says "built for the Vertical AI
Boardroom." Meanwhile the Higgins pipeline hand-rolls its own Lightning/Voltage
integration as a JSON package.

**Action:** `payment_system` is canonical. Wire it in as the payment backend for
Higgins, delete the duplicated Lightning config.

### Cluster J — Legal toolkit (3 → 1)

`OutcLaw` · `EquiLex` · `OpenClaw-CLI-But-Better`

**Evidence:** `OutcLaw` is a 305-file legal AI toolkit (citation fraud detection,
IRAC arguments, FOIA, judicial complaints). `EquiLex` is a compliance monitor.
`OpenClaw-CLI-But-Better` is 7 markdown "ENDEMPTS" archaeology docs + one HTML
dashboard.

**Action:** `OutcLaw` canonical. `EquiLex` → `OutcLaw/compliance/`.
`OpenClaw-CLI-But-Better`'s ENDEMPTS docs → `OutcLaw/docs/endempts/`.

### Cluster K — Android / Termux platform ports (keep, don't merge)

`zeroclaw-android` (32★) · `crown-jules` (3★) · `Hermes-Android-BleakNarratives` ·
`OutClaw-Integration` · `goose-mobile-foxwood-academy` · `Poncho-Villa`

These are genuine ports — Rust-on-aarch64, Jules client, Hermes JS agent. They
have distinct value and shouldn't be folded. But `OutClaw-Integration` (6.8 MB of
docs + 3 images, zero code) should be reduced to a `docs/` folder inside
`OutcLaw`.

### Cluster L — Zip dumps (3 → 0)

`claudio_jr` (1 file: `syntax_shipwrekd_os_bundle.zip`, 1.2 MB) ·
`Rampage-Refactor` (1 file: `rampage-refactor.zip`) ·
`ChAImeleon` (3 zips + LICENSE)

**Action:** extract contents into the canonical repo, then delete. `Rampage-Refactor`
content already exists in `Code-City-Apocalypse/Code_City/rampage-refactor/`.

### Cluster M — Scout siblings (2 → 1)

`ChronoScouts` (6 KB) · `Kronos-Scouts` (7 KB)

**Evidence:** both are tiny, both have `SITREP_CODEX.md` + `fixtures/` +
`harnesses/` + `dist/`. Same template, different name.

**Action:** merge into one `scouts-lab` repo, or fold into `Whorl/scouts/`.

### Cluster N — 1-file and license-only repos (3 → 0)

`Smell-Scan` · `Meatwatch` · `nesting_bestie` · `hotseat` — each holds only a
LICENSE (or a single LICENSE line).

**Action:** `Meatwatch` content lives in `Poncho-Villa` (`meatwatch*.py`).
`hotseat` is a Whorl module. `nesting_bestie` belongs with
`nesting_bestie_taylor_demo`. Delete the stubs.

---

## 4. Ranked punch list

Ordered by (impact ÷ effort). Do them top-down.

| # | Action | Repos touched | Result |
|---|---|---|---|
| 1 | Archive the 26 empty repos | 26 | −22% repo count, zero risk |
| 2 | Merge Mrs. Higgins ×4 → 1 | 4 → 1 | −3 repos, kills fork-per-device |
| 3 | Merge live wrappers ×4 → 1 | 4 → 1 | −3 repos, one green room |
| 4 | Extract `SCOUT_CONTAINER/Syntax-AI-Unified` from Code-City-Apocalypse | 1 → 2 | bench monorepo unburdened |
| 5 | Merge ChronoScouts + Kronos-Scouts | 2 → 1 | −1 repo |
| 6 | Fold `core_framework` into Whorl docs | 1 → 0 | it's a pointer file, not code |
| 7 | Fold Praudit / EquiLex / MemGuard into tribunal | 3 → 0 | one verification suite |
| 8 | Merge Vertical AI frontends into Boardroom | 3 → 0 | −3 repos |
| 9 | Delete zip-dump repos after extracting | 3 → 0 | −3 repos |
| 10 | Build `bleak-ui-kit`, re-point 17 scaffolds | 17 → 12 | −5 repos, no more drift |
| 11 | Move askhole-cli / Negotiator / Kindred → bin-scripts | 3 → 0 | −3 repos |
| 12 | Delete 4 license-only stubs | 4 → 0 | −4 repos |

**If you only do items 1–3 and 9 and 12: 116 repos → 82 repos in an afternoon.**

Full target state after everything: roughly **60–65 repos**, down from 116 — with
the survivors being genuine products, ports, and platform modules rather than
copies of each other.

---

## 5. The pattern behind the sprawl

Worth naming, because it predicts future mess:

1. **One repo per device, not per project.** `mrs-higgins` vs `-a9` vs
   `-chromebook` vs `-moto` differ by filesystem path. Fix: device profiles
   inside one repo.
2. **One repo per provider.** `claude-live-wrapper` vs `gemini-` vs `riffusion-`
   vs `copilot-` differ by SDK folder. Fix: provider adapters inside one repo.
3. **One repo per scaffold.** 17 Vite apps with identical configs. Fix: shared
   template, consumed not copied.
4. **Repos as scratch pads.** 26 empty repos + 3 zip dumps + 4 license stubs.
   Fix: create repos only when there's a second commit to make.
5. **Docs repos masquerading as code repos.** `core_framework` literally says it
   holds no code. Fix: docs live in the repo they describe.

---

## 6. The drive bridge — done, it's live

You asked whether we could bridge me to your Chromebook. We can. I'm running an
HTTP bridge **right now** on the workspace, reachable from your device.

**URL:** `https://work-1-hlucqceaikkyoewj.prod-runtime.all-hands.dev/`
(second lane available at `https://work-2-hlucqceaikkyoewj.prod-runtime.all-hands.dev/`)

Open that URL in any browser on the Chromebook and you get a plain page listing
what's in each direction. Or use curl, same as your `cat << 'EOF'` habit but
without the copy-paste.

**Pull a file from my side to your drive:**

```bash
curl -sS https://work-1-hlucqceaikkyoewj.prod-runtime.all-hands.dev/outbox/roadmap.md -o ~/roadmap.md
```

**Push a file from your drive to my side** (lands in `/workspace/bridge/inbox`,
where I can read it):

```bash
curl -sS -F "file=@/path/to/your/file.txt" https://work-1-hlucqceaikkyoewj.prod-runtime.all-hands.dev/upload
```

Both directions are verified working end to end. The server is one stdlib-only
Python file (`bridge_server.py`) — no dependencies, and it runs as happily on
Termux as it does here, so you can keep a copy locally.

**Important:** this bridge lives inside the session container. It stops when the
conversation ends and needs restarting next time. The file is in this bundle, and
`AGENTS.md` records the exact restart command so the next agent session brings it
back automatically. Keep a local copy too — then you can run it yourself on any
machine with Python and a port.

**Caveat worth stating plainly:** this lane is reachable by anyone who has the
URL while it's up. Don't push secrets, keys, or personal-data dumps through it.
For anything sensitive, keep doing what you're doing — `cat << 'EOF'` into your
own terminal, which never leaves the machine.

---

## 7. TODO checklist

```
[ ] 1.  Run bleak_archive_commands.sh          -> 26 empty repos archived
[ ] 2.  Pick mrs-higgins-chromebook canonical
[ ] 3.  Port 20 unique blobs from mrs-higgins-a9
[ ] 4.  Port 17 unique blobs from mrs-higgins-moto
[ ] 5.  Port 3 unique blobs from mrs-higgins
[ ] 6.  Add device-profiles/ to the canonical Higgins repo
[ ] 7.  Archive mrs-higgins, -a9, -moto
[ ] 8.  Create live-wrappers; move 4 x src/<provider>_sdk/
[ ] 9.  Archive the 4 live-wrapper repos
[ ] 10. Extract SCOUT_CONTAINER/Syntax-AI-Unified -> own repo
[ ] 11. Merge ChronoScouts + Kronos-Scouts -> scouts-lab
[ ] 12. Move core_framework pointer table -> Whorl/docs/ORCHESTRATION.md
[ ] 13. Archive core_framework
[ ] 14. Fold Praudit shims -> tribunal/wrapper/
[ ] 15. Fold EquiLex + MemGuard -> tribunal/guards/
[ ] 16. Merge Vertical AI frontends -> Official-Vertical-AI-Boardroom/ui/
[ ] 17. Extract zip dumps, then delete claudio_jr / Rampage-Refactor / ChAImeleon
[ ] 18. Build bleak-ui-kit; re-point the 17 scaffolds
[ ] 19. Move askhole-cli / Negotiator / Kindred -> bin-scripts
[ ] 20. Delete Smell-Scan / Meatwatch / nesting_bestie / hotseat
[ ] 21. Reconcile duplicate core_framework/ inside a9-codex-grapher
[ ] 22. Decide fate of Skin-Deep (257 MB) and sprint-ralphy (89 MB)
```

---

## 8. Files in this bundle

| File | What it is |
|---|---|
| `BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md` | This document |
| `bleak_unification_catalog.json` | All 116 repos, machine-readable, with cluster + action assigned |
| `bleak_archive_commands.sh` | Ready-to-run `gh` commands for the 26 empty repos |
| `bridge_server.py` | The drive bridge, stdlib-only, runs on Termux too |

Next session we can take any single row off the checklist and actually do it —
merge the Higgins family properly, or build `bleak-ui-kit` — whichever you'd
rather see finished first.
