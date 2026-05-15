---
name: skill-hub
description: Manage your Claude Code skills via a self-hosted visual hub. Regenerate the skills/CLAUDE.md indexes, serve the marketplace page locally or on Vercel, consume the exported decisions JSON to apply move/duplicate/archive/store/note actions across your repos. Triggers — "/skill-hub", "ouvre mon hub de skills", "ménage skills", "trier mes skills", "audit skills perso".
---

# /skill-hub — Pilotage de ton hub de skills

Skill compagnon de [`claude-skill-hub`](https://github.com/Gremelinn0/claude-skill-hub) (le repo public). Tu l'invoques quand tu veux :
- **Faire le ménage** de tes skills (trier garder/store/archiver, déplacer entre dépôts, dupliquer, noter).
- **Éditer un CLAUDE.md** par dépôt sans ouvrir un IDE.
- **Régénérer** l'index quand tu as créé/renommé/supprimé un skill.

Le skill orchestre 4 phases : régénérer les données → ouvrir la page → consommer l'export → appliquer + redéployer.

## §1 Quand invoquer

- `/skill-hub` — quand tu veux ouvrir ton hub et faire un tri.
- "ménage skills" / "trier mes skills" / "audit skills perso" — verbal trigger.
- Routine périodique (mensuelle conseillée) — le drift skills est lent, pas besoin chaque semaine.
- Après création/rename massif de skills (>5 modifs en une session).

## §2 Prérequis (one-time setup)

1. **Cloner** le repo `claude-skill-hub` quelque part sur ton disque :
   ```bash
   git clone https://github.com/Gremelinn0/claude-skill-hub.git ~/claude-skill-hub
   ```
2. **Variables d'environnement** (optionnel — défauts sensés sinon) :
   ```bash
   export SKILL_HUB_PROJECTS_ROOT="$HOME/PROJECTS"        # racine de tes projets
   export SKILL_HUB_GLOBAL_SKILLS="$HOME/.claude/skills"  # skills globaux
   ```
3. **Python 3.8+** disponible (les scripts sont vanilla, aucune dépendance externe).
4. **(Optionnel) Vercel** : `npm i -g vercel` si tu veux déployer ta page en URL persistante au lieu de la servir en local.

## §3 Workflow — les 4 phases

### Phase 0 — Régénérer les données (NON-NÉGOCIABLE avant tri)

Toujours partir d'un index frais. Sinon tu décides sur des skills qui n'existent plus, ou tu rates ceux que tu viens de créer.

```bash
cd <repo-claude-skill-hub>
python tools/generate_skills_index.py
python tools/generate_claude_md_index.py
```

Output : `hub/skills-data.json` et `hub/claude-md-data.json` à jour.

### Phase 1 — Ouvrir la page

Deux options selon ton setup :

**Option A — Local (pas de déploiement)**
```bash
cd <repo>/hub && python -m http.server 3460
# puis ouvre http://localhost:3460/skills-marketplace.html
```

**Option B — Vercel (URL persistante, partageable, accessible depuis tout PC)**
```bash
cd <repo>/hub
npx vercel deploy --prod --yes
# (première fois : npx vercel link pour rattacher au projet Vercel)
```

### Phase 2 — Florent trie, exporte le JSON

L'utilisateur navigue la page : liste master-détail, filtres, recherche, ouvre chaque skill, décide :
- **Garder** (rien à faire)
- **Mettre en réserve** (mv → `<repo>/.claude/skills-store/<dir>/`)
- **Archiver** (mv → `<repo>/.claude/skills/_archive/skills-archive/<date>/<dir>/`)
- **Déplacer** vers un autre dépôt (mv → `<target-repo>/.claude/skills/<dir>/`)
- **Dupliquer** vers plusieurs dépôts (copytree, original gardé)
- **Note** (commentaire seul, pas d'action filesystem)

Chaque décision peut porter un **commentaire** libre. Une fois prêt : bouton **"Télécharger l'export JSON"** → fichier `skill-hub-decisions-<ts>.json`.

### Phase 3 — Appliquer

L'utilisateur partage le fichier exporté avec toi (Claude) :

```bash
python tools/apply_changes.py <fichier>.json
```

Le script :
1. **Backup** tous les fichiers cibles dans `_archive/skill-hub-<ts>/`.
2. **Preview** : liste les actions prévues, demande confirmation `[y/N]`.
3. **Applique** :
   - `archive` → move vers `_archive/skills-archive/<date>/`.
   - `move` → move vers `<target>/.claude/skills/`.
   - `duplicate` → copytree vers chaque target (original gardé).
   - `store` → move vers `<repo>/.claude/skills-store/` + append à `INDEX.md`.
   - `note` → log uniquement, pas d'action filesystem.
   - `flag` (rename/rework) → log seulement.
4. **CLAUDE.md edits** : écrit les nouveaux contenus avec backup auto.
5. **Récap final** : ce qui a été fait, ce qui a été skippé.

Flag `--yes` pour sauter la confirmation interactive (CI / batch).

### Phase 4 — Régénérer + redéployer

Après application des changements, l'index doit refléter la nouvelle réalité :

```bash
python tools/generate_skills_index.py
python tools/generate_claude_md_index.py
# si déployé sur Vercel :
cd hub && npx vercel deploy --prod --yes
```

Commit + push les CLAUDE.md modifiés (chaque repo concerné — pas tous dans le même).

## §4 Format de l'export JSON

Compatible `apply_changes.py`. Schéma :

```json
{
  "source": "skills-marketplace",
  "exported_at": "<ISO>",
  "repos_known": [{"slug": "<repo>", "path": "<chemin>"}],
  "_note": "...",
  "skills_decisions": [
    {
      "dir_name": "<skill-dir>",
      "name": "<skill-name>",
      "current_repo": "<repo-slug>",
      "current_path": "<absolute SKILL.md>",
      "target_repos": ["<target-slug>"],
      "archive": false,
      "rename": false,
      "rework": false,
      "action": "archive | move | duplicate | store | note | flag",
      "comment": "<optionnel — texte libre>"
    }
  ],
  "claude_md_edits": [
    {
      "repo": "<slug>",
      "path": "<absolute CLAUDE.md>",
      "new_content": "<contenu modifié>",
      "edited_at": "<ISO>",
      "previous_size": N,
      "new_size": N
    }
  ]
}
```

## §5 Personnaliser

- **`hub/skills-usage-map.json`** : mappe `<repo>::<skill>` → catégorie usage (ex: "Tester & valider", "Coder une feature"). Édite à la main pour TES domaines.
- **`hub/skills-marketplace.html`** § `const RECOS = { … }` : pré-remplir des recommandations 💡 sur des skills donnés (action + raison).
- **Couleurs / typo** : palette dans le `:root` du CSS (variables `--bg`, `--accent`, `--serif`...).

## §6 Anti-patterns

- ❌ Trier sans Phase 0 (régénération fresh) — tu décides sur des données stales.
- ❌ Appliquer l'export sans vérifier la preview — toujours laisser apply_changes.py confirmer.
- ❌ Hard-coder ses chemins dans les scripts — utilise les env vars `SKILL_HUB_*`.
- ❌ Oublier le commit + push des CLAUDE.md modifiés après apply_changes — les changements ne se synchronisent pas sur ton autre PC sinon.
- ❌ Stocker un skill puis l'oublier pendant 6 mois sans le ressortir — `skills-store/INDEX.md` est ta mémoire, consulte-la.

## §7 Auto-amélioration

À chaque usage :
- Si tu vois des skills sans description, profite-en pour rajouter une description dans leur frontmatter.
- Si tu te répètes la même décision sur N skills similaires, ajoute-les à `RECOS` dans la page pour la prochaine fois.
- Si tu ranges souvent des skills dans une nouvelle catégorie, ajoute-la dans `skills-usage-map.json` § `categories_order`.
