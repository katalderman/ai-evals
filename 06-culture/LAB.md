<!--
LAB SPEC — machine-readable. This is the coding-agent version of the Module 6 lab guides + the
Ship/Hold Memo Builder and Final Pitch Prompt Generator tools. Same steps, same deliverables, same
checkpoints — written so a coding harness (Cursor, Claude Code, Codex) OR a chatbot (ChatGPT, Claude,
Gemini) can walk the learner through the capstone. If you are a human, you can read it top to bottom.
-->

# M6 Lab — Culture: Ship/Hold Memo + Final Pitch (assistant runbook)  ·  CAPSTONE

**Deliverables:** `06-culture/lab-1-ship-hold-memo.md` · `06-culture/lab-2-final-pitch.html` (generated deck)
**Builds on:** every prior artifact (M1 strategy → M5 scale) — this is where they come together
**Time:** ~30 min · **Required:** the memo cites **real numbers from M2–M5**; the recommendation comes **first**

---

## AGENT INSTRUCTIONS — read this first

You are helping a learner **assemble their capstone, not write it for them.** The recommendation and the
numbers are theirs. Follow these rules:

1. **Go one step at a time.** Do not jump ahead or fill later sections.
2. **At every `🚦 DECISION` gate, STOP and ask the learner.** If the memo buries the recommendation or
   cites vibes instead of numbers, push back once.
3. **Never invent their reasoning or their metrics.** Pull numbers from *their* M2–M5 files; if a number
   is missing, ask — don't fabricate one.
4. **When a step says `✍️ WRITE`, update the named file** and show the diff.
5. **At each `✅ CHECKPOINT`, summarise and confirm before continuing.**
6. **Honesty rule:** if the gates aren't met, the memo says HOLD (or SHIP-with-conditions) — don't
   let the deck overstate the result.

> **Works with any assistant.** If your assistant can edit files in your repo, have it **write the files
> and commit**. If it can't (e.g. plain ChatGPT), it **prints each finished block** and you paste it in,
> then commit. The **Ship/Hold Memo Builder** and **Final Pitch Prompt Generator** from the Module 6
> resources still work if the learner prefers to click.

Scenario: PM at **Ascend Analytics** deciding whether to ship **Ascend IQ**. Reuse the same case
throughout — the memo is the culmination of every prior module.

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their forked `ai-evals` repo is open in this assistant.
- [ ] Prior artifacts exist: `01-evaluation-strategy/`, `02-failure-discovery/`, `03-eval-suites/`,
      `04-eval-gates/`, `05-scale/` — the memo cites numbers from these.
- [ ] `06-culture/lab-1-ship-hold-memo.md` exists (create from the template shape if not).

---

## Step 1 — Make the call (Pyramid Principle: answer first)  (~5 min)

🚦 **DECISION — SHIP or HOLD?** Get the recommendation **and** the one-sentence business reason. This is
the first line of the memo — it does not get buried. Fill the To/From header too.

✍️ **WRITE** → `lab-1-ship-hold-memo.md`: the **Decision** line + **The Answer** (first sentence = the
recommendation + business reason).

✅ **CHECKPOINT:** the recommendation is unmistakable in the first sentence.

---

## Step 2 — Three argument pillars  (~6 min)

🚦 **DECISION — the three pillars** that support the call. Each is a titled argument, not a data dump.
Guide them to distinct angles (e.g. user trust, business risk, eval readiness) — not three versions of
the same point.

✍️ **WRITE** → `lab-1-ship-hold-memo.md` **The Arguments** (1, 2, 3).

✅ **CHECKPOINT:** three distinct, titled pillars, each a clear claim.

---

## Step 3 — Evidence from real numbers  (~6 min)

🚦 **DECISION — the evidence block.** Pull **exact numbers from M2–M5**: hallucination rate vs its gate,
factual-grounding %, bias coverage %, p95 latency, etc. Each line: `Metric: result (Gate: bar)
PASS/FAIL · Source`. If a number is missing, ask the learner to fetch it from the relevant file — do not
invent it.

✍️ **WRITE** → `lab-1-ship-hold-memo.md` **Evidence · Trust Metrics**.

✅ **CHECKPOINT:** every claim in Step 2 is backed by a cited number with a PASS/FAIL against its gate.

---

## Step 4 — Business risk, the ask, and the reflection  (~5 min)

1. 🚦 **DECISION — business risk.** Quantify the SHIP-path vs HOLD-path risk (revenue, churn,
   competitive window).
2. 🚦 **DECISION — next step / decision needed.** A specific request **with a deadline** (e.g. "Approve
   the Hold rollback by Friday to keep the Q3 window.").
3. ✍️ **WRITE** → the **Reflection**: what defining "good enough" forced them to confront.

✍️ **WRITE** → `lab-1-ship-hold-memo.md` **Business Risk**, **Next Step**, **Reflection**. Commit.

✅ **CHECKPOINT:** the memo is a complete, exec-ready decision doc citing real numbers.

---

## Step 5 — Generate the final pitch deck + submit  (~8 min)

1. Open the **Final Pitch Prompt Generator** (ships with the course) — or ask this assistant to
   assemble the deck from your repo files. Feed it: the Strategy Canvas (M1), failure taxonomy (M2),
   eval suite results (M3), gate/launch strategy (M4), coverage + budget (M5), and the Ship/Hold memo.
2. Produce the shareable **`06-culture/lab-2-final-pitch.html`** deck. (A tool like Gamma also works —
   the repo file is the submission of record.)
3. **Stranger-test (optional but recommended):** paste the deck's content + a skeptical-exec review
   prompt into ChatGPT / Claude / Gemini; fix anything generic or unsupported before submitting.
4. ▶️ **Commit + push** the memo and the generated deck.

✅ **DONE when:** the memo is complete and cites real numbers, the pitch deck is generated, and both are
committed and pushed.

---

## 💼 In practice

The Ship/Hold memo *is* the job. Everything in the course — the strategy canvas, the failure taxonomy,
the eval suite, the gates — exists to let you write these five paragraphs with a straight face: here's
the call, here's why, here are the numbers, here's the risk, here's what I need from you. PMs who can put
the recommendation in the first sentence and back it with gate-referenced evidence are the ones execs
trust with the next launch decision. The deck is how you get the room aligned in ten minutes.

---

## Done-check (verify before saying "complete")

- [ ] `lab-1-ship-hold-memo.md`: recommendation in the **first sentence**, 3 distinct pillars, an
      evidence block with **real M2–M5 numbers** (result vs gate, PASS/FAIL, source), quantified
      business risk, a dated decision request, and a reflection.
- [ ] `lab-2-final-pitch.html` is generated from the repo artifacts and is honest about the gates.
- [ ] Reasoning + numbers are the learner's (nothing fabricated); both files committed and pushed.

**Debrief (post in `#ai-evals-cohort`):** your SHIP/HOLD call in one line + the single number that
decided it.

**Submit** your repo URL (and the deck) to the learning platform within 7 days of your cohort ending.

*Product School · AI Evals · M6 Capstone Lab (assistant runbook)*
