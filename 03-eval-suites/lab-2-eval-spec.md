# M3 · Lab 2 · Eval Spec, Ascend IQ P0

> Repo file `ai-evals/03-eval-suites/lab-2-eval-spec.md`. The PM's contract for what "good" means and how it's enforced.
>
> P0 carried from M2: **Stale Retrieval**, taxonomy rank #1 (audit row 1). Ascend IQ quoted a cached **$49/user/month** when the current price is **$59/mo**. Suite evidence: [`lab-1-eval-suite.md`](./lab-1-eval-suite.md), where only the Layer 3 judge caught the stale price.

## Part 1 · The 5-Part Eval Spec

| Question | Answer |
|---|---|
| **01 · Target Risk** | Ascend IQ quotes a superseded price as current (e.g. $49 when the current list price is $59), served from a stale pricing-page cache. |
| Risk Type | **Output.** The stale pricing defect manifests directly in the generated customer response, matching our M2 finding that this is a retrieval and caching defect rather than an agentic tool misuse problem. |
| Trust Metric | **Hallucination** (M1 Source Traceability). |
| **02 · Evaluator** | **Hybrid** (Layer 1 code rule + Layer 3 LLM-as-Judge fallback). |
| Detection logic | A deterministic Layer 1 code rule instantly and cheaply verifies the extracted dollar value against current database pricing (the pricing system of record), while the Layer 3 LLM Judge acts as a semantic fallback when source documents lack explicit version tags. Relying on a live pricing database establishes a robust, future-proof contract with Engineering that guarantees stale cache entries are caught even when retrieved documents lack version labels. |
| **03 · Threshold** | **100% current-price accuracy on the pricing gold set; zero stale prices allowed.** |
| Strategy | **Safety First (max TPR).** Our strategy canvas established that traceability wins absolutely on pricing, and quoting an outdated rate creates binding commercial disputes with enterprise clients. |
| **04 · Business Stakes** | Systematically underquoting pricing across our top 50 enterprise accounts ($50K+ ARR) forces either unbudgeted 17% margin discounts or mid-renewal contract disputes that trigger immediate enterprise churn. The failure is deterministic: every pricing query hits the same stale cache until the TTL is fixed. |
| **05 · Owner** | **Joint ownership.** The Retrieval / Platform Engineering Lead owns the gate implementation and cache TTL remediation; I, as Group PM, own the threshold and release sign-off. |

## Part 2 · Three Audience Messages

### A. For Engineering (Jira ticket)

**Stale-price gate for Ascend IQ pricing answers (P0)** · Owner: Retrieval / Platform Engineering Lead · Dependency: read access to the pricing system of record.

> **GIVEN** a query classified as pricing (price, plan, tier, cost, seats)
> **WHEN** Ascend IQ's answer contains a dollar figure
> **THEN** that figure must equal the current list price in the pricing system of record, and any mismatch **blocks** the answer before the user sees it and serves the fallback (B).
>
> **AND GIVEN** the retrieved source has no version or date marker, **THEN** the answer routes to the Layer 3 judge, and a judge FAIL blocks it.
>
> **Done when:** 100% of pricing gold-set cases quote the current price, with 0 stale prices, and the cache TTL fix has shipped.

**Block-and-fallback, not flag-and-send.** A Safety First strategy demands hard-blocking mismatches to prevent legally binding enterprise pricing concessions before a client sees them.

### B. For UX / Design

**Cited handoff.** When the gate blocks an answer, the user sees:

> "Pricing for this plan was updated recently. Here is the current pricing page [link], or I can connect you with your account manager."

Providing a direct link to the live pricing page along with an account manager connection maintains a helpful customer journey, avoids flat dead-ends, and costs the user only a single frictionless follow-up. No flat refusal; a refusal here counts against the over-refusal guardrail metric from M1.

### C. For Leadership (bi-weekly update)

- **Risk avoided:** stale price quotes to the top 50 enterprise accounts ($50K+ ARR each), each one a potential 17% discount concession or renewal dispute. **Coverage:** 100% of pricing queries gated by a deterministic check, with the judge as backstop. **Tracking:** stale-price rate (target 0), pricing-query block rate, and cache TTL fix status.
