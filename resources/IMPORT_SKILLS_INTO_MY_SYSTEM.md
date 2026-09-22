---
name: import-skills-into-my-system
description: >-
  Quand vous avez déjà un système de skills / agents / hooks / règles et que vous voulez l'améliorer
  à partir d'une architecture externe comme ECC sans tout empiler → audite l'existant, fige les sources
  primaires de la référence, construit une architecture cible, décide capacité par capacité quoi
  conserver / remplacer / fusionner / migrer / redessiner / supprimer, puis produit un plan de migration
  réversible et un rapport de validation. À utiliser avant toute migration architecturale ou import massif.
version: 0.2.1
status: experimental
---

# Import Skills Into My System

## Mission

Prendre un système agentique existant et le **faire évoluer vers une meilleure architecture de référence**.

Par défaut, la référence est **Everything Claude Code (ECC)**, mais la méthode peut être appliquée à un autre système documenté.

Le but n'est plus de mettre deux systèmes sur un pied d'égalité et de choisir quelques bonnes idées dans chacun.

Le workflow est :
```text
SYSTÈME ACTUEL
→ ARCHITECTURE DE RÉFÉRENCE
→ DIAGNOSTIC DES ÉCARTS
→ DÉCISIONS CAPACITÉ PAR CAPACITÉ
→ ARCHITECTURE CIBLE
→ MIGRATION
→ VALIDATION
```

Principe :

> La comparaison sert au diagnostic. La migration vers le meilleur système cible est le résultat.

Cette ressource est une **V0.2 expérimentale**. Toujours commencer par un audit, figer la version de la référence, faire un backup et produire un dry-run avant toute mutation.
---
## Quand l'utiliser

Utiliser ce skill quand :

- un système existant contient déjà des skills, agents, hooks, règles, mémoire ou conventions personnalisées ;
- un système externe paraît mieux structuré et vous voulez **migrer vers ses principes**, pas seulement copier ses fichiers ;
- vous hésitez entre garder une brique locale, adopter l'externe, fusionner les deux ou reconstruire ;
- vous voulez intégrer ECC dans un environnement déjà personnalisé sans perdre ce qui fonctionne ;
- vous avez importé plusieurs packs et l'architecture commence à devenir ambiguë.

Ne pas l'utiliser pour :

- installer un pack neuf dans un environnement vide sans personnalisation ;
- comparer deux repos uniquement pour produire un rapport sans intention de migration ;
- copier aveuglément tous les skills d'ECC ;
- supprimer des briques locales sans preuve de remplacement.
---
## Installation / utilisation rapide

Ce fichier est autonome : il n'exige aucun script fourni avec cette ressource.

### Claude Code

Copier ce fichier comme :
```text
.claude/skills/import-skills-into-my-system/SKILL.md
```

pour un usage projet, ou dans votre surface de skills utilisateur si vous voulez l'utiliser sur plusieurs dépôts.

### Autres harnesses

Placer le contenu dans la surface de skills / instructions réutilisables officiellement supportée par votre harness. Les chemins exacts diffèrent selon l'outil : ne pas inventer un chemin de compatibilité.

### Invocation conseillée

Donner au skill :

1. le chemin / repo du système actuel ;
2. la référence à utiliser — ECC par défaut ;
3. les contraintes non négociables ;
4. l'autorisation ou non d'écrire.

Exemple de demande :
```text
Analyse mon système actuel et migre-le vers les principes d'architecture ECC.

Commence en dry-run.
N'écris rien avant d'avoir produit :
REFERENCE_LOCK
CURRENT_ARCHITECTURE
TARGET_ARCHITECTURE
GAP_MAP
DECISION_MATRIX
MIGRATION_PLAN

Préserve explicitement mes personnalisations utiles.
```
---
## Prérequis et dépendances

Requis :

- accès en lecture au système actuel ;
- accès en lecture aux sources de référence ;
- Git ou un mécanisme équivalent pour identifier la version de la référence ;
- capacité à sauvegarder / revenir en arrière avant toute mutation.

Optionnel pour l'exécution :

- accès en écriture au dépôt cible ;
- tests / linters / scripts de vérification propres au système cible ;
- outils de recherche dans le dépôt.

Le skill ne dépend d'aucun outil privé de Florent.
---
## Ce que « migrer vers ECC » veut dire

Cela ne veut **pas** dire :

- recopier les dossiers ECC ;
- installer ses 292 skills ;
- remplacer automatiquement le local par l'externe ;
- imposer Claude Code comme unique surface ;
- supprimer une personnalisation locale qui fonctionne mieux.

Cela veut dire appliquer les **principes architecturaux vérifiés dans les sources ECC** à son propre système :

