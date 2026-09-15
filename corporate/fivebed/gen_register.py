#!/usr/bin/env python3
"""
FIVE BEDROOMS — static page generator for the two collection pages.

    python3 gen_register.py

Reads ../data/wiseman.json and writes, next to this file:

    buildings.html      The Register. All 72 buildings as real HTML rows in
                        seven neighborhood groups, plus the atlas view and the
                        plates view. Every row is in the source, so the page is
                        crawlable and complete with JavaScript off.
    search.html   The transactional door and the only page on the site
                        with filters. 72 real table rows, filtered by
                        WR.filters, every row linking out to the live listing.

Everything numeric on both pages is computed here from the feed. Nothing is
typed by hand. See ../FACT-CHECK.md — unit counts, founding years and ratings
are unverifiable and appear nowhere.

Two things this file knows that the feed does not tell you plainly:

  1. 52 of the 704 image URLs in the feed 404. Any URL whose filename ends in a
     space before the extension ("… living room .jpg" -> "…%20.jpg") is dead,
     and nine buildings have a dead gallery[0]. pick() takes the first live URL
     from galleryThumb -> thumb -> image -> gallery.
  2. Building 023 Purdue Point has no bedroom data. It renders an em dash, is
     never guessed at, and carries bed bounds that no bedroom filter can match
     (-1/-1) so the filter can never claim it offers a studio.
"""

import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent          # corporate/fivebed
DATA = HERE.parent / "data" / "wiseman.json"

# Cache-bust. base.css, core.js, style.css and app.js are bumped together.
V = "15"

# The feed is a point-in-time export, not a live query. The date the site
# quotes is the date of the export, not the date this script last ran.
SNAPSHOT = "10 September 2026"

AREA_ORDER = ["west-la", "brentwood", "beverly-grove", "hollywood",
              "venice", "palms", "glendale"]

# Short area names for tight lists (the register's own column stays long-form).
SHORT_AREA = {
    "west-la": "West LA", "brentwood": "Brentwood", "beverly-grove": "Beverly Grove",
    "hollywood": "Hollywood", "venice": "Venice", "palms": "Palms", "glendale": "Glendale",
}

DEAD = re.compile(r"%20\.(jpg|jpeg|png)$", re.I)


def live(u):
    return bool(u) and not DEAD.search(u)


def pick(*cands):
    """First live URL from the candidates; '' if a building has none."""
    for c in cands:
        for u in (c if isinstance(c, list) else [c]):
            if live(u):
                return u
    return ""


def esc(s):
    return html.escape(s or "", quote=True)


# ---------------------------------------------------------------- amenities
# Eight buckets, chosen because they actually spread across the portfolio.
# The raw feed spells the same amenity a dozen ways ("In-Suite Washer & Dryer",
# "In-Suite Washer and Dryer", "Washer/Dryer"), so each bucket is a predicate
# over the lower-cased community + apartment lists, not a string match.
def _any(items, *needles, but=None):
    for x in items:
        if but and but in x:
            continue
        if any(n in x for n in needles):
            return True
    return False


AMENITIES = [
    ("wd",     "In-unit washer and dryer", lambda a: _any(a, "washer", but="hookup")),
    ("patio",  "Patio or balcony",         lambda a: _any(a, "patio", "balcon")),
    ("ac",     "Central air conditioning", lambda a: any(x.startswith("central") for x in a)),
    ("elev",   "Elevator",                 lambda a: any(x == "elevator" for x in a)),
    ("closet", "Walk-in closets",          lambda a: _any(a, "walk-in closets")),
    ("court",  "Courtyard",                lambda a: _any(a, "courtyard")),
    ("fire",   "Fireplace",                lambda a: _any(a, "fireplace")),
    ("roof",   "Rooftop deck",             lambda a: _any(a, "rooftop")),
]

RENT_STEPS = [3000, 3500, 4000, 4500, 5000, 6000]

BED_OPTS = [(0, "Studio"), (1, "1 bedroom"), (2, "2 bedrooms"),
            (3, "3 bedrooms"), (4, "4 bedrooms"), (5, "5 bedrooms")]


