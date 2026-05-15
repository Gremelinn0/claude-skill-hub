# Claude Skill Hub

> Self-hosted visual hub to triage and pilot all your [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) skills — across global + every project repo. Master-detail page, move/duplicate/archive/store across repos, notes per skill, CLAUDE.md editor. Bring your own skills.

Live demo (mine, for reference) : [https://antigravity-master-hub.vercel.app/skills-marketplace.html](https://antigravity-master-hub.vercel.app/skills-marketplace.html)

## Why

If you write Claude Code skills, you end up with 50, 100, 200 of them across your global `~/.claude/skills/` and every project's `.claude/skills/`. Some are great, some are outdated, some are duplicates of better ones in another repo, some you forgot you wrote. There's no native way to see them all in one place and decide what stays, what moves, what's archived.

This repo gives you that view : a single static HTML page that scans your filesystem, lists every skill with its description / full content / metadata, lets you sort by repo or by usage category, and exposes 5 actions per skill — **Keep / Store / Archive / Move to another repo / Duplicate to several repos** — plus free-form notes. Export your decisions as JSON, run a script, done.

## What you get

- **Master-detail page** (`hub/skills-marketplace.html`) — vanilla HTML/CSS/JS, no framework, ~2000 lines. Two switchable views (by repo / by usage), full-text search, multi-select filters with counters, decisions drawer.
- **3 Python scripts** (`tools/`) — generate `skills-data.json` and `claude-md-data.json` from your filesystem, then `apply_changes.py` consumes the exported decisions and runs the moves/copies safely (with timestamped backups).
- **5 actions per skill** : Keep · Store (`.claude/skills-store/`) · Archive (`_archive/skills-archive/<date>/`) · Move (to another repo) · Duplicate (to N repos, original kept). Each can carry a free-form note that goes into the export.
- **CLAUDE.md editor** — inline textarea for every `CLAUDE.md` file across your repos, with auto sections table-of-contents. Edits go into the same export.
- **A Claude Code skill** (`skill/skill-hub/`) — install it in your `~/.claude/skills/` and invoke `/skill-hub` to orchestrate the full workflow.

## Quickstart (5 steps, ~3 minutes)

```bash
# 1. Clone
git clone https://github.com/Gremelinn0/claude-skill-hub.git ~/claude-skill-hub
cd ~/claude-skill-hub

# 2. Tell it where your stuff is (defaults if you skip this : ~/PROJECTS and ~/.claude/skills)
export SKILL_HUB_PROJECTS_ROOT="$HOME/PROJECTS"
export SKILL_HUB_GLOBAL_SKILLS="$HOME/.claude/skills"

# 3. Scan and produce JSON indexes
python tools/generate_skills_index.py
python tools/generate_claude_md_index.py

# 4. Serve the hub
cd hub && python -m http.server 3460
# Open http://localhost:3460/skills-marketplace.html

# 5. (Optional) Install the companion skill for one-command orchestration
mkdir -p ~/.claude/skills && cp -r skill/skill-hub ~/.claude/skills/
# Now you can invoke /skill-hub in any Claude Code session.
```

Want a persistent URL accessible from any PC ? Deploy `hub/` to Vercel (config included) :
```bash
cd hub && npx vercel deploy --prod --yes
```

## Workflow (every time you want to triage)

1. **Regenerate the index** — `python tools/generate_skills_index.py && python tools/generate_claude_md_index.py`. Always do this first, otherwise you decide on stale data.
2. **Open the page** (local or Vercel).
3. **Triage** — click skills, read their full content, write notes, set actions.
4. **Export** — bottom right button, downloads `skill-hub-decisions-*.json`.
5. **Apply** — `python tools/apply_changes.py skill-hub-decisions-*.json`. Confirm preview, done. Timestamped backup is written to `_archive/skill-hub-<ts>/`.
6. **Regenerate + redeploy** — fresh state for next time.

The companion skill (`/skill-hub`) automates all of this.

## Configuration

Everything via environment variables (no config file) :

| Variable | Default | Description |
|----------|---------|-------------|
| `SKILL_HUB_PROJECTS_ROOT` | `~/PROJECTS` | Where your project repos live |
| `SKILL_HUB_GLOBAL_SKILLS` | `~/.claude/skills` | Global skills directory |
| `SKILL_HUB_GLOBAL_CLAUDE_MD` | `~/.claude/CLAUDE.md` | Global CLAUDE.md file |
| `SKILL_HUB_OUTPUT_DIR` | `<repo>/hub/` | Where to write the JSON indexes |
| `SKILL_HUB_BACKUP_DIR` | `<repo>/_archive/` | Where `apply_changes.py` writes backups |
| `SKILL_HUB_EXCLUDE_REPOS` | (empty) | Repo paths to skip, separated by `;` |

## File layout

```
claude-skill-hub/
├── hub/
│   ├── skills-marketplace.html    # the page (vanilla HTML+CSS+JS, self-contained)
│   ├── skills-usage-map.json      # your custom usage categorization (edit me)
│   └── vercel.json                # Vercel static hosting config
├── tools/
│   ├── generate_skills_index.py   # scans + writes skills-data.json
│   ├── generate_claude_md_index.py # scans + writes claude-md-data.json
│   └── apply_changes.py           # consumes the exported JSON, applies actions
├── skill/
│   └── skill-hub/
│       └── SKILL.md               # Claude Code skill that orchestrates the workflow
└── README.md
```

## Page features in detail

- **Master-detail layout**, no modal. List left, detail panel right. Click a skill → its full SKILL.md unfolds in the panel (no internal scroll, you scroll the page). Toggle full screen on the panel for long contents.
- **Two switchable views** : *By repo* (your filesystem organization) or *By usage* (your custom categorization).
- **Multi-select filters** with counters per option — repo, usage, scope (global/project), decision state. Selected items live inline in the filter trigger (no separate row of active filters).
- **Decisions drawer** — slide-out panel listing every active decision, grouped by action, each clickable + cancellable.
- **Duplicate detection** — any `dir_name` present in more than one repo is marked `⧉` with a comparator block in the detail panel.
- **Pre-filled recommendations** — optional `RECOS` object in the HTML to suggest actions on specific skills (you stay in control).
- **localStorage** persistence — your decisions and filters survive a reload.

## Apply_changes — what each action does

| Action | Filesystem effect |
|--------|-------------------|
| `keep` (default) | Nothing |
| `store` | Move skill dir to `<repo>/.claude/skills-store/<dir>/` + append a row to `skills-store/INDEX.md` |
| `archive` | Move skill dir to `<repo>/.claude/skills/_archive/skills-archive/<date>/<dir>/` |
| `move` | Move skill dir to `<target-repo>/.claude/skills/<dir>/` |
| `duplicate` | Copytree skill dir to each target repo (original kept) |
| `note` | None — note is logged and kept in the export for record |
| `flag` | None — `rename` / `rework` flag, for manual follow-up |

All actions create a timestamped backup at `_archive/skill-hub-<ts>/` first.

## Adapting it to your style

- **Visual style** : edit the `:root` CSS variables (palette, fonts, radius). The current style is "warm editorial" — cream background, terracotta accent, serif titles. Replace at will.
- **Usage categories** : edit `hub/skills-usage-map.json` — your domains (dev, marketing, writing, business, anything).
- **Recommendations** : edit `RECOS` object in the HTML.
- **Excluded paths** : `SKILL_HUB_EXCLUDE_REPOS` env var (skip backups, worktrees, etc.).

## Caveats

- Tested on Windows + Python 3.13. Paths use `/` mixed with `\` — the scripts normalize, but if something breaks on Linux/macOS, the fix is usually a one-line `str.replace("\\", "/")` somewhere obvious.
- The page is **client-side only** — fetches the two JSON files, does everything in JS, exports a JSON the user feeds back to a Python script. No backend. This is intentional : the hub can run from anywhere (local, Vercel, file://), the actions stay reversible and traceable.
- The JSON indexes can be heavy if you have lots of skills with long `SKILL.md` files (mine is 2.5 MB for 150 skills). The page does lazy-render the full content per-skill on click. No noticeable perf issue up to a few hundred skills.

## License

MIT — do whatever you want, just don't blame me if you `move` your skill to the wrong repo. (The backups will save you, but still.)

## Built by

[Florent de Maisoncelle](https://www.linkedin.com/) — extracted from my personal Claude Code workflow. PRs / issues / ideas welcome.