- responsabilités séparées ;
- skills comme méthodes spécialisées chargées à la demande ;
- agents / sub-agents comme unités d'exécution spécialisées ;
- commands comme points d'entrée quand ils sont utiles ;
- routing / orchestration explicites ;
- rules limitées aux contraintes durables ;
- hooks pour les contrôles mécaniques ;
- mémoire séparée du suivi opérationnel et de la source canonique ;
- apprentissage séparé de la mémoire ;
- verification loops avant « done » ;
- un propriétaire canonique par fait / responsabilité ;
- adapters quand plusieurs harnesses doivent utiliser le même système ;
- sécurité appliquée au harness lui-même.

La référence donne la **forme cible**. Le système local fournit les capacités et personnalisations qu'il serait dangereux de perdre.
---
## Sources de référence ECC — primaires

Ne pas utiliser une synthèse secondaire comme seule source.

Pour chaque migration ECC, vérifier directement au minimum :

- Repository : https://github.com/affaan-m/ECC
- README : https://github.com/affaan-m/ECC/blob/main/README.md
- Reference Architecture : https://github.com/affaan-m/ECC/blob/main/docs/ECC-2.0-REFERENCE-ARCHITECTURE.md
- Hooks : https://github.com/affaan-m/ECC/blob/main/hooks/README.md
- Living Docs Governance : https://github.com/affaan-m/ECC/blob/main/skills/living-docs-governance/SKILL.md
- Unified Memory : https://github.com/affaan-m/ECC/blob/main/skills/unified-memory/SKILL.md
- Continuous Learning v2 : https://github.com/affaan-m/ECC/blob/main/skills/continuous-learning-v2/SKILL.md
- Commands Quick Reference : https://github.com/affaan-m/ECC/blob/main/COMMANDS-QUICK-REF.md

ECC évolue vite. Au début de chaque run :

1. relever le commit / tag / date de la référence réellement lue ;
2. conserver ces pointeurs dans le rapport ;
3. ne pas présenter comme principe stable un détail qui n'existe que dans une version ancienne.

**Snapshot utilisé pour relire cette V0.2.1 :**
`affaan-m/ECC@bf70150eb2df8070024e5bdf08e4aa08959e2735` — vérifié le 2026-09-22.

Ce snapshot documente la version publique de ce skill. Il ne remplace jamais le `REFERENCE_LOCK` d'un run futur.
---
## Entrées

### 1. Système actuel

Cartographier au minimum :

- instructions / constitution ;
- skills ;
- agents / sub-agents ;
- commands / points d'entrée ;
- routing / orchestration ;
- rules ;
- hooks ;
- memory ;
- learning / capitalisation ;
- tracker / état opérationnel ;
- documentation canonique ;
- verification loops / tests / QA ;
- outils / MCP ;
- sécurité ;
- adapters / surfaces Claude Code, Codex, Cursor, etc. ;
- scopes global / projet ;
- personnalisations importantes.

### 2. Architecture de référence

Par défaut : ECC.

Extraire **les responsabilités et principes**, pas uniquement les noms de fichiers.

### 3. Contraintes

- éléments explicitement intouchables ;
- runtime / OS / harnesses ;
- dépendances autorisées ;
- règles de sécurité ;
- compatibilité ;
- budget de contexte ;
- coût de maintenance ;
- migration progressive ou big bang interdit.
---
# Workflow

## Étape 0 — Figer la référence

Avant de comparer :

- identifier la version / commit de la référence ;
- conserver les URLs primaires consultées ;
- noter les capacités ou parties de la référence non vérifiées.

Sortie :
```text
REFERENCE
repo:
commit/tag:
date:
sources primaires:
zones non vérifiées:
```
---
## Étape 1 — Extraire l'architecture cible depuis la référence

Construire une carte des responsabilités.

Pour ECC, partir au minimum de :

| Responsabilité | Primitive / owner de référence |
|---|---|
| Méthode spécialisée | Skill |
| Unité d'exécution | Agent / sub-agent |
| Point d'entrée | Command / interface |
| Choix de l'acteur / ordre | Routing / orchestration |
| Contrainte durable | Rule |
| Contrôle mécanique | Hook / test / gate |
| Contexte durable | Memory |
| Apprentissage | Learning / instincts |
| État réel du travail | Tracker / runtime state |
| Vérité gouvernée | Documentation / source canonique |
| Preuve de fin | Verification loop |
| Portage multi-harness | Adapter |
| Sécurité du harness | Security / AgentShield |

Ne pas supposer qu'un dossier précis doit exister dans le système cible.

La question est :

> Quelle responsabilité doit exister, qui en est propriétaire et comment est-elle vérifiée ?
---
## Étape 2 — Auditer le système actuel