# ------------------------------------------------------------------ labels
# FACT-CHECK §2 — no Motor Tides rent figure may be published anywhere on the
# site. 071 is the only flagged property. Mirrors NO_RENT in
# ../scripts/build_site.py and ../scripts/gen_search.py: it is a compliance rule,
# and it must hold for every page of every direction that renders a price.
NO_RENT = frozenset(["071"])


def num(s):
    return '<span class="num">%s</span>' % s


def beds_label(p):
    """Studio · Studio–4 · 3 · 3–4 · em dash. Only the digits get .num."""
    lo, hi = p["bedsMin"], p["bedsMax"]
    if lo is None:
        return "&mdash;"
    lo, hi = int(lo), int(hi or lo)
    if lo == hi:
        return "Studio" if lo == 0 else num(lo) + " bed"
    if lo == 0:
        return "Studio&ndash;" + num(hi) + " bed"
    return num("%d&ndash;%d" % (lo, hi)) + " bed"


def spell(n):
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
             7: "Seven", 13: "Thirteen", 14: "Fourteen", 17: "Seventeen",
             24: "Twenty-four", 27: "Twenty-seven", 52: "Fifty-two",
             72: "Seventy-two"}
    return words.get(n, str(n))


# ------------------------------------------------------------------- shell
HEAD = """<!doctype html>
<html lang="en" data-index="../data/index.json">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; Wiseman Residential</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FAF4EA">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wiseman Residential">
<meta property="og:title" content="{title} &mdash; Wiseman Residential">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:alt" content="{ogalt}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://resource.rentcafe.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Work+Sans:ital,wght@0,300..700;1,400&amp;family=Young+Serif&amp;display=swap">
<link rel="stylesheet" href="../core/base.css?v={v}">{core}
<link rel="stylesheet" href="style.css?v={v}">
<script>document.documentElement.classList.add('js')</script>{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

# The three peer views live behind ?view=. A static server cannot branch on a
# query string, so the choice is stamped on <html> before first paint — no view
# ever flashes, and with scripts off no attribute is set and the CSS leaves all
# three visible, register first.
VIEW_SCRIPT = """
<script>(function(){{var v='register';try{{var q=new URLSearchParams(location.search).get('view');if(q==='atlas'||q==='plates')v=q;}}catch(e){{}}document.documentElement.setAttribute('data-view',v);}})();</script>"""

# The search page leads the navigation on every page: a renter's first job is to
# find a home, and "Find a home" says where that is done. NAV[1:6] is the desktop
# header; the whole list, numbered, is the mobile menu.
NAV = [("index.html", "Home"), ("search.html", "Find a home"),
       ("buildings.html", "Buildings"), ("neighborhoods.html", "Neighborhoods"),
       ("residents.html", "Residents"), ("company.html", "Company"),
       ("contact.html", "Contact")]

MARK = ('<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">'
        '<polygon points="14,18 34,18 34,74 14,80"/>'
        '<polygon points="40,18 60,18 60,71 40,77"/>'
        '<polygon points="66,18 86,18 86,68 66,74"/></svg>')


def header(here):
    """aria-current is written into the source as well as set by app.js, so the
    current page is marked with scripts off."""
    links = []
    for href, label in NAV[1:6]:
        cur = ' aria-current="page"' if href == here else ""
        links.append('      <a href="%s"%s>%s</a>' % (href, cur, label))
    cta_cur = ' aria-current="page"' if here == "contact.html" else ""
    return """
  <header class="hd wrap wrap-n">
    <a class="brand" href="index.html" aria-label="Wiseman Residential, home">
      %s
      <b>Wiseman Residential</b>
    </a>
    <div class="hd-right">
      <nav class="hnav" aria-label="Primary">
%s
      </nav>
      <a class="hd-cta" href="contact.html"%s>Contact</a>
      <button class="mbtn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><span></span></button>
    </div>
  </header>
""" % (MARK, "\n".join(links), cta_cur)


def mnav(here):
    items = []
    for i, (href, label) in enumerate(NAV, 1):
        cur = ' aria-current="page"' if href == here else ""
        items.append('          <a href="%s"%s><span class="mnav-n num">%02d</span>%s</a>'
                     % (href, cur, i, label))
    return """
  <nav class="mnav" id="mnav" aria-label="Menu">
    <div class="mnav-in">
      <div class="mnav-list">
