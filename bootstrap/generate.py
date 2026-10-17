#!/usr/bin/env python3
"""Generate the BleakNarratives consolidation doc-kit.

Reads cluster definitions, renders ROADMAP.md / QRD.md / MRD.txt / TODO.md
per cluster into dist/<repo>/, and emits create_repos.sh for the operator to
run on their own machine (the agent token cannot create repos).

Usage:
    python3 generate.py            # render dist/
    bash create_repos.sh --dry-run # preview repo creation
    bash create_repos.sh --apply   # create + push
"""
import json
import os
import shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")
DIST = os.path.join(HERE, "dist")
TODAY = date.today().isoformat()
OWNER = "BleakNarratives"


def read_tpl(name):
    with open(os.path.join(TPL, name)) as fh:
        return fh.read()


def render(tpl, mapping):
    out = tpl
    for key, value in mapping.items():
        out = out.replace("{{%s}}" % key, str(value))
    return out


def bullet(items):
    return "\n".join("- %s" % i for i in items)


def numbered(items):
    return "\n".join("%d. %s" % (n, i) for n, i in enumerate(items, 1))


def table(rows):
    return "\n".join("| %s | %s |" % (a, b) for a, b in rows)


# ---------------------------------------------------------------------------
# Cluster definitions. Each entry carries real content, not placeholders.
# ---------------------------------------------------------------------------

