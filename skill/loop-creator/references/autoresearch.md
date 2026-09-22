# Adapter portable — AutoResearch

À utiliser quand la boucle est expérimentale : tuning, optimisation, recherche, benchmarks, QA mesurée ou toute situation où chaque tour teste une hypothèse.

## Boucle expérimentale

~~~text
baseline
→ hypothèse
→ expérience
→ mesure
→ KEEP / DISCARD
→ journal
→ hypothèse suivante
~~~

## État minimal

Le tracker doit contenir :
- objectif mesurable ;
- définition de fini ;
- scope ;
- métrique ;
- baseline ;
- backlog d'hypothèses ;
- état courant ;
- limites de mesure ;
- stop.

Un simple program.md convient très bien.

## Journal minimal

Une ligne par expérience :

~~~text
date    hypothese    changement    mesure_avant    mesure_apres    verdict    preuve    notes
~~~

Un TSV, CSV, table ou base de données conviennent ; le format importe moins que la traçabilité.

## Règles

1. Une hypothèse par tour.
2. Mesurer l'effet réel.
3. Prouver que la métrique sait reconnaître un mauvais cas.
4. Un essai non mesurable n'est ni KEEP ni succès.
5. Revenir en arrière si la modification régresse les critères de sécurité / non-régression.
6. Conserver les essais ratés pour ne pas les refaire.
7. Arrêter au cap prévu.

## Isolation

Pour du code, Git est un bon mécanisme de preuve :
- une expérience = un commit identifiable ;
- branche/worktree pour les essais jetables si utile ;
- ne pas promouvoir automatiquement un gagnant vers la branche produit si une décision humaine est prévue.

## Inspiration

Cette mécanique reprend l'idée centrale d'AutoResearch de Andrej Karpathy :
https://github.com/karpathy/autoresearch

AutoResearch montre une boucle concrète où un agent modifie, entraîne pendant un budget fixe, mesure une métrique, garde ou abandonne le changement, journalise puis recommence.