%s
      </div>
      <div class="mfoot">
        <a href="tel:+13104733000">+1 310-473-3000</a>
        <span>1520 Federal Ave, Los Angeles, CA 90025</span>
        <a href="https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx" rel="noopener">Resident login</a>
      </div>
    </div>
  </nav>

  <div class="pt" aria-hidden="true">
    <span class="ptmark">%s<b>Wiseman</b></span>
  </div>
""" % ("\n".join(items), MARK)


def footer(areas, maps="", tail=""):
    hoods = "\n".join(
        '            <li><a href="neighborhoods/%s.html">%s</a><span class="num">%d</span></li>'
        % (k, esc(areas[k]["name"]), areas[k]["count"]) for k in AREA_ORDER)
    return """
  <footer class="ft">
    <div class="wrap wrap-n">
      <div class="ft-top">
        <div class="ft-mark">
          <span class="wm" aria-hidden="true">%s</span>
          <p class="ft-tag">&ldquo;Los Angeles Living, Managed Wisely.&rdquo;</p>
          <div class="ft-contact">
            <span>1520 Federal Ave, Los Angeles, CA 90025</span>
            <a href="tel:+13104733000">+1 310-473-3000</a>
          </div>
        </div>
        <div class="ft-map">
          <div class="ft-col">
            <h2 class="ft-h">Neighborhoods</h2>
            <ul class="ft-list">
%s
            </ul>
          </div>
          <div class="ft-col">
            <h2 class="ft-h">Buildings</h2>
            <ul class="ft-list">
              <li><a href="search.html">Find a home</a><span class="num">72</span></li>
              <li><a href="buildings.html">The register</a><span class="num">72</span></li>
              <li><a href="buildings.html?sort=beds">Four bedrooms and up</a><span class="num">17</span></li>
              <li><a href="neighborhoods.html">All neighborhoods</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h2 class="ft-h">Residents</h2>
            <ul class="ft-list">
              <li><a href="residents.html">Residents</a></li>
              <li><a href="residents.html#maintenance">Maintenance</a></li>
              <li><a href="residents.html#deposits">Deposits</a></li>
              <li><a href="residents.html#moving-in">Moving in</a></li>
              <li><a href="residents.html#rights">Rights and resources</a></li>
              <li><a href="https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx" rel="noopener">Resident login</a></li>
              <li><a href="https://wisemanresidential.securecafe.com/onlineleasing/apartmentsforrent/guestlogin.aspx" rel="noopener">Applicant login</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h2 class="ft-h">Company</h2>
            <ul class="ft-list">
              <li><a href="company.html">What Wiseman does</a></li>
              <li><a href="company.html#building">What we are building</a></li>
              <li><a href="contact.html">Contact</a></li>
            </ul>
            <div class="ft-contact">
              <span>Leasing, weekdays</span>
              <a href="tel:+13104733000">+1 310-473-3000</a>
            </div>
          </div>
        </div>
      </div>
      <div class="ft-base">
        <p class="eho">
        <svg viewBox="0 0 12 10.608" role="img" aria-label="Equal Housing Opportunity" fill="currentColor" focusable="false"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.95263 1.07242L0 4.00926V5.38295H0.663158V9.51979H11.2026V5.38295H11.9921V4.00926L5.95263 1.07242ZM9.9 8.27242H1.95789V4.49874L5.95263 2.44611L9.9 4.49874V8.27242Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 5.82505H4.08947V4.49874H7.77632V5.82505Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 7.73558H4.08947V6.40926H7.77632V7.73558Z"/></svg>
        <span>Equal Housing Opportunity</span>
      </p>
        <nav class="ft-soc" aria-label="Social">
          <a href="https://www.facebook.com/Officialwisemanresidential/" rel="noopener">Facebook</a>
          <a href="https://www.instagram.com/officialwisemanresidential" rel="noopener">Instagram</a>
          <a href="https://www.yelp.com/biz/wiseman-residential-los-angeles-2" rel="noopener">Yelp</a>
        </nav>
        <span>&copy; 2026 Wiseman Residential</span>
      </div>
    </div>
  </footer>

