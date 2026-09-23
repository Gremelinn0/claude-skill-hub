# Hub Master — Template réutilisable

V0 réutilisable prête à l'emploi pour démarrer un nouveau Hub Master personnel (palette light, Token Hub interactif, structure 3 sections).

---

## Ce que contient le template

- **Bannière système** (optionnelle) — lien vers votre page de règles/système
- **Nav sticky** — ancres vers les 3 sections
- **Hero** — titre + stats configurables
- **Section Hubs** — 2 cartes umbrella (structure non-négociable : max 2 projets à la racine)
- **Token Hub** — tracker crédits IA en localStorage, sans backend, modal de mise à jour
- **Section Outils** — 1 carte umbrella pour vos skills/outils perso
- **Footer** — nom + liens

---

## Comment l'utiliser (5 étapes)

**1. Copier le fichier**

```
hub-master-template.html → votre-projet/hub/master-hub/index.html
```

**2. Remplacer les placeholders**

Chercher `[` dans le fichier — chaque `[...]` est un placeholder à remplacer :

| Placeholder | Remplacer par |
|---|---|
| `[Nom du hub]` | Votre nom ou titre du hub (balise `<title>`) |
| `[Votre nom]` | Votre nom (hero + footer) |
| `[Projet 1]`, `[Projet 2]` | Noms de vos 2 projets principaux |
| `[Sous-hub 1]`, `[Sous-hub 2]` | Titres des sous-hubs umbrella |
| `[Description]`, `[Pitch...]` | Descriptions de chaque sous-hub (≤ 2 lignes) |
| `[Tag N]` | Étiquettes courtes (technos, volumes, statuts) |
| `[Lien 1]`, `[Lien 2]` | Vos liens footer (LinkedIn, site, etc.) |

**3. Configurer le Token Hub**

Dans le `<script>` en bas de page, modifier les deux tableaux :

```js
// Comptes Claude Anthropic — dual-bar (Tous modèles + Sonnet)
const CLAUDE_ACCOUNTS = [
  { name:'Claude Pro',  email:'moi@example.com', plan:'Pro',
    allId:'c1-all', sonnetId:'c1-sonnet', resetDays:7 },
  // Ajouter autant de comptes Claude que nécessaire
];

// Comptes Google / Gemini — dual-bar (Gemini + Sonnet via AI Studio)
const AG_ACCOUNTS = [
  { num:1, label:'Google #1', email:'moi@gmail.com', plan:'Pro',
    geminiId:'ag1-gemini', geminiModel:'[Modèle principal]',
    sonnetId:'ag1-sonnet', sonnetModel:'[Modèle secondaire]', resetDays:6 },
  // Ajouter jusqu'à N comptes Google
];
```

Chaque compte génère une ligne avec **2 barres** : gauche = quota principal, droite = quota Sonnet.
Les crédits sont stockés en `localStorage` — persistants entre sessions, sans serveur.

**4. Déployer sur Vercel**

```bash
# Depuis le dossier contenant index.html :
npx vercel --prod --yes
```

Noter l'URL générée (ex : `https://mon-hub.vercel.app`).

**5. Vérifier**

Ouvrir l'URL Vercel — jamais en local une fois déployé (sinon le Token Hub ne reflète pas l'état Vercel).

---

## Palette light — ne pas modifier

Les 15 variables CSS dans `:root` définissent le design system partagé. Les changer casserait la cohérence avec les autres hubs.

Pour changer l'accent : modifier uniquement `--accent` (défaut : violet `#6c5ce7`).

---

## Structure HTML à respecter

```
<body>
  bannière système (optionnelle)
  nav sticky          → ordre : 🏠 Hubs · 🧰 Outils · ⚡ Tokens
  hero
  modal token (caché par défaut)
  <main>
    section#hubs       → 2 cartes .hub-card umbrella max
    section#tools      → 1 carte .hub-card outils
    section#token-hub  → Token Hub JS (toujours EN BAS)
  </main>
  footer
  script Token Hub
</body>
```

Règle absolue : **jamais plus de 2 projets dans `#hubs`**. Si vous avez 3+ projets, créer des sous-hubs séparés et y pointer depuis ces 2 cartes.


---

## Statut

V0 expérimentale / template de départ. Adaptez les sections, comptes, modèles et liens à votre propre système avant mise en production.
