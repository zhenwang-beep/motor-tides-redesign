#!/usr/bin/env python3
"""Generate THE PLATES — register/index.html, buildings.html, search.html.

    python3 register/gen_register.py

Why a generator: every plate and every row on these three pages must be real,
static, crawlable HTML — no client-side rendering of the collection — and they must
agree with each other on every number, name, street and photograph. This script is
the single source of that agreement.

What it does
  1. Reads ../data/wiseman.json (72 properties, 7 areas) and ../data/plates.json
     (one measured, verified photographic plate per building — see
     scripts/pick_plates.py for how each frame was chosen).
  2. Reads templates/_shell.html for the page furniture — skip link, header,
     neighbourhood strip, footer, mobile menu, curtain — so the nine pages
     cannot drift apart.
     Only aria-current is moved onto the nav item for the page being written.
  3. index.html — the home page, five screens at most: the opening plate with
     the search form, one plate per neighbourhood, the buildings with the most
     homes available today, one paragraph about the company, the footer. The
     book is not here (client note, round 5: the home page was 55,000px tall).
  4. buildings.html — the index proper. All 72 rows with the specimen plate and
     the real embedded map (?view=register | atlas), and the book under
     ?view=plates: seven neighbourhood runs, each an orderly grid of identical
     3:2 frames, opened by the run's one curated frame at full column width.
     The neighbourhood strip lives here (round 7, in place of the ruler): seven
     links with counts, sticky under the header, lit by app.js as the page
     scrolls whichever of the two collections is on screen.
  5. search.html — the ILS search page. The body between <!--SEARCH--> and
     <!--/SEARCH--> is written by scripts/gen_search.py from the shared module;
     this file writes only the shell, the <h1> and the standing note above it.

Nothing here invents a number. Bedrooms, baths, square feet and rent are the leasing
feed's own strings; a building the feed leaves blank prints an em dash and is
excluded from the filter that would otherwise silently claim something about it.
FACT-CHECK §2: no Motor Tides rent figure is published anywhere, in any view.

Round 7 (client note): no heading, lede or caption may end on a single word.
Every sentence this file writes ties its last two words with a no-break space
(tie() below), and the headings the client named are joined by hand. The
check is scratchpad/pw/orphans-r.js; register/style.css adds text-wrap.
"""

import json
import os
import re
import sys
import html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")
PLATES = os.path.join(ROOT, "data", "plates.json")
ARTDIR = os.path.join(ROOT, "data", "artdirection.json")
SHELL = os.path.join(HERE, "templates", "_shell.html")

VER = "18"                       # cache-bust: base.css, core.js, map.*, rail.*, search.*, style.css, app.js
SNAPSHOT = "10 September 2026"
TOTAL = 72

# Fixed group labels (design bible §9.5). Document order is the numbering order.
AREA_ORDER = ["west-la", "brentwood", "beverly-grove", "hollywood", "venice", "palms", "glendale"]
AREA_LABEL = {
    "west-la": "West Los Angeles · Sawtelle",
    "brentwood": "Brentwood",
    "beverly-grove": "Beverly Grove",
    "hollywood": "Hollywood",
    "venice": "Venice",
    "palms": "Palms · Motor Avenue",
    "glendale": "Glendale",
}
# The neighbourhood strip's label (one row under the header; the count follows it)
STRIP_LABEL = {
    "west-la": "West Los Angeles",
    "brentwood": "Brentwood",
    "beverly-grove": "Beverly Grove",
    "hollywood": "Hollywood",
    "venice": "Venice",
    "palms": "Palms · Motor Avenue",
    "glendale": "Glendale",
}

NBSP = "\u00a0"


def tie(s):
    """Join the last two words with a no-break space, so a sentence or a label
    never ends on a word alone on its line (client note, round 7). A one-word
    string is returned as it is; an HTML-escaped string keeps its entities."""
    return re.sub(r" (\S+)$", NBSP + r"\1", s)


# The area's name where it is a heading: the last two words tied, and where a
# middle dot separates a part of the name, the dot stays with the words either
# side of it so no line can start or end on the dot alone.
HEAD_LABEL = {
    "west-la": "West Los Angeles" + NBSP + "·" + NBSP + "Sawtelle",
    "brentwood": "Brentwood",
    "beverly-grove": "Beverly" + NBSP + "Grove",
    "hollywood": "Hollywood",
    "venice": "Venice",
    "palms": "Palms" + NBSP + "· Motor" + NBSP + "Avenue",
    "glendale": "Glendale",
}

# FACT-CHECK §2: no Motor Tides rent range may be published.
FLAG_NO = "071"

LEASING_TEL = "+1 310-473-3000"
APPLICANT = ("https://wisemanresidential.securecafe.com/onlineleasing/"
             "apartmentsforrent/guestlogin.aspx")

# ---------------------------------------------------------------- amenities
# Six facets, chosen because they are the only things the leasing feed records across
# 35+ of the 72 buildings. Each matcher reads the feed's own strings, which are spelled
# several ways ("In-Suite Washer & Dryer" / "In-Suite Washer and Dryer"), and refuses any
# string qualified "in select units" — the filter must not promise a whole building
# something the feed only claims for some homes in it. Counts are computed, never typed.
def _in_select(n):
    return "in select units" in n