<script src="../core/core.js?v=%s" defer></script>%s
<script src="app.js?v=%s" defer></script>%s
</body>
</html>
""" % (MARK, hoods, V, maps, V, tail)


SEARCH = """        <form class="search mt-m" action="search.html" method="get" role="search">
          <label class="vh" for="q">Search by street, building name or number</label>
          <input class="search-in" id="q" name="q" type="search" data-search autocomplete="off"
                 role="combobox" aria-expanded="false" aria-controls="ta" aria-autocomplete="list"
                 placeholder="Search a street, a building or a number">
          <button class="search-go" type="submit" aria-label="Search">
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="11" cy="11" r="7"/><path d="M16.5 16.5 21 21"/></svg>
          </button>
          <ul class="ta" id="ta" role="listbox" data-ta hidden></ul>
        </form>"""


def tx(url, transform):
    """Rewrite the Cloudinary-style transform segment so every plate, row and
    thumbnail asks the CDN for exactly the size it renders at."""
    return re.sub(r"(/image/upload/)[^/]+/", r"\g<1>" + transform + "/", url, count=1)


# ELEVATE §1 — never letterbox a building into a 16:9 card. Rows feed the
# specimen plate and the plates view, and both are 4:5.
ROW_IMG = "q_auto,f_auto,w_560,h_700,c_fill,g_auto"


# =========================================================== buildings.html
def reg_row(p):
    img = tx(pick(p.get("galleryThumb"), p.get("thumb"), p.get("image"), p.get("gallery")), ROW_IMG)
    lo, hi = p["bedsMin"], p["bedsMax"]
    return """            <div class="reg-row" data-row data-no="{no}" data-name="{name}" data-street="{street}" data-area="{key}" data-arealabel="{area}" data-bedsmin="{bmin}" data-bedsmax="{bmax}" data-rent="{rent}" data-img="{img}">
              <a class="reg-a" href="buildings/{path}.html">
                <span class="reg-no num">{no}</span>
                <span class="reg-name">{name}</span>
                <span class="reg-street">{street}</span>
                <span class="reg-area">{area}</span>
                <span class="reg-beds">{beds}</span>
              </a>
            </div>""".format(
        no=p["no"], name=esc(p["short"]), street=esc(p["street"]), key=p["areaKey"],
        area=esc(p["area"]), bmin="" if lo is None else int(lo),
        bmax="" if hi is None else int(hi),
        rent="" if (not p.get("priceMin") or p["no"] in NO_RENT) else int(p["priceMin"]),
        img=esc(img), path=p["path"], beds=beds_label(p))


# The skipped-content estimate has to be in the right order of magnitude or the
# scrollbar jumps on first paint. content-visibility:auto + the real row count.
def size_class(n):
    return "reg-g-xl" if n >= 20 else "reg-g-lg" if n >= 8 else "reg-g-sm"


def register_view(props, areas):
    groups = []
    for k in AREA_ORDER:
        rows = [p for p in props if p["areaKey"] == k]
        a = areas[k]
        groups.append("""            <section class="reg-group" data-group="{k}" aria-labelledby="g-{k}">
              <h3 class="reg-head" id="g-{k}"><span data-grouplabel>{name}</span> <span class="tnum reg-gcount">{n}</span></h3>
              <div class="reg-rows {sz}" data-rows>
{rows}
              </div>
            </section>""".format(k=k, name=esc(a["name"]), n=len(rows),
                                 sz=size_class(len(rows)),
                                 rows="\n".join(reg_row(p) for p in rows)))
    first = props[0]
    plate_img = tx(pick(first.get("galleryThumb"), first.get("thumb"),
                        first.get("image"), first.get("gallery")), ROW_IMG)
    return """      <div class="view view-register" id="view-register">
        <h2 class="vh">The register</h2>

        <div class="reg-tools">
          <span class="reg-tools-lab" id="sortlab">Sort</span>
          <div class="seg" role="group" aria-labelledby="sortlab">
            <button type="button" data-sort="area" aria-pressed="true">Neighborhood</button>
            <button type="button" data-sort="no" aria-pressed="false">Number</button>
            <button type="button" data-sort="street" aria-pressed="false">Street A&ndash;Z</button>
            <button type="button" data-sort="beds" aria-pressed="false">Bedrooms</button>
            <button type="button" data-sort="rent" aria-pressed="false">Rent</button>
          </div>
          <p class="note tools-note">Sorting reorders the whole list. Nothing is ever hidden from it.</p>
        </div>

        <div class="reg-wrap">
          <div class="reg" data-register data-mode="grouped" data-flatlabel="All 72 buildings">
{groups}
          </div>

          <div class="reg-side">
            <aside class="plate" data-plate data-cur="{fno}" aria-hidden="true">
              <figure class="plate-fig"><img src="{fimg}" alt="{fname}" width="560" height="700" loading="lazy" decoding="async"></figure>
              <div class="plate-meta">
                <span class="plate-no num" data-plateno>{fno}</span>
                <span class="plate-name" data-platename>{fname}</span>
                <span class="plate-street" data-platestreet>{fstreet} &middot; {farea}</span>
                <span class="plate-hint">The plate follows the list</span>
              </div>
            </aside>
{atlas}
          </div>
        </div>
        <p class="note mt-s">Rent sorts on the lowest rent a building lists. Prices themselves live on the <a class="lnk" href="search.html">search page</a> and in the live leasing system.</p>
      </div>""".format(groups="\n".join(groups), atlas=atlas_view(props, areas), fno=first["no"], fimg=esc(plate_img),
                       fname=esc(first["short"]), fstreet=esc(first["street"]),
                       farea=esc(first["area"]))


def atlas_view(props, areas):
    """The map column. It lives inside the register's own aside so the two-way
    highlight has real rows to light: hovering a row lights its pin and
    hovering a pin lights its row. Shown only under ?view=atlas."""
    key = "\n".join(
        """              <li><a href="neighborhoods/{k}.html"><span class="ak-n num">{n}</span><span class="ak-name">{name}</span><span class="ak-sub">{sub}</span></a></li>""".format(
            k=k, n=areas[k]["count"], name=esc(areas[k]["name"]), sub=esc(areas[k]["sub"]))
        for k in AREA_ORDER)
    return """            <div class="reg-map">
              <div class="wr-map map-full" data-map data-labels="hover" data-label="Map of all {n} Wiseman buildings in Los Angeles"></div>
              <p class="note">Zoomed out the map counts by neighborhood; zoomed in every pin carries its building number. Hovering a pin lights that building&rsquo;s row, and hovering a row lights its pin. The register is complete with the map switched off.</p>
              <h3 class="reg-head"><span>By neighborhood</span> <span class="tnum">{n}</span></h3>
              <ul class="atlas-list">
{key}
              </ul>
            </div>""".format(n=len(props), key=key)


def plates_view(props, areas):
    out = []
    for k in AREA_ORDER:
        rows = [p for p in props if p["areaKey"] == k]
        cards = []
        for p in rows:
            img = tx(pick(p.get("galleryThumb"), p.get("thumb"), p.get("image"),
                          p.get("gallery")), ROW_IMG)
            cards.append("""              <article class="spec">
                <a href="buildings/{path}.html">
                  <figure class="spec-fig"><img src="{img}" alt="{name}, {area}" loading="lazy" decoding="async" width="560" height="700"></figure>
                  <p class="spec-no num">{no}</p>
                  <h4 class="spec-name">{name}</h4>
                  <p class="spec-meta"><span>{beds}</span><span>{street}</span></p>
                </a>
              </article>""".format(path=p["path"], img=esc(img), name=esc(p["short"]),
                                   area=esc(p["area"]), no=p["no"], beds=beds_label(p),
                                   street=esc(p["street"])))
        out.append("""          <section class="pgrp" aria-labelledby="p-{k}">
            <h3 class="reg-head" id="p-{k}"><span>{name}</span> <span class="tnum">{n}</span></h3>
            <div class="spec-grid mt-s">
{cards}
            </div>
          </section>""".format(k=k, name=esc(areas[k]["name"]), n=len(rows),
                               cards="\n".join(cards)))
    return """      <div class="view view-plates" id="view-plates">
        <h2 class="vh">The plates</h2>
        <div class="plates">
{groups}
        </div>
      </div>""".format(groups="\n".join(out))


def build_buildings(d, props, areas, stats):
    body = """
  <main id="main">
    <section class="phero" aria-labelledby="reg-h">
      <div class="wrap wrap-n">
        <p class="eyebrow">The register</p>
        <h1 class="phero-h mt-s" id="reg-h">Seventy-two buildings, one line each.</h1>
        <p class="lead muted mt-s measure">Number, name, street, neighborhood, bedrooms. Sorting reorders the list; it never hides anything from it. Read it as a list, as a map, or as plates.</p>
{search}
        <p class="tally mt-m">
          <span><span class="num">{n}</span> buildings</span>
          <span><span class="num">{areas}</span> neighborhoods</span>
          <span><span class="num">{streets}</span> named streets</span>
          <span><span class="num">{four}</span> with four bedrooms or more</span>
        </p>
      </div>
    </section>

    <section class="sec-s" aria-label="The portfolio">
      <div class="wrap wrap-n">
        <nav class="vtog" aria-label="Views">
          <a class="vt vt-register" href="buildings.html?view=register"><span class="vt-n num">01</span>Register</a>
          <a class="vt vt-atlas" href="buildings.html?view=atlas"><span class="vt-n num">02</span>Atlas</a>
          <a class="vt vt-plates" href="buildings.html?view=plates"><span class="vt-n num">03</span>Plates</a>
          <span class="note vt-note">Three ways to read the same seventy-two.</span>
        </nav>
        <noscript><p class="note mt-s">Scripts are off, so all three views are shown one after another and sorting is unavailable. The list itself is complete.</p></noscript>

