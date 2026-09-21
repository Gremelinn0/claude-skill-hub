---
name: loop-creator
description: >-
  Méthode publique pour créer ou réparer une boucle de travail autonome autour d'une compétence
  existante. La boucle porte la cadence, l'état et l'arrêt ; la compétence propriétaire garde la
  méthode métier. Utiliser quand un chantier doit avancer par reprises successives sans recopier un
  énorme prompt à chaque tour.
version: 0.1.0
status: public
---

# Loop Creator

## Le problème

Le premier réflexe quand on veut faire travailler un agent en boucle est souvent d'écrire un gros
prompt de reprise :

- relis ceci ;
- fais cela ;
- respecte ces règles ;
- reprends à telle étape ;
- vérifie tel test ;
- recommence jusqu'à la fin.

Ça fonctionne au début.

Puis la méthode évolue ailleurs et le prompt copié, lui, reste figé.

Au bout de quelques semaines, la boucle rejoue proprement une version périmée du système.

## Principe

> **La boucle ne porte pas la méthode. Elle porte la cadence et l'état.**

Séparer quatre responsabilités :

1. **La compétence propriétaire** — quoi faire, comment le faire, les pièges, les tests et la définition de fini.
2. **L'état canonique** — où le chantier en est réellement et ce qu'il reste.
3. **Le journal** — ce qui a été tenté, mesuré, gardé ou abandonné.
4. **La boucle** — quand reprendre, avec quelle cadence, et quand s'arrêter.

Le prompt de reprise peut alors rester minuscule, parce qu'il recharge les sources actuelles au lieu
de recopier leur contenu.

## Avant de créer une boucle

### 1. Chercher l'existante

Même sujet + même propriétaire + même cible = **reprendre ou réparer**, jamais créer une deuxième
boucle.

Une boucle dormante reste une boucle existante.

### 2. Nommer la compétence propriétaire

Une boucle sans compétence propriétaire improvise sa méthode à chaque réveil.

Si aucune compétence / procédure n'existe encore, la construire d'abord.

### 3. Définir un résultat mesurable

Éviter :

> améliorer la lecture

Préférer :

> réduire les coupures audibles sous le seuil X sur le scénario Y

La boucle doit savoir distinguer une amélioration réelle d'une impression.

## Les 7 garanties minimales

### 1. Mesurer le vrai résultat

Mesurer l'effet réel, pas seulement un log qui affirme que tout va bien.

### 2. Prouver la mesure avant de l'utiliser

Avant d'optimiser, vérifier que l'instrument sait reconnaître :
- un cas propre ;
- un cas volontairement cassé.

Si le test ne rougit jamais, la métrique ne protège rien.

### 3. Une idée par tour

Un tour = une hypothèse = une modification = une mesure.

Sinon on ne sait plus ce qui a réellement amélioré ou cassé le résultat.

### 4. Un arrêt dur

Définir avant de commencer :
- résultat atteint ;
- nombre maximal de tours ;
- budget atteint ;
- grille épuisée ;
- blocage réel ;
- interruption humaine explicite.

Une boucle sans arrêt n'est pas autonome. Elle est juste infinie.

### 5. Pas de faux « terminé »

Une mesure impossible, polluée ou non vérifiée n'est pas une réussite.

Le statut doit pouvoir dire explicitement :
- PASS ;
- FAIL ;
- NON MESURABLE ;
- BLOQUÉ.

### 6. Un état durable, pas une mémoire de conversation

Le prochain réveil doit retrouver :
- le dernier état ;
- ce qui est déjà acquis ;
- le reliquat ;
- la prochaine action utile ;
- les preuves.

Sans relire tout le transcript précédent.

### 7. Une seule boucle par chantier

Plusieurs boucles concurrentes sur le même objet finissent par :
- rejouer les mêmes tests ;
- modifier les mêmes fichiers ;
- se contredire ;
- ne plus savoir laquelle possède la fin.

## Structure minimale

Un dossier de boucle peut rester très simple :

```text
boucle/
├── program.md
└── results.tsv
```

### program.md