Pour chaque responsabilité :

- owner actuel ;
- emplacement ;
- mécanisme de déclenchement ;
- portée ;
- dépendances ;
- personnalisations locales ;
- preuve / tests ;
- doublons ;
- conflits ;
- coût de contexte ;
- maintenance ;
- état : solide / fragile / absent / ambigu.

Ne pas commencer par les noms de fichiers.
---
## Étape 3 — Construire la GAP MAP

Comparer le système actuel à la cible de référence.

Pour chaque responsabilité / capacité :

| Responsabilité | Référence | Local | Écart | Risque | Action candidate |
|---|---|---|---|---|---|

Types d'écarts fréquents :

- capacité absente ;
- mauvaise primitive ;
- plusieurs owners ;
- règle qui devrait être un hook ;
- mémoire utilisée comme source de vérité ;
- tracking mélangé à la documentation ;
- skill utilisé comme agent ;
- command créée pour chaque skill ;
- contrôle uniquement textuel alors qu'il peut être mécanique ;
- architecture mono-harness alors que plusieurs adapters sont nécessaires ;
- personnalisation utile cachée dans une brique à remplacer.
---
## Étape 4 — Décider capacité par capacité

Une seule décision principale parmi :

### KEEP_LOCAL
Le local satisfait déjà le principe cible et reste meilleur ou plus adapté.

### ADOPT_REFERENCE
Adopter la brique ou le pattern de la référence.

### MERGE
Conserver un owner principal et intégrer les éléments utiles de l'autre côté.

### MIGRATE_CUSTOMIZATIONS
La brique cible devient owner ; les personnalisations locales utiles migrent dedans.

### REDESIGN
Ni l'implémentation locale ni celle de référence ne conviennent telles quelles. Reconstruire selon le principe cible.

### DISCARD
Supprimer une brique devenue redondante, mauvaise ou inutile.

Règle :

> L'architecture de référence gagne sur la structure uniquement quand le principe est réellement vérifié et pertinent. Une meilleure personnalisation locale doit survivre.

### Critère de décision minimal

Pour chaque capacité, justifier la décision avec au moins :

- **preuve locale** : fichier / comportement / test / règle réellement présent ;
- **preuve référence** : source primaire correspondant au pattern retenu ;
- **raison de migration** : quel problème concret la décision corrige ;
- **non-perte** : quelles personnalisations doivent survivre ;
- **preuve de fin** : comment vérifier après migration que la capacité fonctionne encore.

Une décision sans preuve devient `UNRESOLVED`, pas une supposition élégante.
---
## Étape 5 — Dessiner l'architecture cible AVANT les mutations

Produire :

1. responsabilités finales ;
2. owner unique de chacune ;
3. routes / orchestration ;
4. rules réellement permanentes ;
5. hooks / gates mécaniques ;
6. mémoire ;
7. learning ;
8. tracking ;
9. documentation canonique ;
10. adapters ;
11. sécurité ;
12. éléments locaux préservés ;
13. éléments à supprimer.

Le résultat attendu n'est pas :

> « ECC installé par-dessus mon système »

mais :

> « mon système reconstruit selon une architecture de référence, avec mes bonnes personnalisations conservées ».
---
## Étape 6 — Plan de migration

Pour chaque changement :

| Responsabilité / capacité | Décision | Source actuelle | Cible | Personnalisation à préserver | Preuve | Risque |
|---|---|---|---|---|---|---|

Ordre recommandé :

1. backup ;
2. créer les nouveaux owners / nouvelles structures ;
3. migrer les personnalisations ;
4. mettre à jour routing et pointeurs ;
5. ajouter hooks / gates / tests nécessaires ;
6. vérifier les adapters ;
7. basculer les consommateurs ;
8. supprimer les anciens doublons ;
9. mettre à jour la documentation canonique ;
10. re-scan complet.

Préférer une migration par lots réversibles à une réécriture opaque.
---
## Étape 7 — Exécution sûre

Avant écriture :

- backup obligatoire ;
- dry-run ;
- diff du plan ;
- aucune suppression silencieuse ;
- aucun overwrite sans lecture de la cible ;
- aucun import massif « au cas où » ;
- aucune copie de tout ECC si seules certaines responsabilités manquent.

Pendant :

- un lot cohérent à la fois ;
- conserver une possibilité de rollback ;
- tester après chaque changement structurel ;
- ne pas supprimer l'ancien owner avant que le nouveau soit prouvé.
---
## Étape 8 — Validation

Après migration, prouver au minimum :

### Architecture
- chaque responsabilité nécessaire a un owner ;
- pas de double owner implicite ;
- routing cohérent ;
- pas de primitive manifestement mal utilisée.