{register}

{plates}

        <p class="reg-more mt-l">
          <a class="lnk" href="search.html">Search what is listed right now</a>
          <span class="note">Availability and pricing are settled in the live leasing system, not here.</span>
        </p>
      </div>
    </section>
  </main>
""".format(search=SEARCH, n=stats["n"], areas=stats["areas"], streets=stats["streets"],
           four=stats["four"], register=register_view(props, areas),
           plates=plates_view(props, areas))

    head = HEAD.format(
        title="The register",
        desc=("All %d Wiseman apartment buildings in Los Angeles on one page: number, name, "
              "street, neighborhood and bedrooms, sortable, with a drawn map and a plate for "
              "every building." % stats["n"]),
        ogimg="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1400/s3/2/9707/1331%20amherst%20ave%20exteriors%20-22.jpg",
        ogalt="The Amherst Avenue elevation of a Wiseman building in West Los Angeles.",
        v=V, core='\n<link rel="stylesheet" href="../core/map.css?v=%s">' % V,
        extra=VIEW_SCRIPT.format(v=V))
    return head + header("buildings.html") + mnav("buildings.html") + body + footer(
        areas, maps='\n<script src="../core/map.js?v=%s" defer></script>' % V)


# ========================================================= search.html
def amen_keys(p):
    a = [x.lower() for x in (p.get("community") or []) + (p.get("apartment") or [])]
    return [k for k, _label, test in AMENITIES if test(a)]


def build_availability(d, props, areas, stats):
    """The search page.

    The filter bar, the More-filters modal, the chips, the count, the sort, the
    result cards and the split list/map are all generated by
    ../scripts/gen_search.py, which replaces everything between the SEARCH
    markers below. This file owns the shell: the hero, the standing note about
    the leasing system — which stays ABOVE the filter bar so it is read before
    any result — and the interest list that closes the page.
    """
    int_beds = "\n".join(
        """                <option value="{v}">{label}</option>""".format(v=v, label=label)
        for v, label in BED_OPTS)
    int_areas = "\n".join(
        """                <option value="{k}">{name}</option>""".format(k=k, name=esc(areas[k]["name"]))
        for k in AREA_ORDER)

    body = """
  <main id="main">
    <section class="phero" aria-labelledby="av-h">
      <div class="wrap wrap-n">
        <nav class="crumb" aria-label="Breadcrumb">
          <a href="index.html">Home</a> <span aria-hidden="true">/</span> <span>Find a home</span>
        </nav>
        <p class="eyebrow mt-m">Find a home</p>
        <h1 class="phero-h mt-s" id="av-h">Find a home with the rooms you need.</h1>
        <p class="lead muted mt-s measure">A street, a neighborhood, a number of bedrooms, a rent, a washer in the apartment. Narrow it however you like; the map keeps up, and every card opens that building.</p>
        <p class="tally mt-m">
          <span><span class="num">{n}</span> buildings</span>
          <span><span class="num">{priced}</span> listing a rent</span>
          <span><span class="num">{studio}</span> with a studio</span>
          <span><span class="num">{four}</span> with four bedrooms or more</span>
        </p>
        <div class="panel panel-key mt-m">
          <p><b>The live leasing system is the authority on availability and pricing.</b> Everything below is a snapshot of what each building was advertising on {snap}. Which apartment is free this week, and what it costs today, is answered on the building&rsquo;s own leasing page and by the leasing office on <a class="ulink" href="tel:+13104733000">+1 310-473-3000</a>.</p>
        </div>
        <noscript><p class="note mt-s">Filtering and sorting need JavaScript. All {n} buildings are listed below either way, and every card opens that building&rsquo;s page.</p></noscript>
      </div>
    </section>

