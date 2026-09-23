# Méthode — Chercher la cause racine

Utiliser cette méthode pour un bug récurrent, un contournement existant, ou un défaut qui réapparaît sous plusieurs formes.

Objectif : distinguer le symptôme de la cause structurelle.

## Les 4 niveaux

1. **Symptôme** — ce que l'utilisateur ou le système observe.
2. **Cause proche** — le composant qui produit directement l'effet.
3. **Cause mécanique** — le mécanisme qui produit cet état.
4. **Cause structurelle** — le choix d'architecture, l'absence de garde ou la confusion de modèle qui rend le défaut possible.

Ne pas s'arrêter avant le niveau 4 si le problème est réellement structurel.

## Méthode

1. Reformuler le symptôme en une phrase observable.
2. Prouver le comportement avec des données fraîches : logs, traces, mesures, reproduction.
3. Tracer le flux complet du signal de sa source jusqu'à l'effet.
4. Distinguer à chaque étape ce qui est prouvé de ce qui est supposé.
5. Continuer les « pourquoi » jusqu'à atteindre une structure, pas seulement une ligne de code.
6. Classer la forme de la racine.
7. Comparer fix-racine et contournement avant de recommander.

## Formes fréquentes

- deux concepts différents sont traités comme identiques ;
- une garde ou un invariant manque sur un chemin ;
- un composant alimente un autre alors qu'il ne devrait pas ;
- une route legacy continue de s'exécuter ;
- une question est posée dans un contexte où elle n'a pas de sens, puis « corrigée » en ajoutant des exceptions ;
- l'information qui permettait de distinguer deux cas existait, mais a été perdue par normalisation, troncature ou projection.

## Fix-racine vs contournement

Toujours nommer les deux.

**Fix-racine**
- supprime la cause ;
- plus large blast radius ;
- préférable si le défaut récidive ou produit plusieurs symptômes.

**Contournement**
- bloque ou masque l'effet ;
- plus local et moins risqué ;
- acceptable si la zone racine est trop risquée, gelée ou hors scope.

Si un contournement est retenu, dire explicitement que la racine demeure.