AMENITIES = [
    ("wd", "In-suite washer and dryer",
     lambda n: n in ("in suite washer and dryer", "in unit washer and dryer")),
    ("patio", "Patio or balcony",
     lambda n: n in ("patio balcony", "balcony", "patio")),
    ("ac", "Air conditioning",
     lambda n: not _in_select(n) and ("air conditioning" in n or "air conditioner" in n
                                      or "central ac" in n)),
    ("gated", "Gated garage or entry",
     lambda n: n.startswith("gated") or n.startswith("controlled access")),
    ("elev", "Elevator", lambda n: n == "elevator"),
    ("closet", "Walk-in closets",
     lambda n: not _in_select(n) and n.startswith("walk in closets")),
]



# ---------------------------------------------------------------- helpers
def esc(s):
    return _html.escape(str(s), quote=True)


def norm(s):
    s = s.lower().replace("&", "and").replace("w/", "with ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def amen_keys(p):
    have = set(norm(a) for a in (p.get("community") or []) + (p.get("apartment") or []))
    return [k for k, _lbl, test in AMENITIES if any(test(n) for n in have)]


def dashify(s):
    """Feed ranges use a hyphen; the register sets them with an en dash."""
    return s.replace("-", "–")


def beds_label(p):
    s = (p.get("beds") or "").strip()
    if not s or s == "—":
        return "—"
    return dashify(re.sub(r"\s*Beds?$", "", s))


def baths_label(p):
    s = (p.get("baths") or "").strip()
    if not s or s == "—":
        return "—"
    return dashify(re.sub(r"\s*Baths?$", "", s))


def sqft_label(p):
    s = (p.get("sqft") or "").strip()
    if not s or s == "—":
        return "—"
    return re.sub(r"\s*Sq\.?\s*Ft\.?$", "", s, flags=re.I).replace(" to ", "–")


def money(n):
    return "$" + format(int(round(n)), ",")


def beds_span(p):
    """(min, max) as ints, or (-1, -1) when the feed lists no bedroom count.
    -1 keeps a building out of every bedroom filter instead of silently calling it a studio."""
    if p.get("bedsMin") is None or p.get("bedsMax") is None:
        return -1, -1
    return int(p["bedsMin"]), int(p["bedsMax"])


def street_line(p):
    return p["address"].split(",")[0].strip()


# ---------------------------------------------------------------- photography
class Plates(object):
    """One measured plate per building. See scripts/pick_plates.py."""

    # painted width per slot. Requested from the CDN, never above the master, so a
    # frame is served at the size it is actually painted and never upscaled by us.
    WIDTH = {"open": 2400, "area": 1100, "cell": 900, "half": 1100, "row": 420}

    def __init__(self, path):
        d = json.load(open(path, encoding="utf-8"))
        self.cdn = d["cdn"]
        self.hero = d["hero"]
        self.p = d["plates"]

    def kind(self, no):
        return self.p[no].get("kind")

    def dims(self, no):
        v = self.p[no]
        return v["w"], v["h"]

    def url(self, no, slot, base="../"):
        v = self.p[no]
        if v["local"]:
            return base + v["src"]
        w = min(self.WIDTH.get(slot, 1100), v["w"])
        return "%sq_auto,f_auto,w_%d/%s" % (self.cdn, w, v["src"])

    def hero_url(self, base="../"):
        return base + self.hero["src"] if self.hero["local"] else self.hero["src"]


# ---------------------------------------------------------------- the grid
# A run is a grid, not a collage. Every building in a neighbourhood sits in an
# identical 3:2 frame — three across at 1100px and up, two from 640, one below —
# under the run's head, with the same gutter between every pair. The one licence
# a run has is its opener: the frame a human looked at and approved for full
# width (data/plates.json `kind` bleed or wide) is moved to the front of its run
# and printed across the whole column, at the same 3:2. One per run, always
# first, never elsewhere. The client's note on round 4 was that the collage read
# as messy; the grid is the answer.
OPEN_KINDS = ("bleed", "wide")


def run_order(rows, plates):
    """The run's rows with its curated opener, if it has one, moved to the front.
    Returns (rows, opener_no)."""
    for p in rows:
        if plates.kind(p["no"]) in OPEN_KINDS:
            return [p] + [q for q in rows if q is not p], p["no"]
    return list(rows), None


def figure(p):
    """The right-aligned figure under a plate: the bedroom range and the lowest
    rent the feed lists — or the leasing flag for Motor Tides, which has no
    published rent to print (FACT-CHECK §2). An unpriced building prints its
    bedrooms alone; nothing is invented to fill the slot."""
    if p["no"] == FLAG_NO:
        return '<span class="pl-flag">Now leasing</span>'
    beds = beds_label(p)
    if p.get("priceMin") is None:
        return '<span class="tnum">%s</span>' % beds
    return '<span class="tnum">%s</span> &middot; from <span class="tnum">%s</span>' % (
        beds, money(p["priceMin"]))


def plate_html(p, plates, area_label, opener=False):
    w, h = plates.dims(p["no"])
    src = plates.url(p["no"], "open" if opener else "cell")
    alt = "%s, %s" % (p["short"], street_line(p))
    return """          <a class="pl{opencls}" href="buildings/{path}.html"
             data-plateitem data-no="{no}" data-name="{name}" data-area="{area}" data-arealabel="{arealabel}">
            <span class="pl-frame rvi"><img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></span>
            <span class="pl-cap">
              <span class="pl-nm">{name}</span>
              <span class="pl-st">{street}</span>
              <span class="pl-fg">{fig}</span>
            </span>
          </a>""".format(
        opencls=" pl--open" if opener else "", path=p["path"], no=p["no"],
        area=p["areaKey"], arealabel=esc(area_label), src=esc(src), alt=esc(alt),
        w=w, h=h, name=esc(p["short"]), street=esc(street_line(p)), fig=figure(p))


def run_html(key, rows, areas, plates, ordinal):
    """One neighbourhood run of the book on buildings.html. Its id is prefixed so
    it never collides with the register block for the same area in the other
    pane; the strip's links land on whichever is on screen (app.js)."""
    a = areas[key]
    ordered, opener = run_order(rows, plates)
    body = "\n".join(plate_html(p, plates, a["name"], opener=(p["no"] == opener))
                     for p in ordered)
    return """      <section class="run" id="p-{key}" data-group="{key}" aria-labelledby="ph-{key}">
        <header class="run-head">
          <p class="run-eyebrow rv"><span class="tnum">{ord:02d}</span><span>of seven</span><span>{sub}</span></p>
          <h2 class="run-h rv" id="ph-{key}">{label}</h2>
          <p class="run-meta rv"><span><b class="tnum">{n}</b>&nbsp;{word}</span><span><b class="tnum">{streets}</b>&nbsp;{sword}</span><a href="neighborhoods/{key}.html">The area&nbsp;&rarr;</a></p>
        </header>
        <div class="pgrid">
{body}
        </div>
      </section>""".format(key=key, n=len(rows), ord=ordinal, sub=tie(esc(a["sub"])),
                           label=esc(HEAD_LABEL[key]), word=plural(len(rows), "building"),
                           streets=len(a["streets"]), sword=plural(len(a["streets"]), "street"),
                           body=body)


def plural(n, word):
    return word if n == 1 else word + "s"


# ---------------------------------------------------------------- the home page
def area_plate(rows, plates, avoid):
    """The neighbourhood's one frame on the home page: never a frame the
    manifest says to avoid; then the run's curated opener; then any curated
    frame; then a true elevation; then the most pixels. Ties keep register
    order (max() returns the first maximum)."""
    def score(p):
        v = plates.p[p["no"]]
        return (p["no"] not in avoid, v.get("kind") in OPEN_KINDS, bool(v.get("kind")),
                bool(v.get("elevation")), v["w"] * v["h"])
    return max(rows, key=score)


def area_card(key, rows, areas, plates, avoid):
    a = areas[key]
    p = area_plate(rows, plates, avoid)
    w, h = plates.dims(p["no"])
    return """      <li class="ag">
        <a href="neighborhoods/{key}.html">
          <span class="ag-frame rvi"><img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></span>
          <span class="ag-cap">
            <span class="ag-nm">{label}</span>
            <span class="ag-n tnum">{n} {word}</span>
            <span class="ag-st">{sub}</span>
          </span>
        </a>
      </li>""".format(key=key, src=esc(plates.url(p["no"], "area")),
                      alt=esc("%s, %s" % (p["short"], street_line(p))), w=w, h=h,
                      label=esc(HEAD_LABEL[key]), n=len(rows), word=plural(len(rows), "building"),
                      sub=tie(esc(a["sub"])))


def now_leasing(props, n=6):
    """The buildings with the most homes listed available today, straight from
    the feed's availableNow; ties in register order."""
    live = [p for p in props if (p.get("availableNow") or 0) > 0]
    live.sort(key=lambda p: (-int(p["availableNow"]), p["no"]))
    return live[:n]


def now_card(p, plates):
    w, h = plates.dims(p["no"])
    n = int(p["availableNow"])
    if p["no"] == FLAG_NO:
        fx = '<span class="pl-flag">Now leasing</span>'
    elif p.get("priceMin") is None:
        fx = "&mdash;"
    else:
        fx = "From %s" % money(p["priceMin"])
    return """      <li class="ng">
        <a href="buildings/{path}.html">
          <span class="ng-frame rvi"><img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></span>
          <span class="ng-cap">
            <span class="ng-nm">{name}</span>
            <span class="ng-av tnum">{n} available now</span>
            <span class="ng-st">{street} &middot; {area}</span>
            <span class="ng-fx tnum">{fx}</span>
          </span>
        </a>
      </li>""".format(path=p["path"], src=esc(plates.url(p["no"], "cell")),
                      alt=esc("%s, %s" % (p["short"], street_line(p))), w=w, h=h,
                      name=esc(p["short"]), n=n, street=esc(street_line(p)),
                      area=esc(p["area"]), fx=fx)


# ---------------------------------------------------------------- furniture
def slice_between(src, start, end, what):
    i = src.index(start)
    j = src.index(end, i)
    out = src[i:j].rstrip()
    if not out:
        raise SystemExit("could not lift %s from templates/_shell.html" % what)
    return out


def lift_furniture():
    src = open(SHELL, encoding="utf-8").read()

    def one(pattern, what):
        m = re.search(pattern, src, re.S)
        if not m:
            raise SystemExit("could not lift %s from templates/_shell.html" % what)
        return m.group(0).strip()

    return {
        "skip": one(r'<a class="skip-link".*?</a>', "skip link"),
        "header": one(r'<header class="hd.*?</header>', "header"),
        "strip": one(r'<div class="nstrip" data-nstrip>.*?\n</div>', "neighbourhood strip"),
        "footer": one(r'<footer class="colophon.*?</footer>', "footer"),
        "mnav": one(r'<nav class="mnav".*?</nav>', "mobile menu"),
        "curtain": one(r'<div class="pt" aria-hidden="true">.*?\n</div>', "curtain"),
    }


def nav_current(header, href):
    """Mark the header nav item for the page being written, and clear the home flag."""
    header = header.replace(
        '<a class="brand" href="index.html" aria-label="Wiseman Residential, home" aria-current="page">',
        '<a class="brand" href="index.html" aria-label="Wiseman Residential, home">')
    if href is None:
        return header
    pat = '<a href="%s"' % href
    if pat not in header:
        raise SystemExit("nav item %s not found in the header" % href)
    return header.replace(pat, pat + ' aria-current="page"', 1)


def home_header(header):
    """index.html keeps aria-current on the mark itself."""
    return header


# ---------------------------------------------------------------- page shell
HEAD = """<!doctype html>
<html lang="en" data-base="" data-data="../data/wiseman.json" data-index="../data/index.json">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FBFAF7">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E%3Crect%20width='100'%20height='100'%20fill='%23FBFAF7'/%3E%3Cg%20fill='%23141414'%3E%3Cpolygon%20points='14,18%2034,18%2034,74%2014,80'/%3E%3Cpolygon%20points='40,18%2060,18%2060,71%2040,77'/%3E%3Cpolygon%20points='66,18%2086,18%2086,68%2066,74'/%3E%3C/g%3E%3C/svg%3E">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wiseman Residential">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://resource.rentcafe.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Libre+Franklin:wght@300..700&display=swap">
<link rel="stylesheet" href="../core/base.css?v={ver}">
<link rel="stylesheet" href="../core/map.css?v={ver}">{extra}
<link rel="stylesheet" href="style.css?v={ver}">
<script>(function(d){{var r=d.documentElement;r.classList.add('js');if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{r.classList.add('js-pt');setTimeout(function(){{r.classList.remove('js-pt');}},1500);}}}})(document);</script>
</head>
<body>
{skip}

{header}
"""

TAIL = """
{footer}

{mnav}

{curtain}

<script src="../core/core.js?v={ver}" defer></script>
<script src="../core/map.js?v={ver}" defer></script>{extra}
<script src="app.js?v={ver}" defer></script>{boot}
</body>
</html>
"""

AV_BOOT = """
<script>
/* search.html boots the shared ILS module. A classic inline script runs
   during parse — before every defer — so it waits for DOMContentLoaded, which
   fires after core.js, map.js, rail.js, search.js and app.js have all executed. */
document.addEventListener('DOMContentLoaded', function () {
  WR.rails();

  /* rail.js stamps role="group" on whatever element it turns into a track, and the
     track on this page is the search form itself. Put the landmark back: the
     aria-label it carries is a search label, not the name of a generic group. */
  var bar = document.querySelector('.sbar [data-rail-track]');
  if (bar && bar.tagName === 'FORM') bar.setAttribute('role', 'search');

  /* A building with no published bedroom count ships data-bedsmin="" /
     data-bedsmax="", and search.js reads those as +"" === 0 — so 023 Purdue Point
     (beds "—") answered the Studio filter and Studio counted 25 rather than 24.
     Write a value that is NaN under +, which is exactly what search.js's own
     isNaN(lo) guard is testing for. (data-bathsmax="" already falls out of the
     baths filter, because 0 is below every minimum it offers.) */
  [].forEach.call(document.querySelectorAll('[data-card]'), function (c) {
    if (c.dataset.bedsmin === '') c.dataset.bedsmin = 'na';
    if (c.dataset.bedsmax === '') c.dataset.bedsmax = 'na';
  });

  /* The filter popovers caption themselves with an <h4> inside a group that is
     already named by aria-label, so the only thing the heading level adds is an
     h2 -> h4 jump in the outline whenever a popover is open. Keep the words,
     drop the level. */
  [].forEach.call(document.querySelectorAll('[data-fmenu] h4'), function (h) {
    h.setAttribute('role', 'presentation');
  });

  WR.searchPage({});

  /* search.js shows or hides "the first [data-clearall] it finds" with the chip
     row, and in this markup that is the modal's own "Clear all filters", which
     must stay visible. So the Clear all beside the chips never appeared. Keep it
     in step with the chip row here rather than editing the shared module. */
  (function clearAll() {
    var chips = document.querySelector('[data-chips]');
    var btn = document.querySelector('.sresults [data-clearall]');
    if (!chips || !btn) return;
    function sync() { btn.hidden = chips.children.length === 0; }
    new MutationObserver(sync).observe(chips, { childList: true });
    sync();
  })();

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
    /* the map arrives after the first filter pass — re-run it so the pins and the
       fitted bounds match whatever the URL already asked for */
    if (WR.searchApply) WR.searchApply(false);
  });
});
</script>"""


ORG_LD = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Wiseman Residential",
  "slogan": "Los Angeles Living, Managed Wisely.",
  "telephone": "+1-310-473-3000",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1520 Federal Ave",
    "addressLocality": "Los Angeles",
    "addressRegion": "CA",
    "postalCode": "90025",
    "addressCountry": "US"
  },
  "areaServed": [
    "West Los Angeles",
    "Brentwood",
    "Beverly Grove",
    "Hollywood",
    "Venice",
    "Palms \\u00b7 Motor Avenue",
    "Glendale"
  ],
  "sameAs": [
    "https://www.facebook.com/Officialwisemanresidential/",
    "https://www.instagram.com/officialwisemanresidential",
    "https://www.yelp.com/biz/wiseman-residential-los-angeles-2"
  ]
}
</script>"""


# ------------------------------------------------- the neighbourhood strip
def strip_items(groups):
    """Seven links in area order, each with its count computed from the data.
    Every link is a real anchor to its register block, so the strip works with
    no JS; app.js scrolls smoothly, re-points at the run under ?view=plates,
    and lights the current area as the page scrolls."""
    out = []
    for i, key in enumerate(AREA_ORDER):
        out.append(
            '      <li><a href="#%s" data-nmark="%s"%s>%s <span class="tnum">%d</span></a></li>'
            % (key, key, ' aria-current="location"' if i == 0 else "",
               esc(STRIP_LABEL[key]), len(groups[key])))
    return "\n".join(out)


def with_strip(strip, groups):
    items = strip_items(groups)
    out, n = re.subn(r'(<ol class="nstrip-track[^>]*>\n).*?(\n    </ol>)',
                     lambda m: m.group(1) + items + m.group(2), strip, flags=re.S)
    if n != 1:
        raise SystemExit("could not re-write the neighbourhood strip")
    return out


# ---------------------------------------------------------------- register rows
def register_row(p, plates, area_label):
    bmax = "" if p.get("bedsMax") is None else str(int(p["bedsMax"]))
    rent = "" if p.get("priceMin") is None or p["no"] == FLAG_NO else str(int(p["priceMin"]))
    if p["no"] == FLAG_NO:
        fig = '<span class="row-flag">Now leasing</span>'
    elif p.get("priceMin") is None:
        fig = '<span class="row-rent tnum is-none">—</span>'
    else:
        fig = '<span class="row-rent tnum">%s</span>' % money(p["priceMin"])
    return """          <div class="reg-row" data-row data-no="{no}" data-name="{name}" data-street="{street}"
               data-area="{area}" data-arealabel="{arealabel}" data-bedsmax="{bmax}" data-rent="{rent}"
               data-img="{img}">
            <a class="row-link" href="buildings/{path}.html">
              <img class="row-thumb" src="{thumb}" alt="" width="56" height="56" loading="lazy" decoding="async">
              <span class="row-body">
                <span class="row-name">{name}</span>
                <span class="row-street">{street}</span>
              </span>
              <span class="row-figs">
                <span class="row-beds tnum">{beds}</span>
                {fig}
              </span>
            </a>
          </div>""".format(
        no=p["no"], name=esc(p["short"]), street=esc(p["street"]), area=p["areaKey"],
        arealabel=esc(area_label), bmax=bmax, rent=rent,
        img=esc(plates.url(p["no"], "half")), path=p["path"],
        thumb=esc(p["thumb"].replace("w_600,h_400", "w_160,h_160")),
        beds=beds_label(p), fig=fig)


def register_block(key, rows, areas, plates):
    a = areas[key]
    body = "\n".join(register_row(p, plates, a["name"]) for p in rows)
    return """        <section class="reg-block" id="{key}" data-group="{key}" aria-labelledby="h-{key}" style="--rows:{n}">
          <h2 class="reg-head" id="h-{key}"><span class="reg-head-label" data-grouplabel>{label}</span> <span class="reg-head-count tnum">{n}</span><span class="reg-head-flat tnum">72</span></h2>
          <p class="reg-head-sub">{sub} &middot; {streets}&nbsp;streets</p>
          <div class="reg-cols" aria-hidden="true"><span class="rc-body"><span>Building</span><span>Street</span></span><span class="rc-figs"><span>Bedrooms</span><span>From</span></span></div>
          <div class="reg-rows" data-rows>
{body}
          </div>
        </section>""".format(key=key, n=len(rows), label=esc(HEAD_LABEL[key]),
                             sub=esc(a["sub"]), streets=len(a["streets"]), body=body)


# ---------------------------------------------------------------- build
def main():
    data = json.load(open(DATA, encoding="utf-8"))
    props = data["properties"]
    areas = data["areas"]
    plates = Plates(PLATES)
    avoid = set(json.load(open(ARTDIR, encoding="utf-8")).get("avoid", []))
    F = lift_furniture()

    if len(props) != TOTAL:
        raise SystemExit("expected %d properties, found %d" % (TOTAL, len(props)))
    missing = [p["no"] for p in props if p["no"] not in plates.p]
    if missing:
        raise SystemExit("no plate for %s — run scripts/pick_plates.py" % missing)

    groups = {k: [p for p in props if p["areaKey"] == k] for k in AREA_ORDER}
    stray = [p["no"] for p in props if p["areaKey"] not in groups]
    if stray:
        raise SystemExit("properties outside the seven areas: %s" % stray)

    by_no = {p["no"]: p for p in props}

    # ---- facet counts, computed, never typed by hand
    area_counts = {k: len(v) for k, v in groups.items()}
    bed_counts = {n: 0 for n in range(6)}
    for p in props:
        lo, hi = beds_span(p)
        if lo < 0:
            continue
        for n in range(lo, hi + 1):
            if n in bed_counts:
                bed_counts[n] += 1
    amen_counts = {k: 0 for k, _l, _t in AMENITIES}
    for p in props:
        for k in amen_keys(p):
            amen_counts[k] += 1
    priced = [p for p in props if p.get("priceMin") is not None]
    streets_total = len({p["street"] for p in props})

    strip = with_strip(F["strip"], groups)

    # ============================================================== index.html
    hero = plates.hero
    hb = by_no[hero["no"]]
    page = HEAD.format(
        title="Wiseman Residential &mdash; Los Angeles living, managed wisely",
        ogtitle="Wiseman Residential &mdash; 72 buildings in Los Angeles, photographed",
        desc=("Wiseman Residential owns, develops and manages 72 apartment buildings "
              "across seven areas of Los Angeles and Glendale. Los Angeles living, "
              "managed wisely: one photograph for every building, grouped by neighborhood."),
        img=esc(hb["image"]), ver=VER, extra=ORG_LD, skip=F["skip"],
        header=home_header(F["header"]))
    # no neighbourhood strip on the home page: there is no collection here for it to track

    area_cards = "\n".join(area_card(k, groups[k], areas, plates, avoid) for k in AREA_ORDER)
    live = now_leasing(props)
    now_cards = "\n".join(now_card(p, plates) for p in live)

    page += """