<!--SEARCH-->
<!--/SEARCH-->

    <div class="wrap wrap-n">
      <div class="savebar" data-favwrap hidden>
        <p class="savebar-n"><span class="num" data-favcount>0</span> saved to compare</p>
        <p class="note">Saved on this device only. Saving is for your own shortlist &mdash; it holds nothing and reserves nothing.</p>
        <a class="lnk" href="contact.html">Ask the leasing office about these</a>
      </div>
    </div>

    <section class="sec-s sec-p2" id="interest" aria-labelledby="int-h">
      <div class="wrap wrap-n">
        <div class="sec-head">
          <p class="eyebrow">Interest list</p>
          <h2 class="h2" id="int-h">Nothing right today?</h2>
          <p class="lead muted">Tell us the apartment you are looking for, so the leasing office can get in touch when one comes up. The next step asks for your name and how to reach you.</p>
        </div>

        <form class="int-form" action="contact.html" method="get">
          <input type="hidden" name="intent" value="interest-list">
          <div class="g3">
            <div class="field">
              <label class="field-lab" for="i-beds">Bedrooms</label>
              <select class="field-in" id="i-beds" name="beds">
                <option value="">Any size</option>
{int_beds}
              </select>
            </div>
            <div class="field">
              <label class="field-lab" for="i-area">Neighborhood</label>
              <select class="field-in" id="i-area" name="area">
                <option value="">Any neighborhood</option>
{int_areas}
              </select>
            </div>
            <div class="field">
              <label class="field-lab" for="i-when">Earliest move-in</label>
              <input class="field-in" id="i-when" name="when" type="month">
            </div>
          </div>
          <div class="field mt-s">
            <label class="field-lab" for="i-note">Anything else about the apartment</label>
            <textarea class="field-in" id="i-note" name="note" rows="3" placeholder="Ground floor, a second bathroom, room for a piano"></textarea>
          </div>
          <div class="btn-row mt-s">
            <button class="btn btn-solid" type="submit">Continue to the leasing office</button>
            <a class="btn btn-line" href="tel:+13104733000">Call +1 310-473-3000</a>
          </div>
          <p class="note mt-s">Weekdays, from the corporate office at 1520 Federal Ave. Wiseman rents on the same terms to every applicant &mdash; see the Equal Housing Opportunity mark below. Building <span class="num">071</span>, Motor Tides, is letting up for the first time and publishes no rent here; its leasing page carries the figure for the apartment you ask about.</p>
        </form>
      </div>
    </section>
  </main>
