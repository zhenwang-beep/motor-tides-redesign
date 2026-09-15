#!/usr/bin/env python3
# =====================================================================
# WISEMAN RESIDENTIAL — direction: TIDELINE
# Generates the two data-driven pages of this direction:
#
#     tideline/buildings.html      All buildings — all 72 as static rows
#     tideline/search.html   The transactional door — the only filters
#
# Both are written as REAL HTML: every row, every plate, every table cell
# is in the file, so the pages are complete and crawlable with JavaScript
# switched off. JS only sorts, searches, switches view and filters.
#
# Source of truth: ../data/wiseman.json. Nothing here is invented; every
# count, price, bedroom range and photograph comes out of the feed.
#
#     cd corporate/tideline && python3 gen_register.py
# =====================================================================

import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")

with open(DATA, encoding="utf-8") as fh:
    D = json.load(fh)

AREAS = D["areas"]          # dict, authored order = the site's order
PROPS = D["properties"]     # 72
TOTAL = len(PROPS)

CSS_V = "18"                # ILS search skin + the rails handed to core/rail.css
BASE_V = "18"
CORE_V = "18"
APP_V = "18"                 # the bespoke rail mechanic retired in favour of WR.rails
MAP_V = "18"
RAIL_V = "18"
SEARCH_V = "18"

SITE = "https://www.wisemanresidential.com/"


# --------------------------------------------------------------- helpers
def e(s):
    return html.escape("" if s is None else str(s), quote=True)


def tx(url, transform):
    """Swap the Cloudinary-style transform segment of a RentCafe CDN URL."""
    if not url:
        return ""
    return re.sub(r"(/image/upload/)[^/]+/", r"\g<1>" + transform + "/", url, count=1)


THUMB = "q_auto,f_auto,w_600,h_400,c_fill,g_auto"
PLATE = "q_auto,f_auto,w_900,h_675,c_fill,g_auto"
SOCIAL = "q_auto,f_auto,w_1200,h_630,c_fill,g_auto"


def money(n):
    return "$" + format(int(round(n)), ",d")


# FACT-CHECK §2 — no Motor Tides rent figure may be published anywhere on the
# site: the only sourced figure mixes market-rate with deed-restricted homes
# and goes stale fast. Mirrors NO_RENT in scripts/build_site.py, which applies
# the same rule to the generated building and neighbourhood pages.
NO_RENT = frozenset(["071"])


def price_shown(p):
    """What a rent column is allowed to print for this building."""
    return "Now leasing" if p["no"] in NO_RENT else price_label(p)


def rent_attr(p):
    """data-rent for sorting and filtering, suppressed for the same buildings.

    Blank reads as "no published figure" to WR.register and WR.filters alike,
    so 071 behaves exactly like the five buildings that quote on request and
    its figure cannot be inferred from sort order either.
    """
    rent = p.get("priceMin")
    if rent is None or p["no"] in NO_RENT:
        return ""
    return ' data-rent="%d"' % int(rent)


def price_label(p):
    """Same vocabulary as WR.priceLabel in core.js, so the site reads as one."""
    lo, hi = p.get("priceMin"), p.get("priceMax")
    if lo is None:
        return "Call for details"
    if hi and hi > lo:
        return money(lo) + "–" + money(hi)
    return "From " + money(lo)


def beds_label(p):
    """'3-4 Beds' -> '3–4'. 'Studio-2 Beds' -> 'Studio–2'. '—' stays '—'."""
    s = (p.get("beds") or "").strip()
    if not s or s == "—":
        return "—"
    s = re.sub(r"\s*Beds?$", "", s, flags=re.I)
    return s.replace("-", "–")


def baths_label(p):
    s = (p.get("baths") or "").strip()
    if not s or s == "—":
        return "—"
    s = re.sub(r"\s*Baths?$", "", s, flags=re.I)
    return s.replace("-", "–")


def sqft_label(p):
    s = (p.get("sqft") or "").strip()
    if not s or s == "—":
        return "—"
    s = re.sub(r"\s*Sq\.?\s*Ft\.?$", "", s, flags=re.I)
    return s.replace(" to ", "–").replace("-", "–")


# --------------------------------------------------- amenity normalisation
# The feed spells the same amenity several ways ("In-Suite Washer & Dryer"
# and "In-Suite Washer and Dryer"; "Walk-In Closets" and "Walk-In Closets
# w/ Built-In Organizers"). These six are the only ones that appear across
# a large share of the portfolio, so they are the only ones offered as
# filters. Counts are printed when this script runs, and checked in.
AMENITIES = [
    ("wd",       "In-suite washer and dryer",  lambda s: "washer" in s),
    ("outdoor",  "Private patio or balcony",   lambda s: "patio" in s or "balcony" in s),
    ("parking",  "Garage or covered parking",  lambda s: "garage" in s or "covered parking" in s),
    ("ac",       "Central air conditioning",   lambda s: "central" in s and ("air" in s or " ac" in s)),
    ("elevator", "Elevator",                   lambda s: "elevator" in s),
    ("closets",  "Walk-in closets",            lambda s: "walk-in closet" in s),
]


def amen_keys(p):
    labels = [a.lower() for a in (p.get("community") or []) + (p.get("apartment") or [])]
    keys = [k for k, _lab, test in AMENITIES if any(test(a) for a in labels)]
    return keys


AMEN_COUNT = {k: 0 for k, _l, _t in AMENITIES}
for _p in PROPS:
    for _k in amen_keys(_p):
        AMEN_COUNT[_k] += 1

