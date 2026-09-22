---
name: loop-creator
description: >-
  Quand un utilisateur veut créer, reprendre, réparer ou optimiser une boucle autonome, une boucle
  AutoResearch, un agent qui doit progresser par reprises successives ou un chantier qui doit continuer
  jusqu'à un résultat mesuré → architecturer la boucle autour d'une compétence / procédure propriétaire :
  readiness, prémortem, délégation, mesure, état, apprentissage, dry run et arrêt. Réutiliser l'existant ;
  ne jamais recopier toute la méthode dans le prompt de reprise.
version: 0.2.0
status: public
---

# Loop Creator

## Mission

Transformer un objectif + une compétence / procédure propriétaire en une boucle autonome qui peut :
- reprendre sans transcript géant ;
- savoir où elle en est ;
- déléguer intelligemment ;
- mesurer un vrai résultat ;
- capitaliser ce qu'elle apprend ;
- s'arrêter proprement.

Principe :

> La méthode vit dans la compétence. La boucle organise la répétition autour d'elle.

Une boucle n'est pas une deuxième méthode métier.

---

# 1. Avant toute chose : créer ou reprendre ?

Chercher si une boucle existe déjà pour :
- le même objectif ;
- la même compétence propriétaire ;
- le même état canonique.

Si oui :
→ réparer / reprendre la même boucle.

Si non :
→ créer.

Une boucle dormante reste une boucle existante.

Ne jamais créer une jumelle simplement parce que l'ancienne est imparfaite.

---

# 2. Nommer la compétence propriétaire

Question :

> Quelle compétence / procédure sait réellement faire le travail que la boucle va répéter ?

Sans owner clair, la boucle improvise sa méthode à chaque reprise.

Si aucune compétence n'existe :
- trouver une procédure existante à étendre ;
- ou créer / améliorer une compétence avant de lancer la boucle.

Si Anthropic skill-creator est disponible, l'utiliser pour cette étape :
https://github.com/anthropics/skills/tree/main/skills/skill-creator

Loop Creator ne doit pas écrire une mini-méthode parallèle dans son tracker.

---

# 3. Skill Readiness Gate

Avant de faire tourner une méthode des dizaines de fois, vérifier qu'elle supporte réellement l'autonomie.

La compétence doit répondre à ces questions :

### Méthode
Sait-elle quoi faire ?

### Cold start
Une nouvelle session peut-elle agir sans contexte caché ?

### DONE
Sait-elle reconnaître un résultat terminé ?

### Preuve
Existe-t-il une preuve observable plutôt qu'un simple « ça a l'air bon » ?

### Failures
Les principaux pièges sont-ils connus ou détectables ?

### Dependencies
Les outils, fichiers et permissions nécessaires sont-ils réellement disponibles ?

### Scope
Sait-elle ce qu'elle peut et ne peut pas toucher ?

### Réutilisabilité
La méthode est-elle durable, séparée de l'état particulier du chantier ?

Si un critère critique échoue :

> réparer la compétence d'abord.

Puis refaire le gate une fois.

Ne pas entrer dans une boucle infinie où Loop Creator réécrit continuellement la compétence qu'il essaie de boucler.

---

# 4. Faire un pré-mortem

Avant d'armer la boucle, supposer :

> « Elle a tourné plusieurs heures et elle a échoué. Pourquoi ? »

Chercher les vrais scénarios d'échec :
- mauvaise métrique ;
- faux DONE ;
- boucle qui tourne sans apprendre ;
- skill incomplet ;
- état perdu ;
- outil indisponible ;
- action hors scope ;
- coût trop élevé ;
- sous-agent qui ment sur son résultat ;
- collision entre tâches parallèles ;
- apprentissage jamais capitalisé ;
- absence de condition d'arrêt.

Pour une boucle simple, 3 causes sérieuses suffisent.

Pour une boucle longue, coûteuse ou risquée, faire un vrai pré-mortem adversarial multi-angle.

---

# 5. Transformer les risques en architecture

Après le pré-mortem, lire references/orchestration.md.

Construire quatre cartes :
- Failure Map — chaque risque a un owner, une prévention, une détection et un fallback ;
- Responsibility Map — une responsabilité = un propriétaire ;
- Authority Map — AUTO / GATED / FORBIDDEN ;
- Delegation Map — mécanique → skill/agent spécialisé → sous-agent borné → main agent.

La référence porte aussi les règles de parallélisme et les tiers LIGHT / STANDARD / DEEP.

# 11. Les contrats de boucle

Le format de stockage est libre.

La boucle doit seulement satisfaire les contrats suivants.

## Goal Contract

- objectif observable ;
- source / raison ;
- scope ;
- définition de fini.

## State Contract

Le prochain tour doit retrouver :
- statut ;
- acquis ;
- restant ;
- prochaine action ;
- bloqueurs ;
- cap.

## Evidence Contract

Chaque unité de travail conserve :
- action / hypothèse ;
- changement ;
- résultat ;
- preuve ;
- verdict ;
- apprentissage éventuel.

## Measurement Contract

- baseline ;
- métrique du vrai résultat ;
- cas positif ;
- cas volontairement mauvais ;
- seuil de succès.

Une métrique qui ne sait jamais échouer n'est pas une métrique de confiance.

## Stop Contract

