---
name: skill-launcher
description: >-
  Génère des instructions de Projet ChatGPT prêtes à coller à partir d'un repository GitHub de skills.
  À utiliser quand on veut faire de ChatGPT le cockpit de réflexion/planification d'un projet tout en
  gardant les méthodes dans GitHub et en réservant Codex / Claude Code à l'exécution lourde.
  Ne copie jamais les skills dans les instructions : les instructions routent vers les bons SKILL.md.
---

# Skill Launcher

## Mission

Transformer un repository GitHub de compétences en **instructions courtes de Projet ChatGPT prêtes à lancer**.

Le principe :

> GitHub contient les méthodes.
> Les instructions du Projet disent à ChatGPT lesquelles lire et quand.
> Codex / Claude Code restent réservés à l'exécution qui nécessite réellement leur environnement.

Skill Launcher est volontairement simple. Il ne crée pas un nouveau système de skills et ne duplique pas le contenu des skills existants.

---

## Entrées

Récupérer ou demander uniquement ce qui manque réellement :

1. **Repository GitHub canonique** — `owner/repo`
2. **Branche canonique** — `main` par défaut si vérifiée
3. **But du Projet ChatGPT**
4. **Workflow attendu** — étapes et skills correspondants
5. **Frontière d'exécution** — ce qui reste dans ChatGPT vs ce qui part dans Codex / Claude Code
6. **Source canonique métier éventuelle** — Notion, docs, autre repo

Quand GitHub est connecté, vérifier les chemins réels avec le connecteur avant de produire les instructions.

---

## Règles

### 1. GitHub fait foi

Les skills vivent dans GitHub.

Format recommandé :

`skills/<nom-du-skill>/SKILL.md`

Références éventuelles :

`skills/<nom-du-skill>/references/`

Une copie locale peut exister comme cache ou miroir, mais **ne fait pas foi en cas de divergence**.

### 2. Les instructions du Projet sont un routeur

Ne jamais recopier le contenu complet des skills dans les instructions du Projet.

Les instructions doivent seulement dire :
- où est la source canonique ;
- quelle skill utiliser selon l'étape ;
- quand lire ses références ;
- quelle source de vérité métier respecter ;
- quand passer à un agent de code.

### 3. Charger seulement ce qui est nécessaire

Ne pas demander à ChatGPT de lire tout le repository à chaque message.

Router selon l'étape réelle de la tâche.

Exemple :

```text
matière brute → think-structure
sujet compris → linkedin-post-creator
texte stable → refine-output
post final → linkedin-visual
pré-publication → linkedin-prepublish
Taplio si utilisé → programmation après confirmation
sinon → linkedin-publish après confirmation
```

### 4. Ne pas promettre un chargement automatique natif

Formulation correcte :

> « Va lire la skill X dans le repository GitHub connecté. »

Éviter :

> « ChatGPT charge automatiquement toutes mes skills GitHub. »

Le mécanisme dépend de la connexion GitHub disponible et de ses permissions.

### 5. Séparer réflexion et exécution

Par défaut :

**ChatGPT / Projet**
- contexte ;
- recherche ;
- réflexion ;
- cadrage ;
- architecture ;
- planification ;
- diagnostic ;
- review.

**Codex / Claude Code**
- modifications importantes de fichiers ;
- terminal ;
- tests ;
- boucles longues ;
- tâches autonomes ;
- opérations nécessitant leur environnement.

Adapter cette frontière au projet réel.

---

## Format de sortie

Toujours produire deux blocs.

### A. Instructions du Projet — prêtes à coller

Courtes, opérationnelles, sans explication superflue.

Structure :

```text
SOURCE CANONIQUE DES COMPÉTENCES

Repository : <owner/repo>
Branche : <branch>

Pour chaque tâche, identifie d'abord son étape réelle puis lis uniquement la compétence nécessaire dans :
skills/<skill>/SKILL.md

En cas de divergence avec une copie locale, GitHub fait foi.

WORKFLOW
<étape> → <skill>
<étape> → <skill>

RÈGLES
- ne charge pas toutes les skills par défaut ;
- ne duplique pas leur contenu dans les instructions ;
- respecte la source canonique métier si elle existe ;
- réserve Codex / Claude Code aux tâches qui nécessitent réellement leur environnement ;
- ne publie / déploie / envoie rien sans confirmation explicite si le projet l'exige.
```

### B. Setup minimal

Rendre uniquement :
- repo à connecter ;
- skills vérifiées ;
- éventuelle source canonique complémentaire ;
- dépendance ou permission manquante.

---

## Gate final

Avant livraison :

- [ ] le repository existe ;
- [ ] les chemins des skills citées existent ;
- [ ] les instructions restent courtes ;
- [ ] aucune skill n'est dupliquée dans les instructions ;
- [ ] GitHub est clairement défini comme source canonique ;
- [ ] la frontière ChatGPT ↔ agent de code est explicite ;
- [ ] aucune capacité de connexion n'est inventée ;
- [ ] le résultat est directement copiable dans les instructions d'un Projet ChatGPT.