BED_OPTIONS = [(0, "Studio"), (1, "1 bedroom"), (2, "2 bedrooms"),
               (3, "3 bedrooms"), (4, "4 bedrooms"), (5, "5 bedrooms")]
BED_COUNT = {}
for _n, _lab in BED_OPTIONS:
    BED_COUNT[_n] = sum(1 for p in PROPS
                        if p.get("bedsMin") is not None and p["bedsMin"] <= _n <= p["bedsMax"])

RENT_STEPS = [2500, 3000, 3500, 4000, 4500, 5000, 6000]


# ------------------------------------------------------------- furniture
# A renter's first job is to find a home, so the search page leads the nav on
# every page of the site and is one click from any header.
NAV = [
    ("search.html", "Find a home"),
    ("buildings.html", "Buildings"),
    ("neighborhoods.html", "Neighbourhoods"),
    ("residents.html", "Residents"),
    ("company.html", "Company"),
    ("contact.html", "Contact"),
]

MARK = ('<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">'
        '<polygon points="14,18 34,18 34,74 14,80"/>'
        '<polygon points="40,18 60,18 60,71 40,77"/>'
        '<polygon points="66,18 86,18 86,68 66,74"/></svg>')


def head(title, desc, canon, og_img, og_alt, jsonld, maps=False, search=False):
    # The ILS search page needs the map, the rail and the search stylesheets, in
    # that order and all of them BEFORE style.css: rail.css sets
    # [data-rail]{position:relative} and search.css sets .sbar{position:sticky}
    # on the same element, so the sticky bar only survives if search.css lands
    # second — and the direction's own skin block, at the end of style.css, has
    # to land last of all.
    mapcss = ""
    if maps or search:
        mapcss += '<link rel="stylesheet" href="../core/map.css?v=%s">\n' % MAP_V
    if search:
        mapcss += '<link rel="stylesheet" href="../core/rail.css?v=%s">\n' % RAIL_V
        mapcss += '<link rel="stylesheet" href="../core/search.css?v=%s">\n' % SEARCH_V
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E%3Crect%20width='100'%20height='100'%20fill='%230C1A1F'/%3E%3Cg%20fill='%23169BAC'%3E%3Cpolygon%20points='14,18%2034,18%2034,74%2014,80'/%3E%3Cpolygon%20points='40,18%2060,18%2060,71%2040,77'/%3E%3Cpolygon%20points='66,18%2086,18%2086,68%2066,74'/%3E%3C/g%3E%3C/svg%3E">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wiseman Residential">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:alt" content="{og_alt}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#F2EFE7">

<link rel="preconnect" href="https://resource.rentcafe.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&amp;family=Fraunces:opsz,wght,SOFT,WONK@9..144,100..900,0..100,0..1&amp;display=swap">
<link rel="stylesheet" href="../core/base.css?v={BASE_V}">
{mapcss}<link rel="stylesheet" href="style.css?v={CSS_V}">

<script>
document.documentElement.classList.add('js');
if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {{
  document.documentElement.classList.add('js-pt');
}}
addEventListener('load', function () {{
  /* if core.js never arrived, never leave the page behind the curtain */
  if (!window.WR) document.documentElement.classList.remove('js-pt');
}});
</script>

<script type="application/ld+json">
{jsonld}
</script>
</head>
"""


def furniture(current, body_class=""):
    hnav = "\n".join(
        '      <a href="{h}"{c}>{l}</a>'.format(
            h=h, l=l, c=' aria-current="page"' if h == current else "")
        for h, l in NAV)
    mnav = "\n".join(
        '    <a href="{h}"{c}>{l}</a>'.format(
            h=h, l=l, c=' aria-current="page"' if h == current else "")
        for h, l in NAV)
    cls = ' class="%s"' % body_class if body_class else ""
    return f"""
<body{cls}>
<a class="skip-link" href="#main">Skip to content</a>

<div class="pt" aria-hidden="true">
  <div class="ptmark">{MARK}<span>Wiseman Residential</span></div>
</div>

<header class="hd wrap">
  <a class="brand" href="index.html" aria-label="Wiseman Residential, home">
    {MARK}<b>Wiseman Residential</b>
  </a>
  <nav class="hnav" aria-label="Primary">
{hnav}
  </nav>
  <button class="mbtn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><span></span></button>
</header>

<nav class="mnav" id="mnav" aria-label="Primary, mobile">
{mnav}
  <div class="mfoot">
    <p>1520 Federal Ave, Los Angeles, CA 90025</p>
    <p><a href="tel:+13104733000">+1 310-473-3000</a></p>
  </div>