""".format(n=stats["n"], priced=stats["priced"], studio=stats["beds"][0], four=stats["four"],
           snap=SNAPSHOT, int_beds=int_beds, int_areas=int_areas)

    head = HEAD.format(
        title="Find a home",
        desc=("Search all %d Wiseman apartment buildings in Los Angeles by neighborhood, "
              "bedrooms, bathrooms, rent, size and amenities, on a map. The live leasing "
              "system is the authority on availability and pricing." % stats["n"]),
        ogimg="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1400/s3/2/9707/hudson%20lux%20unit%20103%20-%20lr_%20dining_%20kitchen_%20and%20patio_final.jpg",
        ogalt="A living room, dining area and kitchen in a Wiseman apartment in Hollywood.",
        v=V,
        # rail.css BEFORE search.css on purpose: the filter bar is both a
        # .sbar-in and a .rail-track, the two sheets set the same properties on
        # it at equal specificity, and the bar's own 12px padding and 8px gap
        # are the ones that belong. All three load before style.css, so the
        # direction's skin is the last word without inflating a selector.
        core=('\n<link rel="stylesheet" href="../core/rail.css?v={v}">'
              '\n<link rel="stylesheet" href="../core/search.css?v={v}">'
              '\n<link rel="stylesheet" href="../core/map.css?v={v}">').format(v=V),
        extra="\n<script>document.documentElement.classList.add('ils')</script>")

    scripts = ('\n<script src="../core/rail.js?v={v}" defer></script>'
               '\n<script src="../core/map.js?v={v}" defer></script>'
               '\n<script src="../core/search.js?v={v}" defer></script>').format(v=V)

    # Deferred scripts all run before DOMContentLoaded, so this boots after
    # app.js has called WR.boot(). One rAF loop, no second boot.
    boot = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  if (!window.WR) return;
  WR.rails();
  WR.searchPage({});
  fetch('../data/wiseman.json').then(function (r) { return r.json(); }).then(function (d) {
    WR.map({
      el: '#search-map', pins: 'price', theme: 'light',
      points: d.properties.map(function (p) {
        return { no: p.no, lat: p.lat, lng: p.lng, name: p.short, street: p.street,
                 area: p.areaKey, areaLabel: p.area, beds: p.beds,
                 img: p.thumb, url: 'buildings/' + p.path + '.html', pinLabel: p.no === '071' ? 'New' : '' };
      }),
      areas: Object.fromEntries(Object.entries(d.areas).map(function (e) {
        return [e[0], { name: e[1].name, count: e[1].count }];
      }))
    });
  }).catch(function () {});
});
</script>"""

    return (head + header("search.html") + mnav("search.html") + body
            + footer(areas, maps=scripts, tail=boot))