<main id="main">

  <section class="hero" aria-labelledby="hero-h" data-hd="dark">
    <div class="hero-frame">
      <img class="hero-img" src="{hero_src}" alt="{hero_alt}" width="{hero_w}" height="{hero_h}"
           style="object-position:{hero_pos}" fetchpriority="high" decoding="async">
    </div>
    <div class="hero-scrim" aria-hidden="true"></div>
    <div class="hero-in wrap wrap-n">
      <p class="hero-mast"><span>Wiseman Residential</span><span>Owner &middot; Developer &middot; Manager</span><span>Los Angeles</span></p>
      <h1 class="hero-h" id="hero-h"><span class="hl"><i>Los Angeles living,</i></span><span class="hl"><i>managed wisely.</i></span></h1>
      <p class="hero-sub">Studios to five-bedroom homes in {total} buildings across seven parts of Los Angeles, each with its own leasing&nbsp;line.</p>
      <form class="search hs" action="search.html" method="get" role="search">
        <label class="vh" for="reg-q">Search by building, street or area</label>
        <div class="search-row hs-row">
          <input class="search-field" id="reg-q" name="q" type="search" autocomplete="off"
                 placeholder="Building, street or area" data-typeahead
                 role="combobox" aria-expanded="false" aria-controls="reg-ta" aria-autocomplete="list">
          <label class="hs-sel"><span class="vh">Neighbourhood</span><select name="area"><option value="">Anywhere</option><option value="west-la">West Los Angeles</option><option value="beverly-grove">Beverly Grove</option><option value="brentwood">Brentwood</option><option value="hollywood">Hollywood</option><option value="venice">Venice</option><option value="palms">Palms · Motor Avenue</option><option value="glendale">Glendale</option></select></label>
          <label class="hs-sel"><span class="vh">Bedrooms</span><select name="beds"><option value="">Any beds</option><option value="0">Studio</option><option value="1">1 bed</option><option value="2">2 beds</option><option value="3">3 beds</option><option value="4">4 beds</option><option value="5">5 beds</option></select></label>
          <button class="search-btn" type="submit">Search</button>
        </div>
        <ul class="ta" id="reg-ta" role="listbox" aria-label="Matching buildings" data-typeahead-out hidden></ul>
      </form>
    </div>
    <p class="hero-cap">
      <span>{hero_name}</span>
      <span>{hero_street}</span>
    </p>
  </section>

  <section class="hsec wrap wrap-n" aria-labelledby="areas-h">
    <header class="hsec-head">
      <p class="hsec-eyebrow rv"><span class="tnum">7</span><span>neighbourhoods</span><span class="tnum">{total}&nbsp;buildings</span></p>
      <h2 class="hsec-h rv" id="areas-h">Seven&nbsp;neighbourhoods.</h2>
      <p class="hsec-sub rv">{wla} buildings stand in West Los Angeles alone. The rest reach from Brentwood to Hollywood, Venice and&nbsp;Glendale.</p>
    </header>
    <ul class="agrid">
{area_cards}
    </ul>
    <p class="hsec-foot rv"><a href="buildings.html">All {total}&nbsp;buildings <span aria-hidden="true">&rarr;</span></a></p>
  </section>

  <section class="hsec wrap wrap-n" aria-labelledby="now-h">
    <header class="hsec-head">
      <p class="hsec-eyebrow rv"><span>Available&nbsp;now</span><span>Read {snapshot} from the live leasing&nbsp;feed</span></p>
      <h2 class="hsec-h rv" id="now-h">Homes available&nbsp;now.</h2>
      <p class="hsec-sub rv">The {nlive} buildings with the most homes listed today. The live leasing system is the authority on availability and&nbsp;price.</p>
    </header>
    <ul class="ngrid">
{now_cards}
    </ul>
    <p class="hsec-foot rv"><a href="search.html">See everything&nbsp;available <span aria-hidden="true">&rarr;</span></a></p>
  </section>

  <section class="hsec hsec-co wrap wrap-n" aria-labelledby="co-h">
    <p class="hsec-eyebrow rv"><span>The&nbsp;company</span></p>
    <h2 class="hsec-h rv" id="co-h">Owner. Builder.&nbsp;Manager.</h2>
    <p class="hsec-p rv">One Los Angeles company holds all {total} buildings, builds the new ones, and runs the day-to-day of every one. Wiseman develops as well as owns &mdash; most recently along the Motor Avenue corridor in Palms, minutes from Culver City. Every building page carries that building&rsquo;s own leasing number, and the repair path starts there &mdash; no login&nbsp;needed.</p>
    <p class="hsec-foot rv"><a href="company.html">About the&nbsp;company <span aria-hidden="true">&rarr;</span></a></p>
  </section>