</nav>
"""


FOOTER = """
<!-- ======================================================== FOOTER. -->
<footer id="site-map" class="ft bleed" data-hd="dark">
  <div class="wrap wrap-n">
    <div class="ft-map">
      <div class="ft-col">
        <h2 class="ft-h">Neighbourhoods</h2>
        <ul class="ft-list">
          <li><a href="neighborhoods/west-la.html">West Los Angeles</a> <span class="tnum">27</span></li>
          <li><a href="neighborhoods/brentwood.html">Brentwood</a> <span class="tnum">13</span></li>
          <li><a href="neighborhoods/beverly-grove.html">Beverly Grove</a> <span class="tnum">14</span></li>
          <li><a href="neighborhoods/hollywood.html">Hollywood</a> <span class="tnum">13</span></li>
          <li><a href="neighborhoods/venice.html">Venice</a> <span class="tnum">2</span></li>
          <li><a href="neighborhoods/palms.html">Palms &middot; Motor Avenue</a> <span class="tnum">2</span></li>
          <li><a href="neighborhoods/glendale.html">Glendale</a> <span class="tnum">1</span></li>
          <li><a href="neighborhoods.html">All seven</a> <span class="tnum">72</span></li>
        </ul>
      </div>
      <div class="ft-col">
        <h2 class="ft-h">The portfolio</h2>
        <ul class="ft-list">
          <li><a href="search.html">Find a home</a></li>
          <li><a href="buildings.html">All buildings</a> <span class="tnum">72</span></li>
          <li><a href="neighborhoods.html">Neighbourhoods</a> <span class="tnum">7</span></li>
          <li><a href="company.html">Company</a></li>
          <li><a href="careers.html">Careers</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="ft-col">
        <h2 class="ft-h">Residents</h2>
        <ul class="ft-list">
          <li><a href="residents.html#maintenance">Report a repair</a></li>
          <li><a href="https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx" target="_blank" rel="noopener">Pay rent &mdash; resident login</a></li>
          <li><a href="https://wisemanresidential.securecafe.com/onlineleasing/apartmentsforrent/guestlogin.aspx" target="_blank" rel="noopener">Apply &mdash; applicant login</a></li>
          <li><a href="residents.html#deposits">Security deposits</a></li>
          <li><a href="residents.html#moving-in">Moving in</a></li>
          <li><a href="residents.html#rights">Rights &amp; resources</a></li>
        </ul>
      </div>
      <div class="ft-col">
        <h2 class="ft-h">Wiseman Residential</h2>
        <address class="ft-addr">
          1520 Federal Ave, Los Angeles, CA 90025<br>
          Leasing <a href="tel:+13104733000">+1 310-473-3000</a>
        </address>
        <p class="ft-social">
          <a class="lnk" href="https://www.facebook.com/Officialwisemanresidential/" target="_blank" rel="noopener">Facebook</a>
          <a class="lnk" href="https://www.instagram.com/officialwisemanresidential" target="_blank" rel="noopener">Instagram</a>
          <a class="lnk" href="https://www.yelp.com/biz/wiseman-residential-los-angeles-2" target="_blank" rel="noopener">Yelp</a>
        </p>
      </div>
    </div>

    <nav class="ft-legal" aria-label="Legal and utility">
      <a href="privacy.html">Privacy Policy</a>
      <a href="accessibility.html">Accessibility</a>
      <a href="privacy-choices.html">Your Privacy Choices</a>
      <a href="#site-map">Site Map</a>
    </nav>
    <div class="ft-base">
      <span class="ft-brand">""" + MARK + """<b>Wiseman Residential</b></span>
      <p class="eho"><svg viewBox="0 0 12 10.608" role="img" aria-label="Equal Housing Opportunity" fill="currentColor" focusable="false"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.95263 1.07242L0 4.00926V5.38295H0.663158V9.51979H11.2026V5.38295H11.9921V4.00926L5.95263 1.07242ZM9.9 8.27242H1.95789V4.49874L5.95263 2.44611L9.9 4.49874V8.27242Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 5.82505H4.08947V4.49874H7.77632V5.82505Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 7.73558H4.08947V6.40926H7.77632V7.73558Z"/></svg><span>Equal Housing Opportunity</span></p>
      <p class="ft-copy">&copy; 2026 Wiseman Residential</p>
    </div>
  </div>
</footer>
"""


def scripts(extra, maps=False, search=False):
    mapjs = ""
    if search:
        mapjs += '<script src="../core/rail.js?v=%s" defer></script>\n' % RAIL_V
    if maps or search:
        mapjs += '<script src="../core/map.js?v=%s" defer></script>\n' % MAP_V
    if search:
        mapjs += '<script src="../core/search.js?v=%s" defer></script>\n' % SEARCH_V
    return f"""
