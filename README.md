# Rando Trail · rando-trail.fr

Blog statique (HTML/CSS pur, zéro JavaScript) optimisé SEO, prêt pour GitHub Pages.

## Mettre en ligne sur GitHub Pages
1. Crée un dépôt (ex. `rando-trail`) et pousse **le contenu du dossier `dist/`** à la racine (ou tout le projet et configure Pages sur `/dist` via une Action).
2. Settings → Pages → Source : `main` / `root`.
3. Domaine : le fichier `CNAME` (rando-trail.fr) est déjà généré. Dans Settings → Pages, saisis `rando-trail.fr`, coche « Enforce HTTPS », et chez ton registrar ajoute 4 enregistrements A vers 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 (+ un CNAME `www` vers `ton-pseudo.github.io`).

## Avant de publier
- Complète `mentions-legales.html` (obligatoire en France : éditeur, contact).
- Déclare le site dans **Google Search Console** et soumets `sitemap.xml`.

## Tes photos
Dépose `images/moi.jpg` (carré), `images/chaussures.jpg` et `images/montres.jpg` (format 16:8), puis relance `python3 build.py` : elles remplacent les blocs de couleur.

## Ajouter un article
1. Crée `content/mon-article.html` (fragment : `<h2 id="...">` pour le sommaire auto, `{{FAQ}}` pour la FAQ).
2. Ajoute une entrée dans `ARTICLES` (slug, titres, description, FAQ, produits).
3. `python3 build.py` → tout est régénéré (sitemap, JSON-LD, images de partage).

## Structure du site
- `articles.html` : tous les articles, rangés par type (Comparatifs, Tests produits, Guides). Pour un nouvel article, mets `"type": "tests"` (ou `comparatifs`, `guides`) dans `ARTICLES`. Les sujets « en préparation » se gèrent dans `UPCOMING_ARTICLES`.
- `plans-entrainement.html` : liste `PLANS`. Quand un plan est prêt, crée sa page et renseigne son `slug` : la carte passe de « Bientôt » à « Disponible ».
- `a-propos.html` : présentation + récits de course (liste `RECITS`).
- `pages_extra.py` : le code des pages Articles, Plans et Récits.

## Ce qui est déjà en place côté SEO
Titres/meta descriptions uniques, canonical, Open Graph + images 1200×630, JSON-LD (Article, BreadcrumbList, FAQPage, ItemList, WebSite), sitemap.xml, robots.txt, 404, sommaire à ancres, maillage interne, HTML sémantique, pages ultra légères.