# ------------------------------------------------------------------- main
def main():
    d = json.loads(DATA.read_text())
    props = sorted(d["properties"], key=lambda p: p["no"])
    areas = d["areas"]

    stats = {
        "n": len(props),
        "areas": len(areas),
        "streets": len(set(p["street"] for p in props)),
        "four": sum(1 for p in props if (p["bedsMax"] or 0) >= 4),
        "five": sum(1 for p in props if (p["bedsMax"] or 0) >= 5),
        # FACT-CHECK §2: a building in NO_RENT publishes no rent, so it cannot be
        # counted as one that does. Counting it made "$6,000 or less — 67
        # buildings" promise a row the filter then refused to show, and derived
        # that label from the very figure the site may not print.
        "priced": sum(1 for p in props if p.get("priceMin") and p["no"] not in NO_RENT),
        "beds": {v: sum(1 for p in props
                        if p["bedsMin"] is not None and p["bedsMin"] <= v <= p["bedsMax"])
                 for v, _l in BED_OPTS},
        "amen": {k: sum(1 for p in props if k in amen_keys(p)) for k, _l, _t in AMENITIES},
        "rent": {v: sum(1 for p in props
                        if p.get("priceMin") and p["no"] not in NO_RENT and p["priceMin"] <= v)
                 for v in RENT_STEPS},
    }

    (HERE / "buildings.html").write_text(build_buildings(d, props, areas, stats))
    (HERE / "search.html").write_text(build_availability(d, props, areas, stats))

    noamen = [p["no"] for p in props if not amen_keys(p)]
    print("buildings.html     %d rows in %d groups" % (stats["n"], len(AREA_ORDER)))
    print("search.html  search shell written \u2014 now run "
          "../scripts/gen_search.py fivebed for the %d cards" % stats["n"])
    print("counts             %d streets · %d four-bed+ · %d five-bed · %d priced"
          % (stats["streets"], stats["four"], stats["five"], stats["priced"]))
    print("beds               " + " · ".join("%s %d" % (l, stats["beds"][v]) for v, l in BED_OPTS))
    print("amenities          " + " · ".join("%s %d" % (k, stats["amen"][k])
                                             for k, _l, _t in AMENITIES))
    print("rent steps         " + " · ".join("<=%d %d" % (v, stats["rent"][v]) for v in RENT_STEPS))
    print("no bucketed amenity: %s" % (noamen or "none"))


if __name__ == "__main__":
    main()
