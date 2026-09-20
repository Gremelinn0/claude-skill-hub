---
name: import-skills-into-my-system
description: >-
  Audite un pack externe de skills avant de l'importer dans un système existant.
  Compare d'abord les architectures puis les capacités, et décide pour chaque capacité
  s'il faut garder le local, adopter l'externe, fusionner, migrer les personnalisations,
  redessiner ou écarter. Utiliser avant toute importation massive de skills.
version: 0.1.0
status: experimental
---

# Import Skills Into My System

## Mission

Importer un pack externe sans partir du principe que :

- le système actuel doit survivre ;
- le pack externe est meilleur parce qu'il est plus gros ;
- deux skills proches doivent forcément coexister ;
- « copier les fichiers » équivaut à intégrer un système.

Principe :

> Optimiser le système final, pas la survie du système actuel.

Cette ressource est une **V0 expérimentale**. Commencer par un audit et un dry-run. Ne jamais écraser
un système existant sans backup ni plan de migration explicite.

---

## Entrées

1. système actuel :
   - repo / dossier ;
   - skills ;
   - agents ;
   - hooks ;
   - règles ;
   - mémoire ;
   - outils / MCP ;
   - conventions de scope global / projet ;

2. pack externe :
   - repo / dossier ;
   - architecture ;
   - capacités ;
   - dépendances ;
   - instructions d'installation ;

3. contraintes :
   - éléments à préserver ;
   - chemins / runtime ;
   - dépendances autorisées ;
   - règles de sécurité ;
   - budget de contexte / maintenance.

---

## Étape 1 — Comparer les architectures AVANT les fichiers

Construire deux cartes :

### Système actuel
- comment les tâches sont routées ;
- où vivent les règles ;
- comment les skills sont découverts ;
- quels agents / hooks / outils existent ;
- quelles couches sont globales ou projet ;
- comment le système teste, mesure et maintient ses compétences.

### Pack externe
Même carte.

Ne pas commencer par « quels fichiers ont le même nom ? ».

Le vrai premier diagnostic est :

> Les deux systèmes résolvent-ils les mêmes responsabilités avec la même architecture ?

---

## Étape 2 — Construire la carte des capacités

Pour chaque capacité réelle, lister :

- capacité ;
- owner local ;
- owner externe ;
- chevauchement ;
- personnalisations locales ;
- dépendances ;
- qualité / maturité ;
- tests disponibles ;
- coût de maintenance ;
- conflits éventuels.

Un skill n'est pas une capacité.
Plusieurs fichiers peuvent couvrir une seule capacité.
Une capacité peut aussi être portée par une règle, un hook, un agent ou un outil.

---

## Étape 3 — Décider capacité par capacité

Une seule décision parmi :

### KEEP_LOCAL
Le système local couvre mieux la capacité.

### ADOPT_EXTERNAL
La brique externe est meilleure et peut remplacer la locale.

### MERGE_INTO_LOCAL
Le local reste owner, mais absorbe des éléments externes utiles.

### MIGRATE_CUSTOMIZATIONS
La brique externe devient owner ; les personnalisations locales utiles migrent dedans.

### REDESIGN
Ni le local ni l'externe ne doivent survivre tels quels. Concevoir une meilleure cible.

### DISCARD_EXTERNAL
La capacité externe n'apporte rien au système cible.

Ne jamais choisir automatiquement KEEP_LOCAL juste parce que le local existe déjà.

---

## Étape 4 — Dessiner le système cible

Avant toute copie, produire :

1. architecture cible ;
2. owners finaux ;
3. skills / agents / hooks / règles à conserver ;
4. éléments supprimés ;
5. personnalisations à migrer ;
6. dépendances à ajouter ;
7. chemins cibles ;
8. ordre de migration.

Le résultat attendu n'est pas :

> « voici 50 nouveaux skills installés »

mais :

> « voici le meilleur système final après comparaison ».

---

## Étape 5 — Plan de migration

Pour chaque changement :

| Capacité | Décision | Source | Cible | Personnalisation à préserver | Test | Risque |
|---|---|---|---|---|---|---|

Puis ordonner :

1. backup ;
2. création / migration des nouveaux owners ;
3. transfert des personnalisations ;
4. tests ;
5. mise à jour des routes / docs ;
6. suppression des doublons ;
7. re-scan du système ;
8. preuve qu'aucune capacité utile n'a disparu.

---

## Étape 6 — Exécution sûre

Avant écriture :

- backup obligatoire ;
- dry-run ;
- aucune suppression silencieuse ;
- aucun overwrite sans comparaison ;
- aucun import massif « au cas où » ;
- préserver les personnalisations explicitement utiles ;
- documenter les décisions REDESIGN et DISCARD.

Après écriture :

- lancer les tests ;
- vérifier les routes ;
- vérifier les dépendances ;
- rechercher les doublons ;
- vérifier que chaque capacité a un owner clair ;
- comparer le système final au plan cible.

---

## Sortie

Toujours produire :

### 1. Diagnostic architecture
Local vs externe.

### 2. Matrice de décision
Une ligne par capacité.

### 3. Système cible
Owners et structure finale.

### 4. Plan de migration
Ordonné et exécutable.

### 5. Risques / bloqueurs
Ce qui ne peut pas être tranché sans intervention humaine.

### 6. Résultat de validation
- capacités perdues : 0 ou liste explicite ;
- doublons restants ;
- routes cassées ;
- dépendances manquantes ;
- tests passés / échoués.

---

## Gate final

- [ ] architectures comparées avant les fichiers ;
- [ ] capacités cartographiées ;
- [ ] aucune préférence automatique pour le local ou l'externe ;
- [ ] une décision unique par capacité ;
- [ ] personnalisations locales préservées ou explicitement abandonnées ;
- [ ] système cible défini avant migration ;
- [ ] backup / dry-run prévus ;
- [ ] tests définis ;
- [ ] doublons et routes vérifiés après migration.

## Limite actuelle

Cette version est une **V0 méthodologique**. Elle formalise le raisonnement d'import et de migration,
mais ne garantit pas qu'un pack tiers est sûr, compatible ou de qualité. L'audit du code et des
dépendances du pack reste nécessaire.
