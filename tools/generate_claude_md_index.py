#!/usr/bin/env python3
"""Scan tous les CLAUDE.md (global ~/.claude/CLAUDE.md + chaque dépôt PROJECTS/) et output claude-md-data.json.

Réutilise les filtres de generate_skills_index.py (worktrees + backups exclus).
Format JSON aligné skills-data.json — repos[] + files[] avec full_content + sections[].
"""

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Configuration via variables d'environnement (override possible) — mêmes que generate_skills_index.py :
#   SKILL_HUB_PROJECTS_ROOT  : racine projets (défaut: ~/PROJECTS)
#   SKILL_HUB_GLOBAL_CLAUDE_MD : chemin du CLAUDE.md global (défaut: ~/.claude/CLAUDE.md)
#   SKILL_HUB_OUTPUT_DIR     : dossier de sortie (défaut: ../hub/)
#   SKILL_HUB_EXCLUDE_REPOS  : exclus, séparés par ";"
PROJECTS_ROOT = Path(os.environ.get("SKILL_HUB_PROJECTS_ROOT") or (Path.home() / "PROJECTS"))
GLOBAL_CLAUDE_MD = Path(os.environ.get("SKILL_HUB_GLOBAL_CLAUDE_MD") or (Path.home() / ".claude" / "CLAUDE.md"))
OUTPUT_DIR = Path(os.environ.get("SKILL_HUB_OUTPUT_DIR") or (Path(__file__).resolve().parent.parent / "hub"))

_env_excludes = os.environ.get("SKILL_HUB_EXCLUDE_REPOS", "")
EXCLUDE_REPO_PATHS = {p.strip() for p in _env_excludes.split(";") if p.strip()}

# Worktrees / sous-dossiers internes ignorés (CLAUDE.md de worktree non pertinents)
EXCLUDE_PATH_FRAGMENTS = (
    ".claude/worktrees/",
    "_archive/",
    "anthropic-capture/",  # asset interne
    "marketplace-backup-v1/",
)


def slugify_repo(repo_path: str) -> str:
    """`3- Wisper/speak-app-dev` → `speak-app-dev`. Last segment, lowercased, ascii-safe."""
    last = repo_path.split("/")[-1] if "/" in repo_path else repo_path
    last = re.sub(r'^\d+\s*-?\s*', '', last)
    last = last.strip().lower()
    last = re.sub(r'[^a-z0-9]+', '-', last)
    return last.strip('-') or 'repo'


def last_commit_hash(target: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%h", str(target.name)],
            capture_output=True, text=True, cwd=target.parent
        )
        return result.stdout.strip() or ""
    except Exception:
        return ""


def extract_sections(content: str) -> list[dict]:
    """Extrait H1/H2/H3 du markdown — utile pour table des matières dans le hub."""
    sections = []
    for i, line in enumerate(content.splitlines(), start=1):
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            sections.append({"level": 1, "title": s[2:].strip(), "line": i})
        elif s.startswith("## ") and not s.startswith("### "):
            sections.append({"level": 2, "title": s[3:].strip(), "line": i})
        elif s.startswith("### "):
            sections.append({"level": 3, "title": s[4:].strip(), "line": i})
    return sections


def scan_claude_md(claude_md: Path, scope: str, repo: str, repo_path: str) -> dict | None:
    """Lit un CLAUDE.md unique → dict file."""
    if not claude_md.exists() or not claude_md.is_file():
        return None
    try:
        full_content = claude_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    try:
        stat = claude_md.stat()
        size = stat.st_size
        last_modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
    except Exception:
        size = len(full_content.encode("utf-8"))
        last_modified = ""

    return {
        "repo": repo,
        "repo_path": repo_path,
        "scope": scope,
        "path": str(claude_md).replace("\\", "/"),
        "size": size,
        "lines": len(full_content.splitlines()),
        "last_modified": last_modified,
        "last_commit_hash": last_commit_hash(claude_md),
        "full_content": full_content,
        "sections": extract_sections(full_content),
    }