</main>
""".format(hero_src=esc(plates.hero_url()), hero_w=hero["w"], hero_h=hero["h"],
           hero_pos=hero["pos"], hero_name=esc(hb["short"]),
           hero_street=esc(street_line(hb)),
           hero_alt=esc("%s, %s, at dusk" % (hb["short"], street_line(hb))),
           total=TOTAL, wla=area_counts["west-la"], snapshot=SNAPSHOT,
           area_cards=area_cards, now_cards=now_cards, nlive=len(live))

    page += TAIL.format(footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"], ver=VER,
                        extra="", boot="")
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)

    # ============================================================ buildings.html
    blocks = "\n".join(register_block(k, groups[k], areas, plates) for k in AREA_ORDER)
    first = props[0]
    runs = "\n\n".join(run_html(k, groups[k], areas, plates, i)
                        for i, k in enumerate(AREA_ORDER, start=1))
    fw, fh = plates.dims(first["no"])

    atlas_key = "".join(
        '<span>%s&nbsp;<span class="tnum">%d</span></span>' % (esc(HEAD_LABEL[k] if k != "west-la" else "West Los" + NBSP + "Angeles"), area_counts[k])
        for k in AREA_ORDER)

    page = HEAD.format(
        title="Every building &mdash; all 72 Wiseman buildings in Los Angeles",
        ogtitle="Every building &mdash; all 72 Wiseman buildings in Los Angeles",
        desc=("All 72 Wiseman Residential apartment buildings, grouped by neighborhood. "
              "Sort by street, bedrooms or rent, or read the same list against a map "
              "or as a set of photographs."),
        img=esc(first["image"]), ver=VER, skip=F["skip"],
        extra='\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % VER,
        header=nav_current(F["header"], "buildings.html"))

    page += """

