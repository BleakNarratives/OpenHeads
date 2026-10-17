# SESSION_CONTEXT.md — universal agent context block

> Paste this, or have it auto-loaded, at the start of any agent session.
> It is deliberately short. Everything longer lives in the links at the bottom.

---

## Who you are working with

A solo, self-taught developer working from a Chromebook (Crostini) and Android
(Termux). No team, no funding, no formal training, currently homeless. Three
large rescue dogs in their care. Time and attention are constrained by survival.

They generate ideas faster than one person can consolidate them, which is why
the account has sprawled to 116 repos. **The sprawl is not a character flaw.**
It is the predictable output of high idea velocity with no one to delegate to.

## What you are working on

`github.com/BleakNarratives` — roughly 90+ GB of novel work across 116 public
repos. Swarm orchestration, agent verification, predictive market modeling,
simulated beta testing, legal AI tooling, gamified codebase visualization.

The current effort is **consolidation**: merging overlapping repos into fewer,
sharper products. Target is ~60 repos from 116.

## The three rules that matter most

1. **Never narrate work you did not do.** Run it, or mark it unverified. This
   account builds tooling whose entire premise is that AI agents claim "done"
   without proof. Do not be that agent here.
2. **Prefer deleting to adding.** The stated problem is too much, not too
   little. A smaller diff is a better diff.
3. **Defer scope, do not execute it.** New idea → `ROADMAP.md` "Out of scope"
   with one sentence. Then stop. Adding features is the failure mode.

## Constraints

- **Runtime:** Termux, Crostini, Android aarch64. No Docker, no GPU, no paid
  cloud, no desktop-only dependencies.
- **Offline-first** where possible. The core loops must work with no network.
- **Do not** comment on naming conventions, language, or tone. The operator has
  named this directly and did not ask for help with it.
- **Do not** propose renaming things unless it fixes a real technical problem.

## The document system (four files, four jobs)

| File | Audience | Job |
|---|---|---|
| `QRD.md` | next **agent** | Handoff: intent, state, guardrails |
| `MRD.txt` | the **human** | only body-required work |
| `ROADMAP.md` | both | plan, scope, parked ideas |
| `TODO.md` | both | one-line tasks, `[A]`/`[H]`/`[B]` tagged |

Read the QRD of the repo you are in before touching code. Update it before you
finish. That is the handshake.

## Where to go deeper

- `README.md` — what OpenHeads is and how to use it
- `analysis/BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md` — full account analysis
- `analysis/bleak_unification_catalog.json` — all 116 repos, machine-readable
- `bootstrap/dist/<repo>/QRD.md` — per-repo handoff
- `handoffs/` — per-CLI kickdown prompts

## If you are unsure what to do

Pick the top unfinished item from the `TODO.md` of the repo you are in. Do it
end to end. Do not re-summarize, do not propose a plan, do not ask which one to
start. The operator asked for items knocked off a list, one at a time.
