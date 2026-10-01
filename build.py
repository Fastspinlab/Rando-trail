#!/usr/bin/env python3
"""Générateur du site Rando Trail.
Usage : python3 build.py  -> écrit le site statique dans ./dist (prêt pour GitHub Pages).
Ajouter un article : créez content/mon-article.html puis ajoutez une entrée dans ARTICLES.
Tes photos : dépose-les dans ./images (voir PHOTOS plus bas), elles remplacent automatiquement les blocs de couleur.
"""
import html, json, math, os, re, shutil
import pages_extra as px

SITE_URL = "https://rando-trail.fr"
SITE_NAME = "Rando Trail"
TAGLINE = "Trail & rando"
AUTHOR = "Nicolas"
AUTHOR_BIO = "Traileur. Je cours en montagne dès que je peux et j'écris ici les guides que j'aurais aimé lire avant d'acheter mon matos."
LANG = "fr"
TODAY = "2026-09-30"

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
IMG_DIR = os.path.join(ROOT, "images")

# Photos optionnelles : si le fichier existe dans ./images, il est utilisé.
PHOTOS = {
    "moi": "images/moi.jpg",                                   # ta tête (carré)
    "meilleures-chaussures-trail": "images/chaussures.jpg",    # couverture article (16:8)
    "meilleure-montre-gps-trail": "images/montres.jpg",
}


def photo(key):
    p = PHOTOS.get(key)
    return p if p and os.path.exists(os.path.join(ROOT, p)) else None


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,700..800'
         '&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,800&family=Young+Serif&display=swap">')

ARTICLES = [
    {
        "slug": "meilleures-chaussures-trail",
        "file": "chaussures.html",
        "category": "Chaussures",
        "type": "comparatifs",
        "cover": "yellow",
        "cover_big": "9 paires",
        "cover_small": "Poids · drop · accroche",
        "title": "Meilleures chaussures de trail 2026 : comparatif et guide d'achat",
        "seo_title": "Chaussures de trail 2026 : comparatif des meilleurs modèles",
        "h1": "Les meilleures chaussures de trail en 2026",
        "description": "Comparatif 2026 des meilleures chaussures de trail : Hoka, Salomon, La Sportiva, Saucony… Poids, drop, accroche et conseils pour choisir selon ton terrain.",
        "lede": "Neuf paires classées selon l'endroit où tu cours : boue, rocher, ultra, petit budget. Avec le tableau pour comparer et ce qu'il faut regarder avant de sortir la carte bleue.",
        "read": 12,
        "published": "2026-09-30",
        "faq": [
            ("Quelle pointure prendre en trail ?",
             "En général une demi-pointure au-dessus de ta pointure de ville. Le pied gonfle et avance en descente : garde environ un centimètre devant le gros orteil."),
            ("Quel drop choisir ?",
             "Il n'y a pas de drop idéal. 6 à 8 mm conviennent à la plupart des coureurs qui viennent de la route. Les petits drops (0 à 4 mm) demandent d'habituer mollets et tendon d'Achille progressivement."),
            ("Combien de kilomètres dure une chaussure de trail ?",
             "Entre 600 et 1 000 km selon ton poids, ton terrain et le modèle. Surveille les crampons, la mousse qui s'écrase et les douleurs qui apparaissent sans raison."),
            ("Je peux faire du trail avec mes chaussures de route ?",
             "Sur des chemins secs et roulants, oui. Dès que ça devient boueux, rocheux ou raide, l'accroche et la protection d'une vraie chaussure de trail deviennent une question de sécurité."),
            ("Gore-Tex ou pas ?",
             "Seulement pour l'hiver, la neige ou le froid humide. Le reste de l'année, une tige respirante qui sèche vite est plus agréable, parce que l'eau finit toujours par rentrer par le haut."),
        ],
        "items": ["Hoka Speedgoat 7", "Hoka Tecton X 4", "La Sportiva Prodigio Pro", "Saucony Peregrine 16", "Brooks Cascadia 20",
                  "Altra Lone Peak 9", "Salomon Speedcross 6", "Inov8 TrailTalon", "La Sportiva Akasha II"],
    },
    {
        "slug": "meilleure-montre-gps-trail",
        "file": "montres.html",
        "category": "Montres GPS",
        "type": "comparatifs",
        "cover": "forest",
        "cover_big": "120 h",
        "cover_small": "Autonomie · cartes · prix",
        "title": "Meilleure montre GPS trail 2026 : comparatif Garmin, Coros, Suunto",
        "seo_title": "Montre GPS trail 2026 : comparatif Garmin, Coros, Suunto",
        "h1": "Quelle montre GPS pour le trail en 2026 ?",
        "description": "Comparatif 2026 des meilleures montres GPS pour le trail et l'ultra : autonomie, cartes, précision GPS et prix des Garmin, Coros, Suunto et Amazfit.",
        "lede": "Huit montres passées au crible de ce qui compte en montagne : l'autonomie, la navigation, le dénivelé et le poids au poignet. Et combien d'heures de GPS prendre pour ta course.",
        "read": 11,
        "published": "2026-09-30",
        "faq": [
            ("Quelle autonomie pour faire l'UTMB ?",
             "La plupart des finishers mettent entre 30 et 46 heures. Vise au moins 60 heures de GPS en mode standard, ou prévois une petite batterie externe pour recharger en courant."),
            ("Le GPS multi-bande sert à quelque chose en trail ?",
             "Oui, surtout en forêt dense, en vallée encaissée ou près des falaises, où la trace est bien plus propre. Il vide la batterie plus vite, donc sur un ultra long le mode standard suffit souvent."),
            ("Les cartes sont indispensables ?",
             "Le suivi de trace GPX suffit pour la plupart des courses balisées. Les cartes deviennent très utiles en reco, en itinérance ou quand le balisage disparaît dans le brouillard."),
            ("Le cardio au poignet est fiable ?",
             "Correct en endurance. Pour le fractionné, les côtes courtes ou quand tu tiens des bâtons, une ceinture cardio reste plus précise."),
            ("Garmin, Coros ou Suunto ?",
             "Garmin a l'écosystème le plus complet, Coros la meilleure autonomie pour le prix, Suunto un bon compromis design et cartes gratuites. Choisis d'abord l'autonomie et le budget, puis l'appli qui te plaît."),
        ],
        "items": ["Garmin Forerunner 970", "Garmin Enduro 3", "Garmin Fenix 8", "Coros Vertix 2S", "Suunto Vertical 2",
                  "Coros Apex 4", "Amazfit T-Rex 3 Pro", "Suunto Run"],
    },
]

