"""Pages Articles, Plans d'entraînement et récits (importé par build.py)."""
import html

esc = html.escape


def phases_bar(PHASES, compact=False):
    cells = ""
    week = 1
    for name, n, cls, desc in PHASES:
        cells += f'<div class="phase {cls}" style="grid-column: span {n}"><span class="kicker">{esc(name)}</span>'
        cells += f'<span class="weeks">S{week}–S{week + n - 1}</span>'
        if not compact:
            cells += f'<p>{esc(desc)}</p>'
        cells += '</div>'
        week += n
    ticks = "".join(f'<span>{i}</span>' for i in range(1, 13))
    return (f'<figure class="phases{" compact" if compact else ""}" aria-label="Les 4 phases d\'un plan de 12 semaines">'
            f'<div class="phase-row">{cells}</div><div class="week-ticks" aria-hidden="true">{ticks}</div></figure>')


def crumbs(label):
    return (f'<nav class="crumbs" aria-label="Fil d\'Ariane"><ol><li><a href="./">Accueil</a></li>'
            f'<li>{esc(label)}</li></ol></nav>')


def build_articles_hub(g):
    path = "articles.html"
    title = f"Articles trail et rando : comparatifs, tests, guides · {g['SITE_NAME']}"
    desc = "Tous les articles de Rando Trail : comparatifs de matériel de trail, tests produits et guides pour bien choisir ton équipement et progresser."
    sections, nav = "", ""
    for key, label, blurb in g["ARTICLE_TYPES"]:
        items = [a for a in g["ARTICLES"] if a.get("type") == key]
        soon = [u for u in g["UPCOMING_ARTICLES"] if u[0] == key]
        count = f'{len(items)} article{"s" if len(items) > 1 else ""}' if items else "bientôt"
        nav += f'<a class="chip" href="#{key}"><b>{esc(label)}</b><span>{count}</span></a>'
        cards = "".join(g["post_card"](a) for a in items)
        cards += "".join(f'<div class="soon-card"><span class="kicker">{esc(k)} · en préparation</span><h3>{esc(t)}</h3></div>' for _, k, t in soon)
        if not cards:
            cards = '<div class="soon-card"><span class="kicker">En préparation</span><h3>Les premiers articles arrivent.</h3></div>'
        sections += (f'<section class="section wrap" id="{key}" aria-labelledby="h-{key}">'
                     f'<div class="section-head"><div><h2 id="h-{key}" class="serif">{esc(label)}</h2>'
                     f'<p class="section-sub">{esc(blurb)}</p></div></div><div class="posts">{cards}</div></section>\n')
    url = g["url"]
    ld = g["jsonld"]({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Articles", "url": url(path),
                      "description": desc, "inLanguage": "fr-FR",
                      "mainEntity": {"@type": "ItemList", "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "url": url(a["slug"] + ".html"), "name": a["title"]}
                          for i, a in enumerate(g["ARTICLES"])]}})
    body = (f'<div class="page-top"><div class="wrap">{crumbs("Articles")}'
            f'<h1 class="loud">Les articles</h1>'
            f'<p class="lede">Comparatifs, tests produits et guides pour choisir ton matos de trail et de rando. Je les mets à jour à chaque nouvelle génération.</p>'
            f'<div class="chips" style="margin-top:24px">{nav}</div></div></div>\n{sections}')
    return g["page"](g["head"](title, desc, path, extra=ld), body, "articles")


def build_plans(g):
    path = "plans-entrainement.html"
    title = f"Plans d'entraînement 12 semaines : 10 km, trail, SaintéLyon · {g['SITE_NAME']}"
    desc = "Plans d'entraînement running et trail sur 12 semaines : réussir son 10 km, préparer la SaintéLyon, son premier trail ou son premier ultra."
    cards = ""
    for p in g["PLANS"]:
        tag = "Disponible" if p["slug"] else "Bientôt"
        inner = (f'<span class="kicker plan-tag{" on" if p["slug"] else ""}">{tag}</span>'
                 f'<h3>{esc(p["title"])}</h3><p>{esc(p["goal"])}</p>'
                 f'<dl class="specs"><div><dt>Durée</dt><dd>12 semaines</dd></div><div><dt>Niveau</dt><dd>{esc(p["level"])}</dd></div>'
                 f'<div><dt>Rythme</dt><dd>{esc(p["sessions"])}</dd></div></dl>')
        cards += f'<a class="plan-card" href="{p["slug"]}.html">{inner}</a>' if p["slug"] else f'<div class="plan-card">{inner}</div>'
    ld = g["jsonld"]({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Plans d'entraînement",
                      "url": g["url"](path), "description": desc, "inLanguage": "fr-FR"})
    body = f"""<div class="page-top"><div class="wrap">{crumbs("Plans d'entraînement")}
  <h1 class="loud">Plans d'entraînement</h1>
  <p class="lede">Des plans sur 12 semaines pour arriver prêt le jour J, du 10 km à l'ultra. Tu choisis ta course, tu suis les semaines, tu cours.</p>
</div></div>

<section class="section wrap" aria-labelledby="h-plans">
  <div class="section-head"><h2 id="h-plans" class="serif">Choisis ta course</h2></div>
  <div class="plans">{cards}</div>
</section>

<section class="section wrap" aria-labelledby="h-construit">
  <div class="section-head"><div><h2 id="h-construit" class="serif">Comment sont construits mes plans</h2>
  <p class="section-sub">Tous les plans suivent les mêmes quatre phases. Seuls le volume et les séances changent selon la course.</p></div></div>
  {phases_bar(g["PHASES"])}
  <div class="rules">
    <div><h3>Une progression douce</h3><p>Le volume monte petit à petit, et une semaine plus légère revient régulièrement pour que le corps assimile.</p></div>
    <div><h3>Des séances qui ont un but</h3><p>Endurance fondamentale, fractionné, côtes, sortie longue, renforcement. Chaque séance est expliquée.</p></div>
    <div><h3>Adaptable à ta vie</h3><p>Tu rates une séance ? Pas de panique. Chaque plan dit quelles séances sont prioritaires.</p></div>
  </div>
  <p class="table-note" style="margin-top:22px">Ces plans sont des conseils généraux. En cas de douleur, de reprise après blessure ou de doute sur ta santé, demande l'avis d'un médecin.</p>
</section>"""
    return g["page"](g["head"](title, desc, path, extra=ld), body, "plans")


def recits_html(RECITS):
    if RECITS:
        cards = "".join(f'<a class="soon-card" href="{r["slug"]}.html"><span class="kicker">{esc(r["race"])} · {esc(r["date"])}</span><h3>{esc(r["title"])}</h3></a>' for r in RECITS)
    else:
        cards = ('<div class="soon-card"><span class="kicker">Premier récit · en préparation</span>'
                 "<h3>Les coulisses de mes courses, du départ à la ligne d'arrivée.</h3>"
                 "<p>Le parcours, ce qui a marché, les coups de moins bien, et le matos que j'avais sur le dos.</p></div>")
    return f'<h2 id="recits">Mes récits de course</h2><div class="posts" style="margin-top:18px">{cards}</div>'