<script src="../core/core.js?v={CORE_V}" defer></script>
<script src="app.js?v={APP_V}" defer></script>
{mapjs}
{extra}
</body>
</html>
"""


# =====================================================================
# 1. buildings.html — ALL BUILDINGS
# =====================================================================
def build_register():
    og = tx(PROPS[12]["image"], SOCIAL)

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "All 72 Wiseman apartment buildings in Los Angeles",
        "url": SITE + "buildings.html",
        "isPartOf": {"@type": "WebSite", "name": "Wiseman Residential", "url": SITE},
        "about": {
            "@type": "Organization",
            "name": "Wiseman Residential",
            "url": SITE,
            "telephone": "+1 310-473-3000",
        },
        "breadcrumb": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Wiseman Residential", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": "Buildings",
                 "item": SITE + "buildings.html"},
            ],
        },
    }, indent=2)

    out = [head(
        "All 72 Wiseman buildings in Los Angeles | Wiseman Residential",
        "Every one of the 72 apartment buildings Wiseman Residential owns, builds and manages in Los Angeles, "
        "grouped by neighbourhood and sortable by street, bedrooms or rent. Read it as a list, "
        "as an atlas or as plates.",
        SITE + "buildings.html",
        og,
        "A Wiseman apartment building in West Los Angeles.",
        jsonld,
        maps=True,
    )]
    out.append(furniture("buildings.html"))

    a = out.append
    a('\n<main id="main">\n')

    # ---------------------------------------------------------- masthead
    a("""  <!-- ================================================= PAGE OPENING. -->
  <section class="sec sec-tight page-top page-top-tabs wrap wrap-n" aria-labelledby="page-h">
    <ol class="crumbs" aria-label="Breadcrumb">
      <li><a href="index.html">Home</a></li>
      <li><span aria-current="page">Buildings</span></li>
    </ol>
    <div class="sec-head mt-4">
      <p class="kicker">All buildings</p>
      <h1 class="t-1 rv" id="page-h">All seventy&#8209;two, in one list.</h1>
      <p class="lede rv rv-d1">Grouped by neighbourhood, with a running count. Sort it however you
        need it &mdash; by street, by the largest home in the building, or by the rent the
        leasing feed publishes today. Nothing is held back behind a filter.</p>
    </div>
    <!-- View switch and sort share ONE row at >=1100px (view left, sort
         right, one hairline under); below 1100 they stack. The sort buttons
         are queried globally, so they drive the register from here. -->
    <div class="viewsort" data-viewsort>
      <nav class="viewbar" aria-label="Register views">
        <a href="buildings.html?view=register" data-viewlink="register" aria-current="page">List</a>
        <a href="buildings.html?view=atlas" data-viewlink="atlas">Atlas</a>
        <a href="buildings.html?view=plates" data-viewlink="plates">Plates</a>
      </nav>
      <div class="jsonly viewsort-sort" data-sortwrap>
        <div class="sortbar" role="group" aria-label="Sort the list">
          <span class="kicker">Sort</span>
          <button type="button" data-sort="area" aria-pressed="true">Neighbourhood</button>
          <button type="button" data-sort="no" aria-pressed="false">Recommended</button>
          <button type="button" data-sort="street" aria-pressed="false">Street A&ndash;Z</button>
          <button type="button" data-sort="beds" aria-pressed="false">Bedrooms</button>
          <button type="button" data-sort="rent" aria-pressed="false">Rent</button>
        </div>
      </div>
    </div>
  </section>
""")

    # ------------------------------------------------------- atlas view
    # The heading only. The map itself lives inside the register layout, in
    # the column the specimen plate otherwise occupies, so the two-way
    # highlight ([data-row][data-no] <-> pin) has real rows to light.
    a("""
  <!-- ==================================================== VIEW: ATLAS. -->
  <section class="sec sec-tight wrap wrap-n view-alt" id="view-atlas" data-view="atlas" aria-labelledby="atlas-h">
    <div class="sec-head">
      <p class="kicker">Atlas</p>
      <h2 class="t-2" id="atlas-h">Seventy-two buildings, on the real city.</h2>
      <p class="body">Every building is a dot on the real map. Point at a dot to light its row,
        or at a row to light its dot.</p>
    </div>
  </section>
""")

    # ---------------------------------------------------- register view
    a("""
  <!-- ===================================================== VIEW: LIST. -->
  <section class="sec sec-tight wrap wrap-n" id="view-register" data-view="register" aria-labelledby="reg-h">
    <h2 class="vh" id="reg-h">All buildings, as a list</h2>

    <div class="reg-bar">
      <form class="search" action="search.html" method="get" role="search" data-regform>
        <label class="field-lbl" for="q">Find a street, a neighbourhood or a building</label>
        <div class="search-row">
          <input class="search-in" type="search" id="q" name="q" autocomplete="off"
                 placeholder="Brockton, Hollywood, Motor Tides&hellip;" data-regq>
          <button class="search-go" type="submit">Search <span class="arw" aria-hidden="true">&#8594;</span></button>
        </div>
      </form>
    </div>

    <noscript><p class="small mt-3">Sorting, search and the other two views need JavaScript. The
      list below is complete without it: all 72 buildings, grouped by neighbourhood.</p></noscript>

    <p class="small mt-3" data-status hidden><span data-statustext></span>
      <a class="lnk" href="buildings.html">Show all 72</a></p>

    <div class="reg-lay">
      <div data-register data-mode="grouped">
""")

    for key, area in AREAS.items():
        rows = [p for p in PROPS if p["areaKey"] == key]
        a('        <section class="reg-group" data-group="%s" aria-labelledby="g-%s">\n' % (e(key), e(key)))
        a('          <h3 class="reg-head" id="g-%s"><span data-grouplabel>%s</span>'
          '<span class="tnum" data-groupcount="%d">%d</span></h3>\n'
          % (e(key), e(area["name"]), len(rows), len(rows)))
        a('          <div class="reg-rows" data-rows>\n')
        for p in rows:
            beds_max = p.get("bedsMax")
            a('            <div class="reg-row" data-row data-no="%s" data-name="%s" data-street="%s"'
              ' data-area="%s" data-arealabel="%s" data-bedsmax="%s"%s data-lat="%s" data-lng="%s"'
              ' data-img="%s">\n'
              % (e(p["no"]), e(p["short"]), e(p["street"]), e(p["areaKey"]), e(p["area"]),
                 ("%d" % int(beds_max)) if beds_max is not None else "",
                 rent_attr(p),
                 e(p["lat"]), e(p["lng"]), e(tx(p["image"], PLATE))))
            a('              <a href="buildings/%s.html">'
              '<span class="reg-name">%s</span>'
              '<span class="reg-street">%s &middot; %s</span>'
              '<span class="reg-meta reg-beds tnum">%s</span>'
              '<span class="reg-meta reg-rent tnum">%s</span></a>\n'
              % (e(p["path"]), e(p["short"]), e(p["street"]), e(p["area"]),
                 e(beds_label(p) + (" beds" if beds_label(p) != "—" else "")),
                 e(price_shown(p))))
            a('            </div>\n')
        a('          </div>\n')
        a('        </section>\n')

    first = PROPS[0]
    a("""      </div>

      <aside class="plate" data-plate aria-hidden="true">
        <div class="plate-img"><img src="%s" alt="" width="900" height="675" loading="lazy" decoding="async"></div>
        <div class="plate-meta">
          <span class="plate-name" data-platename>%s</span>
          <span class="plate-street" data-platestreet>%s &middot; %s</span>
        </div>
        <p class="micro mt-2">Point at a row, or tab through them, to bring the building up here.</p>
      </aside>

      <div class="reg-map" id="portfolio-map" data-labels="hover" hidden>
        <p class="atlas-fb small">A map of all 72 buildings loads here. The list beside it is
          complete and does not need it.</p>
      </div>
    </div>
  </section>
