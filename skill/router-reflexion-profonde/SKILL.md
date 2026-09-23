---
name: router-reflexion-profonde
description: >-
  Orchestrates a read-only deep-reasoning phase before execution for complex, structural,
  cross-cutting, or hard-to-reverse problems. Use when an AI is likely to jump to a plausible
  answer too quickly, when the real problem is unclear, or when you need facts, system mapping,
  root-cause analysis, real alternatives, falsifiable success criteria, and a pre-mortem before
  any change. Triggers include "think deeply before acting", "challenge the plan", "find the root
  cause", "take a step back", and French equivalents such as "réfléchis avant d'agir".
---

# Deep Reflection Router

## Purpose

Turn a complex request into a **decision-quality understanding before execution**.

This skill exists to prevent a common failure mode: an AI understands the user's intent, produces
a plausible answer, and starts acting before it has actually investigated the problem.

Default posture: **read-only / observe-only**.

You may inspect, measure, map, compare, model, and challenge. Do not modify files, deploy, commit,
send, purchase, delete, or otherwise mutate the target system until the decision package is ready
and the execution mandate is clear.

## When to use

Use this router when at least one is true:

- the problem is ambiguous, structural, or spans multiple components;
- a previous fix treated symptoms instead of causes;
- the change is costly or difficult to reverse;
- several plausible solutions exist;
- the plan depends on unverified assumptions;
- the user explicitly asks for deep thinking before action.

Do not use it for trivial, fully specified, reversible tasks.

## Depth

| Level | Use when | Minimum treatment |
|---|---|---|
| D1 | Local non-trivial decision | framing + one main analysis lens + inline pre-mortem |
| D2 | Structural / cross-cutting problem | evidence + system map + 2 complementary lenses + 3 options + pre-mortem |
| D3 | Architecture / migration / high-cost decision | D2 + independent challenge + non-loss criteria + explicit decision gate |

An explicit invocation of this skill implies at least D2 unless the user says otherwise.

## Package structure

This public skill is **self-contained**.

The specialized methods that may exist as separate private/internal skills in another system are bundled here as references:

- `references/poser-le-probleme.md` — full problem framing before solutioning;
- `references/racine.md` — structural root-cause analysis;
- `references/optimise-systeme.md` — objective system optimization;
- `references/challenge-premortem.md` — adversarial pre-mortem.

They are **methods inside this skill**, not installation prerequisites.

Installing / copying this folder must be sufficient to use the router.

## Routing rule

Do not run every method. Choose the **smallest set of lenses that can change the decision**.

| Signal | Bundled method |
|---|---|
| unclear / incomplete problem map | load `references/poser-le-probleme.md` |
| recurring bug / symptom / workaround | load `references/racine.md` |
| bloated / tangled system or governance problem | load `references/optimise-systeme.md` |
| important plan not yet executed | load `references/challenge-premortem.md` |
| architecture / source-of-truth ambiguity | use the system-mapping workflow in this file, plus root-cause or optimization if needed |
| one idea is being refined too early | use the option-generation workflow in this file |
| business / market / strategy decision | hand off to a strategy-consulting router if one is installed; otherwise stay in generic decision analysis |

Load a bundled reference only when its method is needed.

If the host happens to have an equivalent local skill, it may use that local owner instead. But the public package must never require it.

Never pretend an unavailable external skill was called.

## Workflow

### 1. Lock execution

State that the current phase is analysis only.

Capture:
- the request;
- what is already decided;
- what is explicitly out of scope;
- the decision that must be made.

### 2. Frame the whole problem

For ambiguous or repeatedly misunderstood problems, load `references/poser-le-probleme.md` first.

Write separately:

1. observed symptom / dissatisfaction;
2. desired outcome;
3. system capable of producing that outcome;
4. decision to make now;
5. objective signal that would prove improvement.

If the success signal cannot be written, the problem is not framed yet.

### 3. Reconstruct reality

Build a fact base before recommending.

Separate:
- **FACT** — observed / measured;
- **INFERENCE** — derived from facts;
- **ASSUMPTION** — plausible but unverified;
- **CONTRADICTION** — evidence that conflicts;
- **UNKNOWN** — required information not yet available.

Prefer runtime evidence, logs, real consumers, and current owners over documentation alone.

### 4. Map the system

Trace the useful chain end to end:

`input → mechanisms → owners → sources of truth → execution → evidence → decision`

Look for:
- hidden state;
- duplicated authority;
- missing feedback loops;
- silent transformations;
- copied information;
- unclear ownership;
- places where evidence is lost.

### 5. Go below the symptom

For recurring defects, workarounds, or symptoms that keep returning, load `references/racine.md`.

Ask why until you reach a structural cause that can explain recurrence.

Examples:
- wrong owner;
- missing gate;
- unreliable signal;
- duplicated source of truth;
- bad unit of work;
- invisible dependency;
- feedback loop that never closes.

Do not stop at "the file is wrong" or "the agent forgot".

### 6. Open options before converging

For D2/D3, produce at least 3 genuinely different options.

A useful default set:
- accept / reduce scope;
- minimal intervention;
- structural correction.

For each option show:
- upside;
- cost;
- risk / blast radius;
- reversibility;
- residual debt;
- success signal.

Reject weak options explicitly so they do not return later under a new name.

### 7. Build a falsifiable thesis

Use this form:

> If we change **X** in system **Y**, we expect **Z**, measured by **M**, without losing **N**.

List:
- assumptions;
- prerequisites;
- rollback;
- PASS criteria;
- ABORT criteria.

A plan that cannot fail in its wording cannot be tested.

### 8. Attack the plan

For material or hard-to-reverse plans, load `references/challenge-premortem.md`.

Before execution, run a pre-mortem:

- What is the strongest reason this plan could fail?
- Which assumption would reverse the recommendation if false?
- What second-order effect are we ignoring?
- What would a smart critic attack first?
- What evidence would make us pivot?

Update the plan when the challenge is stronger than the original thesis.

### 9. Return the decision package

Use:

```text
🔒 MODE: analysis only
🎯 Request:
🧭 Real problem:
🔭 Depth / scope:
📏 Facts:
❓ Assumptions / unknowns:
🧩 System map:
🧬 Root cause / structural pattern:
🛤️ Options:
🗡️ Challenge / pre-mortem:
✅ Recommendation:
📐 PASS / ABORT:
🗂️ Execution plan:
➡️ Next owner / next step:
```

## System optimization branch

When the problem is not one defect but the quality of the system itself — too many rules, duplicated responsibilities, stale maps, weak ownership, or excessive maintenance cost — load `references/optimise-systeme.md`.

Its invariant is simple: **measure before simplifying, then re-measure after the change.**

## Handoff to execution

After the decision is clear:
- if the user already authorized execution, hand off to the correct implementation owner;
- otherwise stop at the decision package.

This router should not become a permanent project manager or implementation skill.

## Quality bar

Before finishing, verify that another agent could:
1. understand the real problem;
2. find the facts behind the conclusion;
3. explain why alternatives were rejected;
4. challenge the recommendation using the same criteria;
5. execute without inventing a missing decision;
6. know when to stop.

## Anti-patterns

- acting "just to make progress" while the problem is still being reframed;
- treating documentation as runtime proof;
- producing one solution and asking a pre-mortem to bless it;
- confusing more analysis with better analysis;
- listing files instead of mapping a capability;
- using every framework because it is available;
- making a recommendation that has no kill condition.
