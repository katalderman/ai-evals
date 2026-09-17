<!--
LAB SPEC — machine-readable. This is the coding-agent version of the Module 5 lab guides + the
Coverage Matrix and Budget Crisis interactive tools. Same steps, same deliverables, same checkpoints —
written so a coding harness (Cursor, Claude Code, Codex) OR a chatbot (ChatGPT, Claude, Gemini) can
walk the learner through both M5 labs. If you are a human, you can read it top to bottom.
-->

# M5 Lab — Scale: Coverage Matrix + Budget Crisis (assistant runbook)

**Deliverables:** `05-scale/lab-1-coverage-matrix.md` · `05-scale/lab-2-budget-crisis.md`
**Builds on:** your M2 failure taxonomy + M1 trust metrics (have them open)
**Time:** ~25 min · **Required:** the matrix must show **≥2 ❌ gaps**; the budget must respect the **$200K cap** with **max 3 Level-3 slots**

---

## AGENT INSTRUCTIONS — read this first

You are helping a learner **complete this lab, not do it for them.** The judgement calls — which gaps to
accept, where to spend — are theirs. Follow these rules:

1. **Go one step at a time.** Do not jump ahead or fill later sections.
2. **At every `🚦 DECISION` gate, STOP and ask the learner.** If they mark everything ✅ or spread the
   budget evenly, push back once: force a real gap and a real trade-off.
3. **Never invent their reasoning.** Offer 2–3 options + a recommendation; the learner picks and says
   why. Record *their* words and numbers.
4. **When a step says `✍️ WRITE`, update the named file** and show the diff.
5. **At each `✅ CHECKPOINT`, summarise and confirm before continuing.**

> **Works with any assistant.** If your assistant can edit files in your repo, have it **write to the
> deliverable file and commit**. If it can't (e.g. plain ChatGPT), it **prints the finished markdown
> block** and you paste it into the file, then commit. Same deliverable either way.
>
> The interactive **Coverage Matrix Tool** and **Budget Crisis Tool** from the Module 5 resources still
> work if the learner prefers to click — they produce the same markdown. This runbook reaches the same
> deliverable by conversation.

This lab uses the **Ascend IQ / Ascend Analytics** scenario carried from earlier modules. Reuse the same
product and failure modes — don't invent new ones.

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their forked `ai-evals` repo is open in this assistant.
- [ ] They have their M2 failure modes / taxonomy and M1 trust metrics handy.
- [ ] `05-scale/lab-1-coverage-matrix.md` and `05-scale/lab-2-budget-crisis.md` exist (create from the
      template shape if not — don't fill fields yet).

---

## LAB 1 — Coverage Matrix

### Step 1 — Score the coverage row  (~5 min)

For the product, score each risk column **✅ / ⚠️ / ❌**: Hallucination · Bias · Latency · Toxicity ·
Drift Monitoring.

🚦 **DECISION — force honesty.** An all-green matrix isn't real. Require **at least 2 ❌** and make the
learner say why each cell is where it is (what's actually evaluated today vs. not).

✍️ **WRITE** → `lab-1-coverage-matrix.md` **Coverage row** (+ the product name).

✅ **CHECKPOINT:** the row has ≥2 ❌ and each rating has a one-line justification.

### Step 2 — Method + ground truth for two covered risks  (~4 min)

Pick two ✅/⚠️ cells. For each: **how you evaluate it** and **what you grade against** (the ground
truth).

✍️ **WRITE** → `lab-1-coverage-matrix.md` **Method + Ground Truth**.

✅ **CHECKPOINT:** two risks have a concrete method + a named ground-truth source.

### Step 3 — Accept one gap, mitigate another  (~4 min)

🚦 **DECISION — strategic acceptance.** Which ❌ are they *accepting* for now, and why is it acceptable
right now? Get the **kill criterion / date** that would change the call.

🚦 **DECISION — critical mitigation.** Which ❌ can they **not** accept? Get a concrete mitigation plan
with a **date/owner** — not "we'll add it later".

✍️ **WRITE** → `lab-1-coverage-matrix.md` **Strategic acceptance** + **Critical mitigation**. Commit.

✅ **CHECKPOINT:** one accepted gap (with kill criterion) + one critical gap (with dated plan).

---

## LAB 2 — Budget Crisis

### Step 4 — Allocate Level 1/2/3 under the cap  (~8 min)

Allocate coverage Level (L1/L2/L3) across the five failure modes under a **$200,000/quarter cap** with
**max 3 items at Level 3**.

Reference L3 costs: Hallucination $85K · Context $70K · Attribution $65K · Bias $55K · Latency $25K.
L2 ≈ 10% of L3, L1 ≈ 5% of L3.

🚦 **DECISION — the grid.** For each of the 5 failures (with its trust metric + risk rating), pick a
Level and cost. **Enforce the constraints:** total ≤ $200K and ≤ 3 L3 slots. If the learner blows the
cap, make them cut — that trade-off *is* the lab.

✍️ **WRITE** → `lab-2-budget-crisis.md` **Portfolio decision grid** + the total L3 spend / slots used.

✅ **CHECKPOINT:** the grid respects the cap and the 3-L3 limit, with a running total.

### Step 5 — Defend the fallbacks  (~4 min)

For every non-L3 item, name the **cheaper fallback method** you'll run instead, and — especially if you
downgraded a P0/P1 — the **story you could defend in a customer incident review**.

✍️ **WRITE** → `lab-2-budget-crisis.md` **Fallback methods**. Commit + push both files.

✅ **CHECKPOINT:** every non-L3 item has a defensible fallback.

---

## 💼 In practice

This is the conversation you have with Finance and your eng lead every quarter: you can't evaluate
everything to the max, so *where do you spend and what do you consciously not cover?* The coverage matrix
is how you show leadership the honest state of quality across a portfolio; the budget grid is how you
defend those choices when money is tight. "We accepted this gap on purpose, here's the kill criterion" is
a career-saving sentence in an incident review — far better than an all-green chart that was never true.

---

## Done-check (verify before saying "complete")

- [ ] `lab-1-coverage-matrix.md`: coverage row with **≥2 ❌**, two methods+ground-truth, one accepted gap (with kill criterion), one dated critical mitigation.
- [ ] `lab-2-budget-crisis.md`: grid within the **$200K cap** and **≤3 L3 slots**, running total, and a defensible fallback for every non-L3 item.
- [ ] Reasoning is in the learner's words; both files committed and pushed.

**Debrief (post in `#ai-evals-cohort`):** the one ❌ gap you accepted and the kill criterion that would
force you to close it.

**Next:** Module 6 — Culture: the Ship/Hold memo and your final pitch.

*Product School · AI Evals · M5 Lab (assistant runbook)*