# Types d'articles affichés dans la page Articles (ajoute "type" à chaque article)
ARTICLE_TYPES = [
    ("comparatifs", "Comparatifs", "Plusieurs produits face à face, classés selon ton terrain."),
    ("tests", "Tests produits", "Un produit, des kilomètres, un avis franc."),
    ("guides", "Guides & conseils", "Tout ce qu'il faut savoir pour bien choisir et bien courir."),
]

# Sujets annoncés « en préparation » (supprime une ligne quand l'article est publié)
UPCOMING_ARTICLES = [
    ("tests", "Test", "Hoka Speedgoat 7 : mon avis après des centaines de kilomètres"),
    ("guides", "Guide", "Bien choisir son gilet d'hydratation"),
    ("guides", "Guide", "Bâtons de trail : quand et comment s'en servir"),
    ("comparatifs", "Comparatif", "Les meilleures frontales pour courir de nuit"),
]

# Plans d'entraînement : ajoute un dict avec "slug" quand un plan est publié
PLANS = [
    {"title": "Réussir son 10 km", "level": "Débutant à intermédiaire", "sessions": "3 à 4 séances / semaine", "goal": "Passer sous l'heure ou battre ton record", "slug": None},
    {"title": "Préparer la SaintéLyon", "level": "Intermédiaire", "sessions": "4 à 5 séances / semaine", "goal": "Finir de nuit, sur un parcours roulant et exigeant", "slug": None},
    {"title": "Premier trail de 30 km", "level": "Débutant trail", "sessions": "3 à 4 séances / semaine", "goal": "Découvrir le dénivelé sans se blesser", "slug": None},
    {"title": "Premier ultra de 80 km", "level": "Confirmé", "sessions": "5 séances / semaine", "goal": "Tenir la distance et gérer la nuit", "slug": None},
]