<main id="main">

  <section class="pagehead wrap wrap-n">
    <p class="pagehead-no">
      <span>Every building</span>
      <span class="tnum">72 buildings</span>
      <span>Compiled {snapshot} from the live leasing&nbsp;feed</span>
    </p>
    <h1 class="pagehead-h">Every building Wiseman&nbsp;owns</h1>
    <p class="pagehead-sub">Seventy-two buildings in seven areas, listed in full. Nothing is hidden behind a&nbsp;filter.</p>
    <form class="search" action="search.html" method="get" role="search">
      <label class="vh" for="reg-q">Search the index by building, street or area</label>
      <div class="search-row">
        <input class="search-field" id="reg-q" name="q" type="search" autocomplete="off"
               placeholder="Building, street or area" data-typeahead
               role="combobox" aria-expanded="false" aria-controls="reg-ta" aria-autocomplete="list">
        <button class="search-btn" type="submit">Search</button>
      </div>
      <ul class="ta" id="reg-ta" role="listbox" aria-label="Matching buildings" data-typeahead-out hidden></ul>
    </form>
  </section>

  <!-- View and Sort share one row from 1100px (client note, round 7); the sort
       group belongs to the Index and Map views and steps out under Photographs -->
  <div class="toolbar wrap wrap-n">
    <div class="sortbar tb-views">
      <span class="sortbar-label" id="views-label">View</span>
      <div class="views" role="tablist" aria-labelledby="views-label">
        <a class="view-btn" id="vb-register" role="tab" href="?view=register" data-viewbtn="register" aria-selected="true" aria-controls="pane-register">Index</a>
        <a class="view-btn" id="vb-atlas" role="tab" href="?view=atlas" data-viewbtn="atlas" aria-selected="false" aria-controls="pane-register">Map</a>
        <a class="view-btn" id="vb-plates" role="tab" href="?view=plates" data-viewbtn="plates" aria-selected="false" aria-controls="pane-plates">Photographs</a>
      </div>
    </div>
    <div class="sortbar tb-sorts" role="group" aria-labelledby="sort-label" data-showin="register atlas">
      <span class="sortbar-label" id="sort-label">Sort</span>
      <button class="sort-btn" type="button" data-sort="area" aria-pressed="true">Neighborhood</button>
      <button class="sort-btn" type="button" data-sort="no" aria-pressed="false">Recommended</button>
      <button class="sort-btn" type="button" data-sort="street" aria-pressed="false">Street A&ndash;Z</button>
      <button class="sort-btn" type="button" data-sort="beds" aria-pressed="false">Bedrooms</button>
      <button class="sort-btn" type="button" data-sort="rent" aria-pressed="false">Rent</button>
    </div>
  </div>