""" % (e(tx(first["image"], PLATE)), e(first["short"]),
       e(first["street"]), e(first["area"])))

    # ------------------------------------------------------ plates view
    a("""
  <!-- =================================================== VIEW: PLATES. -->
  <section class="sec sec-tight wrap wrap-n view-alt" id="view-plates" data-view="plates" aria-labelledby="plates-h">
    <div class="sec-head">
      <p class="kicker">Plates</p>
      <h2 class="t-2" id="plates-h">The same seventy-two, photographed.</h2>
      <p class="body">One frame per building, straight from the leasing feed, grouped by
        neighbourhood exactly as the list is. Name and street underneath.</p>
    </div>
""")
    # The same seven groups, in the same order and under the same heading as
    # the register, so the two views read as one collection. Every frame is
    # the same 3:2 crop; the sheet is a plain grid with 1px gutters.
    for key, area in AREAS.items():
        rows = [p for p in PROPS if p["areaKey"] == key]
        a('    <section class="plates-group" data-platesgroup="%s" aria-labelledby="pg-%s">\n' % (e(key), e(key)))
        a('      <h3 class="reg-head" id="pg-%s"><span>%s</span>'
          '<span class="tnum">%d</span></h3>\n' % (e(key), e(area["name"]), len(rows)))
        a('      <ul class="plates">\n')
        for p in rows:
            a('        <li class="plate-cell"><a href="buildings/%s.html">'
              '<span class="plate-cell-fig"><img src="%s" alt="%s, %s" loading="lazy" decoding="async" width="600" height="400"></span>'
              '<span class="plate-cell-meta"><span class="plate-cell-st">%s</span>'
              '<span class="plate-cell-ad">%s &middot; %s</span></span></a></li>\n'
              % (e(p["path"]), e(tx(p["image"], THUMB)), e(p["short"]), e(p["area"]),
                 e(p["short"]), e(p["street"]), e(p["area"])))
        a('      </ul>\n')
        a('    </section>\n')
    a("""  </section>
""")

    # ---------------------------------------------------------- the line
    a("""
  <!-- ============================== ONE LINE OUT, TO THE LEASING DOOR. -->
  <section class="sand-ground bleed-tight">
    <div class="wrap wrap-n">
      <p class="lede measure">This is the whole portfolio, open or not.
        <a class="lnk" href="search.html">What is available now <span class="arw" aria-hidden="true">&#8594;</span></a></p>
    </div>
  </section>

</main>
""")

    a(FOOTER)
    a(scripts(REGISTER_JS, maps=True))

    return "".join(out)


REGISTER_JS = """<script>
/* buildings.html — the only page-local script. Adds nothing to app.js:
   it calls WR.register / WR.atlas, switches the three peer views behind
   real URLs, and searches the rows already in the page. No rAF loop;
   WR.onScroll remains the only one on the site.
   core.js and app.js are deferred, so they have both run and booted by
   DOMContentLoaded — this must wait for it. */
