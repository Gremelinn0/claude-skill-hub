# Orchestration maps — Failure, Responsibility, Authority, Delegation

Charger cette référence après le pré-mortem, quand il faut transformer les risques en architecture d'exécution.

# 5. Failure Map

Chaque risque réel doit obtenir un propriétaire.

| Risque | Owner | Prévention | Détection | Fallback |
|---|---|---|---|---|
| méthode faible | skill | readiness | test sortie | réparer skill |
| métrique mensongère | harness | negative control | gate | réparer mesure |
| état perdu | state store | persistance | cold-start test | restaurer |
| collision parallèle | orchestrateur | dépendances | conflit | séquentialiser |
| apprentissage perdu | learning path | routing | audit journal | promouvoir |
| action irréversible | authority gate | permission | gate | demander validation |

Principe :

> un risque important sans owner ni contrôle = boucle pas prête.

---

# 6. Responsibility Map

Séparer les responsabilités.

~~~text
Méthode
→ compétence / procédure propriétaire

État courant
→ tracker

Historique / preuves
→ journal

Mesure
→ harness

Validation de la mesure
→ gate

Invariant déterministe
→ check / script / hook

Cadence
→ moteur de boucle

Décision globale
→ agent principal

Sous-tâche spécialisée
→ skill / agent spécialisé

Apprentissage durable
→ propriétaire canonique
~~~

Cette séparation est directement inspirée d'un principe très utile des systèmes agentiques modernes :
ne pas demander à un seul prompt de porter toutes les responsabilités.

---

# 7. Authority Map

Une boucle doit savoir ce qu'elle a le droit de faire seule.

Classer chaque action :

### AUTO
- lecture ;
- analyse ;
- test ;
- action réversible déjà autorisée.

### GATED
- publication ;
- envoi externe ;
- suppression ;
- achat / dépense ;
- déploiement sensible ;
- autre action irréversible sans politique explicite.

### FORBIDDEN
Tout ce qui est hors scope.

Une boucle techniquement parfaite mais autorisée à faire n'importe quoi n'est pas fiable.

---

# 8. Delegation Map

Ne pas faire utiliser le modèle principal pour toutes les tâches.

Pour chaque travail répété, tester cet ordre :

~~~text
1. Peut-il être mécanique ?
2. Existe-t-il un skill / agent spécialisé ?
3. Peut-il partir dans un sous-agent borné ?
4. Le main agent est-il vraiment nécessaire ?
~~~

## Mécanique d'abord

Privilégier script / test / parser / comparaison / compteur / métrique lorsque le résultat est déterministe.

Ne pas payer un LLM pour vérifier quelque chose qu'un test peut décider exactement.

## Agent spécialisé

Si une compétence sait déjà faire le travail :
→ l'appeler.

## Sous-agent borné

Bon candidat si :
- contexte limité ;
- entrée claire ;
- sortie structurée ;
- résultat vérifiable.

## Main Agent

Le garder pour :
- architecture ;
- arbitrage ;
- synthèse globale ;
- décisions ambiguës.

---

# 9. Parallélisme

Paralléliser uniquement les tâches :
- indépendantes ;
- sans état mutable commun ;
- dont les résultats peuvent être vérifiés puis intégrés séparément.

Si B dépend de A :
→ séquentiel.

Si A et B écrivent le même fichier / tracker :
→ séquentiel ou isolation explicite.

---

# 10. Choisir la puissance nécessaire

Ne pas figer des noms de modèles dans la compétence.

Classer le besoin :

### LIGHT
Extraction, tri, classification, contrôle quasi déterministe.

### STANDARD
Recherche structurée, implémentation bornée, synthèse locale.

### DEEP
Architecture, arbitrage, ambiguïté forte, synthèse globale.

Puis utiliser le modèle le moins coûteux réellement capable de satisfaire le contrat.

> cheapest capable executor

La correspondance exacte entre tiers et modèles peut évoluer avec le runtime.

---