def discover_claude_md_files() -> list[tuple[Path, str, str, str]]:
    """Renvoie [(claude_md_path, scope, repo_slug, repo_path)].

    Inclut :
    - global ~/.claude/CLAUDE.md
    - PROJECTS/CLAUDE.md (root projet global)
    - chaque CLAUDE.md à profondeur 1-3 sous PROJECTS/ (filtré worktrees/backups)
    """
    found = []

    # Global ~/.claude/CLAUDE.md
    if GLOBAL_CLAUDE_MD.exists():
        found.append((GLOBAL_CLAUDE_MD, "global", "global", "~/.claude"))

    # PROJECTS/CLAUDE.md (root)
    root_md = PROJECTS_ROOT / "CLAUDE.md"
    if root_md.exists():
        found.append((root_md, "global", "projects-root", "PROJECTS"))

    # Tous les CLAUDE.md sous PROJECTS/ (profondeur 1 à 4)
    for depth_glob in ("*/CLAUDE.md", "*/*/CLAUDE.md", "*/*/*/CLAUDE.md", "*/*/*/*/CLAUDE.md"):
        for md in PROJECTS_ROOT.glob(depth_glob):
            if not md.is_file():
                continue
            md_str = str(md).replace("\\", "/")
            if any(frag in md_str for frag in EXCLUDE_PATH_FRAGMENTS):
                continue
            # Détermine repo : 1er ou 2 premiers segments sous PROJECTS_ROOT
            rel_parts = md.relative_to(PROJECTS_ROOT).parts[:-1]  # drop CLAUDE.md
            if not rel_parts:
                continue  # déjà géré par root_md
            # repo_path = up to 2 levels (compromis lisibilité — éq skills script)
            if len(rel_parts) >= 2:
                repo_path = "/".join(rel_parts[:2])
            else:
                repo_path = rel_parts[0]
            if repo_path in EXCLUDE_REPO_PATHS:
                continue
            slug = slugify_repo(repo_path)
            found.append((md, "projet", slug, repo_path))

    return found


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "claude-md-data.json"

    files_data = []
    repos_summary = {}  # slug -> { path, count }

    discovered = discover_claude_md_files()

    # Dédoublonner sur path (au cas où plusieurs glob matchent)
    seen_paths = set()
    for md_path, scope, slug, repo_path in discovered:
        path_key = str(md_path).replace("\\", "/").lower()
        if path_key in seen_paths:
            continue
        seen_paths.add(path_key)

        entry = scan_claude_md(md_path, scope, slug, repo_path)
        if entry is None:
            continue
        files_data.append(entry)
        if slug not in repos_summary:
            repos_summary[slug] = {"path": repo_path, "count": 0}
        repos_summary[slug]["count"] += 1

    # Tri stable : global d'abord, puis par repo slug, puis par path
    files_data.sort(key=lambda f: (0 if f["scope"] == "global" else 1, f["repo"], f["path"]))

    repos_list = [
        {"slug": slug, "path": info["path"], "count": info["count"]}
        for slug, info in sorted(repos_summary.items(), key=lambda kv: (0 if kv[0] == "global" else 1, kv[0]))
    ]

    counts_by_repo = {slug: info["count"] for slug, info in repos_summary.items()}

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "total": len(files_data),
            "global": sum(1 for f in files_data if f["scope"] == "global"),
            "projet": sum(1 for f in files_data if f["scope"] == "projet"),
            "repos": counts_by_repo,
        },
        "repos": repos_list,
        "files": files_data,
    }

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"OK {len(files_data)} CLAUDE.md written to {output_path}")
    print(f"  Repos: {len(repos_list)}")
    for r in repos_list:
        print(f"    {r['count']:3d}  [{r['slug']}]  {r['path']}")


if __name__ == "__main__":
    main()