CLUSTERS = [
    {
        "repo": "bleak-higgins",
        "cluster": "A - Mrs. Higgins pipeline",
        "status": "canonical (merging in 3 repos)",
        "description": "Local autonomous SaaS routing pipeline. Canonical home for the Mrs-Higgins family.",
        "what_this_is": (
            "A fully local, offline-capable SaaS routing pipeline that runs on an\n"
            "Android phone under Termux. It loads product packages, generates\n"
            "platform-specific listings, creates Lightning invoices, follows up on\n"
            "unpaid leads, reconciles payments, and reports what is actually working.\n\n"
            "The crew of scripts (front_desk_lady, bookkeeper, the_closer, copywriter,\n"
            "scout, the_ledger, briefing) is the product. One shell command runs it."
        ),
        "why": (
            "It is the closest thing in this account to a revenue loop that needs no\n"
            "KYC, no cloud, and no team. Lightning is the only payment rail that does\n"
            "not require identity documents, and this pipeline already integrates it.\n"
            "That makes it the fastest available path to a first dollar given the\n"
            "operator's current constraints."
        ),
        "canonical_status": (
            "This repo IS canonical. Three sibling repos are absorbed into it:\n"
            "`mrs-higgins`, `mrs-higgins-a9`, `mrs-higgins-moto`.\n\n"
            "They were never different projects. They are the same pipeline pointed\n"
            "at different device paths. The shared README is byte-identical across all\n"
            "four, as are setup.sh, mrs_higgins.sh, the static assets, the templates,\n"
            "and all ~50 saas_packages/*.json files."
        ),
        "code_state": (
            "Four repos, 460 files total, collapsing to ~210 distinct blobs.\n\n"
            "| Repo | Files | Unique blobs |\n"
            "|---|---|---|\n"
            "| mrs-higgins | 21 | 3 |\n"
            "| mrs-higgins-a9 | 76 | 20 |\n"
            "| mrs-higgins-moto | 26 | 17 |\n"
            "| mrs-higgins-chromebook | 337 | 109 (canonical) |\n\n"
            "40 unique blobs need to be ported in from the three siblings."
        ),
        "works": "Not verified by an agent yet. Operator reports the loop runs end to end.",
        "broken": "Unknown - no test suite exists.",
        "unverified": "Everything. Pass 1 was analysis only; no code was executed.",
        "runtime": "Termux / Android aarch64 primary; Crostini secondary",
        "purpose": "One canonical Mrs-Higgins pipeline, device-agnostic, with a profile per target device.",
        "current_state": "4 repos to be merged into 1. Porting not yet started.",
        "in_scope": [
            "The pipeline loop: load packages, route, invoice, follow up, reconcile, report",
            "Device profiles for Termux, Crostini, and moto targets",
            "Lightning payments via Voltage",
            "Ollama-powered copy generation",
            "The saas_packages catalogue",
        ],
        "deferred": [
            ("Web dashboard", "The CLI briefing already answers the question. A dashboard is a second way to do something that works."),
            ("Multi-user support", "One operator. There is no second user."),
            ("Cloud sync", "Offline-first is a requirement, not a limitation to fix."),
            ("Plugin system", "Nothing needs plugins yet."),
        ],
        "plan": [
            ("Create the canonical repo", "Push mrs-higgins-chromebook's tree as the initial commit of bleak-higgins."),
            ("Port 20 unique blobs from a9", "Diff against canonical, copy in what is genuinely new."),
            ("Port 17 unique blobs from moto", "Same process."),
            ("Port 3 unique blobs from mrs-higgins", "Same process."),
            ("Add device-profiles/", "Extract the hardcoded device paths into profiles: termux.yaml, crostini.yaml, moto.yaml."),
            ("Archive the three siblings", "With a redirect note in each README."),
            ("First real run", "Execute the loop on the Chromebook and record what actually happens."),
        ],
        "deps": [
            ("payment_system", "Lightning + Monero + Stripe + license keys", "exists, not wired"),
            ("passive_income_swarm", "FastAPI gateway if a network face is needed", "exists, separate"),
        ],
        "risks": [
            ("Voltage API changes", "Payment loop breaks", "Wrap in one adapter module so only one file changes"),
            ("Device paths hardcoded", "Runs on one device only", "device-profiles/ is the fix; do it in pass 2"),
            ("No tests", "Cannot tell working from broken", "Add one smoke test that runs the briefing command"),
        ],
        "cluster_members": "mrs-higgins, mrs-higgins-a9, mrs-higgins-chromebook (canonical), mrs-higgins-moto, The-Werkz (carries a 5th copy)",
        "merge_plan": (
            "1. Seed new repo from mrs-higgins-chromebook tree\n"
            "2. Port unique blobs from a9, moto, mrs-higgins\n"
            "3. Introduce device-profiles/, refactor path references to read from them\n"
            "4. Archive the three siblings with a pointer README"
        ),
        "next": [
            "Seed bleak-higgins from mrs-higgins-chromebook",
            "Diff and port the 40 unique blobs from the three siblings",
            "Write device-profiles/ and refactor path references",
        ],
        "questions": [
            "Which device is the actual production target - the moto or the Chromebook?",
            "Is Voltage still the payment provider, or has that changed?",
        ],
        "mrd_blockers": [
            ("SET UP THE LIGHTNING WALLET AND RECEIVE ADDRESS",
             "The pipeline creates invoices, but someone has to hold the wallet and receive the money. An agent cannot custody funds.",
             ["Create or open a Lightning wallet that accepts incoming payments",
              "Point front_desk_config.json at the receive address",
              "Send yourself a 1-sat test payment and confirm it reconciles"],
             "under an hour", "$0",
             "A test payment reconciles in income_summary.json"),
            ("DECIDE THE PRICE FOR EACH SAAS PACKAGE",
             "The pipeline can generate listings, but only you can decide what to charge. Pricing is a business decision with consequences.",
             ["Open saas_packages/ and set a price on the packages worth selling",
              "Start with 3 packages, not 50",
              "Record the prices in one place the pipeline reads"],
             "one evening", "$0",
             "Every package in the catalogue has a price or is marked free"),
        ],
    },
    {
        "repo": "bleak-whorl",
        "cluster": "E - Swarm core",
        "status": "canonical (absorbing 5 repos)",
        "description": "Field intelligence and agent deployment workbench. Canonical swarm core.",
        "what_this_is": (
            "A modular, portable Python ecosystem that runs entirely on Termux with no\n"
            "cloud and no Docker. SQLite + Ollama + Nostr.\n\n"
            "Modules: scouts (intel ingestion), forge (pitch engine), hotseat\n"
            "(three-voice stress test), loom (CodeCity-Bench topological analysis),\n"
            "agents (deployed), tailor (QRD engine), nostr (agent intercom), slice\n"
            "(confidence-gated split inference), core (shared models + SQLite)."
        ),
        "why": (
            "This is the actual orchestration substrate for the whole account. It is\n"
            "already modular, already Termux-native, and already has the shape every\n"
            "other swarm repo is trying to reach. Consolidating here removes five\n"
            "parallel attempts at the same thing."
        ),
        "canonical_status": (
            "This repo IS canonical. Absorbing: `Vigil`, `SyntaxIntelligence`,\n"
            "`Swarmulacrum`, `core_framework`, `propagated_node`, `Concierge`.\n\n"
            "Note that `core_framework` states in its own README that it contains\n"
            "**no copied source code** - every file is a pointer into canonical trees.\n"
            "It is a documentation repo wearing a code repo's clothes."
        ),
        "code_state": (
            "Whorl: 160 files, 84 Python modules, already modular.\n\n"
            "Absorbed material:\n"
            "- Vigil: integrity.py, geometry.py, fabrication.py - the scout substrate\n"
            "- SyntaxIntelligence: the 6-tier governance ladder (Recruit to Council)\n"
            "- Swarmulacrum: audit reports, white paper, core/, bin/\n"
            "- core_framework: pointer table only, no code\n"
            "- propagated_node, Concierge: small node + entry pieces"
        ),
        "works": "Whorl installs and its modules import. Slice has tests (tests/test_slice*.py).",
        "broken": "Unknown for the absorbed repos - not executed.",
        "unverified": "Whether Vigil/SyntaxIntelligence integrate cleanly. Not attempted.",
        "runtime": "Termux, offline-first, SQLite + Ollama",
        "purpose": "One swarm core. Every other swarm-shaped repo folds in here or is archived.",
        "current_state": "Whorl is healthy and modular. Six repos queued for absorption.",
        "in_scope": [
            "The module set already in Whorl: scouts, forge, hotseat, loom, agents, tailor, nostr, slice, core",
            "Vigil's integrity/geometry/fabrication as whorl/scouts/ substrate",
            "SyntaxIntelligence's tier ladder as whorl/governance/",
            "SQLite persistence and offline operation",
        ],
        "deferred": [
            ("Web UI", "The CLI is the interface. A web UI is a second front end."),
            ("Plugin registry", "Modules are plugins already."),
            ("Distributed multi-node", "propagated_node exists but single-node is not finished."),
            ("Renaming modules for consistency", "Churn without function."),
        ],
        "plan": [
            ("Seed bleak-whorl from Whorl", "Clean tree, no history rewrite."),
            ("Add whorl/scouts/integrity + geometry + fabrication", "Port from Vigil, keep the HMAC signing and quadratic dispersion logic intact."),
            ("Add whorl/governance/tiers", "Port the 6-tier ladder from SyntaxIntelligence."),
            ("Move core_framework's pointer table into docs/ORCHESTRATION.md", "It is documentation. Treat it as documentation."),
            ("Reconcile the duplicate core_framework/", "It also exists inside a9-codex-grapher. One of them is stale."),
            ("Archive the absorbed repos", "With pointer READMEs."),
        ],
        "deps": [
            ("Vigil", "integrity.py, geometry.py, fabrication.py", "to absorb"),
            ("SyntaxIntelligence", "tier ladder", "to absorb"),
            ("Agentic-Almanac", "supplies docs/AGENT_ALMANAC.json to whorl/src/skill/scout.py", "exists"),
        ],
        "risks": [
            ("Absorbing too much at once", "Nothing works and nothing is testable", "Absorb one repo per pass, verify imports after each"),
            ("Whorl's own tests are thin", "Regressions go unnoticed", "Add an import smoke test for every module first"),
        ],
        "cluster_members": "Whorl (canonical), Vigil, SyntaxIntelligence, Swarmulacrum, core_framework, propagated_node, Concierge",
        "merge_plan": (
            "1. Seed bleak-whorl from Whorl\n"
            "2. Absorb Vigil as whorl/scouts/{integrity,geometry,fabrication}.py\n"
            "3. Absorb SyntaxIntelligence tiers as whorl/governance/tiers.py\n"
            "4. core_framework pointer table becomes docs/ORCHESTRATION.md\n"
            "5. Archive Vigil, SyntaxIntelligence, Swarmulacrum, core_framework, propagated_node, Concierge"
        ),
        "next": [
            "Write an import smoke test covering every Whorl module",
            "Absorb Vigil's three files into whorl/scouts/ and re-run the smoke test",
            "Move core_framework's pointer table into docs/ORCHESTRATION.md",
        ],
        "questions": [
            "Is Vigil's HMAC signing still wanted, or was that superseded?",
            "Does propagated_node need to stay separate for actual multi-device use?",
        ],
        "mrd_blockers": [
            ("DECIDE THE SCOPE OF THE SWARM CORE",
             "An agent cannot decide what this system is for. Without that, absorption order is guesswork.",
             ["Write one sentence: what does this swarm actually do that earns money?",
              "If the answer is 'scout for market opportunities', say so plainly",
              "Everything not serving that sentence gets deferred"],
             "one hour of thinking", "$0",
             "ROADMAP.md section 'In scope' has three items and no more"),
        ],
    },
    {
        "repo": "bleak-verification",
        "cluster": "D - Verification and adversarial review",
        "status": "canonical (absorbing 4 repos)",
        "description": "Catch AI agents that narrate work they did not do. Engine plus commercial face.",
        "what_this_is": (
            "A verification gate for AI coding agents. It watches an agent work and\n"
            "flags every claim - 'done', 'verified', 'all tests pass' - that is not\n"
            "backed by evidence.\n\n"
            "The founding measurement: across thirty AI coding sessions, assistants\n"
            "claimed 215 files of work. Fifteen existed. Two hundred files described in\n"
            "confident complete sentences were never created."
        ),
        "why": (
            "This is the most immediately sellable thing in the account. The problem is\n"
            "real, universal, and the buyer (a developer or an engineering manager)\n"
            "already knows they have it. Pricing tiers are already drafted in\n"
            "ConstraintOps. It needs packaging, not invention."
        ),
        "canonical_status": (
            "This repo IS canonical. Absorbing: `ConstraintOps` (product, pricing,\n"
            "docs), `Praudit` (shim wrappers), `EquiLex` (compliance monitor),\n"
            "`MemGuard` (OOM defense).\n\n"
            "`tribunal` is the engine. `ConstraintOps` is the commercial face. The\n"
            "other three are runtime guards with the same verdict-bus shape."
        ),
        "code_state": (
            "tribunal: 74 KB, 11 Python modules, 8 shell scripts, a VSCode extension,\n"
            "boardroom/, docs/, tests/.\n\n"
            "ConstraintOps: 144 KB, 49 markdown files (positioning, pricing, outreach,\n"
            "client forms), 22 Python modules, 6 HTML.\n\n"
            "Praudit: 26 files, mostly shims (openclaw_shim.py, molt_shim.py,\n"
            "vibe_skill_shim.py) plus agent_kernel.py.\n\n"
            "EquiLex: 13 KB compliance monitor. MemGuard: 28 KB PSI-driven OOM defense."
        ),
        "works": "tribunal has tests/ and a CLI. Not executed by an agent yet.",
        "broken": "Unknown.",
        "unverified": "The whole suite. Pass 1 was analysis only.",
        "runtime": "Termux-compatible Python; VSCode extension is desktop-side",
        "purpose": "One verification product: engine, guards, and a sellable service around it.",
        "current_state": "Engine and product docs exist separately. Not yet joined.",
        "in_scope": [
            "Claim detection: catch 'done' / 'verified' / 'tests pass' without evidence",
            "Evidence checking against actual filesystem and test state",
            "The ConstraintOps service offering and its pricing tiers",
            "Runtime guards: OOM pressure and compliance checks",
        ],
        "deferred": [
            ("Supporting every CLI agent", "Start with one. Gemini CLI or Codex CLI, whichever is actually used."),
            ("A hosted SaaS version", "Local first. Hosting is a second business."),
            ("The VSCode extension", "CLI proves the concept; the extension is distribution later."),
        ],
        "plan": [
            ("Seed bleak-verification from tribunal", "Engine first."),
            ("Bring ConstraintOps docs into docs/service/", "Positioning, pricing, client forms, outreach."),
            ("Fold Praudit shims into wrapper/", "They are integration adapters."),
            ("Fold EquiLex and MemGuard into guards/", "Both produce verdicts on runtime state."),
            ("Write one end-to-end demo", "An agent claims done; the tool catches it. That demo is the product."),
            ("Archive the four absorbed repos", "With pointer READMEs."),
        ],
        "deps": [
            ("Official-Vertical-AI-Boardroom", "Tribunal cites it as the source methodology", "exists"),
        ],
        "risks": [
            ("Scope: supporting all agents", "Nothing ships", "One agent integration first, proven end to end"),
            ("Overlap with Code City", "Two places to maintain verification", "Code City consumes this; it does not reimplement it"),
        ],
        "cluster_members": "tribunal (canonical), ConstraintOps, Praudit, EquiLex, MemGuard",
        "merge_plan": (
            "1. Seed bleak-verification from tribunal\n"
            "2. ConstraintOps docs -> docs/service/\n"
            "3. Praudit shims -> wrapper/\n"
            "4. EquiLex + MemGuard -> guards/\n"
            "5. Archive all four"
        ),
        "next": [
            "Seed bleak-verification from tribunal",
            "Build the end-to-end demo: agent claims done, tool catches it",
            "Move ConstraintOps pricing and outreach docs into docs/service/",
        ],
        "questions": [
            "Which CLI agent do you actually use day to day? That is the first integration.",
            "Is the $250/48h audit report still the intended offer, or has that changed?",
        ],
        "mrd_blockers": [
            ("POST THE CONSTRAINTOPS OFFER WHERE BUYERS ALREADY ARE",
             "An agent can write the post. It cannot have an account, and it cannot be you when a buyer replies.",
             ["Pick one venue: Hacker News, a subreddit, or a Discord you are already in",
              "Post the offer with the real number from your own transcript audit",
              "Be present to answer replies for the first few hours"],
             "2 hours", "$0",
             "The offer is live and someone has replied"),
            ("RUN THE AUDIT ON YOUR OWN TRANSCRIPTS FIRST",
             "The 215-files-claimed / 15-existed finding is your proof. It needs to be reproducible by you on demand, not just asserted.",
             ["Pick 3 of your own past sessions",
              "Run the detector, record the real numbers",
              "That number is the headline of every sales conversation"],
             "one evening", "$0",
             "You have a repeatable number you can state with confidence"),
        ],
    },
    {
        "repo": "bleak-ui-kit",
        "cluster": "C - React/Vite scaffold sprawl",
        "status": "NEW - replaces 17 scaffold repos",
        "description": "Shared React/Vite starter. Replaces 17 near-identical scaffold repos.",
        "what_this_is": (
            "One Vite + React + TypeScript starter that the account's front-end work\n"
            "consumes instead of copying.\n\n"
            "Seventeen repos in this account are clones of the same scaffold. Their\n"
            "tsconfig.json is byte-identical in 15 of them. vite.config.ts is identical\n"
            "in 12. The differences are almost entirely in App.tsx."
        ),
        "why": (
            "Seventeen copies of one config file is 17 places for the same bug to live\n"
            "and 17 upgrades to perform by hand. A shared starter converts that into one\n"
            "place. It is the cheapest large win in the account."
        ),
        "canonical_status": (
            "This repo is NEW and IS canonical for scaffolding. The 17 scaffold repos\n"
            "either consume it or get archived.\n\n"
            "Triage recommendation: archive `another-flop`, `are_n_dee`,\n"
            "`Tentative-Title`, `reverse_filter`, `homeless_mike_tarot` outright - the\n"
            "names indicate experiments. Keep the rest for feature extraction."
        ),
        "code_state": (
            "17 repos, 656 files total, 580 distinct blobs. Only 10 blobs are shared\n"
            "by 3+ repos, which means the duplication is in config, not in features.\n\n"
            "Scaffold repos: ShipWrekD-OS-Syntax-AI-Driven-IDE, Vertical-AI,\n"
            "Vert-AI-AI-Studio-Fromtend, ModMind-GlassRing-and-Company,\n"
            "ModMind-Identity-Utility, Kick-Rock, another-flop, are_n_dee,\n"
            "reverse_filter, Eww, Tentative-Title, homeless_mike_tarot,\n"
            "nesting_bestie_taylor_demo, odds-of-the-gods, fd_cohort,\n"
            "EquiNex-Universal-Dashboard, Pivot"
        ),
        "works": "Each scaffold presumably runs. None verified by an agent.",
        "broken": "Unknown.",
        "unverified": "Which of the 17 contain real features worth extracting.",
        "runtime": "Node/Vite. Build output is static, so it deploys anywhere.",
        "purpose": "One starter. Every front end consumes it. No more scaffold copies.",
        "current_state": "17 parallel scaffolds. Consolidation not started.",
        "in_scope": [
            "Vite + React + TypeScript starter with the account's shared config",
            "Shared components: layout, theming, the metadata.json convention",
            "A documented way to consume it",
        ],
        "deferred": [
            ("A component library", "A starter, not a design system. Components come from real apps."),
            ("Storybook", "Heavy dependency, no current user."),
            ("Publishing to npm", "Local consumption first. npm is distribution later."),
        ],
        "plan": [
            ("Extract the canonical config set", "tsconfig.json, vite.config.ts, index.html, metadata.json."),
            ("Triage the 17 repos", "Which are products, which are experiments."),
            ("Build the starter", "Config plus a minimal App shell plus README."),
            ("Re-point the survivors", "Consume the starter, delete local config copies."),
            ("Archive the experiments", "The five named above, unless told otherwise."),
        ],
        "deps": [
            ("EquiNex-Universal-Dashboard", "richest scaffold, best extraction source", "exists"),
            ("odds-of-the-gods", "largest at 156 files, has real components", "exists"),
        ],
        "risks": [
            ("Breaking a working app", "Lost work", "Extract first, migrate one app at a time"),
            ("Nobody adopts it", "18 scaffolds instead of 17", "Migrate one real app end to end as proof"),
        ],
        "cluster_members": "17 scaffold repos listed in section 5, plus Code-City-Apocalypse and Skin-Deep which also carry scaffolds",
        "merge_plan": (
            "1. Extract shared config into bleak-ui-kit\n"
            "2. Migrate one real app (EquiNex-Universal-Dashboard) as proof\n"
            "3. Migrate the survivors one at a time\n"
            "4. Archive the experiments"
        ),
        "next": [
            "Extract the canonical tsconfig/vite.config/index.html set",
            "Triage the 17: product, experiment, or already dead",
            "Migrate EquiNex-Universal-Dashboard as the first consumer",
        ],
        "questions": [
            "Which of the 17 scaffolds are you still actively working on?",
            "Is odds-of-the-gods (156 files, a game) a product or a hobby?",
        ],
        "mrd_blockers": [
            ("TRIAGE THE 17 SCAFFOLDS: PRODUCT OR EXPERIMENT",
             "Only you know which of these you intend to finish. An agent guessing wrong wastes the migration effort.",
             ["Open the 17 repos, spend 30 seconds each",
              "Mark each: PRODUCT, EXPERIMENT, or DEAD",
              "That list is the migration order"],
             "30 minutes", "$0",
             "A triage list exists and the five experiments are archived"),
        ],
    },
    {
        "repo": "bleak-tools",
        "cluster": "H + N - Operator toolbelt and stubs",
        "status": "NEW - absorbs 8 small repos",
        "description": "The operator toolbelt. Small CLI tools, shims, and utilities in one place.",
        "what_this_is": (
            "One home for the account's small, genuinely useful command-line tools.\n"
            "Each is 2-10 files. Individually too small to justify a repo; together they\n"
            "are a real toolbelt.\n\n"
            "Absorbs: bin-scripts (74 files, 28 Python, 20 shell), askhole-cli,\n"
            "Negotiator, Kindred, Concierge, propagated_node, Gemini-CLI-Bridge,\n"
            "pattern_journal."
        ),
        "why": (
            "Eight repos averaging under 15 KB each. Each one costs a full repo's\n"
            "overhead - a README, a license, a CI config, a place in the mental model -\n"
            "for a single script. Consolidating them removes 7 repos from the account\n"
            "and makes the tools actually findable."
        ),
        "canonical_status": (
            "This repo is NEW and IS canonical for small tools.\n\n"
            "`bin-scripts` is the backbone - it is already an operator toolbelt with a\n"
            "description that reads '~/bin operator toolbelt'. The others attach to it."
        ),
        "code_state": (
            "bin-scripts: 74 files (28 Python, 20 shell) - vault tools, agentfork,\n"
            "boot_heal, cache_guard, ecosystem_sync, err_watch, freebuff_doctor,\n"
            "hook_server, llama-serve, market_scan.\n\n"
            "Plus: askhole-cli (2 files), Negotiator (7), Kindred (16),\n"
            "Concierge (2), propagated_node (27), Gemini-CLI-Bridge (3),\n"
            "pattern_journal (8)."
        ),
        "works": "bin-scripts is in daily use per its own description.",
        "broken": "Unknown for the absorbed tools.",
        "unverified": "Everything else.",
        "runtime": "Termux / Crostini shell + Python",
        "purpose": "One toolbelt. Every small tool lives here and is documented in one index.",
        "current_state": "bin-scripts exists and works. Seven repos to absorb.",
        "in_scope": [
            "bin-scripts as the base, with an indexed README",
            "The small CLI tools: askhole, Negotiator, Kindred, Concierge",
            "Gemini-CLI-Bridge, pattern_journal",
        ],
        "deferred": [
            ("Unifying the CLI interface", "They are separate tools. A wrapper is a second way to call them."),
            ("Packaging as a pip install", "Local use first."),
        ],
        "plan": [
            ("Seed bleak-tools from bin-scripts", "It is the base."),
            ("Add tools/ per absorbed tool", "One directory each, preserving the original file."),
            ("Write the tool index", "One line per tool in the README so they are findable."),
            ("Archive the 7 absorbed repos", "With pointer READMEs."),
        ],
        "deps": [],
        "risks": [
            ("Tools rot unmaintained", "Toolbelt becomes a graveyard", "The README index names what is actually used vs parked"),
        ],
        "cluster_members": "bin-scripts (base), askhole-cli, Negotiator, Kindred, Concierge, propagated_node, Gemini-CLI-Bridge, pattern_journal",
        "merge_plan": (
            "1. Seed bleak-tools from bin-scripts\n"
            "2. tools/<name>/ per absorbed tool\n"
            "3. Indexed README\n"
            "4. Archive the 7"
        ),
        "next": [
            "Seed bleak-tools from bin-scripts",
            "Move askhole-cli and Negotiator in as tools/",
            "Write the one-line-per-tool index",
        ],
        "questions": [
            "Which bin-scripts entries do you actually run regularly? Those get documentation first.",
        ],
        "mrd_blockers": [
            ("MARK WHICH TOOLS YOU ACTUALLY USE",
             "An agent cannot know which of the 74 bin-scripts entries matter to your day. Without that, documentation effort goes to the wrong places.",
             ["Run ls ~/bin and mark what you have used in the last month",
              "Those get full documentation",
              "Everything else gets a one-line description and is left alone"],
             "30 minutes", "$0",
             "The README index distinguishes active tools from parked ones"),
        ],
    },
    {
        "repo": "bleak-outclaw",
        "cluster": "J - Legal toolkit",
        "status": "canonical (absorbing 3 repos)",
        "description": "Pro se legal AI toolkit. Citation fraud detection, IRAC arguments, FOIA, judicial complaints.",
        "what_this_is": (
            "A legal AI toolkit for people representing themselves in court. It analyzes\n"
            "legal documents, detects citation fraud, generates IRAC legal arguments,\n"
            "files FOIA requests, and produces judicial complaints. Runs locally.\n\n"
            "Modules include outclaw_arch.py (citation extraction - USC, CFR, F.3d,\n"
            "case names) and outclaw_semantic.py (classifies citations as\n"
            "support/oppose/neutral)."
        ),
        "why": (
            "Real audience with real need and real willingness to pay - pro se\n"
            "litigants have no cheaper alternative. It is also the largest single\n"
            "codebase in the legal cluster at 305 files, so most of the work is done."
        ),
        "canonical_status": (
            "This repo IS canonical. Absorbing: `EquiLex` (compliance monitor),\n"
            "`OpenClaw-CLI-But-Better` (ENDEMPTS docs + dashboard),\n"
            "`OutClaw-Integration` (6.8 MB of docs, zero code)."
        ),
        "code_state": (
            "OutcLaw: 305 files, 97 Python, 78 txt, 43 md, 31 json, 13 shell,\n"
            "12 html, plus 5 PDF and 4 DOCX. Directories include OutClaw_Main,\n"
            "OutClaw_Grievances, OutClaw_Judicial_Complaints, OutClaw_Research,\n"
            "OutClaw_Admin_Warfare, OllamaWrapper.\n\n"
            "Note: there is a stray directory literally named '=' in the tree - worth\n"
            "a look."
        ),
        "works": "Unknown - not executed.",
        "broken": "Unknown.",
        "unverified": "Everything.",
        "runtime": "Termux-compatible Python, local models via Ollama",
        "purpose": "One legal toolkit. Citation analysis, argument generation, filing support.",
        "current_state": "305 files exist. Not consolidated, not verified.",
        "in_scope": [
            "Citation extraction and classification",
            "IRAC argument generation",
            "FOIA request generation",
            "Judicial complaint drafting",
            "Local-only operation",
        ],
        "deferred": [
            ("A web interface", "CLI first."),
            ("Supporting non-federal jurisdictions", "Federal first, proven."),
            ("Fine-tuning a legal model", "Prompt the existing model until that stops working."),
        ],
        "plan": [
            ("Seed bleak-outclaw from OutcLaw", "305 files as the base."),
            ("Clean the stray '=' directory and duplicate dirs", "OutClaw_Judicial_Complaints and its (1) twin."),
            ("Fold EquiLex in as compliance/", "It is a compliance monitor; same domain."),
            ("Move ENDEMPTS docs to docs/endempts/", "From OpenClaw-CLI-But-Better."),
            ("Reduce OutClaw-Integration to docs/deployment/", "It is 6.8 MB of markdown and 3 images, no code."),
            ("Verify one real pipeline", "Feed a real document, get a real citation analysis."),
        ],
        "deps": [
            ("OllamaWrapper", "already inside OutcLaw", "exists"),
        ],
        "risks": [
            ("Legal accuracy", "Bad output harms a real litigant", "Never present output as legal advice; it is a drafting aid"),
            ("Repo size", "2.4 MB plus PDFs and DOCX", "Move binaries out of git if they grow"),
        ],
        "cluster_members": "OutcLaw (canonical), EquiLex, OpenClaw-CLI-But-Better, OutClaw-Integration",
        "merge_plan": (
            "1. Seed bleak-outclaw from OutcLaw\n"
            "2. Clean stray directories\n"
            "3. EquiLex -> compliance/\n"
            "4. ENDEMPTS docs -> docs/endempts/\n"
            "5. OutClaw-Integration -> docs/deployment/\n"
            "6. Archive the three"
        ),
        "next": [
            "Seed bleak-outclaw from OutcLaw",
            "Clean the '=' directory and the duplicate Judicial_Complaints dirs",
            "Run one real document through the citation pipeline",
        ],
        "questions": [
            "Is the target federal courts only, or state too?",
            "Are you yourself using this for an active case? If so, that is the test case.",
        ],
        "mrd_blockers": [
            ("TEST IT ON A REAL DOCUMENT YOU ALREADY HAVE",
             "An agent can run the code. It cannot judge whether the legal output is correct - that requires someone who knows the case.",
             ["Pick a real filing or decision you have on hand",
              "Run it through the citation pipeline",
              "Check whether the extracted citations are actually right"],
             "2 hours", "$0",
             "You have seen real output and know whether it is trustworthy"),
            ("DECIDE THE DISCLAIMER AND LIABILITY POSITION",
             "Legal tooling carries real risk if someone relies on it. An agent cannot make that call.",
             ["Decide the exact disclaimer language",
              "Decide whether this is a tool you use yourself or one you sell",
              "Put the disclaimer in the README and in the CLI output"],
             "one hour", "$0",
             "A disclaimer exists and appears wherever output is produced"),
        ],
    },
    {
        "repo": "bleak-vertical-ai",
        "cluster": "G - Vertical AI / Boardroom",
        "status": "canonical (absorbing 5 repos)",
        "description": "AI expert model boardroom. Multi-persona analysis and adversarial review.",
        "what_this_is": (
            "A boardroom of AI expert personas that analyze a question from multiple\n"
            "angles and produce a debrief. Also the origin of the adversarial review\n"
            "methodology that tribunal later pointed at code.\n\n"
            "Components: boardroom.py, boardroom_bridge.py, chairman.py,\n"
            "board_debrief.py, buffface_server.py."
        ),
        "why": (
            "It is the account's most-referenced concept - tribunal explicitly cites it\n"
            "as the source methodology. It also has a clear product shape: simulated\n"
            "expert panels for business modeling, pitch review, and product critique."
        ),
        "canonical_status": (
            "This repo IS canonical. Absorbing: `Vertical-AI`, `Vertical-AI-V4`,\n"
            "`Vertical-AI-Notebook-LM`, `Vert-AI-AI-Studio-Fromtend`, `vertical_local`.\n\n"
            "Six repos share one product name. Three are front ends for the same engine."
        ),
        "code_state": (
            "Official-Vertical-AI-Boardroom: 106 files, 46 Python, 30 txt, 9 md,\n"
            "8 html. Includes a MarketScout.zip and several .log files.\n\n"
            "Vertical-AI-V4: 28 files with a swarm_engine.py, codebase_graph_scanner.py,\n"
            "codebase_evolution_daemon.py, idle_detector.py, market_intelligence.py,\n"
            "promise_logger.py.\n\n"
            "vertical_local: 4 files, docs only (MRD.txt, QRD.md, ROADMAP.md, runbook.txt)."
        ),
        "works": "Unknown - not executed.",
        "broken": "Unknown.",
        "unverified": "Everything.",
        "runtime": "Python, local models",
        "purpose": "One boardroom engine with multiple front ends, and a clear product offering.",
        "current_state": "Six repos, one concept, no consolidation.",
        "in_scope": [
            "The boardroom engine: personas, debate, debrief",
            "The chairman / adjudication logic",
            "One front end (CLI)",
        ],
        "deferred": [
            ("Three separate front ends", "One CLI until the engine is proven."),
            ("The Notebook-LM audio deep dive", "A different product wearing the same name."),
            ("Codebase evolution daemon", "Ambitious, unrelated to the boardroom's core job."),
        ],
        "plan": [
            ("Seed bleak-vertical-ai from Official-Vertical-AI-Boardroom", "The real engine."),
            ("Verify the boardroom runs", "One question in, one debrief out."),
            ("Move MarketScout.zip out of git", "Binaries do not belong in the tree."),
            ("Absorb the front ends as ui/", "Or archive them, if the CLI is enough."),
            ("Decide the Notebook-LM's fate", "It may be its own product."),
        ],
        "deps": [
            ("payment_system", "README says it was built for the Boardroom", "exists"),
            ("tribunal", "cites Boardroom as its methodology source", "related"),
        ],
        "risks": [
            ("Six repos, one name", "Nobody knows which is current", "One canonical, explicit archives"),
            ("Log files and zips in git", "Bloats the repo", "Gitignore and remove"),
        ],
        "cluster_members": "Official-Vertical-AI-Boardroom (canonical), Vertical-AI, Vertical-AI-V4, Vertical-AI-Notebook-LM, Vert-AI-AI-Studio-Fromtend, vertical_local",
        "merge_plan": (
            "1. Seed bleak-vertical-ai from Official-Vertical-AI-Boardroom\n"
            "2. Verify one boardroom run end to end\n"
            "3. Front ends -> ui/, or archive\n"
            "4. vertical_local docs -> docs/\n"
            "5. Archive the absorbed repos"
        ),
        "next": [
            "Seed bleak-vertical-ai from the Boardroom",
            "Run one question through the boardroom and record the output",
            "Move MarketScout.zip and the .log files out of the tree",
        ],
        "questions": [
            "Is Vertical-AI-Notebook-LM part of this product or a separate thing?",
            "Which of the three front ends do you actually use?",
        ],
        "mrd_blockers": [
            ("RUN ONE REAL QUESTION THROUGH THE BOARDROOM",
             "An agent can execute it. Only you can judge whether the debrief is actually useful or just plausible-sounding.",
             ["Pick a real business question you care about",
              "Run it through the boardroom",
              "Judge honestly: is the output useful, or is it convincing noise?"],
             "1 hour", "$0",
             "You know whether this product has real value or just a good demo"),
            ("DECIDE WHICH FRONT END IS THE PRODUCT",
             "Three front ends is three products. An agent cannot pick for you.",
             ["Look at all three",
              "Pick one. Archive or defer the other two",
              "That decision unlocks all front-end work"],
             "1 hour", "$0",
             "One front end is designated and the others are deferred in ROADMAP.md"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render_cluster(c):
    tpl_roadmap = read_tpl("ROADMAP.md")
    tpl_qrd = read_tpl("QRD.md")
    tpl_mrd = read_tpl("MRD.txt")
    tpl_todo = read_tpl("TODO.md")

    common = {
        "REPO": c["repo"],
        "CLUSTER": c["cluster"],
        "STATUS": c["status"],
        "DATE": TODAY,
        "PASS": "1",
        "MODEL_OR_AGENT": "OpenHands (Claude)",
        "PURPOSE": c["purpose"],
        "CURRENT_STATE": c["current_state"],
        "RUNTIME": c["runtime"],
        "CANONICAL_STATUS": c["canonical_status"],
        "WHAT_THIS_IS": c["what_this_is"],
        "WHY": c["why"],
        "CODE_STATE": c["code_state"],
        "WORKS": c["works"],
        "BROKEN": c["broken"],
        "UNVERIFIED": c["unverified"],
        "CLUSTER_MEMBERS": c["cluster_members"],
        "MERGE_PLAN": c["merge_plan"],
        "IN_SCOPE_LIST": numbered(c["in_scope"]),
        "DEFERRED_TABLE": table(c["deferred"]),
        "PLAN_LIST": "\n".join("- [ ] **%s** \u2014 %s" % (a, b) for a, b in c["plan"]),
        "DEPS_TABLE": table([(a, "%s (%s)" % (b, s)) for a, b, s in c["deps"]]) or "| none | - | - |",
        "RISKS_TABLE": "\n".join("| %s | %s | %s |" % (a, b, d) for a, b, d in c["risks"]),
        "NEXT_LIST": numbered(c["next"]),
        "NOW_LIST": "\n".join([
            "- [ ] [A] %s" % (c["next"][0] if len(c["next"]) > 0 else "Triage the cluster"),
            "- [ ] [A] %s" % (c["next"][1] if len(c["next"]) > 1 else "Verify the merged tree runs"),
            "- [ ] [A] %s" % (c["next"][2] if len(c["next"]) > 2 else "Archive absorbed repos"),
            "- [ ] [H] %s" % (c["mrd_blockers"][0][0] if c["mrd_blockers"] else "see MRD.txt"),
        ]),
        "LATER_LIST": "\n".join([
            "- [ ] [A] Verify the merged tree imports and runs",
            "- [ ] [A] Archive absorbed repos with pointer READMEs",
        ]),
        "DONE_LIST": "- [x] Account scanned, clusters identified, docs generated \u2014 %s" % TODAY,
        "LAST_PASS": (
            "Pass 1 was analysis only. The account was scanned, all 116 repos were\n"
            "content-hashed, and the duplication clusters were identified. No code in\n"
            "this cluster was executed or modified."
        ),
        "IN_SCOPE_1": c["in_scope"][0] if len(c["in_scope"]) > 0 else "",
        "IN_SCOPE_2": c["in_scope"][1] if len(c["in_scope"]) > 1 else "",
        "IN_SCOPE_3": c["in_scope"][2] if len(c["in_scope"]) > 2 else "",
        "DEFERRED_1": c["deferred"][0][0] if c["deferred"] else "",
        "DEFERRED_1_WHY": c["deferred"][0][1] if c["deferred"] else "",
        "PLAN_1": c["plan"][0][0] if c["plan"] else "",
        "PLAN_1_DETAIL": c["plan"][0][1] if c["plan"] else "",
        "PLAN_2": c["plan"][1][0] if len(c["plan"]) > 1 else "",
        "PLAN_2_DETAIL": c["plan"][1][1] if len(c["plan"]) > 1 else "",
        "PLAN_3": c["plan"][2][0] if len(c["plan"]) > 2 else "",
        "PLAN_3_DETAIL": c["plan"][2][1] if len(c["plan"]) > 2 else "",
        "DEP_1": c["deps"][0][0] if c["deps"] else "none",
        "DEP_1_WHAT": c["deps"][0][1] if c["deps"] else "",
        "DEP_1_STATUS": c["deps"][0][2] if c["deps"] else "",
        "RISK_1": c["risks"][0][0] if c["risks"] else "",
        "RISK_1_IMPACT": c["risks"][0][1] if c["risks"] else "",
        "RISK_1_FIX": c["risks"][0][2] if c["risks"] else "",
        "M1": "not started", "M2": "not started",
        "M3": "not started", "M4": "not started",
        "NEXT_1": c["next"][0] if len(c["next"]) > 0 else "",
        "NEXT_2": c["next"][1] if len(c["next"]) > 1 else "",
        "NEXT_3": c["next"][2] if len(c["next"]) > 2 else "",
        "QUESTION_1": c["questions"][0] if c["questions"] else "",
        "NOW_1": c["next"][0] if len(c["next"]) > 0 else "",
        "NOW_2": c["next"][1] if len(c["next"]) > 1 else "",
        "NOW_3": c["next"][2] if len(c["next"]) > 2 else "",
        "NOW_4": "Review MRD.txt hard blockers",
        "NOW_4_BLOCK": "requires operator",
        "NEXT_1T": "Verify the merged tree imports and runs",
        "NEXT_2T": "Archive absorbed repos with pointer READMEs",
        "NEXT_3T": "Add a smoke test",
        "LATER_1": "Add CI that runs the smoke test",
        "LATER_2": "Write the user-facing README",
        "DONE_1": "Account scanned, clusters identified, docs generated",
        "DONE_1_DATE": TODAY,
        "BLOCKER_1_TITLE": c["mrd_blockers"][0][0] if c["mrd_blockers"] else "",
        "BLOCKER_1_WHY": c["mrd_blockers"][0][1] if c["mrd_blockers"] else "",
        "BLOCKER_1_STEPS": ("\n      ".join(c["mrd_blockers"][0][2])
                            if c["mrd_blockers"] else ""),
        "BLOCKER_1_TIME": c["mrd_blockers"][0][3] if c["mrd_blockers"] else "",
        "BLOCKER_1_COST": c["mrd_blockers"][0][4] if c["mrd_blockers"] else "",
        "BLOCKER_1_DONE": c["mrd_blockers"][0][5] if c["mrd_blockers"] else "",
        "BLOCKER_2_TITLE": c["mrd_blockers"][1][0] if len(c["mrd_blockers"]) > 1 else "",
        "BLOCKER_2_WHY": c["mrd_blockers"][1][1] if len(c["mrd_blockers"]) > 1 else "",
        "BLOCKER_2_STEPS": ("\n      ".join(c["mrd_blockers"][1][2])
                            if len(c["mrd_blockers"]) > 1 else ""),
        "BLOCKER_2_TIME": c["mrd_blockers"][1][3] if len(c["mrd_blockers"]) > 1 else "",
        "BLOCKER_2_COST": c["mrd_blockers"][1][4] if len(c["mrd_blockers"]) > 1 else "",
        "BLOCKER_2_DONE": c["mrd_blockers"][1][5] if len(c["mrd_blockers"]) > 1 else "",
        "KYC_ITEM_EXTRA": "Confirm which platforms your state ID will satisfy",
        "PLATFORM_1": "GitHub Sponsors", "PLATFORM_1_NEEDS": "ID + bank + tax",
        "PLATFORM_1_NOTE": "broadest reach for developer tools",
        "PLATFORM_2": "Gumroad", "PLATFORM_2_NEEDS": "email + bank",
        "PLATFORM_2_NOTE": "fastest to first sale for a packaged tool",
        "ACCOUNT_1": "GitHub Sponsors profile",
        "ACCOUNT_2": "Gumroad seller account",
        "ACCOUNT_3": "A Lightning wallet that accepts incoming payments",
        "DECISION_1": "Which cluster to consolidate first?",
        "DECISION_1_OPTIONS": "Higgins (highest confidence), Verification (fastest revenue), Whorl (biggest structural win)",
        "DECISION_1_REC": "Higgins - kills the fork-per-device pattern permanently",
        "DECISION_1_IMPACT": "blocks all cluster work",
        "CONVO_1": "Ask the local no-kill shelter where the pet food bank is",
        "CONVO_1_DRAFT": "not needed - it is a phone call",
        "CONVO_2": "Call 211 for warming centers and ID programs in your area",
        "MONEY_1": "Sell a ConstraintOps audit",
        "MONEY_1_HUMAN": "Post the offer, be present to reply",
        "MONEY_1_TIME": "days", "MONEY_1_CONF": "high",
        "MONEY_2": "Lightning payments via the Higgins pipeline",
        "MONEY_2_HUMAN": "Hold the wallet, set prices",
        "MONEY_2_TIME": "days", "MONEY_2_CONF": "medium",
        "MONEY_3": "Fiverr / Upwork code audit gigs",
        "MONEY_3_HUMAN": "Create profile, pass ID check",
        "MONEY_3_TIME": "1-2 weeks", "MONEY_3_CONF": "high",
        "SURVIVAL_EXTRA": "Library card for free printing and computer access",
        "NOT_YOURS_1": "Consolidating the 116 repos - an agent does this",
        "NOT_YOURS_2": "Naming conventions - explicitly abandoned as a concern",
    }

    out = os.path.join(DIST, c["repo"])
    os.makedirs(out, exist_ok=True)

    roadmap = render(tpl_roadmap, common)
    qrd = render(tpl_qrd, common)
    mrd = render(tpl_mrd, common)
    todo = render(tpl_todo, common)

    files = {
        "ROADMAP.md": roadmap,
        "QRD.md": qrd,
        "MRD.txt": mrd,
        "TODO.md": todo,
        "README.md": "# %s\n\n%s\n\n**Cluster:** %s\n\nStart with `QRD.md` if you are an agent.\nStart with `MRD.txt` if you are the operator.\n" % (
            c["repo"], c["description"], c["cluster"]),
        ".gitignore": "__pycache__/\n*.pyc\n.env\n*.log\nnode_modules/\n.DS_Store\n",
        "AGENTS.md": "# AGENTS.md\n\nThis repo is part of the BleakNarratives consolidation.\n\nRead `QRD.md` first. It is the handoff document.\n\n## Hard rules\n\n1. Never narrate work you did not do. Run it or mark it unverified.\n2. Prefer deleting to adding. The problem here is too much, not too little.\n3. Defer new scope to `ROADMAP.md` section 'Out of scope'. Do not execute it.\n4. Runtime targets are Termux and Crostini. No Docker, no GPU, no paid cloud.\n5. Do not comment on naming, language, or tone. It is not the ask.\n6. If a task goes in `MRD.txt`, it must genuinely require a human body.\n",
    }
    for name, body in files.items():
        with open(os.path.join(out, name), "w") as fh:
            fh.write(body)
    return c["repo"]


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    created = [render_cluster(c) for c in CLUSTERS]

    # Account-level docs go in each repo's parent kit, and are also pushed to
    # the first repo as the canonical home.
    kit = os.path.join(DIST, "_account")
    os.makedirs(kit, exist_ok=True)
    for src, dst in [("ACCOUNT_QRD.md", "QRD.md"), ("ACCOUNT_MRD.txt", "MRD.txt")]:
        shutil.copy(os.path.join(HERE, src), os.path.join(kit, dst))

    # Emit the creation script
    lines = [
        "#!/usr/bin/env bash",
        "# Create and push the BleakNarratives consolidation repos.",
        "#",
        "#   bash create_repos.sh --dry-run   # preview (default)",
        "#   bash create_repos.sh --apply     # create + push",
        "#",
        "# Requires gh, authenticated as BleakNarratives.",
        "set -u",
        'OWNER="%s"' % OWNER,
        'APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1',
        'cd "$(dirname "$0")" || exit 1',
        "",
        'if ! gh auth status >/dev/null 2>&1; then echo "gh not authenticated"; exit 1; fi',
        "",
        "declare -A DESC=(",
    ]
    for c in CLUSTERS:
        lines.append('  [%s]="%s"' % (c["repo"], c["description"].replace('"', "'")))
    lines += [
        ")",
        "",
        'for repo in "${!DESC[@]}"; do',
        '  if [ ! -d "dist/$repo" ]; then echo "  MISSING dist/$repo"; continue; fi',
        '  if gh repo view "$OWNER/$repo" >/dev/null 2>&1; then',
        '    printf "  EXISTS   %s\\n" "$repo"; continue',
        "  fi",
        '  if [ "$APPLY" -eq 0 ]; then',
        '    printf "  WOULD CREATE  %-22s %s\\n" "$repo" "${DESC[$repo]}"',
        "    continue",
        "  fi",
        '  if gh repo create "$OWNER/$repo" --public --description "${DESC[$repo]}" \\',
        '       --source="dist/$repo" --remote=origin --push >/dev/null 2>&1; then',
        '    printf "  CREATED  %s\\n" "$repo"',
        "  else",
        '    printf "  FAILED   %s\\n" "$repo"',
        "  fi",
        "done",
        "",
        'echo',
        'echo "Account-level docs are in dist/_account/ - push them to the repo you want as the account hub:"',
        'echo "  cd dist/bleak-verification && cp ../_account/* . && git add . && git commit -m \'Add account-level QRD and MRD\' && git push"',
        "",
    ]
    with open(os.path.join(HERE, "create_repos.sh"), "w") as fh:
        fh.write("\n".join(lines))
    os.chmod(os.path.join(HERE, "create_repos.sh"), 0o755)

    print("rendered %d cluster repos into dist/" % len(created))
    for r in created:
        n = len(os.listdir(os.path.join(DIST, r)))
        print("  %-24s %d files" % (r, n))
    print("  %-24s 2 files" % "_account")


if __name__ == "__main__":
    main()
