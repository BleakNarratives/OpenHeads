# Handoff — Generic (any agent, any CLI)

Use this when the tool is not listed, or when you are unsure. It works for any
agent that can read files and run shell commands.

---

## The universal kickdown

Paste this into any agent at the start of a session:

```
Read ~/OpenHeads/SESSION_CONTEXT.md first. It is the handshake.

Then read the QRD for whichever repo you are working in:
  ~/OpenHeads/bootstrap/dist/<repo>/QRD.md

If you do not know which repo, run: ls ~/OpenHeads/bootstrap/dist

Rules that apply to everything you do here:
1. Never narrate work you did not do. Run it, or mark it unverified.
2. Prefer deleting to adding. The problem here is too much, not too little.
3. Defer new scope to ROADMAP.md section "Out of scope". Do not execute it.
4. Runtime targets are Termux and Crostini. No Docker, no GPU, no paid cloud.
5. Do not comment on naming, language, or tone.
6. If a task goes in MRD.txt, it must genuinely require a human body.

Then pick the top unfinished item from that repo's TODO.md and do it end to end.
Do not re-summarize the situation. Do not propose a plan. Do not ask which one
to start. Just do the next thing and report what actually happened.
```

---

## The four repo kits, and what each is for

| Repo | Cluster | The job |
|---|---|---|
| `bleak-higgins` | Mrs-Higgins pipeline | Merge 4 device-forked repos into one. Fastest path to a real revenue loop (Lightning needs no KYC). |
| `bleak-verification` | Verification | Merge tribunal + ConstraintOps + guards. Most immediately sellable. |
| `bleak-whorl` | Swarm core | Merge 6 swarm repos into one modular core. Biggest structural win. |
| `bleak-ui-kit` | React scaffolds | Replace 17 scaffold clones with one shared starter. |
| `bleak-tools` | Operator toolbelt | Absorb 8 tiny tool repos into one indexed toolbelt. |
| `bleak-outclaw` | Legal toolkit | Consolidate the 305-file legal AI toolkit. |
| `bleak-vertical-ai` | Vertical AI | Merge 6 repos sharing one product name. |

---

## If the agent has no file access

Some tools are chat-only. In that case, paste `SESSION_CONTEXT.md` directly into
the conversation, then the relevant QRD. Both are written to stand alone.

You can print them with:

```bash
oh                 # the context block
oh qrd bleak-whorl # a repo's handoff
```

---

## Escalation rule

If an agent hits something that needs a human — a signup, a payment, an account,
a legal decision, a judgment call about whether output is good — it should write
the item into that repo's `MRD.txt` with exact steps, and stop. Do not guess.
Do not work around it. The MRD is the channel for "this needs the operator."

An agent that invents a workaround for a human-only blocker is creating a second
problem, not solving the first.