PHASES = [  # (nom, nb semaines, classe CSS, description)
    ("Foncier", 4, "p1", "Du volume tranquille pour construire la base."),
    ("Développement", 4, "p2", "On ajoute le fractionné et les côtes."),
    ("Spécifique", 2, "p3", "Des séances au plus près de la course."),
    ("Affûtage", 2, "p4", "On réduit pour arriver frais le jour J."),
]

# Récits de course : ajoute {"title", "date", "race", "slug"} quand tu en publies un
RECITS = []

TERRAINS = [
    ("Dans la boue", "Speedcross 6", "meilleures-chaussures-trail.html#salomon-speedcross-6"),
    ("Sur du rocher", "Prodigio Pro", "meilleures-chaussures-trail.html#la-sportiva-prodigio-pro"),
    ("En ultra", "Tecton X 4", "meilleures-chaussures-trail.html#hoka-tecton-x-4"),
    ("Tu débutes", "Cascadia 20", "meilleures-chaussures-trail.html#brooks-cascadia-20"),
    ("Pied large", "Lone Peak 9", "meilleures-chaussures-trail.html#altra-lone-peak-9"),
    ("Budget serré", "Peregrine 16", "meilleures-chaussures-trail.html#saucony-peregrine-16"),
    ("UTMB sans recharger", "Enduro 3", "meilleure-montre-gps-trail.html#garmin-enduro-3"),
    ("Montre à moins de 500 €", "Apex 4", "meilleure-montre-gps-trail.html#coros-apex-4"),
]

esc = html.escape


