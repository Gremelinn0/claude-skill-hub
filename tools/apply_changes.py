#!/usr/bin/env python3
"""Lit un JSON exporté depuis skills-marketplace.html et applique les changements.

Format JSON attendu (clé `source: "skills-marketplace"` ou `"monitoring-center"`) :
- claude_md_edits[]  : nouveau contenu pour CLAUDE.md ciblés
- skills_decisions[] : actions move/duplicate/archive/store/note/flag pour skills

Workflow :
1. Backup tous les fichiers cibles dans `_archive/skill-hub-<ts>/`
2. Affiche diff résumé (avant/après)
3. Demande confirmation 1 fois pour le batch
4. Applique writes CLAUDE.md
5. Applique skills decisions
6. Affiche résumé final

Configuration via variables d'environnement :
  SKILL_HUB_PROJECTS_ROOT : racine projets (défaut: ~/PROJECTS)
  SKILL_HUB_GLOBAL_SKILLS : skills globaux (défaut: ~/.claude/skills)
  SKILL_HUB_BACKUP_DIR    : où mettre les backups (défaut: ./_archive/ relatif au repo)

Usage:
    python apply_changes.py skill-hub-decisions-*.json [--yes]
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BACKUP_ROOT = Path(os.environ.get("SKILL_HUB_BACKUP_DIR") or (SCRIPT_DIR.parent / "_archive"))
PROJECTS_ROOT = Path(os.environ.get("SKILL_HUB_PROJECTS_ROOT") or (Path.home() / "PROJECTS"))
GLOBAL_SKILLS_DIR = Path(os.environ.get("SKILL_HUB_GLOBAL_SKILLS") or (Path.home() / ".claude" / "skills"))


def slug_to_skills_dir(slug: str, repos_known: list) -> Path | None:
    """Convertit slug repo → chemin .claude/skills/ absolu."""
    if slug == "global":
        return GLOBAL_SKILLS_DIR
    repo_info = next((r for r in repos_known if r["slug"] == slug), None)
    if not repo_info:
        return None
    raw = repo_info["path"]
    # Accepte path absolu OU relatif (~/... ou relatif à PROJECTS_ROOT)
    if raw.startswith("~"):
        repo_path = Path(raw).expanduser()
    elif Path(raw).is_absolute():
        repo_path = Path(raw)
    else:
        repo_path = PROJECTS_ROOT / raw
    return repo_path / ".claude" / "skills"


def short(p: str, n: int = 70) -> str:
    if len(p) <= n:
        return p
    return "…" + p[-(n - 1):]


def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_changes.py <monitoring-changes-*.json> [--yes]")
        sys.exit(1)

    auto_yes = "--yes" in sys.argv
    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"ERR : fichier introuvable {json_path}")
        sys.exit(2)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    if data.get("source") not in ("skills-marketplace", "monitoring-center"):
        print(f"WARN : source='{data.get('source')}' (attendu 'skills-marketplace' ou 'monitoring-center'). Continue quand même.")

    md_edits = data.get("claude_md_edits", [])
    skill_decisions = data.get("skills_decisions", [])
    skill_edits = data.get("skills_edits", [])
    repos_known = data.get("repos_known", [])

    if not md_edits and not skill_decisions and not skill_edits:
        print("Aucun changement dans le JSON. Rien à appliquer.")
        return

    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_dir = BACKUP_ROOT / f"skill-hub-{ts}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # ── Preview ──
    print("=" * 70)
    print(f"Plan d'application — {json_path.name}")
    print("=" * 70)

    if md_edits:
        print(f"\n📁 CLAUDE.md à éditer ({len(md_edits)}) :")
        for e in md_edits:
            delta = e.get("new_size", 0) - e.get("previous_size", 0)
            sign = "+" if delta >= 0 else ""
            print(f"   [{e['repo']:20s}] {short(e['path'])}  ({sign}{delta} bytes)")

    if skill_edits:
        print(f"\n✏ SKILL.md à éditer inline ({len(skill_edits)}) :")
        for e in skill_edits:
            delta = e.get("new_size", 0) - e.get("previous_size", 0)
            sign = "+" if delta >= 0 else ""
            print(f"   [{e['current_repo']:20s}] {e['dir_name']}  ({sign}{delta} chars)")

    if skill_decisions:
        print(f"\n🛠 Décisions skills ({len(skill_decisions)}) :")
        for d in skill_decisions:
            action = d.get("action", "?")
            targets = d.get("target_repos", [])
            extra = ""
            if d.get("rename"): extra += " +rename"
            if d.get("rework"): extra += " +rework"
            print(f"   [{d['current_repo']:20s} → {','.join(targets) or '∅':30s}] {action:9s} {d['dir_name']}{extra}")

    print(f"\n📂 Backups → {backup_dir}")

    if not auto_yes:
        ans = input("\nAppliquer ces changements ? [y/N] ").strip().lower()
        if ans not in ("y", "o", "yes", "oui"):
            print("Annulé.")
            return

    # ── Backup CLAUDE.md ──
    backed = []
    for e in md_edits:
        src = Path(e["path"])
        if not src.exists():
            print(f"  WARN  {src} introuvable — skip")
            continue
        rel = e["repo"] + "_" + src.name
        dest = backup_dir / "claude-md" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        backed.append((src, dest))

    # ── Apply CLAUDE.md edits ──
    edit_count = 0
    for e in md_edits:
        src = Path(e["path"])
        if not src.exists():
            continue
        try:
            src.write_text(e["new_content"], encoding="utf-8")
            edit_count += 1
            print(f"  EDIT  {short(str(src))}")
        except Exception as ex:
            print(f"  FAIL  {src} : {ex}")

    # ── Apply SKILL.md edits (write new content with backup) ──
    skill_edit_done = 0
    for e in skill_edits:
        src = Path(e["current_path"])
        if not src.exists():
            print(f"  WARN  SKILL.md introuvable {src} — skip édit")
            continue
        rel = e["current_repo"] + "_" + e["dir_name"] + "_SKILL.md"
        bkp = backup_dir / "skill-md" / rel
        bkp.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, bkp)
            src.write_text(e["new_content"], encoding="utf-8")
            skill_edit_done += 1
            print(f"  EDIT-SKILL  {e['dir_name']} ({e['current_repo']})")
        except Exception as ex:
            print(f"  FAIL-SKILL  {src} : {ex}")

    # ── Apply skill decisions ──
    skill_done = 0
    skill_skipped = []
    for d in skill_decisions:
        action = d.get("action")
        dir_name = d["dir_name"]
        cur_path = Path(d["current_path"])
        cur_skill_dir = cur_path.parent
        if not cur_skill_dir.exists():
            skill_skipped.append((dir_name, "current dir not found"))
            continue

        if action == "archive":
            # Move to <repo>/.claude/skills/_archive/skills-archive/<date>/<dir>/
            arch_root = cur_skill_dir.parent / "_archive" / "skills-archive" / ts
            arch_root.mkdir(parents=True, exist_ok=True)
            dest = arch_root / dir_name
            try:
                shutil.move(str(cur_skill_dir), str(dest))
                print(f"  ARCH  {dir_name} → {short(str(dest))}")
                skill_done += 1
            except Exception as ex:
                skill_skipped.append((dir_name, f"archive fail: {ex}"))

        elif action == "move":
            target_slug = d["target_repos"][0]
            target_skills_dir = slug_to_skills_dir(target_slug, repos_known)
            if not target_skills_dir:
                skill_skipped.append((dir_name, f"target slug '{target_slug}' inconnu"))
                continue
            target_skills_dir.mkdir(parents=True, exist_ok=True)
            dest = target_skills_dir / dir_name
            if dest.exists():
                skill_skipped.append((dir_name, f"déjà présent dans {target_slug}"))
                continue
            try:
                shutil.move(str(cur_skill_dir), str(dest))
                print(f"  MOVE  {dir_name} → {target_slug}")
                skill_done += 1
            except Exception as ex:
                skill_skipped.append((dir_name, f"move fail: {ex}"))

        elif action == "duplicate":
            # Garde courant + copie dans chaque cible supplémentaire
            for target_slug in d["target_repos"]:
                if target_slug == d["current_repo"]:
                    continue
                target_skills_dir = slug_to_skills_dir(target_slug, repos_known)
                if not target_skills_dir:
                    skill_skipped.append((f"{dir_name}→{target_slug}", "slug inconnu"))
                    continue
                target_skills_dir.mkdir(parents=True, exist_ok=True)
                dest = target_skills_dir / dir_name
                if dest.exists():
                    skill_skipped.append((f"{dir_name}→{target_slug}", "déjà présent"))
                    continue
                try:
                    shutil.copytree(str(cur_skill_dir), str(dest))
                    print(f"  DUPL  {dir_name} → {target_slug}")
                    skill_done += 1
                except Exception as ex:
                    skill_skipped.append((f"{dir_name}→{target_slug}", f"copy fail: {ex}"))

        elif action == "store":
            # Move to <repo>/.claude/skills-store/<dir>/ + ajout d'une entrée INDEX.md
            store_root = cur_skill_dir.parent.parent / "skills-store"
            store_root.mkdir(parents=True, exist_ok=True)
            dest = store_root / dir_name
            if dest.exists():
                skill_skipped.append((dir_name, "déjà présent dans skills-store"))
                continue
            try:
                shutil.move(str(cur_skill_dir), str(dest))
                # Append à INDEX.md (créé si absent)
                idx = store_root / "INDEX.md"
                if not idx.exists():
                    idx.write_text(
                        "# Skill Store\n\n"
                        "> Skills dormants (pas chargés automatiquement par Claude). "
                        "Récupérer en déplaçant le dossier vers `.claude/skills/`.\n\n"
                        "| Skill | Stocké le | Note |\n|-------|-----------|------|\n",
                        encoding="utf-8"
                    )
                comment = d.get("comment", "")
                with idx.open("a", encoding="utf-8") as f:
                    f.write(f"| `{dir_name}` | {datetime.now().strftime('%Y-%m-%d')} | {comment} |\n")
                print(f"  STORE {dir_name} → {short(str(dest))}")
                skill_done += 1
            except Exception as ex:
                skill_skipped.append((dir_name, f"store fail: {ex}"))

        elif action == "note":
            # Pas d'action filesystem — juste une annotation. Affichée dans le log.
            comment = d.get("comment", "")
            print(f"  NOTE  {dir_name} ({d['current_repo']}) : {comment}")

        elif action == "flag":
            # rename / rework only — pas d'action filesystem
            tags = []
            if d.get("rename"): tags.append("rename")
            if d.get("rework"): tags.append("rework")
            print(f"  FLAG  {dir_name} (à traiter manuellement : {','.join(tags)})")

        else:
            skill_skipped.append((dir_name, f"action inconnue '{action}'"))

    # ── Recap ──
    print("\n" + "=" * 70)
    print(f"OK · {edit_count} CLAUDE.md écrits · {skill_edit_done} SKILL.md écrits · {skill_done} skills traités · backup {backup_dir.name}")
    if skill_skipped:
        print(f"\nSkippés ({len(skill_skipped)}) :")
        for name, reason in skill_skipped:
            print(f"   {name} : {reason}")

    # ── Suggestions next-step ──
    print("\nProchaines étapes recommandées :")
    print("  1. python tools/generate_skills_index.py  (régénérer le JSON)")
    print("  2. python tools/generate_claude_md_index.py")
    print("  3. (Optionnel) Redéployer la page Vercel pour refléter les changements")
    print("  4. Commit + push les CLAUDE.md modifiés (chaque repo concerné)")


if __name__ == "__main__":
    main()
