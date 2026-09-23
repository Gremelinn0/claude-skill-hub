---
name: router-reflexion-profonde
description: >-
  Orchestrates a read-only reasoning phase whenever a task deserves real thought before action:
  decisions, writing, strategy, planning, debugging, product work, architecture, or any ambiguous
  task where the first plausible answer may be premature. Frames just enough, then loads only the
  methods that matter: problem framing, root-cause analysis, system optimization, alternatives, or
  adversarial pre-mortem. Skip it for trivial, fully specified work.
---

# Deep Reflection Router

## Purpose

Turn a task that deserves reflection into **decision-quality understanding before execution**.

This skill exists to prevent a common failure mode: an AI understands the user's intent, produces
a plausible answer, and starts acting before it has actually investigated the problem.

Default posture: **read-only / observe-only**.

You may inspect, measure, map, compare, model, and challenge. Do not modify files, deploy, commit,
send, purchase, delete, or otherwise mutate the target system until the decision package is ready
and the execution mandate is clear.

## When to use

Use this router whenever a task is not trivial and the quality of the reasoning matters before action.

Typical signals:
- the problem or goal is still ambiguous;
- facts and assumptions are mixed;
- several plausible options exist;
- a previous answer or fix treated the wrong problem;
- the work has meaningful consequences;
- the user explicitly asks to think, challenge, compare, or investigate before acting.

This applies to technical and non-technical work alike.

Do not use it for trivial, fully specified tasks where reflection would add ceremony rather than value.

## Depth

| Level | Use when | Minimum treatment |
|---|---|---|
| D1 | Any non-trivial task where an immediate answer would be premature | light framing + one useful lens + decision / answer |
| D2 | Multiple hypotheses, options, dependencies or consequences | evidence + 2 complementary lenses + alternatives + contradiction |
| D3 | High-cost, hard-to-reverse or strategic decision | D2 + independent challenge + non-loss criteria + explicit decision gate |

An explicit invocation starts at the **minimum sufficient depth**. Do not turn a D1 task into a D2/D3 ceremony.

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

### 2. Frame only as much as the task needs

Write:
1. what must be understood, decided, or produced;
2. what is already established;
3. which assumptions or unknowns could change the answer;
4. the success criterion.

Load `references/poser-le-probleme.md` only when the **problem map itself is uncertain**: several objects or actors, repeated misunderstanding, ambiguous scope, or conflicting roles.

The router chooses methods. It does not turn every method into a mandatory checklist.

### 3. Reconstruct reality

Build a fact base before recommending.

Separate:
- **FACT** — observed / measured;
- **INFERENCE** — derived from facts;
- **ASSUMPTION** — plausible but unverified;
- **CONTRADICTION** — evidence that conflicts;
- **UNKNOWN** — required information not yet available.

Prefer runtime evidence, logs, real consumers, and current owners over documentation alone.

### 4. Map a system only when a system is actually involved

If the task depends on multiple components, actors, sources of truth or dependencies, trace the useful chain end to end:

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

### 8. Attack the plan when the plan deserves it

For material, uncertain or hard-to-reverse plans, load `references/challenge-premortem.md`.

Do not run a pre-mortem on every D1 task.

When appropriate, ask:

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
