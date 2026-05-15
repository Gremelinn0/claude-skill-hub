#!/usr/bin/env python3
"""Scan personal skills (global + tous les dépôts PROJECTS/) and output skills-data.json.

repo = label court du dépôt (slug). Permet aux pages HTML de filtrer par dépôt
via boutons dynamiques. `repo_path` garde le chemin lisible complet (tooltip).
"""

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Configuration via variables d'environnement (override possible) :
#   SKILL_HUB_GLOBAL_SKILLS  : dossier des skills globaux (défaut: ~/.claude/skills)
#   SKILL_HUB_PROJECTS_ROOT  : racine des projets contenant des .claude/skills (défaut: ~/PROJECTS)
#   SKILL_HUB_OUTPUT_DIR     : dossier où écrire skills-data.json (défaut: ../hub/ relatif à ce script)
#   SKILL_HUB_EXCLUDE_REPOS  : chemins de dépôts à ignorer, séparés par ";" (relatifs à PROJECTS_ROOT)
GLOBAL_SKILLS_DIR = Path(os.environ.get("SKILL_HUB_GLOBAL_SKILLS") or (Path.home() / ".claude" / "skills"))
PROJECTS_ROOT = Path(os.environ.get("SKILL_HUB_PROJECTS_ROOT") or (Path.home() / "PROJECTS"))
OUTPUT_DIR = Path(os.environ.get("SKILL_HUB_OUTPUT_DIR") or (Path(__file__).resolve().parent.parent / "hub"))

EXCLUDE_DIRS = {"_archive"}
EXCLUDE_PREFIXES = ("anthropic-skills:", "bmad:", "caveman:", "cowork-plugin-management:")
EXCLUDE_NAMES = {"init", "review", "security-review"}

# Dépôts ignorés au scan (worktrees temporaires, backups…). Override via env var.
_default_excludes = {
    # Ajoute ici les chemins relatifs à PROJECTS_ROOT que tu veux exclure.
    # Exemple : "old-stuff/backup", "feature-x/worktree-tmp"
}
_env_excludes = os.environ.get("SKILL_HUB_EXCLUDE_REPOS", "")
EXCLUDE_REPO_PATHS = _default_excludes | {p.strip() for p in _env_excludes.split(";") if p.strip()}


def parse_frontmatter(skill_md: Path) -> dict:
    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm = content[3:end]
    result = {}
    for line in fm.splitlines():
        m = re.match(r'^(name|description)\s*:\s*(.*)', line)
        if m:
            result[m.group(1)] = m.group(2).strip()
    return result


def extract_summary(skill_md: Path, max_chars: int = 600) -> str:
    """Extract 1er paragraphe humain post-frontmatter (avant premier `##` ou H1).

    Skip H1 (`# Title`), prend contenu paragraphe(s) avant 1er `## section`.
    """
    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

    # Skip frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:]

    lines = content.splitlines()
    summary_lines = []

    for line in lines:
        stripped = line.strip()
        # Skip leading empty lines
        if not stripped and not summary_lines:
            continue
        # Skip ANY H1 (title) anywhere — `# Title`
        if stripped.startswith("# ") and not stripped.startswith("## "):
            continue
        # Stop at first H2/H3 section header
        if stripped.startswith("## ") or stripped.startswith("### "):
            break
        # Stop at horizontal rule
        if stripped == "---":
            break
        summary_lines.append(line)
        # Stop if we've collected enough
        if sum(len(l) for l in summary_lines) > max_chars * 1.5:
            break

    summary = "\n".join(summary_lines).strip()
    # Clean : remove trailing/leading whitespace per line
    if len(summary) > max_chars:
        summary = summary[:max_chars].rsplit(" ", 1)[0] + "…"
    return summary


def count_lines(skill_md: Path) -> int:
    try:
        return len(skill_md.read_text(encoding="utf-8", errors="replace").splitlines())
    except Exception:
        return 0


def last_commit_hash(skill_dir: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%h", str(skill_dir)],
            capture_output=True, text=True, cwd=skill_dir.parent
        )
        return result.stdout.strip() or ""
    except Exception:
        return ""