Il route vers le travail ; il ne recopie pas toute la méthode.

Exemple :

```markdown
# Boucle — <sujet>

Compétence propriétaire : /<skill>

## Objectif mesurable
<résultat visé>

## Terminé quand
<critères objectifs>

## État actuel
<ce qui est acquis / restant / bloqué>

## Scope
<ce qui peut être modifié>

## Métrique
<comment observer le vrai résultat>

## Arrêt
<résultat atteint / cap / blocage / interruption>
```

### results.tsv

Une ligne par expérience :

```text
date    hypothese    changement    mesure    verdict    preuve    notes
```

Le journal porte l'historique. Le prompt de reprise n'a pas besoin de le raconter.

## Prompt de reprise

Le principe est volontairement court :

```text
/loop <cadence> /<competence> — reprends la boucle <slug> : lis l'état d'abord, une idée par tour, mesure le vrai résultat, journalise la preuve, STOP au cap.
```

Adapte la syntaxe de `/loop` au moteur disponible dans ton environnement.

Ce qui compte n'est pas la commande exacte.

Ce qui compte est que le réveil **recharge la compétence et l'état actuels** au lieu d'embarquer une
copie figée de leur méthode.

## Créer vs réparer

### CRÉER

Quand aucune boucle ne couvre encore le chantier :

1. identifier la compétence propriétaire ;
2. écrire l'objectif mesurable ;
3. écrire les critères de fin ;
4. préparer la métrique et son test positif/négatif ;
5. créer l'état + journal ;
6. définir la cadence ;
7. armer la boucle.

### RÉPARER / REPRENDRE

Quand une boucle existe déjà :

1. comprendre pourquoi elle s'est arrêtée ;
2. vérifier ce qui a changé pendant son sommeil ;
3. capitaliser les nouveaux apprentissages ;
4. corriger son état / ses critères devenus faux ;
5. conserver les preuves déjà acquises ;
6. recalculer la cadence ;
7. rallumer **la même boucle**.

Ne jamais relancer aveuglément un vieux prompt après plusieurs semaines : il décrit probablement un
monde qui n'existe plus.

## Exemple

Tu veux qu'un agent améliore automatiquement un pipeline de transformation.

Mauvaise boucle :

> « Relis toute l'architecture, applique ces 25 règles, ouvre tels fichiers, teste X, Y, Z… »

Bonne boucle :

- `/pipeline-transform` possède la méthode et les tests ;
- `program.md` dit où en est le chantier ;
- `results.tsv` conserve les expériences ;
- le réveil appelle seulement la compétence et demande de reprendre la boucle.

Quand `/pipeline-transform` est amélioré, le prochain réveil profite immédiatement de la nouvelle
version.

Aucun prompt de reprise à réécrire.

## Ce que cette ressource ne contient volontairement pas

Cette version publique décrit la méthode portable.

Elle ne publie pas :
- les hooks privés de l'auteur ;
- ses chemins de fichiers ;
- ses tableaux de bord internes ;
- ses conventions de dépôt ;
- ses métriques produit ;
- ses incidents et historiques privés.

Ces éléments sont utiles dans un environnement précis, pas dans une ressource réutilisable par tous.

## Gate avant de dire qu'une boucle est prête

- [ ] une compétence / procédure propriétaire existe ;
- [ ] aucune autre boucle ne possède déjà le même chantier ;
- [ ] l'objectif est mesurable ;
- [ ] la métrique observe le résultat réel ;
- [ ] la métrique a été testée sur un cas propre et un cas cassé ;
- [ ] les critères de fin sont écrits avant le premier tour ;
- [ ] le cap / arrêt dur est défini ;
- [ ] l'état survit à la conversation ;
- [ ] le journal permet de comprendre les expériences précédentes ;
- [ ] le prompt de reprise route vers les sources actuelles au lieu de recopier la méthode.

---

Cette ressource est une version publique et volontairement portable d'une méthode utilisée sur des
boucles de développement réelles. Elle est conçue pour être adaptée au moteur de boucle, au système
de tests et à la structure de projet de chacun.