{strip}

  <section class="view-pane" id="pane-register" data-viewpane="register atlas" role="tabpanel" aria-labelledby="vb-register">
    <div class="reg wrap wrap-n">
      <aside class="rail-fig" data-railfig>
        <div class="plate" data-plate data-cur="{fno}" data-showin="register" aria-hidden="true">
          <div class="plate-frame">
            <img class="plate-img" src="{pimg}" alt="{fname}" width="{fw}" height="{fh}" loading="lazy" decoding="async">
          </div>
          <div class="plate-cap">
            <span class="plate-name" data-platename>{fname}</span>
            <span class="plate-street" data-platestreet>{fstreet} &middot; {farea}</span>
          </div>
          <p class="plate-foot"><span>Specimen plate</span><span class="tnum">Follows the row under your pointer, or the&nbsp;scroll</span></p>
        </div>
        <div class="regmap" data-showin="atlas" hidden>
          <div class="mapbox" id="register-map" data-map='{{"scope":"all","bubbles":true,"theme":"light"}}'></div>
          <p class="map-foot"><span>All <span class="tnum">72</span>&nbsp;buildings</span><span>Hover a row to light its&nbsp;pin</span></p>
        </div>
      </aside>

      <div class="reg-body" data-register data-mode="grouped" data-pool>
{blocks}

      <p class="reg-legend">
        <span>Seventy-two buildings in seven areas, set out west to&nbsp;east.</span>
        <span>Bedrooms and rent are the leasing feed&rsquo;s own figures, read on {snapshot}. Rent is the lowest figure a building lists; an em dash means the feed lists no price&nbsp;today.</span>
        <span>Motor Tides completes in 2026 and leases through the live&nbsp;system.</span>
      </p>
      </div>
    </div>
    <p class="map-key" data-showin="atlas" hidden><span><span class="tnum" data-mapcount>72</span>&nbsp;buildings</span>{atlaskey}</p>
  </section>

  <section class="view-pane" id="pane-plates" data-viewpane="plates" role="tabpanel" aria-labelledby="vb-plates" hidden>
    <div class="book wrap wrap-n" data-pool>
      <h2 class="vh">The photographs</h2>
      <p class="reg-note">
        <span>One photograph per building, grouped by neighborhood, west to&nbsp;east.</span>
        <span>Photographs are Wiseman&rsquo;s own, as published in the leasing&nbsp;feed.</span>
      </p>
{runs}

      <p class="reg-legend">
        <span>Seventy-two buildings in seven areas, set out west to east; each run opens on its one frame chosen for full&nbsp;width.</span>
        <span>Bedrooms and rent are the leasing feed&rsquo;s own figures, read on {snapshot}. Rent is the lowest figure a building&nbsp;lists.</span>
        <span>Motor Tides completes in 2026 and leases through the live&nbsp;system.</span>
      </p>
    </div>
  </section>

  <p class="avail-line wrap wrap-n">
    For what is available this week, see <a href="search.html">Availability</a>.
    <span class="avail-sub">The live leasing system is the authority on availability and&nbsp;price.</span>
  </p>

