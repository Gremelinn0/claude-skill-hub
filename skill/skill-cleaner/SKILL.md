---
name: skill-cleaner
description: >-
  Audit, merge, deduplicate and reorganize Agent Skills without losing useful knowledge.
  Use when importing a third-party skill, resolving overlaps between skills, cleaning a large
  skill collection, or deciding whether to keep, merge, move, store or archive a skill.
  Preserve user/project-specific methods and conventions; generic imported methodology is
  complementary by default, not authoritative.
---

# Skill Cleaner

Clean and consolidate a collection of Agent Skills without flattening the user's own way of working.

The goal is not "fewer skills". The goal is a system where every surviving skill has a clear
responsibility, overlaps are intentional, and no useful knowledge is silently lost.

## Core rule: preserve specificity

When an imported skill overlaps with an existing one, distinguish **generic methodology** from
**local specificity**.

Default precedence:

1. Explicit user instructions.
2. Project- or organization-specific rules and conventions.
3. Existing local workflow choices that are still intentional.
4. Imported generic methodology.

An imported skill should therefore **complete** the local method before it **replaces** it.

If two methods overlap:

- identical rule → keep one canonical version;
- generic rule + local specialization → keep the local specialization and merge only the useful generic parts;
- compatible but different approaches → keep both as conditional branches when their contexts differ;
- direct contradiction → do not silently choose; preserve the local rule and surface the conflict;
- obsolete local rule explicitly superseded by the user → replace it and record the migration.

## Workflow

### 1. Inventory before judging

For every relevant skill, inspect the actual content, not only its name or description.

Capture:

- purpose and triggers;
- inputs and outputs;
- tools or environment assumptions;
- workflow/method;
- project-specific conventions;
- dependencies and references;
- unique knowledge that appears nowhere else.

A similar name is only a signal. It is not proof of duplication.

### 2. Identify the owner

Ask:

> Where should this knowledge canonically live?

Prefer the narrowest durable owner:

- project-specific method → project skill;
- team/company convention → team/company skill;
- generic reusable method → global/shared skill;
- reference material → reference/documentation rather than the main skill.

Do not promote project-specific knowledge into a global skill merely because several agents use it.

### 3. Map the overlap

Classify each meaningful block:

| Relationship | Meaning | Default action |
|---|---|---|
| Duplicate | Same rule, same scope, same purpose | Keep one canonical copy |
| Complement | Adds useful non-conflicting detail | Merge |
| Specialization | Local version narrows or adapts a generic rule | Preserve local version |
| Alternative | Different valid method for a different context | Keep both conditionally |
| Conflict | Rules cannot both be followed in the same context | Surface conflict |
| Historical | Explains a past decision but is not active guidance | Move to reference/archive |
| Obsolete | Superseded and no longer useful | Archive/remove after verification |

### 4. Non-loss check

Before deleting, slimming or merging any content:

1. identify every useful block being removed;
2. verify whether it already exists elsewhere;
3. if not, move it to its canonical owner;
4. keep durable rationale/history when it prevents future mistakes;
5. only then remove the redundant source.

Never archive or delete content you have not actually inspected.

### 5. Give one verdict per skill

Use one primary verdict:

- **KEEP** — distinct responsibility, already clean.
- **KEEP + SLIM** — distinct responsibility, but contains material that belongs elsewhere.
- **MERGE** — useful content belongs in another skill.
- **MOVE** — useful skill, wrong scope or owner.
- **STORE / DORMANT** — still valid, but not needed in the active context.
- **ARCHIVE** — superseded, historical or dead.
- **DECISION REQUIRED** — a real unresolved conflict would change behavior.

Usage frequency can help decide active vs dormant, but it is not proof that a skill is useless.

## Importing a third-party skill

When the user adds a complete external skill:

1. read the external skill and the closest local skills;
2. extract the external method into atomic rules/steps;
3. mark each item as duplicate, complement, specialization, alternative or conflict;
4. preserve local/user-specific choices by default;
5. merge only the external elements that add value;
6. avoid creating a second competing skill when one canonical skill can absorb the useful parts;
7. report meaningful conflicts instead of hiding them.

### Example

Existing local rule:

> Write LinkedIn posts without Markdown formatting because the publishing workflow expects plain text.

Imported generic skill:

> Use Markdown headings and bold text to improve readability.

Result:

- do **not** replace the local rule;
- keep the plain-text publishing constraint;
- reuse any other useful readability principles from the imported skill that do not require Markdown.

The generic method is a source of reusable technique, not permission to erase local constraints.

## Output format

For each affected skill:

```text
Skill: <name>
Verdict: KEEP | KEEP + SLIM | MERGE | MOVE | STORE | ARCHIVE | DECISION REQUIRED

Why:
- <one-sentence responsibility>

Overlap:
- <what is duplicated/complementary/conflicting>

Preserved specificity:
- <local/user/project rules kept>

Merged or moved:
- <useful blocks and destination>

Risk:
- <what could break>

Verification:
- <how to confirm behavior is unchanged>
```

## Execution rules

- Prefer reversible changes.
- Keep backups or use version control before destructive changes.
- Update active references when renaming or moving a skill.
- Do not leave accidental duplicate active copies.
- Do not rewrite a whole skill when a targeted merge is enough.
- Do not invent missing requirements.
- After changes, verify that expected triggers and workflows still work.

## Final gate

Before declaring the cleanup complete, confirm:

- every surviving skill has a clear responsibility;
- user/project-specific methodology was preserved unless explicitly superseded;
- imported generic rules only replaced local rules with explicit justification;
- no useful unique knowledge was lost;
- no unintended duplicates remain;
- references and triggers still resolve;
- unresolved behavioral conflicts are visible to the user.
