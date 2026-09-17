<!--
LAB SPEC — machine-readable. This is the coding-agent version of the Module 4 labs (Eval Gate Map, CI
Gate Demo, Launch Strategy). Same steps, same deliverables, same checkpoints — written so a coding
harness (Cursor, Claude Code, Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk the learner through
the M4 labs. If you are a human, you can read it top to bottom.
-->

# M4 Lab — Eval Gates: Gate Map + CI Policy + Launch Strategy (assistant runbook)

**Deliverables:** `04-eval-gates/lab-1-gate-map.md` · `lab-ci-gate-policy.md` · `lab-2-launch-strategy.md`
**Builds on:** your M2 failures + M3 eval specs (each gate enforces an eval you already wrote)
**Time:** ~30 min · **Required:** end with **≥1 Hard, ≥1 Soft, ≥1 Advisory** gate and a defended merge call

---

## AGENT INSTRUCTIONS — read this first

You are helping a learner **complete this lab, not do it for them.** The placements, floors, and the
merge decision are theirs. Follow these rules:

1. **Go one step at a time.** Do not jump ahead or fill later sections.
2. **At every `🚦 DECISION` gate, STOP and ask the learner.** If they make everything a Hard gate, push
   back: over-gating blocks every release; under-gating ships the P0.
3. **Never invent their reasoning.** Offer 2–3 options + a recommendation; the learner picks and says why.
4. **When a step says `✍️ WRITE`, update the named file** and show the diff.
5. **At each `✅ CHECKPOINT`, summarise and confirm before continuing.**

> **Works with any assistant.** If your assistant can edit files in your repo, have it **write to the
> deliverable files and commit**. If it can't (e.g. plain ChatGPT), it **prints the finished markdown**
> and you paste it in, then commit. The **Eval Gate Mapping Tool**, **CI Gate Demo**, and **Launch
> Strategy Builder** from the Module 4 resources still work if the learner prefers to click.

Rule to enforce throughout: **CI policy is per-dimension — never one blended "quality" number** — and CI
uses **deterministic fixtures/replay**, not live model calls. Don't gate correct behavior (e.g. a correct
legal refusal).

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their forked `ai-evals` repo is open; M2 failures + M3 eval specs exist.
- [ ] `lab-1-gate-map.md`, `lab-ci-gate-policy.md`, `lab-2-launch-strategy.md` exist (create from template shape if not).

---

## LAB 1 — Eval Gate Map

### Step 1 — Place each failure on severity × pipeline stage  (~8 min)

For the verified failures (exclude any correct-behavior row), 🚦 **DECISION — per failure:** severity
(**Advisory / Soft / Hard**) × placement (**PR / Staging / Release**) + a one-line rationale. Require
**at least one of each severity**.

✍️ **WRITE** → `lab-1-gate-map.md`: the Gate Map table (+ the sample-interaction references). Commit.

✅ **CHECKPOINT:** every failure placed with a rationale; ≥1 Hard, ≥1 Soft, ≥1 Advisory.

---

## LAB 2 — CI Gate Policy (PR #218 replay)

### Step 2 — Set floors + max-regression, then make the merge call  (~8 min)

Using the PR #218 replay (a 30-case regression golden set), 🚦 **DECISION — per dimension:** the **floor**,
the **max regression**, and whether it's **blocking** vs warn-only (faithfulness/task-completion/tool-
selection/safety typically blocking; latency/cost typically warn-only). Then read main vs PR deltas and
make the **merge call**.

✍️ **WRITE** → `lab-ci-gate-policy.md`: the dimension table (floors, max reg, blocking, result), the gate
result, and the merge decision with its reason. Commit.

✅ **CHECKPOINT:** a per-dimension policy + a BLOCK/PASS decision justified by a specific regression.

---

## LAB 3 — Launch Strategy (release criteria)

### Step 3 — Release criteria + CI policy + Soft-gate mitigation  (~8 min)

🚦 **DECISION — release criteria:** for Hard/Soft/Advisory, the metric, numeric threshold, dataset, and
method. Then restate the **CI gate policy** (per-dimension, ≥30-case golden set, deterministic replay).
Then the **Soft-gate mitigation lever** (staged rollout / feature flag / beta label / delay) + one
sentence on how it contains the risk while you ship.

✍️ **WRITE** → `lab-2-launch-strategy.md`: §4.0 Release Criteria, §4.1 CI Gate Policy, §4.2 Mitigation
Plan. Commit + push all three files.

✅ **CHECKPOINT:** numeric release criteria + a per-dimension CI policy + a named mitigation lever.

---

## 💼 In practice

Gates are where evals stop being a report and start being a control: they're the yes/no that actually
blocks a bad change from reaching users. The Hard/Soft/Advisory split is the political skill — it lets you
protect the P0 without becoming the PM who blocks every release over a latency blip. The per-dimension CI
policy is exactly what you hand an eng lead to wire into the pipeline, and "here's the floor, here's what
blocks a merge, here's the rollout lever if a soft gate slips" is a launch plan a director will sign.

---

## Done-check (verify before saying "complete")

- [ ] `lab-1-gate-map.md`: every verified failure placed on severity × stage, with ≥1 Hard/Soft/Advisory.
- [ ] `lab-ci-gate-policy.md`: per-dimension floors + max-regression + blocking flags and a justified merge call.
- [ ] `lab-2-launch-strategy.md`: numeric release criteria, a per-dimension CI policy, and a Soft-gate mitigation lever.
- [ ] Correct behavior isn't gated; policy is per-dimension (not blended); files committed and pushed.

**Debrief (post in `#ai-evals-cohort`):** the one dimension you made blocking and the regression size that
would flip your merge call.

**Next:** Module 5 — Scale: coverage matrix + eval budget across the portfolio.

*Product School · AI Evals · M4 Lab (assistant runbook)*