Définir avant le premier tour :
- résultat atteint ;
- nombre / coût / temps maximal ;
- stagnation ;
- espace de recherche épuisé ;
- blocage non levable ;
- interruption humaine.

---

# 12. Adapter AutoResearch

Pour une boucle expérimentale de développement, tuning ou recherche :

→ lire references/autoresearch.md

Le mapping typique devient :

~~~text
program.md = état
results.tsv = journal
1 hypothèse = 1 unité de travail
commit = transaction / preuve
KEEP / DISCARD = verdict
~~~

Cette structure n'est PAS obligatoire pour toutes les boucles.

---

# 13. Learning Promotion

Une observation ponctuelle reste dans le journal.

Elle devient un apprentissage durable seulement si elle est :
- suffisamment prouvée ;
- généralisable ;
- utile au-delà du tour courant.

Puis router :

~~~text
nouvelle méthode
→ Skill

invariant
→ Rule / règle durable

contrôle déterministe
→ Check / Hook / Script

connaissance métier
→ Documentation / Memory

état courant
→ Tracker
~~~

Si l'apprentissage doit améliorer la compétence propriétaire :

> utiliser le workflow de création / amélioration de skill plutôt que modifier silencieusement le SKILL.md depuis la boucle.

Le prochain tour recharge alors automatiquement la méthode actuelle.

---

# 14. Dry Run obligatoire

Avant l'armement, exécuter un cycle réel ou simulé.

Vérifier :

- cold start ;
- bon skill chargé ;
- bon état retrouvé ;
- bonne délégation ;
- output des sous-agents ;
- vraie métrique ;
- mauvais cas détecté ;
- preuve journalisée ;
- apprentissage correctement routé ;
- reprise après interruption ;
- STOP.

Pour une action sensible, le dry run peut s'arrêter juste avant le gate final.

---

# 15. Gate avant armement

Une boucle est prête seulement si :

- [ ] une compétence propriétaire existe ;
- [ ] aucune autre boucle ne possède déjà le chantier ;
- [ ] Skill Readiness passe ;
- [ ] le pré-mortem a été traité ;
- [ ] les risques importants ont un owner ;
- [ ] l'autorité est claire ;
- [ ] la délégation est claire ;
- [ ] l'objectif est mesurable ;
- [ ] la métrique observe le vrai résultat ;
- [ ] un mauvais cas fait échouer la mesure ;
- [ ] l'état survit à la conversation ;
- [ ] le journal conserve les preuves ;
- [ ] le chemin d'apprentissage est défini ;
- [ ] le stop est défini ;
- [ ] le dry run passe.

---

# 16. Prompt de reprise

Le prompt doit rester court.

Exemple générique :

~~~text
/loop <cadence> /<competence> — reprends <boucle> : état d'abord, une unité de travail, preuve, journal, STOP au cap.
~~~

La syntaxe exacte dépend du moteur disponible.

Ce qui compte :

> le réveil recharge la compétence et l'état actuels au lieu d'embarquer une copie figée de leur méthode.

---

# 17. Réparer une boucle existante

Ne pas tout migrer d'un coup.

À la prochaine optimisation :

1. préserver son état ;
2. préserver son journal ;
3. préserver ses preuves ;
4. garder la même identité ;
5. ajouter uniquement les contrats/gates manquants ;
6. supprimer un artefact legacy uniquement après avoir prouvé que son information vit ailleurs.

C'est une migration « on touch ».

---

# 18. Quand NE PAS utiliser Loop Creator

Ce n'est pas une vraie boucle autonome si la répétition n'a ni progression ni apprentissage.

Exemples :

- rappel tous les lundis → scheduler / routine ;
- newsletter hebdomadaire identique → routine ;
- gros chantier one-shot → plan / sprint ;
- simple alerte conditionnelle → watcher si disponible.

Une vraie boucle a au minimum :
- un objectif qui progresse ;
- un état ;
- une unité de travail ;
- une preuve ;
- un stop.

---

# Sources d'inspiration

## AutoResearch — Andrej Karpathy

https://github.com/karpathy/autoresearch

Ce projet fournit une mécanique extrêmement simple et puissante :
expérience → budget fixe → mesure → garder / abandonner → journal → recommencer.

Loop Creator reprend cette logique expérimentale quand le problème s'y prête.

## ECC — Everything Claude Code

https://github.com/affaan-m/ECC

ECC pousse notamment des idées utiles autour de la séparation des responsabilités, de la vérification,
des hooks/checks, de la mémoire, de l'apprentissage et de l'orchestration.

Loop Creator combine ces inspirations avec une idée centrale :

> la boucle ne remplace pas les skills ; elle les orchestre dans le temps.

---

# Résultat attendu

Avant armement, produire mentalement ou explicitement :

~~~text
LOOP_ARCHITECTURE

MODE:
OBJECTIF:
OWNER_SKILL:
SKILL_READINESS:
PREMORTEM:
FAILURE_MAP:
RESPONSIBILITY_MAP:
AUTHORITY_MAP:
DELEGATION_MAP:
STATE:
EVIDENCE:
MEASUREMENT:
STOP:
LEARNING:
DRY_RUN:
READY_TO_ARM:
~~~

Si READY_TO_ARM = false :
→ corriger le propriétaire du défaut.

Ne jamais « armer quand même ».
