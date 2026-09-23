# Public skills

This folder contains the **canonical standalone skill packages published directly in this repository**.

The public skill ecosystem is larger than this folder: specialized toolkits stay in their own repositories so there is only one canonical copy to maintain.

## Skills in this repository

| Skill | Purpose |
|---|---|
| [`skill-hub`](./skill-hub/SKILL.md) | Audit and manage a multi-repo skill collection. |
| [`skill-cleaner`](./skill-cleaner/SKILL.md) | Merge, deduplicate and reorganize overlapping skills without losing local specificity. |
| [`import-skills-into-my-system`](./import-skills-into-my-system/SKILL.md) | Migrate an existing agent system toward a reference architecture while preserving useful customizations. |
| [`loop-creator`](./loop-creator/SKILL.md) | Build resumable autonomous work loops without freezing the business method inside the resume prompt. |
| [`skill-finder-research`](./skill-finder-research/SKILL.md) | Research and benchmark external skills/methods before adoption. |
| [`router-reflexion-profonde`](./router-reflexion-profonde/SKILL.md) | Self-contained deep-reasoning router bundling problem framing, root-cause, system optimization and pre-mortem methods. |
| [`router-consulting-strategy`](./router-consulting-strategy/SKILL.md) | Route business decisions through consulting-style framing, hypotheses, options and stress tests. |

## Other public skill repositories

These are intentionally **not duplicated here**.

### Productivity — Claude sessions

[`Gremelinn0/productivity-claude-sessions-toolkit`](https://github.com/Gremelinn0/productivity-claude-sessions-toolkit)

- [`claude-sessions-migration`](https://github.com/Gremelinn0/productivity-claude-sessions-toolkit/blob/master/skills/claude-sessions-migration/SKILL.md)

### Productivity — Claude ↔ GPT

[`Gremelinn0/productivity-claude-gpt-bridge`](https://github.com/Gremelinn0/productivity-claude-gpt-bridge)

- [`claude-gpt`](https://github.com/Gremelinn0/productivity-claude-gpt-bridge/blob/master/skills/claude-gpt/SKILL.md)

### Productivity — Session supervision

[`Gremelinn0/productivity-claude-session-supervisor`](https://github.com/Gremelinn0/productivity-claude-session-supervisor)

- [`claude-session-supervisor`](https://github.com/Gremelinn0/productivity-claude-session-supervisor/blob/master/skills/claude-session-supervisor/SKILL.md)

### Productivity — Claude Code system pack

[`Gremelinn0/productivity-claude-code-system-pack`](https://github.com/Gremelinn0/productivity-claude-code-system-pack)

- [`capitaliser`](https://github.com/Gremelinn0/productivity-claude-code-system-pack/blob/main/skills/capitaliser/SKILL.md)
- [`clean-rules-cleanup`](https://github.com/Gremelinn0/productivity-claude-code-system-pack/blob/main/skills/clean-rules-cleanup/SKILL.md)
- [`optimise-systeme`](https://github.com/Gremelinn0/productivity-claude-code-system-pack/blob/main/skills/optimise-systeme/SKILL.md)
- [`propage-systeme`](https://github.com/Gremelinn0/productivity-claude-code-system-pack/blob/main/skills/propage-systeme/SKILL.md)
- [`skill-quality-guard`](https://github.com/Gremelinn0/productivity-claude-code-system-pack/blob/main/skills/skill-quality-guard/SKILL.md)

### Sales / HubSpot toolkit

[`Gremelinn0/sales-hubspot-toolkit`](https://github.com/Gremelinn0/sales-hubspot-toolkit)

- [`claude-breeze`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/claude-breeze/SKILL.md)
- [`claude-ia-delegation`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/claude-ia-delegation/SKILL.md)
- [`crm-investigation-output`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/crm-investigation-output/SKILL.md)
- [`hubspot-create-list`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/hubspot-create-list/SKILL.md)
- [`hubspot-crm`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/hubspot-crm/SKILL.md)
- [`hubspot-email-design`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/hubspot-email-design/SKILL.md)
- [`hubspot-marketing-segments`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/hubspot-marketing-segments/SKILL.md)
- [`hubspot-segments-audit`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/hubspot-segments-audit/SKILL.md)
- [`hubspot-workflows-audit`](https://github.com/Gremelinn0/sales-hubspot-toolkit/blob/master/skills/hubspot-workflows-audit/SKILL.md)

## Structure rule

- `skill/<name>/SKILL.md` = canonical standalone skills owned by this repo.
- `resources/` = compatibility links, deprecated resources and non-skill supporting material.
- A skill whose real owner is another public toolkit remains there and is linked above instead of copied here.

Current catalog: **24 standalone public skills across 6 repositories**.