addEventListener('DOMContentLoaded', function () {
  'use strict';
  if (!window.WR) return;
  var W = window.WR;

  var list = document.querySelector('[data-register]');
  var rows = [].slice.call(document.querySelectorAll('[data-row]'));
  var groups = [].slice.call(document.querySelectorAll('.reg-group'));
  var TOTAL = rows.length;

  /* sort controls + the specimen plate (hover AND keyboard focus) */
  W.register({ list: '[data-register]', flatLabel: 'All buildings' });

  /* ---------------------------------------------------------- search */
  /* The rows are the corpus — no second fetch, no dropdown. The form has a
     real action= and name="q", so buildings.html?q=brockton works with no
     JS at all; this only answers without a round trip. */
  var hay = rows.map(function (r) {
    return (r.dataset.name + ' ' + r.dataset.street + ' ' +
            r.dataset.arealabel).toLowerCase();
  });
  var form = document.querySelector('[data-regform]');
  var input = document.querySelector('[data-regq]');
  var status = document.querySelector('[data-status]');
  var statusText = document.querySelector('[data-statustext]');
  var term = '';

  function applySearch() {
    var t = term.trim().toLowerCase();
    var flat = list.dataset.mode === 'flat';
    var shown = 0, i;
    for (i = 0; i < rows.length; i++) {
      var ok = !t || hay[i].indexOf(t) > -1;
      rows[i].hidden = !ok;
      if (ok) shown++;
    }
    groups.forEach(function (g, gi) {
      var c = g.querySelector('[data-groupcount]');
      if (flat) {
        g.hidden = gi > 0;
        if (gi === 0 && c) c.textContent = shown;
        return;
      }
      var vis = 0;
      for (var j = 0; j < rows.length; j++) {
        if (rows[j].dataset.area === g.dataset.group && !rows[j].hidden) vis++;
      }
      g.hidden = !!t && vis === 0;
      if (c) c.textContent = t ? vis : c.dataset.groupcount;
    });
    if (status) {
      status.hidden = !t;
      if (statusText) {
        statusText.textContent = t
          ? (shown + (shown === 1 ? ' building matches ' : ' buildings match ') + '\\u201C' + term.trim() + '\\u201D.')
          : '';
      }
    }
  }

  function pushTerm() {
    try {
      var u = new URL(location.href);
      if (term.trim()) u.searchParams.set('q', term.trim()); else u.searchParams.delete('q');
      history.replaceState(null, '', u);
    } catch (err) {}
  }

  if (input) {
    input.addEventListener('input', function () { term = input.value; applySearch(); pushTerm(); });
  }
  if (form) {
    /* bound to the form itself, so it runs before core's transition
       delegate and the curtain never drops on a same-page search */
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      term = input ? input.value : '';
      applySearch(); pushTerm();
    });
  }
  /* The specimen rests on the FIRST row of the current sort, not just the
     first-authored building — so re-sorting updates the resting plate. Core
     still owns hover/focus; this only moves the default. */
  var plateEl = document.querySelector('[data-plate]');
  function restSpecimen() {
    if (!plateEl) return;
    var first = document.querySelector('[data-row]:not([hidden])');
    if (!first) return;
    var img = plateEl.querySelector('img'),
        nm = plateEl.querySelector('[data-platename]'),
        st = plateEl.querySelector('[data-platestreet]');
    plateEl.dataset.cur = first.dataset.no;
    if (img && first.dataset.img) { img.src = first.dataset.img; img.alt = first.dataset.name; }
    if (nm) nm.textContent = first.dataset.name;
    if (st) st.textContent = first.dataset.street + ' \\u00B7 ' + first.dataset.arealabel;
  }

  /* re-apply after a sort: these listeners are added after WR.register's,
     so they run once the rows have been re-parented */
  [].forEach.call(document.querySelectorAll('[data-sort]'), function (b) {
    b.addEventListener('click', function () { applySearch(); restSpecimen(); });
  });

  /* ----------------------------------------------------------- views */
  var views = {};
  [].forEach.call(document.querySelectorAll('[data-view]'), function (v) {
    views[v.dataset.view] = v;
  });
  var links = [].slice.call(document.querySelectorAll('[data-viewlink]'));
  var plate = document.querySelector('[data-plate]');
  var sortWrap = document.querySelector('[data-sortwrap]');
  var mapHost = document.getElementById('portfolio-map');
  var mapBuilt = false;

  /* The real map. Every point is read off the row that is already in the
     page, so the popup can never disagree with the register — including the
     rent, which FACT-CHECK suppresses for 071 in the row and therefore in
     the popup too. */
  function buildMap() {
    if (!W.map || !mapHost) return;
    var pts = [];
    rows.forEach(function (r) {
      var la = parseFloat(r.dataset.lat), ln = parseFloat(r.dataset.lng);
      if (!la || !ln) return;
      var link = r.querySelector('a');
      var beds = r.querySelector('.reg-beds');
      var rent = r.querySelector('.reg-rent');
      pts.push({
        no: r.dataset.no, lat: la, lng: ln,
        name: r.dataset.name, street: r.dataset.street,
        area: r.dataset.area, areaLabel: r.dataset.arealabel,
        beds: beds ? beds.textContent.trim() : '',
        rent: rent ? rent.textContent.trim() : '',
        img: r.dataset.img,
        url: link ? link.getAttribute('href') : ''
      });
    });
    var areas = {};
    [].forEach.call(document.querySelectorAll('.reg-group[data-group]'), function (g) {
      var label = g.querySelector('[data-grouplabel]');
      var count = g.querySelector('[data-groupcount]');
      if (!label || !count) return;
      areas[g.dataset.group] = { name: label.textContent.trim(), count: +count.dataset.groupcount || 0 };
    });
    W.map({
      el: '#portfolio-map', theme: 'light', points: pts, areas: areas,
      label: 'Map of all ' + pts.length + ' Wiseman buildings across Los Angeles',
      /* the container was display:none until a moment ago, so Leaflet's first
         size reading can be stale: measure again, then fit. */
      onReady: function (m, L) {
        var b = L.latLngBounds(pts.map(function (p) { return [p.lat, p.lng]; }));
        setTimeout(function () {
          m.invalidateSize();
          /* the same proportional padding map.js fits with. A flat 44px each
             side spends a third of a 320px phone panel on air and costs a
             whole zoom level, which opened the portfolio over Santa Clarita. */
          var px = Math.max(16, Math.min(48, Math.round(mapHost.clientWidth * 0.05)));
          var py = Math.max(16, Math.min(48, Math.round(mapHost.clientHeight * 0.06)));
          m.fitBounds(b, { padding: [px, py] });
        }, 60);
      }
    });
  }

  function setView(name, push) {
    if (!views[name]) name = 'register';
    /* Atlas is not a replacement for the register — it is the register with
       a map in the column the specimen plate usually holds. */
    var atlas = name === 'atlas';
    views.register.hidden = name === 'plates';
    Object.keys(views).forEach(function (k) {
      if (k !== 'register') views[k].classList.toggle('on', k === name);
    });
    if (plate) plate.hidden = atlas;
    /* sort does nothing in Plates (statically grouped), so hide it there;
       it is meaningful in List and Atlas, which both re-sort the register. */
    if (sortWrap) sortWrap.hidden = name === 'plates';
    if (mapHost) mapHost.hidden = !atlas;
    var lay = document.querySelector('.reg-lay');
    if (lay) lay.classList.toggle('atlas-on', atlas);
    links.forEach(function (a) {
      if (a.dataset.viewlink === name) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    if (atlas && !mapBuilt) { mapBuilt = true; buildMap(); }
    else if (atlas && W.mapInstance) {
      /* coming back to the atlas from another view: re-measure, never re-init */
      setTimeout(function () { W.mapInstance.invalidateSize(); }, 40);
    }
    if (push) {
      try {
        var u = new URL(location.href);
        u.searchParams.set('view', name);
        history.pushState(null, '', u);
      } catch (err) {}
    }
  }

  /* bound to each link, not delegated: a target-phase preventDefault runs
     before core's document-level transition handler, so switching view
     never drops the page curtain */
  links.forEach(function (a) {
    a.addEventListener('click', function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || ev.button) return;
      ev.preventDefault();
      setView(a.dataset.viewlink, true);
    });
  });
  addEventListener('popstate', function () {
    var p = new URLSearchParams(location.search);
    term = p.get('q') || '';
    if (input) input.value = term;
    applySearch();
    setView(p.get('view') || 'register', false);
  });

  /* ------------------------------------------------- restore from URL */
  var params = new URLSearchParams(location.search);
  term = params.get('q') || '';
  if (input) input.value = term;
  applySearch();
  setView(params.get('view') || 'register', false);
});
</script>"""


# =====================================================================
# 2. search.html — THE TRANSACTIONAL DOOR
# =====================================================================
def build_availability():
    """The ILS marketplace door.

    Everything between <!--SEARCH--> and <!--/SEARCH--> is written by
    scripts/gen_search.py, which is shared by all three directions: the sticky
    filter bar, the More-filters modal, the chips, the live count, the sort
    control and the 72 static result cards beside a real Leaflet map. This
    function owns only the page's own furniture — head, breadcrumb, a compact
    <h1> and one line, the footer and the page wiring. The standing note about
    the live leasing system is the one-liner gen_search.py prints under the count.
    """
    og = tx(PROPS[68]["image"], SOCIAL)

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Find a home — Wiseman Residential",
        "url": SITE + "search.html",
        "description": ("Search and filter 72 Wiseman apartment buildings in Los Angeles by "
                        "neighbourhood, bedrooms, baths, rent, size and features, on a live map. "
                        "The live leasing system is the authority on availability and pricing."),
        "isPartOf": {"@type": "WebSite", "name": "Wiseman Residential", "url": SITE},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint",
                       "urlTemplate": SITE + "search.html?q={search_term_string}"},
            "query-input": "required name=search_term_string",
        },
        "breadcrumb": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Wiseman Residential", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": "Find a home",
                 "item": SITE + "search.html"},
            ],
        },
    }, indent=2)

    out = [head(
        "Find a home &mdash; search 72 buildings | Wiseman Residential",
        "Search and filter every Wiseman building in Los Angeles by neighbourhood, bedrooms, baths, "
        "rent, size and features, on a live map. Studios to five bedrooms across seven neighbourhoods.",
        SITE + "search.html",
        og,
        "A Wiseman apartment building on Venice Boulevard, Los Angeles.",
        jsonld,
        search=True,
    )]
    out.append(furniture("search.html", body_class="searchpage"))
    a = out.append

    a('\n<main id="main">\n')

    a("""  <!-- ================================================= PAGE OPENING.
       Breadcrumb, a modest H1 and one line — compact, so the filter bar is in
       the first screen. The standing note about the live leasing system is the
       one-line .snote gen_search.py prints under the result count. -->
  <section class="search-top wrap wrap-n" aria-labelledby="page-h">
    <ol class="crumbs" aria-label="Breadcrumb">
      <li><a href="index.html">Home</a></li>
      <li><span aria-current="page">Find a home</span></li>
    </ol>
    <h1 class="search-h1" id="page-h">Find a home in Los&nbsp;Angeles.</h1>
    <p class="search-line">Filter by neighbourhood, bedrooms, baths, rent, size and features. The map keeps pace with the list.</p>
    <noscript>
      <p class="small measure mt-3">The filters need JavaScript. All %d buildings are listed below
        with the bedrooms, baths, square footage and rent their listings publish, and every one
        links to its own page.</p>
    </noscript>
  </section>

  <!-- The search block below is written by scripts/gen_search.py and opens at <h3>
       (the card name). Without this the outline runs h1 -> h3 and the results have
       no heading of their own. It is set visually hidden rather than printed: the
       live count and the filter bar already announce the region on screen. -->
  <h2 class="vh">Matching buildings</h2>

