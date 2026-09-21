---
name: skill-finder-research
description: Research operator that benchmarks external AI-agent skills and proven practitioner methods before adoption. Use when you need to find a missing capability, compare several candidate skills, or improve an existing workflow without blindly installing whatever is most popular.
---

# Skill Finder Research

## Mission

Find the best existing building block for a task before creating one from scratch.

This skill can search for:
- an installable skill;
- a reusable script or workflow;
- a proven method from a practitioner;
- a better approach to absorb into an existing system.

It does **not** install, modify, merge or publish anything. It returns a research-backed adoption decision.

## Input

Before searching, define:

1. **Expected outcome** — what concrete result should the capability produce?
2. **Existing capability** — what already exists locally, if anything?
3. **Target host** — Claude Code, Codex, another agent/runtime.
4. **Constraints** — permissions, stack, language, cost, licensing, maintenance.
5. **Acceptance criteria** — what would make one candidate clearly better than another?

If the request is vague, rewrite it as a testable task first.

## Choose a mode

| Situation | Mode | Goal |
|---|---|---|
| No existing capability covers the task | **INSTALLABLE** | Find a real external skill worth adopting |
| A capability exists but performs poorly | **METHOD** | Find better mechanisms to absorb without creating a duplicate |
| Both are relevant | **MIXED** | Compare installable artifacts and external methods |

## Research workflow

### 1. Build the search brief

Translate the need into precise English domain vocabulary:
- desired output;
- core verbs;
- tool/runtime;
- constraints;
- synonyms and adjacent terminology.

Prefer search terms that describe the actual task, not only the product name.

### 2. Search in evidence order

Use this priority:

1. **Official sources** — vendor docs, official repositories, specifications.
2. **Maintained collections** — reputable curators with visible authorship, history and license.
3. **Targeted GitHub search** — open the real `SKILL.md`, scripts and references.
4. **Marketplaces/directories** — useful for discovery, never sufficient as proof of quality.
5. **Practitioner sources** — in METHOD mode, research the native professional surface for the domain.

Always open the canonical source. A marketplace card, star count or search snippet is not enough.

### 3. Inspect serious candidates

For every serious candidate, verify:
- complete skill/instruction file;
- source and author;
- license;
- last meaningful update;
- dependencies;
- scripts and commands;
- network access;
- secrets/permissions;
- compatibility with the target runtime;
- overlap with the existing system;
- whether the README claims match the actual implementation.

### 4. Apply hard gates before scoring

Reject a candidate before scoring if it fails any of these:

- **Provenance** — source cannot be traced confidently.
- **Safety** — suspicious scripts, excessive permissions, unsafe secret handling.
- **Compatibility** — cannot realistically run in the target environment.
- **Structure** — the real implementation is incomplete or materially different from the advertised capability.

For candidates that pass, score comparatively:

| Criterion | Weight |
|---|---:|
| Fit to the exact task | 30 |
| Quality of procedure / instructions | 20 |
| Verification / testing discipline | 15 |
| Maintenance / freshness | 10 |
| Portability | 10 |
| Security | 10 |
| Context / complexity cost | 5 |

Popularity is only a weak tie-breaker.

### 5. Test when safe

When temporary installation or execution is safe and explicitly allowed:

1. inspect statically first;
2. prepare 2–3 realistic cases;
3. include one difficult case and one out-of-scope case;
4. compare candidates with the same brief;
5. separate **tested**, **declared** and **inferred** behavior.

If installation is not authorized, return a static assessment and list the tests still required.

### 6. Return one adoption verdict

Choose one:

- **INSTALL** — missing capability; candidate clearly passes the gates.
- **ABSORB THE METHOD** — keep the existing capability but incorporate better mechanisms.
- **KEEP EXISTING** — no meaningful gain demonstrated.
- **REJECT** — risk, duplication, weak quality or incompatibility.
- **WATCH** — promising, but not sufficiently proven yet.

## Required output

```text
Research: <need>
Mode: <INSTALLABLE | METHOD | MIXED>

Testable need:
<one sentence>

Existing capability:
<name or none>

Sources scanned:
<official · repositories · directories · practitioner sources>

Candidate | Type | Canonical source | Score | Risk | Verdict
...

Recommendation:
<one main verdict>

Why:
- <fact 1>
- <fact 2>
- <fact 3>

What to install or absorb:
<precise elements>

Tested / declared / inferred:
<clear separation>

Next step:
<one concrete next action>
```

## Guardrails

- Search in English first unless the domain requires another language.
- Never install directly from a marketplace listing without tracing the canonical source.
- Never execute third-party scripts before inspection.
- Never confuse popularity with quality.
- Avoid creating duplicate capabilities when an existing one can absorb the improvement.
- Cite canonical sources, dates, limitations and any relevant conflicts of interest.
- Do not mutate the user's system automatically; return a decision package first.

## Public version note

This file is a standalone public edition of Skill Finder Research. Internal routing, private project references and non-portable dependencies have been intentionally removed.
