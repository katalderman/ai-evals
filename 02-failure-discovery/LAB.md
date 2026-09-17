<!--
LAB SPEC — machine-readable. This is the coding-agent version of the Module 2 labs (Failure Audit +
Failure Taxonomy Canvas). Same steps, same deliverables, same checkpoints — written so a coding harness
(Cursor, Claude Code, Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk the learner through both
M2 labs. If you are a human, you can read it top to bottom.
-->

# M2 Lab — Failure Audit + Taxonomy (assistant runbook)

**Deliverables:** `02-failure-discovery/audit-log.md` · `02-failure-discovery/failure-taxonomy.md`
**Builds on:** `01-evaluation-strategy/strategy-canvas.md` (severity is anchored to those trust metrics)
**Time:** ~30 min · **Required:** score all 20 rows and confirm failures with human overrides

---

## AGENT INSTRUCTIONS — read this first

You are helping a learner **complete this lab, not do it for them.** The tags, overrides, and
prioritization are theirs. Follow these rules:

1. **Go one step at a time.** Do not jump ahead or fill later sections.
2. **At every `🚦 DECISION` gate, STOP and ask the learner.** If they rubber-stamp every judge score,
   push back: the human-override step is the point.
3. **Never invent their reasoning.** Offer 2–3 options + a recommendation; the learner picks and says why.
4. **When a step says `✍️ WRITE`, update the named file** and show the diff.
5. **When a step says `▶️ RUN`, the judge runs in LangSmith/promptfoo** — give exact steps, then have the
   learner paste back the scored rows. **Match rows by the `query` text, not the row number** (LangSmith
   reorders on upload).
6. **At each `✅ CHECKPOINT`, summarise and confirm before continuing.**

> **Works with any assistant.** If your assistant can edit files in your repo, have it **write to the
> deliverable files and commit**. If it can't (e.g. plain ChatGPT), it **prints the finished markdown**
> and you paste it in, then commit. The **Failure Audit Walkthrough** and **Failure Taxonomy Canvas**
> tools from the Module 2 resources still work if the learner prefers to click.

Data: the 20-row **Ascend IQ** dataset (`Modules/M2 - Ascend IQ Sample Data.csv`: `query`, `prediction`,
`reference`).

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their forked `ai-evals` repo is open; `strategy-canvas.md` (M1) exists.
- [ ] They have the 20-row dataset and their LangSmith/promptfoo judge from M1.
- [ ] `audit-log.md` and `failure-taxonomy.md` exist (create from the template shape if not).

---

## LAB 1 — Failure Audit

### Step 1 — Score all 20 rows  (~7 min)

▶️ **RUN the judge** over all 20 rows (LangSmith or promptfoo): each row gets `1` = PASS / `0` = FAIL.
Have the learner paste the scored rows back, matched **by query text**.

✅ **CHECKPOINT:** all 20 rows have a judge score.

### Step 2 — Human overrides + tags  (~7 min)

🚦 **DECISION — the override rule.** For every row the judge failed for a **refusal**, check the query:
refusing a private/legal/unauthorized request means the guardrail worked → override to **1 (PASS)** and
note it. A refusal of a genuinely safe, answerable query stays **0 (FAIL)**.

🚦 **DECISION — tag each confirmed failure** with one Trust Metric: `#HALLUCINATION`, `#UX_TRUST`,
`#ROBUSTNESS`, or `#FAIRNESS`, plus a one-line reason.

✍️ **WRITE** → `audit-log.md`: the **audit rows** table, the **human overrides**, and the **one-line
summary** (total confirmed failures + count per tag). Commit.

✅ **CHECKPOINT:** every FAIL has an override decision (where relevant), a tag, and a reason; the summary
matches the table counts.

---

## LAB 2 — Failure Taxonomy

### Step 3 — Prioritize the Top 3  (~8 min)

🚦 **DECISION — rank the top 3 failures.** For each: failure type · trust tag · (optional) agentic mode ·
**Frequency** (≥3 of 20 = HIGH) · **Severity** (P0–P3, a strategic call about business cost) · business
impact. Anchor severity to the **M1 trust metrics**, not just how often it happens.

✍️ **WRITE** → `failure-taxonomy.md` **Top 3 Prioritized Failures** table.

✅ **CHECKPOINT:** three ranked failures with frequency + severity + impact.

### Step 4 — #1 business-impact statement + defense  (~4 min)

🚦 **DECISION — the #1 risk's business-impact statement** in leadership language:
*"This failure matters because [technical error] results in [business consequence]."* Name the concrete
cost (revenue, churn, legal, trust) — not the bug. Then defend the prioritization in 2–3 bullets.

✍️ **WRITE** → `failure-taxonomy.md` **#1 Risk · Business Impact** + **Defending the Prioritization**.
Commit + push both files.

✅ **CHECKPOINT:** the #1 risk has a leadership-language impact statement and a defended ranking.

---

## 💼 In practice

Auditing real outputs is where you find out what your feature *actually* does wrong, versus what you
feared. The human-override step is a career skill: it's how you stop an over-eager judge from "failing"
correct guardrail behavior and torching trust in your own metrics. The taxonomy turns a pile of failures
into a prioritized list an eng team can act on — and the P0 business-impact statement is the sentence
that gets a fix funded. "Here are our top 3 failure modes, ranked by business cost" is exactly what
leadership wants from a PM.

---

## Done-check (verify before saying "complete")

- [ ] `audit-log.md`: all 20 rows scored, refusal overrides applied, each confirmed FAIL tagged + reasoned, summary matches counts.
- [ ] `failure-taxonomy.md`: Top 3 ranked with frequency + severity + impact, a #1 business-impact statement, and a 2–3 bullet defense.
- [ ] Severity is anchored to the M1 trust metrics; reasoning is the learner's; both files committed and pushed.

**Debrief (post in `#ai-evals-cohort`):** your #1 failure mode and the one-sentence business cost that
makes it a P0.

**Next:** Module 3 — Eval Suites: build and run the 3-layer suite, trajectory eval, and eval spec.

*Product School · AI Evals · M2 Lab (assistant runbook)*