<!--SEARCH-->
<!--/SEARCH-->
</main>
""" % TOTAL)

    a(FOOTER)
    a(scripts(AVAILABILITY_JS, search=True))
    return "".join(out)


AVAILABILITY_JS = """<script>
/* search.html — page wiring only. core.js, app.js, rail.js, map.js and
   search.js are all deferred, so every one of them has run by DOMContentLoaded.
   Nothing here authors markup and nothing here opens a second rAF loop. */
addEventListener('DOMContentLoaded', function () {
  'use strict';
  if (!window.WR) return;

  /* The header is fixed and the filter bar sticks underneath it, so both
     heights are measured rather than guessed: the bar parks exactly under the
     header and the map column starts exactly where the bar ends. A resize
     listener, not a scroll loop. */
  var hd = document.querySelector('.hd');
  var bar = document.querySelector('.sbar');
  function metrics() {
    var s = document.documentElement.style;
    if (hd) s.setProperty('--hdh', hd.offsetHeight + 'px');
    if (bar) s.setProperty('--sbarh', bar.offsetHeight + 'px');
  }
  metrics();
  addEventListener('resize', metrics);
  if (window.ResizeObserver && bar) new ResizeObserver(metrics).observe(bar);

  WR.rails();

  /* core/rail.js stamps role="group" on whatever it is handed as a track so the
     focusable scroll container has a name. Here the track IS the search <form>,
     which shipped as role="search" — so making the bar a rail silently deleted
     the page's only search landmark. Hand it back after rails() has run. The
     aria-label the module found is the form's own, and tabindex="0" keeps the
     scrollable region keyboard-reachable either way. */
  var sform = bar && bar.querySelector('form[data-rail-track]');
  if (sform) sform.setAttribute('role', 'search');

  /* The filter bar is itself a rail, and core/rail.js binds Arrow/Home/End on
     the track to scroll it. The track is the <form>, so those keys would bubble
     up out of the search box and the rent selects and move the rail instead of
     the caret. Stop exactly those four keys at the control, and nothing else —
     Escape still has to reach the popover and the dialog. */
  if (bar) {
    var NAV = { ArrowLeft: 1, ArrowRight: 1, Home: 1, End: 1 };
    [].forEach.call(bar.querySelectorAll('input, select, textarea'), function (el) {
      el.addEventListener('keydown', function (e) { if (NAV[e.key]) e.stopPropagation(); });
    });
  }

  /* search.js drives `[data-clearall]` off the FIRST one it finds in the root,
     and in this markup that is the dialog's, not the one beside the chips. Two
     bugs came out of that single line:
       1. the Clear all beside the chips never appeared at all;
       2. the dialog's own Clear all was hidden whenever no filter was set, and
          .fmodal-f is space-between — so ticking the first filter threw the
          Apply button 415px across the dialog.
     Drive both off the module's own wr:filtered event rather than duplicating a
     line of its logic: the chips one appears and disappears, the dialog one
     keeps its place and greys out, so the primary action never moves. Register
     it BEFORE searchPage so the first pass, hydrated from the URL, counts too. */
  var root = document.querySelector('[data-search]');
  var chipsClear = root && root.querySelector('.sresults [data-clearall]');
  var modalClear = root && root.querySelector('.fmodal [data-clearall]');
  if (root && chipsClear) {
    root.addEventListener('wr:filtered', function () {
      var any = !!root.querySelector('.chip-f');
      chipsClear.hidden = !any;
      if (modalClear) { modalClear.hidden = false; modalClear.disabled = !any; }
    });
  }

  /* scripts/gen_search.py writes data-bedsmin="" / -bedsmax="" / -bathsmin="" /
     -bathsmax="" for a building whose listing publishes no figure — 023 Purdue
     Point reads "—" for beds, baths, size and rent. core/search.js guards that
     case with isNaN(+d.bedsmin), but +'' is 0, not NaN, so an empty attribute
     read as "studio, zero beds" and 023 came back under the Studio filter
     advertising a home it does not list (25 results where the data says 24).
     Drop the empty attributes so the module's own guard fires as written. */
  [].forEach.call(document.querySelectorAll('[data-card]'), function (c) {
    ['bedsmin', 'bedsmax', 'bathsmin', 'bathsmax'].forEach(function (k) {
      if (c.dataset[k] === '') delete c.dataset[k];
    });
  });

  WR.searchPage({});

  /* The real map, filtered in step with the list. No rent is passed to any pin:
     FACT-CHECK bans a Motor Tides figure anywhere, and a popup is anywhere. */
  fetch('../data/wiseman.json').then(function (r) { return r.json(); }).then(function (d) {
    WR.map({
      el: '#search-map', pins: 'price',
      theme: 'light',
      label: 'Map of the Wiseman buildings matching the current filters',
      points: d.properties.map(function (p) {
        return {
          no: p.no, lat: p.lat, lng: p.lng, name: p.short, street: p.street,
          area: p.areaKey, areaLabel: p.area, beds: p.beds,
          img: p.thumb, url: 'buildings/' + p.path + '.html', pinLabel: p.no === '071' ? 'New' : ''
        };
      }),
      areas: Object.keys(d.areas).reduce(function (o, k) {
        o[k] = { name: d.areas[k].name, count: d.areas[k].count };
        return o;
      }, {})
    });
  });
});
</script>"""


# =====================================================================
def main():
    pages = {
        "buildings.html": build_register(),
        "search.html": build_availability(),
    }
    for name, body in pages.items():
        path = os.path.join(HERE, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("wrote %-18s %6d bytes" % (name, len(body.encode("utf-8"))))

    print("\nportfolio  %d buildings, %d areas" % (TOTAL, len(AREAS)))
    print("bedrooms   " + " · ".join("%s %d" % (l, BED_COUNT[n]) for n, l in BED_OPTIONS))
    print("features   " + " · ".join("%s %d" % (l, AMEN_COUNT[k]) for k, l, _t in AMENITIES))
    print("no rent    %d buildings quote on request"
          % sum(1 for p in PROPS if p.get("priceMin") is None))


if __name__ == "__main__":
    main()
