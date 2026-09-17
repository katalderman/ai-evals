# AI Evaluation Strategy Canvas

> Repo file `ai-evals/01-evaluation-strategy/strategy-canvas.md` (the repo is your submission).
> Becomes the **Strategy Canvas** slide of the final pitch deck you assemble in Module 6.

**Feature under evaluation:** Ascend IQ — the grounded, RAG-backed analytics copilot inside Ascend Analytics.

## 1. Product Strategy, The Context

- **Target user:** RevOps and Customer Success leads at mid-market SaaS companies. Business operators, not analysts — they own a number, but they can't write SQL and have no data team on call.
- **Key use case:** Ask a plain-language question about their account data ("why did Northeast usage drop last month?") or about Ascend's own product and pricing, and get a short, sourced answer they can act on or forward to a customer.
- **Value proposition:** An answer in 30 seconds instead of a three-day analyst ticket — and the user doesn't have to decide whether to trust it, because every claim cites where it came from.

## 2. Measurements, The Execution

- **User promise.** _For RevOps and CS leads who own a number but can't write SQL, Ascend IQ promises to answer in plain language with every claim traceable to its source — and to say "I don't know" rather than guess — so that they act on our analytics without a data team, and Ascend keeps the trust its renewals depend on._
- **Top 3 trust metrics:**
  - **Source Traceability**, every factual claim in an answer — number, date, account name, price — is supported by a retrieved chunk the user can open. *Signal:* decompose each answer into atomic claims; score **% of answers containing ≥ 1 unsupported claim**. Deliberately any-fail rather than an average, because one invented number poisons the whole answer for a user who can't check it.
  - **Calibrated Abstention**, when retrieval doesn't support an answer, Ascend IQ says so instead of filling the gap. *Signal:* on a held-out set of deliberately unanswerable queries, **% that abstain or ask a clarifying question rather than assert** — reported **paired with over-refusal rate on answerable queries**, or the metric is trivially gamed by a copilot that refuses everything.
  - **Decision Sufficiency**, the answer carries enough for the user to take the next action — the figure, its direction, its timeframe, and what changed — without a follow-up question or opening the dashboard themselves. *Signal:* a rater reading **only the answer** must recover (a) the next action and (b) the figure it rests on; score **% where both are recoverable**.
- **Why these three:** Each one buys a different business lever, and together they cover the promise end to end.
  - **Source Traceability** supports compliance, and that the output can be audited and traced back to its source.
  - **Calibrated Abstention** supports user retention and growth by preventing bad experiences.
  - **Decision Sufficiency** drives adoption by making the tool actionable.
  - **Deliberately not chosen: latency.** Trust trumps speed, so that's why I didn't choose latency.

## 3. Strategic Trade-Offs, The Cost

### Trade-off 1 · Source Traceability ↔ Decision Sufficiency

**We split this call by what a wrong answer costs.**

- **Pricing, contract, billing and legal questions — Traceability wins absolutely.** No claim ships without a citation, even where that makes the answer less satisfying. A cited non-answer costs the user one follow-up; an invented price costs a contract dispute. This is the compliance case: the output has to be auditable back to its source.
- **Internal trend and usage questions — Decision Sufficiency wins.** The copilot may synthesize across sources provided every underlying figure is cited. A hedge-stuffed answer here just sends the user back to the analyst queue, which is the exact failure the product exists to remove.

**Cost we accept:** two regimes means the eval suite has to classify the query first, and misrouting a pricing question into the permissive regime becomes its own failure mode to test for.

### Trade-off 2 · Calibrated Abstention ↔ Coverage (answer rate)

**We prioritize Abstention over Coverage.**

A missing answer costs one analyst ticket — the status quo we were already living with. A confident wrong answer costs the user's belief in every answer we have ever given them, including the correct ones. Retention turns on the second cost, not the first.

**Cost we accept:** a visibly lower answer rate, and early complaints that the copilot is unhelpful before it is tuned. We keep ourselves honest with the paired over-refusal metric — if refusals on *answerable* queries climb, that is a regression, not a win.

---
_Generated from the AI Evaluation Strategy Canvas, M1 lab tool, AI Evals Certification._
