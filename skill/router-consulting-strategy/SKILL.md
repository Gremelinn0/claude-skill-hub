---
name: router-consulting-strategy
description: >-
  Routes business and strategy questions through consulting-style problem solving: crisp framing,
  MECE structure, hypothesis-led analysis, explicit assumptions, real strategic options, economics,
  prioritization, scenario stress tests, and answer-first recommendations. Use for ambiguous business
  decisions, market or product strategy, investment choices, prioritization, business cases, or when
  the user wants the AI to reason more like a strategy consultant.
---

# Consulting Strategy Router

## Purpose

Turn an ambiguous business, product, or strategy question into a **structured, evidence-aware,
decision-ready recommendation**.

The goal is not to name frameworks. The goal is to use the smallest amount of consulting structure
needed to make a better decision.

Core principles:
- structure before analysis;
- hypotheses before exhaustive research;
- facts separated from assumptions;
- real options before recommendation;
- 80/20 focus;
- explicit trade-offs;
- answer first;
- state what would change the answer.

## Boundary with Deep Reflection Router

If `router-reflexion-profonde` is installed:

- use **Consulting Strategy Router** for business / market / product / allocation / economics /
  prioritization decisions;
- use **Deep Reflection Router** for system investigation, architecture, runtime evidence,
  root-cause analysis, and technical cross-cutting problems.

### Handoff

Consulting → deep reflection:
- formulate one bounded technical/system question;
- request facts, contradictions, and unknowns;
- bring the result back into the business decision.

Deep reflection → consulting:
- pass the already-established fact base;
- use this router only for options, economics, prioritization, and the recommendation.

Avoid recursive handoffs. One router owns the current phase.

## Core workflow

### 1. Name the decision

Write:
- decision to make;
- decision-maker / audience;
- desired outcome;
- constraints;
- time horizon;
- in-scope / out-of-scope.

If context is missing, state provisional assumptions and continue instead of returning only questions.

### 2. Structure the problem

Build the smallest useful MECE structure.

Good structure:
- branches do not overlap;
- together they cover what can change the decision;
- each branch can be tested.

Do not build a giant issue tree for a simple binary decision.

### 3. Build the evidence register

Tag important claims:

- **F — Fact:** observed or sourced;
- **I — Inference:** derived from facts;
- **A — Assumption:** judgment filling a gap;
- **E — Estimate:** calculated from facts + assumptions.

For every load-bearing assumption, capture:
- importance;
- evidence strength;
- confidence;
- test that could invalidate it;
- action if it fails.

### 4. Generate real options

Create a small set of meaningfully different paths.

For each:
- upside;
- trade-off;
- feasibility;
- risk;
- economics if relevant;
- strategic fit;
- what must be true.

Do not let the preferred option win by default because the alternatives were not examined equally.

### 5. Choose the right lens

Use only when relevant:

| Decision type | Useful lens |
|---|---|
| unclear current state | situation assessment |
| fragile beliefs | assumption audit |
| path selection | strategic options |
| investment / ROI | business case |
| too many initiatives | prioritization |
| competitor / market reactions | war gaming |
| major strategic risk | risk & mitigation |
| strategy → execution | transformation roadmap |
| executive written decision | decision memo |

Frameworks such as Porter, SWOT, BCG, JTBD, RICE, or a profit tree are tools, not defaults.
The problem chooses the framework.

### 6. Analyze the 20% that can flip the decision

Prioritize:
- the hypotheses with the largest impact on the recommendation;
- the weakest evidence among the most important assumptions;
- the few data points that could kill an option.

Avoid "boiling the ocean".

### 7. Stress-test the recommendation

Before concluding:

- strongest counter-argument;
- assumption that would reverse the decision;
- adverse scenario;
- likely competitor/customer reaction;
- early warning signal;
- kill condition;
- runner-up option tested with the same rigor.

If the counter-case is stronger, change the recommendation.

### 8. Synthesize answer-first

Default output:

```text
🎯 Decision:
✅ Recommendation:
📐 Why (max 3 load-bearing reasons):
📏 Evidence:
❓ Critical assumptions:
🛤️ Options and trade-offs:
🗡️ Counter-case / stress test:
⚠️ Risks + mitigations:
🛑 Kill conditions:
➡️ Next tests / actions:
```

## Optional integrations

This router works standalone.

If installed, it can delegate specialized analysis to external skills such as:
- `management-consulting` by gcamilo;
- `situation-assessment`, `assumption-audit`, `strategic-options`,
  `business-case-builder`, `initiative-prioritizer`, `war-gaming`,
  `transformation-roadmap`, and `decision-memo` from strategy-skills-for-claude.

Never claim an integration ran unless it is actually installed and invoked.

## Credits / further reading

This router was assembled from common strategy-consulting practices and from ideas found in:
- https://github.com/gcamilo/management-consulting
- https://github.com/aapersh/strategy-skills-for-claude

Those projects remain separate upstream resources. This skill does not imply affiliation with or
endorsement by any consulting firm.

## Anti-patterns

- framework salad;
- SWOT as a substitute for analysis;
- one option presented as inevitable;
- unsupported market numbers;
- consensus between multiple models treated as evidence;
- long research that does not change the decision;
- vague recommendations without owner, test, or next move;
- a recommendation with no condition that would reverse it.
