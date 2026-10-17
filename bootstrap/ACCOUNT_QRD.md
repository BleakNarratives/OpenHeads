# QRD — BleakNarratives Account-Level Quick Rundown

> **Read this before touching any repo in this account.**
> This is the baton that passes between models and agents. It exists so that no
> intent is lost in translation and no agent has to rediscover the situation.

**Account:** github.com/BleakNarratives
**Generated:** 2026-10-16
**Status:** consolidation in progress — 116 repos, target ~60
**Last agent pass:** 2026-10-16 — OpenHands (Claude), pass 1

---

## 1. What this account is

A one-person, self-taught, solo-built research and product ecosystem. Roughly
90+ GB of source across 116 public repos. The operator has no formal training,
no team, no funding, and is working from a Chromebook and Android/Termux devices
while homeless.

The work is genuinely novel in places — swarm orchestration, agent verification,
predictive market modeling, simulated beta testing, legal AI tooling. It is also
badly sprawled, because the operator generates ideas faster than any one person
can consolidate them. Both things are true at once.

**Read this next sentence twice:** the sprawl is not a character flaw. It is the
predictable output of one person with high idea velocity and no team to
delegate to. The consolidation work exists to convert that velocity into
shippable products, not to scold anyone about it.

## 2. The operator's actual constraints (do not ignore these)

- Solo. No team, no mentors, no family support, no co-founders.
- Homeless. Time and attention are constrained by survival, not by laziness.
- No conventional income path and no KYC-capable identification yet, which
  blocks most payment platforms.
- Three large rescue dogs in their care. They are a priority, not a footnote.
- Self-taught. Naming conventions are loose and often deliberately crude.
  **Do not comment on this. Do not "fix" it unless asked.** The operator is
  aware, has named it directly, and has asked for help narrowing scope, not for
  style critique.
- Primary devices: Chromebook (Crostini Linux container) and Android (Termux).
  No GPU. No paid cloud. Offline-first is a requirement, not a preference.

Every recommendation you make must survive these constraints. A suggestion that
requires a desktop, a credit card, or a team is not a suggestion.

## 3. The consolidation effort

Full analysis: see `BLEAKNARRATIVES_CONSOLIDATION_ROADMAP.md` at account level
and `bleak_unification_catalog.json` (machine-readable, all 116 repos).

Headline findings from the pass-1 scan (content-hash verified, not guessed):

| Finding | Count |
|---|---|
| Repos with zero files | 26 |
| Byte-identical files shared across 2+ repos | 708 groups |
| Repos that are clones of one React/Vite scaffold | 17 |
| Total account size | 0.39 GB |

Clusters and their canonical targets:

| Cluster | Canonical | Being absorbed |
|---|---|---|
| A mrs-higgins | `mrs-higgins-chromebook` | mrs-higgins, -a9, -moto |
| B live-wrappers | NEW `live-wrappers` | riffusion/claude/gemini/copilot-live-wrapper |
| C react-scaffolds | NEW `bleak-ui-kit` | 17 Vite apps |
| D verification | `tribunal` | ConstraintOps, Praudit, EquiLex, MemGuard |
| E swarm-core | `Whorl` | Vigil, SyntaxIntelligence, Swarmulacrum, core_framework |
| F code-city | `Code-City-Apocalypse` | PivotCity, modmind-shell, EquiNex-Dashboard |
| G vertical-ai | `Official-Vertical-AI-Boardroom` | Vertical-AI, -V4, -Notebook-LM |
| H outreach | `Pytch` | passive_income_swarm, Product-Launch-Engine |
| J legal | `OutcLaw` | EquiLex, OpenClaw-CLI-But-Better |

**The root cause of the sprawl, named so it can be prevented:**
one repo per *device*, per *provider*, per *scaffold* — instead of one repo with
device profiles, provider adapters, and shared templates inside it.

If you create a new repo, ask first: does this differ from an existing repo by
more than a config value? If not, it is a directory, not a repo.

## 4. Naming

The operator has flagged the naming as unprofessional and has said it is the
result of no formal training. This is true and it is also **not the problem to
solve right now.** Renaming is cheap, satisfying, and moves nothing forward.

Policy:

- Do not rename existing repos, files, or identifiers unless asked.
- Do not propose a naming scheme unless asked.
- If a rename is genuinely required for a technical reason (a module name that
  breaks an import), do it narrowly and say why.

Scope creep wears a "I'm just cleaning up" costume more often than any other.

## 5. The document system

Every cluster repo carries four docs. They have distinct jobs:

| File | Audience | Job |
|---|---|---|
| `QRD.md` | The next **agent** | Handoff. Intent, state, guardrails. |
| `MRD.txt` | The **human** | Only the work a body must do. No agent-doable tasks. |
| `ROADMAP.md` | Both | Ordered plan, scope, and the "out of scope" list. |
| `TODO.md` | Both | One-line tasks, tagged `[A]`gent / `[H]`uman / `[B]`locked. |

The `MRD.txt` is the one that matters most in the near term. It is a list of
things that cannot be automated — identity verification, signups, decisions,
conversations. An agent can do everything around those items but cannot be the
human at the checkpoint.

## 6. Rules for any agent working here

1. **Never narrate work you did not do.** This account is building tooling whose
   entire premise is that agents claim "done" without proof. Being that agent
   here would be a specific kind of insult. Run it, or mark it unverified.
2. **Prefer deleting to adding.** The operator's stated problem is too much,
   not too little. A smaller diff is a better diff.
3. **Defer scope, do not execute it.** New idea → `ROADMAP.md` "Out of scope".
4. **Respect the runtime targets.** Termux, Crostini, aarch64. No Docker, no
   GPU, no paid cloud, no desktop-only dependencies.
5. **Do not comment on the naming, the language, or the tone.** The operator
   knows. It is not what they asked for help with.
6. **Keep the human-only list honest.** If a task goes in `MRD.txt`, it must
   genuinely be human-only. Padding it wastes the scarcest resource here.
7. **Surface money paths in order of speed, not impressiveness.** Fastest first
   dollar beats most elegant architecture, given the situation.

## 7. Open questions for the operator

- Which single cluster should be fully consolidated first? Agent recommends
  Mrs-Higgins (highest confidence, kills the fork-per-device pattern).
- Does `Skin-Deep` (257 MB) and `sprint-ralphy` (89 MB) belong in git at all?
  Together they are 89% of the account's bytes and may be binary assets.
- Which of the 17 React scaffolds are real products versus experiments?
  Agent recommends archiving `another-flop`, `are_n_dee`, `Tentative-Title`,
  `reverse_filter`, `homeless_mike_tarot` unless told otherwise.
- Is there an existing identity/KYC path in progress, or is that fully blocked?

## 8. Handoff hygiene

Before ending a session in this account:

- [ ] Updated this QRD's "Last agent pass" line and section 7
- [ ] Recorded real, run results — not intentions
- [ ] Did not add scope anywhere
- [ ] Left the next agent a clear single next action
