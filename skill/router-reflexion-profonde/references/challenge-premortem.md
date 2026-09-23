# Méthode — Pré-mortem adversarial

Utiliser cette méthode lorsqu'un plan, une architecture ou une stratégie existe déjà mais n'est pas encore engagée.

Objectif : chercher activement les raisons concrètes pour lesquelles le plan pourrait échouer avant de l'exécuter.

## Méthode en 6 étapes

### 1. Figer la thèse

Formuler le plan en 1 ou 2 phrases falsifiables.

Exemple :
> Nous allons faire X en modifiant Y pour obtenir Z.

Si la thèse ne peut pas être formulée clairement, revenir au cadrage.

### 2. Supposer l'échec

Se placer mentalement après l'échec :

> Le plan a échoué. Pourquoi ?

Cette formulation évite de demander simplement « quels sont les risques ? », qui produit souvent une liste générique.

### 3. Choisir les angles adversariaux

Prendre uniquement les angles qui peuvent réellement mordre sur le cas :
- runtime ;
- régressions ;
- architecture ;
- dépendances ;
- adoption ;
- economics ;
- marché ;
- organisation ;
- sécurité ;
- réversibilité.

### 4. Attaquer

Chaque angle doit chercher à réfuter la thèse.

Une objection utile contient au moins un élément concret :
- scénario ;
- preuve ;
- mesure ;
- dépendance ;
- contradiction.

### 5. Trier

Classer les objections :

- **Bloquant** — détruit la thèse.
- **À mitiger** — réel mais traitable.
- **Bruit** — théorique, hors scope ou déjà couvert.

### 6. Rendre un verdict

Choisir :

- **PIVOTER** — la thèse ne survit pas ;
- **DURCIR PUIS ENGAGER** — le plan tient après ajout de protections ;
- **ENGAGER** — aucun défaut matériel n'a été trouvé.

## Garde-fou

Ne jamais inventer des objections pour « faire sérieux ».

Un pré-mortem utile peut conclure qu'aucun bloqueur important n'a été trouvé.