def url(path=""):
    return SITE_URL.rstrip("/") + "/" + path


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def head(title, description, path, og_type="website", og_image="og/accueil.png", extra=""):
    canonical = url(path)
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url(og_image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffd84d">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="style.css">
{extra}"""


def brand():
    return f'<a class="brand" href="./" aria-label="{SITE_NAME}, accueil"><span class="mark" aria-hidden="true"><i></i><i></i></span>{SITE_NAME}</a>'


def header(current=""):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<a class="skip" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="wrap">
    {brand()}
    <nav class="nav" aria-label="Navigation principale">
      {a("articles.html", "Articles", "articles")}
      {a("plans-entrainement.html", "Plans d'entraînement", "plans")}
      {a("a-propos.html", "Qui je suis", "about")}
    </nav>
  </div>
</header>"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div>{brand()}<p>Le blog d'un traileur qui compare le matos de trail et de rando. Sans blabla, et à jour.</p></div>
    <nav aria-label="Liens de pied de page">
      <a href="articles.html">Articles</a>
      <a href="plans-entrainement.html">Plans d'entraînement</a>
      <a href="a-propos.html">Qui je suis</a>
      <a href="a-propos.html#recits">Récits de course</a>
      <a href="mentions-legales.html">Mentions légales</a>
    </nav>
  </div>
</footer>"""


def page(head_html, body_html, current=""):
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
{head_html}
</head>
<body>
{header(current)}
<main id="contenu">
{body_html}
</main>
{footer()}
</body>
</html>
"""


def fmt_date(iso):
    months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    y, m, d = iso.split("-")
    return f"{int(d)} {months[int(m) - 1]} {y}"


def face(cls="face"):
    p = photo("moi")
    inner = f'<img src="{p}" alt="{AUTHOR}" width="120" height="120">' if p else AUTHOR[0]
    return f'<div class="{cls}" aria-hidden="{"false" if p else "true"}">{inner}</div>'


def post_card(a):
    p = photo(a["slug"])
    if p:
        cover = f'<div class="cover" style="padding:0"><img src="{p}" alt="" loading="lazy"></div>'
    else:
        cover = (f'<div class="cover cover-{a["cover"]}"><span class="kicker">{esc(a["category"])}</span>'
                 f'<div><div class="loud">{esc(a["cover_big"])}</div><div class="kicker" style="margin-top:8px">{esc(a["cover_small"])}</div></div></div>')
    return f"""<a class="post" href="{a['slug']}.html">
  {cover}
  <div class="post-body">
    <h3>{esc(a['h1'])}</h3>
    <p>{esc(a['lede'])}</p>
    <div class="post-meta"><span>Mis à jour le {fmt_date(TODAY)}</span><span>{a['read']} min</span></div>
  </div>
</a>"""


def build_home():
    title = f"{SITE_NAME} · Comparatifs matériel trail et randonnée"
    desc = "Le blog d'un traileur : comparatifs de chaussures de trail, montres GPS et matos de rando. Des avis francs pour choisir selon ton terrain."
    ld = jsonld({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": url() + "#site", "url": url(), "name": SITE_NAME, "inLanguage": "fr-FR",
             "description": desc, "publisher": {"@id": url() + "#org"}},
            {"@type": "Organization", "@id": url() + "#org", "name": SITE_NAME, "url": url(), "logo": url("favicon.svg")},
            {"@type": "Blog", "name": f"Le blog {SITE_NAME}", "url": url(),
             "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": url(a["slug"] + ".html"),
                           "datePublished": a["published"]} for a in ARTICLES]},
        ],
    })
    body = f"""<section class="hero wrap">
  <div class="hero-panel">
    <div>
      <p class="kicker">{TAGLINE} · le matos au banc d'essai</p>
      <h1 class="loud" style="margin-top:14px">Ton matos de trail, sans blabla.</h1>
      <p class="hero-sub">Je compare les chaussures, les montres et l'équipement de rando pour que tu achètes une fois, et la bonne.</p>
      <div class="hero-cta">
        <a class="btn btn-dark" href="articles.html">Lire les articles</a>
        <a class="btn btn-light" href="plans-entrainement.html">Plans d'entraînement</a>
      </div>
    </div>
    <div class="stack" aria-hidden="true">
      <div class="fiche fiche-1">
        <span class="kicker stamp">Mon n°1</span>
        <span class="kicker">Chaussure · polyvalente</span>
        <h2>Hoka Speedgoat 7</h2>
        <dl><div><dt>Poids</dt><dd>258 g</dd></div><div><dt>Drop</dt><dd>5 mm</dd></div><div><dt>Crampons</dt><dd>4,5 mm</dd></div></dl>
      </div>
      <div class="fiche fiche-2">
        <span class="kicker">Montre · ultra</span>
        <h2>Garmin Enduro 3</h2>
        <div class="big">120 h</div>
        <p style="margin-top:4px">de GPS. L'UTMB sans recharger.</p>
      </div>
    </div>
  </div>
</section>

<section class="section wrap" aria-labelledby="derniers">
  <div class="section-head">
    <h2 id="derniers" class="serif">Les derniers articles</h2>
    <a class="btn btn-dark" href="articles.html">Tous les articles →</a>
  </div>
  <div class="posts">{"".join(post_card(a) for a in ARTICLES[:3])}</div>
</section>

<section class="section wrap">
  <div class="hello">
    {face()}
    <div>
      <h2 class="serif">Salut, moi c'est {AUTHOR}.</h2>
      <p>Je cours en montagne dès que je peux. Ce blog, c'est ce que j'aurais aimé lire avant d'acheter mon matos : des avis francs, classés selon le terrain, avec les chiffres qui comptent. Bientôt, tu y trouveras aussi mes récits de course.</p>
      <a class="btn btn-yellow" href="a-propos.html">Qui je suis</a>
    </div>
  </div>
</section>"""
    return page(head(title, desc, "", extra=ld), body)


def build_toc(content):
    items = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', content)
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items if i != "en-bref")
    return f'<nav class="toc" aria-label="Sommaire"><p class="kicker">Au programme</p><ol>{lis}</ol></nav>'


def build_article(a):
    with open(os.path.join(ROOT, "content", a["file"]), encoding="utf-8") as f:
        content = f.read()
    faq_html = '<div class="faq">' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>" for q, r in a["faq"]) + "</div>"
    content = content.replace("{{FAQ}}", faq_html)
    path = a["slug"] + ".html"
    ld = jsonld({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": a["title"], "description": a["description"],
             "datePublished": a["published"], "dateModified": TODAY, "inLanguage": "fr-FR",
             "mainEntityOfPage": url(path), "image": url(f"og/{a['slug']}.png"),
             "author": {"@type": "Person", "name": AUTHOR, "url": url("a-propos.html")},
             "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": url("favicon.svg")}}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": url()},
                {"@type": "ListItem", "position": 2, "name": "Articles", "item": url("articles.html")},
                {"@type": "ListItem", "position": 3, "name": a["h1"]}]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a["faq"]]},
            {"@type": "ItemList", "name": a["h1"], "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n} for i, n in enumerate(a["items"])]},
        ],
    })
    extra = ld + f'\n<meta property="article:published_time" content="{a["published"]}">\n<meta property="article:modified_time" content="{TODAY}">'
    others = [o for o in ARTICLES if o is not a]
    related = ""
    if others:
        related = '<section class="related"><h2 class="serif">À lire ensuite</h2><div class="posts">' + "".join(post_card(o) for o in others) + "</div></section>"
    current = "articles"
    body = f"""<div class="article-top">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><ol><li><a href="./">Accueil</a></li><li><a href="articles.html">Articles</a></li><li>{esc(a['category'])}</li></ol></nav>
    <h1>{esc(a['h1'])}</h1>
    <p class="lede">{esc(a['lede'])}</p>
    <div class="byline">{face()}<span>Par <strong>{AUTHOR}</strong></span><span>Mis à jour le <time datetime="{TODAY}">{fmt_date(TODAY)}</time></span><span>{a['read']} min de lecture</span></div>
  </div>
</div>
<div class="wrap layout">
  {build_toc(content)}
  <article class="prose">
{content}
<aside class="author" aria-label="L'auteur">{face()}<div><p><strong>{AUTHOR}</strong>, derrière {SITE_NAME}</p><p>{esc(AUTHOR_BIO)}</p></div></aside>
{related}
  </article>
</div>"""
    return page(head(a["seo_title"], a["description"], path, "article", f"og/{a['slug']}.png", extra), body, current)


def simple_page(path, title, desc, h1, inner, current="", robots=None):
    h = head(title, desc, path)
    if robots:
        h = h.replace('content="index, follow, max-image-preview:large"', f'content="{robots}"')
    if path == "a-propos.html":
        body = f"""<div class="page-top"><div class="wrap">{px.crumbs("Qui je suis")}
  <div class="about-head">{face()}<div><h1 class="serif">{h1}</h1><p class="lede">{esc(AUTHOR_BIO)}</p></div></div>
</div></div>
<div class="wrap page" style="padding-top:8px"><div class="prose">{inner}</div></div>"""
    else:
        body = f"""<div class="wrap page">{px.crumbs(h1)}<h1 style="margin-top:22px">{h1}</h1><div class="prose">{inner}</div></div>"""
    return page(h, body, current)


ABOUT = f"""<h2>Pourquoi Rando Trail ?</h2>
<p>Parce que je passe de l'un à l'autre toute l'année : du trail à fond sur les sentiers, de la rando quand je prends le temps. J'ai lancé ce site parce que la plupart des comparatifs classent le matos sans dire pour quel terrain ni pour quel coureur. Ici, chaque conseil part de là : où tu cours, combien de temps, avec quel budget.</p>
<h2>Comment je travaille</h2>
<ul>
  <li>Je pars des fiches techniques, des tests publiés et des retours de coureurs.</li>
  <li>Quand j'ai couru avec un modèle, je le dis.</li>
  <li>J'explique les critères (drop, stack, autonomie, accroche) pour que tu puisses juger toi-même.</li>
  <li>Je mets les guides à jour à chaque nouvelle génération.</li>
</ul>
<h2>Les liens d'affiliation</h2>
<p>Certains liens peuvent être affiliés : si tu achètes via ces liens, {SITE_NAME} touche une petite commission, sans surcoût pour toi. Ça ne change rien à mes avis.</p>"""

LEGAL = f"""<h2>Éditeur du site</h2>
<p>{SITE_NAME} est édité par : [Nom et prénom] · [Adresse] · Contact : [adresse e-mail].<br>Directeur de la publication : [Nom].</p>
<h2>Hébergement</h2>
<p>GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<h2>Liens d'affiliation</h2>
<p>Certains liens du site sont des liens d'affiliation. Ils n'entraînent aucun surcoût pour le lecteur.</p>
<h2>Données personnelles et cookies</h2>
<p>Ce site ne dépose pas de cookie publicitaire. Si une mesure d'audience est ajoutée, elle sera décrite ici avec tes droits d'accès, de rectification et de suppression.</p>"""

NOT_FOUND = """<p>Ce sentier ne mène nulle part. La page a sans doute bougé.</p>
<p><a href="./">Retour à l'accueil</a> · <a href="meilleures-chaussures-trail.html">Chaussures de trail</a> · <a href="meilleure-montre-gps-trail.html">Montres GPS</a></p>"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#ffd84d"/><rect x="6" y="8" width="20" height="6.5" rx="1.5" fill="#ffffff" stroke="#121613" stroke-width="2"/><rect x="6" y="17.5" width="20" height="6.5" rx="1.5" fill="#121613"/></svg>"""


def og_image(path, kicker, title):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#ffd84d")
    d = ImageDraw.Draw(img)
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fb = ImageFont.truetype(bold, 70)
    d.rounded_rectangle([80, 80, 130, 96], 3, fill="#ffffff", outline="#121613", width=3)
    d.rounded_rectangle([80, 102, 130, 118], 3, fill="#121613")
    d.text((148, 78), SITE_NAME.upper(), font=ImageFont.truetype(bold, 38), fill="#121613")
    kf = ImageFont.truetype(bold, 26)
    kw = d.textlength(kicker.upper(), font=kf)
    d.rounded_rectangle([80, 210, 80 + kw + 36, 256], 23, fill="#121613")
    d.text((98, 218), kicker.upper(), font=kf, fill="#ffd84d")
    words, lines, cur = title.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fb) > 1040:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    y = 290
    for ln in lines[:3]:
        d.text((80, y), ln, font=fb, fill="#121613"); y += 86
    img.save(path)


