# Prompt pack — what to say to your AI assistant

> **Prefer the guided path?** Each module folder has a **`LAB.md`** runbook. Paste it into
> your assistant (*"walk me through `03-eval-suites/LAB.md` one step at a time"*) and it runs
> the whole module for you — asking your decisions, telling you exactly what to run in
> LangSmith/promptfoo, and writing each deliverable file. This prompt pack is the
> **quick-reference / fallback**: the same prompts, if you'd rather drive each step by hand.

You build your eval system by **directing an AI assistant** (ChatGPT, Claude, Gemini, or a coding agent
like Cursor / Claude Code / Codex). You describe your product and your judgement calls in plain English;
the assistant drafts the artifacts and — if it can edit files in your fork — writes and commits them for
you. The eval *runs* (scoring rows, computing κ, replaying regressions) happen in **LangSmith** (free
Developer tier) or **promptfoo** (local fallback); the assistant tells you exactly what to click.

Two habits that make this work:
- **Own the judgement calls.** The trust metrics, the definition of "good", the severity ratings, the
  ship/hold call — these are yours. The assistant drafts; you decide.
- **Paste real numbers back.** After each eval run, paste the results in so the assistant writes the
  artifact from *your* data, not a guess.

---

## Setup (once)

> I'm taking Product School's AI Evals course. Open my forked `ai-evals` repo. Confirm the folder
> structure (`01-evaluation-strategy` … `06-culture`) and that each module folder has a `LAB.md`. I'll
> use LangSmith (free tier) to run evals and a model API key for the judge. Don't commit any keys.

---

## M1 — Evaluation strategy + first eval

> Walk me through `01-evaluation-strategy/LAB.md`. Help me pick 3 trust metrics tied to my product's user
> promise, draft two prompt versions, and set up a first LLM-as-a-Judge eval (judge from a *different*
> model family than the generator). Write `strategy-canvas.md` and `eval-harness-proof.md` as we go.

## M2 — Failure audit + taxonomy

> Walk me through `02-failure-discovery/LAB.md`. I'll paste the 20 scored rows from LangSmith (matched by
> query text). Help me apply the refusal human-override rule, tag each confirmed failure, and prioritize a
> Top 3 by frequency + severity. Write `audit-log.md` and `failure-taxonomy.md`.

## M3 — Eval suites

> Walk me through `03-eval-suites/LAB.md` using my P0 case from M2. Help me read the 3-layer suite result,
> grade the trajectory by path (not just the answer), and write the 5-part eval spec with a numeric
> threshold and three audience messages. Write the four M3 files.

## M4 — Eval gates

> Walk me through `04-eval-gates/LAB.md`. Help me place each failure on severity × pipeline stage (≥1
> Hard/Soft/Advisory), set per-dimension floors + max-regression for the PR #218 replay, make the merge
> call, and write the release criteria. Keep CI policy per-dimension, never one blended number.

## M5 — Scale

> Walk me through `05-scale/LAB.md`. Force at least 2 ❌ gaps in my coverage matrix, and hold me to the
> $200K cap with max 3 Level-3 slots in the budget grid. Write `lab-1-coverage-matrix.md` and
> `lab-2-budget-crisis.md` with a defensible fallback for every non-L3 item.

## M6 — Culture (capstone)

> Walk me through `06-culture/LAB.md`. Help me write the Ship/Hold memo with the recommendation in the
> first sentence and real numbers from M2–M5, then assemble the final pitch deck from my repo. Be honest
> about any gate that isn't met.

---

## Handy follow-ups (any module)

- *"Show me what you changed and why."*
- *"That metric is too generic — tie it to my user promise."*
- *"Give me 2–3 options and a recommendation, then let me choose."*
- *"Now commit the file with a clear message."*