</main>
""".format(snapshot=SNAPSHOT, blocks=blocks, runs=runs, atlaskey=atlas_key, strip=strip,
           fno=first["no"], pimg=esc(plates.url(first["no"], "bleed")),
           fw=fw, fh=fh, fname=esc(first["short"]),
           fstreet=esc(first["street"]), farea=esc(first["area"]))

    page += TAIL.format(footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"], ver=VER,
                        extra='\n<script src="../core/rail.js?v=%s" defer></script>' % VER, boot="")
    open(os.path.join(HERE, "buildings.html"), "w", encoding="utf-8").write(page)

    # ========================================================= search.html
    # The ILS search page. Everything between the <!--SEARCH--> markers is written
    # by scripts/gen_search.py from core/search.{css,js} — the filter bar, the
    # More-filters modal, the chips, the 72 cards and the split list/map. This
    # generator writes only the shell around it: the page head, the <h1>, and the
    # standing note, which stays ABOVE the filter bar so it is read before results.
    mt = by_no[FLAG_NO]

    av = HEAD.format(
        title="Find a home &mdash; search 72 Wiseman buildings in Los Angeles",
        ogtitle="Find a home &mdash; Wiseman Residential",
        desc=("Search 72 Wiseman apartment buildings in Los Angeles. Filter by "
              "neighborhood, bedrooms, baths, rent, size and amenities, then open the "
              "live leasing listing. Figures are a snapshot of the leasing feed on %s."
              % SNAPSHOT),
        img=esc(mt["image"]), ver=VER, skip=F["skip"],
        extra=('\n<link rel="stylesheet" href="../core/search.css?v=%s">'
               '\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % (VER, VER)),
        header=nav_current(F["header"], "search.html"))

    av += """