def slugify_repo(repo_path: str) -> str:
    """`3- Wisper/speak-app-dev` → `speak-app-dev`. Last segment, lowercased, ascii-safe."""
    last = repo_path.split("/")[-1] if "/" in repo_path else repo_path
    last = re.sub(r'^\d+\s*-?\s*', '', last)  # strip "0- " / "3- "
    last = last.strip().lower()
    last = re.sub(r'[^a-z0-9]+', '-', last)
    return last.strip('-') or 'repo'


def scan_skills(base_dir: Path, scope: str, repo: str, repo_path: str) -> list[dict]:
    skills = []
    if not base_dir.exists():
        return skills

    for skill_dir in sorted(base_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name in EXCLUDE_DIRS:
            continue
        if any(skill_dir.name.startswith(p) for p in EXCLUDE_PREFIXES):
            continue
        if skill_dir.name in EXCLUDE_NAMES:
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(skill_md)
        try:
            full_content = skill_md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            full_content = ""
        skills.append({
            "name": fm.get("name") or skill_dir.name,
            "dir_name": skill_dir.name,
            "description": fm.get("description") or "",
            "summary": extract_summary(skill_md),
            "full_content": full_content,
            "scope": scope,
            "repo": repo,
            "repo_path": repo_path,
            "path": str(skill_md).replace("\\", "/"),
            "lines": count_lines(skill_md),
            "last_commit_hash": last_commit_hash(skill_dir),
        })

    return skills


def discover_project_repos() -> list[tuple[Path, str]]:
    """Trouve tous les dossiers `<X>/.claude/skills/` sous PROJECTS/.

    Retourne [(skills_dir, repo_path_relative)]. Profondeur max 3 sous PROJECTS/.
    """
    found = []
    if not PROJECTS_ROOT.exists():
        return found

    for skills_dir in PROJECTS_ROOT.glob("*/.claude/skills"):
        if skills_dir.is_dir():
            rel = str(skills_dir.parent.parent.relative_to(PROJECTS_ROOT)).replace("\\", "/")
            if rel not in EXCLUDE_REPO_PATHS:
                found.append((skills_dir, rel))

    for skills_dir in PROJECTS_ROOT.glob("*/*/.claude/skills"):
        if skills_dir.is_dir():
            rel = str(skills_dir.parent.parent.relative_to(PROJECTS_ROOT)).replace("\\", "/")
            if rel not in EXCLUDE_REPO_PATHS:
                found.append((skills_dir, rel))

    return found


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "skills-data.json"

    all_skills = []
    repos_summary = []

    global_skills = scan_skills(GLOBAL_SKILLS_DIR, "global", "global", "~/.claude/skills")
    all_skills.extend(global_skills)
    repos_summary.append(("global", "~/.claude/skills", len(global_skills)))

    project_repos = discover_project_repos()
    for skills_dir, repo_path in project_repos:
        repo_slug = slugify_repo(repo_path)
        scoped = scan_skills(skills_dir, "projet", repo_slug, repo_path)
        if scoped:
            all_skills.extend(scoped)
            repos_summary.append((repo_slug, repo_path, len(scoped)))

    # Aggregate counts par repo (pour stats)
    repo_counts = {}
    for s in all_skills:
        repo_counts[s["repo"]] = repo_counts.get(s["repo"], 0) + 1

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "global": sum(1 for s in all_skills if s["scope"] == "global"),
            "projet": sum(1 for s in all_skills if s["scope"] == "projet"),
            "total": len(all_skills),
            "repos": repo_counts,
        },
        "repos": [
            {"slug": slug, "path": path, "count": cnt}
            for slug, path, cnt in repos_summary
        ],
        "skills": all_skills,
    }

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"OK {len(all_skills)} skills written to {output_path}")
    print(f"  Repos found: {len(repos_summary)}")
    for slug, path, cnt in repos_summary:
        print(f"    {cnt:3d}  [{slug}]  {path}")


if __name__ == "__main__":
    main()
