<!--
LAB SPEC — machine-readable. This is the coding-agent version of the Module 3 labs (Eval Suite,
Trajectory Eval, Judge Calibration, Eval Spec). Same steps, same deliverables, same checkpoints —
written so a coding harness (Cursor, Claude Code, Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk
the learner through the M3 labs. If you are a human, you can read it top to bottom.
-->

# M3 Lab — Eval Suites: Suite + Trajectory + Spec (assistant runbook)

**Deliverables:** `03-eval-suites/lab-1-eval-suite.md` · `lab-1b-trajectory.md` · `lab-2-eval-spec.md` · (async) `lab-judge-calibration.md`
**Builds on:** the single **P0 failure** you tagged in the M2 audit (carry it through — don't invent a new one)
**Time:** ~35 min core (+ calibration async) · **Required:** run the 3-layer suite on your P0 case

---

## AGENT INSTRUCTIONS — read this first

You are helping a learner **complete this lab, not do it for them.** The rubric, thresholds, and the
"what I'd ship next" call are theirs. Follow these rules:

1. **Go one step at a time.** Do not jump ahead or fill later sections.
2. **At every `🚦 DECISION` gate, STOP and ask the learner.** If they mark a passing-looking trajectory
   PASS despite a skipped step, push back: grade the *path*, not the vibe.
3. **Never invent their reasoning.** Offer 2–3 options + a recommendation; the learner picks and says why.
4. **When a step says `✍️ WRITE`, update the named file** and show the diff.
5. **When a step says `▶️ RUN`, the suite runs in LangSmith/promptfoo** — give exact steps, then have the
   learner paste back the results.
6. **At each `✅ CHECKPOINT`, summarise and confirm before continuing.**

> **Works with any assistant.** If your assistant can edit files in your repo, have it **write to the
> deliverable files and commit**. If it can't (e.g. plain ChatGPT), it **prints the finished markdown**
> and you paste it in, then commit. The **Eval Suite Walkthrough**, **Trajectory Eval Lab**, **Judge
> Calibration**, and **Eval Spec Builder** tools from the Module 3 resources still work if the learner
> prefers to click.

Carry the **same P0 Ascend IQ case** from M2 through every lab here and into the M6 deck.

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their forked `ai-evals` repo is open; the M2 taxonomy + the P0 case are picked.
- [ ] LangSmith/promptfoo + judge are ready (from M1/M2).
- [ ] `lab-1-eval-suite.md`, `lab-1b-trajectory.md`, `lab-2-eval-spec.md`, `lab-judge-calibration.md` exist.

---

## LAB 1a — Runnable 3-layer eval suite

### Step 1 — Run the suite on your P0 case  (~8 min)

Restate the P0 case (query · prediction · reference) carried from M2. Then ▶️ **RUN** the three
evaluators on it: **Layer 1 · Code** (deterministic regex/keyword), **Layer 2 · Safety** (mandated-refusal
gate), **Layer 3 · Judge** (semantic LLM-as-Judge). Each returns `1` = caught / `0` = missed + reasoning.

🚦 **DECISION — read the result:** Layer 1/2 caught it → *the Win*; only Layer 3 → *the Insight*; nothing
caught it → *the Gap*. Which case is theirs, and why? Then the **single highest-leverage change** to ship
next (a Layer 1 rule, routing through Layer 2, or tightening the Layer 3 rubric).

✍️ **WRITE** → `lab-1-eval-suite.md`: P0 case, the 3-layer results table, the read, and "what I'd ship next". Commit.

✅ **CHECKPOINT:** the suite ran on the real P0 case with a defended read + one next change.

---

## LAB 1b — Trajectory eval

### Step 2 — Grade the path, not the answer  (~7 min)

Use the Ascend IQ usage-drop task. 🚦 **DECISION — matching mode** (default **unordered** — strict is
over-used). Score six dimensions **PASS/PARTIAL/FAIL**: tool selection · argument correctness · no
redundant/looping steps · recovery · plan coherence · task completion. Then the **verdict** (SHIP/HOLD) —
a plausible final answer does **not** excuse a failed path on a P0.

✍️ **WRITE** → `lab-1b-trajectory.md`: matching mode, score, dimension table, verdict. Commit.

✅ **CHECKPOINT:** six dimensions scored + a verdict that reflects the path.

---

## LAB 2 — Eval Spec

### Step 3 — The 5-part spec + three audience messages  (~10 min)

🚦 **DECISION — the 5-part spec** for the P0: (1) target risk + risk type (output/trajectory) + trust
metric; (2) evaluator type + detection logic; (3) **threshold** (a number, not a vibe) + strategy
(safety-first / growth-first / balanced); (4) business stakes; (5) owner. Add trajectory fields only if
risk type = trajectory.

🚦 **DECISION — three audience messages:** (A) Engineering — acceptance criteria in GIVEN/WHEN/THEN form;
(B) UX/Design — the fallback experience when the gate blocks; (C) Leadership — one ROI bullet (risk
avoided + coverage + what you're tracking).

✍️ **WRITE** → `lab-2-eval-spec.md`: the 5-part spec + the three messages. Commit + push.

✅ **CHECKPOINT:** the spec has a numeric threshold and an owner; all three audience messages are concrete.

---

## LAB (async) — Judge Calibration

### Step 4 — Calibrate to κ ≥ 0.60  (extra practice)

▶️ **RUN:** label the 12 grounding traces, compute **Cohen's κ**, and if κ < 0.60, diagnose the
disagreement (e.g. the judge rewards length, not grounding) and **revise the rubric** (add an explicit
rule + a one-shot fail example), then re-measure.

✍️ **WRITE** → `lab-judge-calibration.md`: κ, confusion matrix, diagnosis, rubric revision. Commit.

✅ **CHECKPOINT:** κ ≥ 0.60 (or a documented revision plan to get there).

---

## 💼 In practice

The 3-layer suite is the core mental model of the whole field: cheap deterministic checks first, a safety
gate next, an expensive judge only where semantics demand it — so you're not paying an LLM to check
things a regex could. Trajectory evals are what you reach for the moment your feature is an *agent* and a
right-looking answer can hide a broken path. The eval spec is the PM's actual deliverable: the contract
that tells Eng exactly what "good" means in GIVEN/WHEN/THEN, so quality stops being an argument and
becomes a test.

---

## Done-check (verify before saying "complete")

- [ ] `lab-1-eval-suite.md`: 3-layer results on the real P0 case + a defended read + one next change.
- [ ] `lab-1b-trajectory.md`: matching mode, six scored dimensions, a path-aware verdict.
- [ ] `lab-2-eval-spec.md`: 5-part spec with a numeric threshold + owner, and three concrete audience messages.
- [ ] `lab-judge-calibration.md`: κ computed with a diagnosis + rubric revision (async is fine).
- [ ] Same P0 carried throughout; reasoning is the learner's; all files committed and pushed.

**Debrief (post in `#ai-evals-cohort`):** which layer caught your P0 — and the one eval-spec threshold you
found hardest to set as a number.

**Next:** Module 4 — Eval Gates: where each eval runs in the pipeline and what blocks a merge.

*Product School · AI Evals · M3 Lab (assistant runbook)*