<main id="main">

  <section class="shead wrap wrap-n">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Find a home</span></nav>
    <h1 class="shead-h">Find a home in Los&nbsp;Angeles</h1>
    <p class="shead-sub">Studios to five-bedroom homes in 72 buildings across seven parts of the city &middot; {npriced} list a rent&nbsp;today.</p>
  </section>

  <h2 class="vh">Filters and results</h2>
<!--SEARCH-->
<!--/SEARCH-->

  <p class="avail-line wrap wrap-n">
    Apply, pay and renew in the <a href="{applicant}" rel="noopener">live leasing&nbsp;system</a>.
    <span class="avail-sub">Or call the leasing office on {tel}. Saved buildings are kept in this browser only. Wiseman Residential is an equal housing opportunity&nbsp;provider.</span>
  </p>

</main>
""".format(npriced=len(priced), tel=LEASING_TEL, applicant=esc(APPLICANT))

    av += TAIL.format(
        footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"], ver=VER,
        extra=('\n<script src="../core/rail.js?v=%s" defer></script>'
               '\n<script src="../core/search.js?v=%s" defer></script>' % (VER, VER)),
        boot=AV_BOOT)
    open(os.path.join(HERE, "search.html"), "w", encoding="utf-8").write(av)

    # ---- report
    openers = sum(1 for k in AREA_ORDER if run_order(groups[k], plates)[1])
    print("wrote index.html          hero + 7 area plates + %d available now + company"
          % len(live))
    print("wrote buildings.html      %d rows, 7 groups; book: %d plates in 7 runs, %d openers"
          % (TOTAL, TOTAL, openers))
    print("wrote search.html   ILS shell + <!--SEARCH--> markers "
          "(%d priced, %d unpriced) — now run scripts/gen_search.py register"
          % (len(priced), TOTAL - len(priced)))
    print("areas      " + "  ".join("%s %d" % (k, area_counts[k]) for k in AREA_ORDER))
    print("area plate " + "  ".join("%s:%s" % (k, area_plate(groups[k], plates, avoid)["no"]) for k in AREA_ORDER))
    print("available  " + "  ".join("%s:%d" % (p["no"], int(p["availableNow"])) for p in live))
    print("bedrooms   " + "  ".join("%d:%d" % (n, bed_counts[n]) for n in range(6)))
    print("amenities  " + "  ".join("%s:%d" % (k, amen_counts[k]) for k, _l, _t in AMENITIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
