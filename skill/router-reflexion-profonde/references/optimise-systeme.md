# Méthode — Optimiser un système objectivement

Utiliser cette méthode lorsqu'un ensemble de règles, compétences, documents, processus ou composants devient difficile à maintenir.

Objectif : mesurer avant de simplifier.

## Principe

Ne jamais conclure « le système est trop complexe » uniquement à l'impression.

Mesurer d'abord :
- volume ;
- doublons ;
- éléments dormants ;
- règles ou responsabilités mal placées ;
- cartes périmées ;
- fonctions mélangées ;
- contrôles annoncés mais inexistants ;
- documentation qui ne correspond plus au comportement réel.

## Passe en 7 étapes

### 1. Cibler
Définir le système examiné et son périmètre.

### 2. Cartographier
Identifier les owners, sources de vérité, flux et artefacts réellement utilisés.

### 3. Mesurer
Produire des chiffres et observations reproductibles.

### 4. Identifier les problèmes
Chercher notamment :
- doublons ;
- bloat ;
- mauvais niveau de responsabilité ;
- cartes obsolètes ;
- jobs mélangés ;
- éléments orphelins ;
- règles en prose jamais contrôlées.

### 5. Concevoir plusieurs corrections
Ouvrir plusieurs options si le correctif n'est pas mécanique.

Pour chacune :
- bénéfice ;
- coût ;
- blast radius ;
- dette résiduelle ;
- signal de succès.

### 6. Choisir le bon niveau de correction
Corriger chez le propriétaire du problème, pas à l'endroit le plus pratique.

### 7. Re-mesurer
Reprendre les mêmes métriques après correction.

Une optimisation sans mesure avant/après reste une préférence, pas une preuve.

## Garde-fou

Ne pas transformer automatiquement chaque règle en contrôle mécanique.

Un gate est justifié surtout quand :
1. le défaut est déjà arrivé ;
2. il resterait invisible sans mesure.

Sinon, conserver une règle claire et légère.