### Non-perte
- personnalisations locales utiles conservées ;
- capacités utiles perdues = 0 ou liste explicitement acceptée ;
- dépendances critiques présentes.

### Vérification
- tests / gates concernés passent ;
- hooks réellement chargés ;
- routes réellement atteignables ;
- docs pointent vers les sources canoniques ;
- memory ≠ tracker ≠ vérité canonique ;
- adapters cohérents avec les harnesses réellement utilisés.

### Nettoyage
- doublons restants explicités ;
- anciennes routes supprimées ;
- fichiers / owners obsolètes retirés ;
- aucun ancien système laissé actif « au cas où » sans raison.

### Stop conditions

S'arrêter avant mutation et demander un arbitrage humain si :

- la référence contredit une contrainte métier / sécurité non négociable ;
- deux owners candidats sont réellement équivalents et le choix change le comportement public ;
- une personnalisation locale importante ne peut pas être comprise ou testée ;
- le backup / rollback n'est pas fiable ;
- une suppression détruirait une capacité sans remplaçant prouvé.
---
# Sortie obligatoire

## 1. REFERENCE_LOCK
Version et sources primaires.

## 2. CURRENT_ARCHITECTURE
Carte du système actuel.

## 3. TARGET_ARCHITECTURE
Architecture cible dérivée de la référence.

## 4. GAP_MAP
Écarts entre actuel et cible.

## 5. DECISION_MATRIX
KEEP_LOCAL / ADOPT_REFERENCE / MERGE / MIGRATE_CUSTOMIZATIONS / REDESIGN / DISCARD.

## 6. MIGRATION_PLAN
Ordre exact, risques, rollback, preuves.

## 7. VALIDATION_REPORT
Non-perte, doublons, routes, tests, documentation, adapters.

### Format compact attendu

```text
REFERENCE_LOCK
- repo:
- commit/tag:
- sources:
- non vérifié:

CURRENT_ARCHITECTURE
- ...

TARGET_ARCHITECTURE
- ...

GAP_MAP
| responsabilité | local | référence | écart | risque |

DECISION_MATRIX
| capacité | décision | preuve locale | preuve référence | personnalisation à préserver | preuve de fin |

MIGRATION_PLAN
1. ...
2. ...

VALIDATION_REPORT
- capacités perdues:
- doublons restants:
- routes cassées:
- tests:
- rollback:
```
---
# Gate final

- [ ] référence figée et sourcée depuis les fichiers primaires ;
- [ ] responsabilités extraites avant comparaison des fichiers ;
- [ ] système actuel cartographié ;
- [ ] architecture cible définie avant mutation ;
- [ ] une décision par responsabilité / capacité ;
- [ ] personnalisations locales explicitement traitées ;
- [ ] aucune copie aveugle de l'arborescence de référence ;
- [ ] backup et dry-run ;
- [ ] migration réversible par lots ;
- [ ] preuves de fonctionnement après chaque lot ;
- [ ] aucun double owner implicite restant ;
- [ ] rapport final de non-perte.

## Exemple minimal

Système actuel :
```text
CLAUDE.md contient 40 règles
12 skills portent à la fois méthode + contrôle
aucun hook
une MEMORY.md sert aussi de tracker
```

Référence ECC :
```text
rules = contraintes durables
skills = méthodes
hooks = contrôles mécaniques
memory ≠ tracker ≠ source canonique
```

Exemple de décisions possibles :
```text
coding-standards → KEEP_LOCAL
pre-commit-checks → REDESIGN en hooks
memory/task-status → REDESIGN en deux owners
custom-sales-skill → KEEP_LOCAL
review workflow → MIGRATE_CUSTOMIZATIONS vers une boucle de review séparée
```

Le résultat n'est pas « installer ECC », mais **rendre les responsabilités du système cible plus explicites et vérifiables**.
---
## Statut de validation de cette ressource

- structure / sources ECC : relues sur sources primaires le 2026-09-22 ;
- portabilité : aucune dépendance privée volontaire ;
- sécurité : backup + dry-run + rollback obligatoires ;
- méthode : **expérimentale** ;
- migration complète end-to-end avec cette V0.2.1 : **pas encore revendiquée comme éprouvée**.

Ne pas retirer ce statut tant qu'un cas réel n'a pas produit un `VALIDATION_REPORT` complet.
---
## Limite actuelle

Cette V0.2 formalise une migration **architecturale guidée par une référence**.

Elle ne prouve pas automatiquement que toute décision d'ECC convient à votre contexte. ECC reste une source de patterns et une architecture de référence, pas une vérité universelle.

Les choix de runtime, sécurité, compatibilité et coût doivent être validés dans le système cible réel.