def strip_for_artifact(doc):
    """Le lecteur d'artefacts ajoute son propre squelette : on retire doctype/html/head/body."""
    doc = re.sub(r"<!doctype html>\s*", "", doc, flags=re.I)
    doc = re.sub(r"</?html[^>]*>\s*", "", doc)
    doc = re.sub(r"</?head>\s*", "", doc)
    doc = re.sub(r"</?body>\s*", "", doc)
    doc = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", doc)
    return doc


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "og"))
    shutil.copy(os.path.join(ROOT, "style.css"), DIST)
    if os.path.isdir(IMG_DIR):
        shutil.copytree(IMG_DIR, os.path.join(DIST, "images"))
    files = {
        "index.html": build_home(),
        "a-propos.html": simple_page("a-propos.html", f"Qui je suis et mes récits de course · {SITE_NAME}", f"Qui écrit {SITE_NAME}, comment je compare le matériel de trail, et mes récits de course.", f"Salut, moi c'est {AUTHOR}", ABOUT + px.recits_html(RECITS), "about"),
        "articles.html": px.build_articles_hub(globals()),
        "plans-entrainement.html": px.build_plans(globals()),
        "mentions-legales.html": simple_page("mentions-legales.html", f"Mentions légales · {SITE_NAME}", f"Mentions légales, hébergement et affiliation du site {SITE_NAME}.", "Mentions légales", LEGAL),
        "404.html": simple_page("404.html", f"Page introuvable · {SITE_NAME}", "Cette page n'existe pas.", "Page introuvable", NOT_FOUND, robots="noindex"),
    }
    for a in ARTICLES:
        files[a["slug"] + ".html"] = build_article(a)
    for name, doc in files.items():
        with open(os.path.join(DIST, name), "w", encoding="utf-8") as f:
            f.write(doc)
    with open(os.path.join(DIST, "favicon.svg"), "w") as f:
        f.write(FAVICON)
    entries = [("", "weekly", "1.0")] + [("articles.html", "weekly", "0.8"), ("plans-entrainement.html", "weekly", "0.8")] + [(a["slug"] + ".html", "monthly", "0.9") for a in ARTICLES] + [("a-propos.html", "monthly", "0.5")]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for p, c, pr in entries)
    sm += "</urlset>\n"
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {url('sitemap.xml')}\n")
    open(os.path.join(DIST, ".nojekyll"), "w").write("")
    open(os.path.join(DIST, "CNAME"), "w").write(SITE_URL.split("://")[1].rstrip("/") + "\n")
    og_image(os.path.join(DIST, "og", "accueil.png"), TAGLINE, "Ton matos de trail, sans blabla.")
    for a in ARTICLES:
        og_image(os.path.join(DIST, "og", a["slug"] + ".png"), "Comparatif " + a["category"], a["h1"])
    os.makedirs(os.path.join(ROOT, "artifact"), exist_ok=True)
    with open(os.path.join(ROOT, "artifact", "index.html"), "w", encoding="utf-8") as f:
        f.write(strip_for_artifact(files["index.html"]))
    print("Site généré dans", DIST, "->", sorted(files))


if __name__ == "__main__":
    main()
