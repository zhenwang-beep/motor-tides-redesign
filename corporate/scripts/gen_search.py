#!/usr/bin/env python3
"""Generate the ILS search interface and splice it into each direction's availability page.

The markup is shared across all three directions because `core/search.css` and
`core/search.js` are shared; each direction supplies only its own page shell and skins
the components through its own palette tokens.

Each direction's `search.html` must contain the marker pair:

    <!--SEARCH-->  ... anything ...  <!--/SEARCH-->

Everything between them is replaced. Run:

    python3 scripts/gen_search.py                # every direction that has the markers
    python3 scripts/gen_search.py tideline
"""
import json, os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")

E = lambda s: html.escape(str(s if s is not None else ""), quote=True)

AMENITIES = [
    ("in-unit-laundry", "In-unit washer &amp; dryer"),
    ("parking", "Parking"),
    ("air-conditioning", "Air conditioning"),
    ("elevator", "Elevator"),
    ("patio-balcony", "Patio or balcony"),
    ("walk-in-closets", "Walk-in closets"),
    ("gated", "Gated / controlled access"),
    ("courtyard", "Courtyard"),
    ("rooftop", "Rooftop deck"),
    ("fitness", "Fitness centre"),
    ("bike-storage", "Bike storage"),
    ("fireplace", "Fireplace"),
    ("dishwasher", "Dishwasher"),
    ("pool", "Pool"),
    ("package-locker", "Package locker"),
    ("ev-charging", "EV charging"),
]
FEATURES = [
    ("four-plus-bedrooms", "Four bedrooms or more"),
    ("studio", "Has studios"),
    ("townhome", "Townhome layout"),
    ("on-site-manager", "On-site manager"),
    ("wheelchair", "Wheelchair access"),
]
PRICES = [1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000]
SQFT = [400, 600, 800, 1000, 1200, 1500, 2000]
BEDS = [("0", "Studio"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5+")]
BATHS = [("1", "1+"), ("2", "2+"), ("3", "3+"), ("4", "4+")]

CHEV = '<svg class="cav" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4"/></svg>'
HEART = ('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 17S3 12.6 3 7.9A3.9 3.9 0 0 1 10 5.6 '
         '3.9 3.9 0 0 1 17 7.9C17 12.6 10 17 10 17Z"/></svg>')


def money(n):
    return "$" + format(int(n), ",d")


def dropdown(key, label, body, wide=False, right=False):
    return f"""<div class="fpop" data-fpop>
  <button type="button" class="fbtn" data-fbtn="{key}" data-label="{label}" aria-expanded="false" aria-haspopup="true">
    <span data-fbtn-label>{label}</span>{CHEV}
  </button>
  <div class="fmenu{' right' if right else ''}" data-fmenu role="group" aria-label="{label} filter" hidden>
    {body}
    <div class="fmenu-foot">
      <button type="button" class="lnk-clear" data-clear="{key}">Clear</button>
      <span class="scount"><b data-count>0</b> buildings</span>
    </div>
  </div>
</div>"""


WORDS = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
         8: "Eight", 9: "Nine", 10: "Ten"}


def no_figure_count(props):
    """Buildings the rent filter must skip: no published rent, or a rent this site may
    not publish (NO_RENT). Computed, never typed — BUILD-SPEC copy rules."""
    return sum(1 for p in props if p.get("priceMin") is None or p["no"] in NO_RENT)


def build_bar(areas, nofig=0):
    NOFIG_WORD = WORDS.get(nofig, str(nofig))
    area_opts = "".join(
        f'<label class="opt"><input type="checkbox" name="area" value="{E(k)}">'
        f'<span>{E(a["name"])}</span><span class="cnt">{a["count"]}</span></label>'
        for k, a in sorted(areas.items(), key=lambda kv: -kv[1]["count"])
    )
    beds = "".join(
        f'<label class="seg"><input type="checkbox" name="beds" value="{v}">{t}</label>' for v, t in BEDS
    )
    baths = "".join(
        f'<label class="seg"><input type="checkbox" name="baths" value="{v}">{t}</label>' for v, t in BATHS
    )
    pmin = "".join(f'<option value="{p}">{money(p)}</option>' for p in PRICES)
    pmax = "".join(f'<option value="{p}">{money(p)}</option>' for p in PRICES)
    amen = "".join(
        f'<label class="opt"><input type="checkbox" name="amen" value="{k}">'
        f'<span>{t}</span><span class="cnt"></span></label>' for k, t in AMENITIES
    )
    feat = "".join(
        f'<label class="opt"><input type="checkbox" name="feature" value="{k}">'
        f'<span>{t}</span><span class="cnt"></span></label>' for k, t in FEATURES
    )
    sq = "".join(f'<option value="{s}">{s:,}+ sq ft</option>' for s in SQFT)

    return f"""<div class="sbar" data-rail data-rail-label="Filter controls">
 <form class="sbar-in rail-track free" data-rail-track role="search" aria-label="Search Wiseman buildings">
  <div class="sfield">
    <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="9" cy="9" r="6"/><path d="M13.5 13.5L18 18"/></svg>
    <label class="vh" for="q">Search by building, street or neighbourhood</label>
    <input id="q" name="q" type="search" placeholder="Building, street or neighbourhood" autocomplete="off">
  </div>
  {dropdown("area", "Neighbourhood", f'<h4 aria-level="2">Neighbourhood</h4><div class="opts">{area_opts}</div>')}
  {dropdown("beds", "Beds", f'<h4 aria-level="2">Bedrooms</h4><div class="segs">{beds}</div>')}
  {dropdown("baths", "Baths", f'<h4 aria-level="2">Bathrooms</h4><div class="segs">{baths}</div>')}
  {dropdown("price", "Price", f'''<h4 aria-level="2">Monthly rent</h4>
    <div class="rng">
      <div><label class="vh" for="pmin">Minimum rent</label>
        <select class="sel" id="pmin" name="pmin"><option value="">No min</option>{pmin}</select></div>
      <span>to</span>
      <div><label class="vh" for="pmax">Maximum rent</label>
        <select class="sel" id="pmax" name="pmax"><option value="">No max</option>{pmax}</select></div>
    </div>
    <p class="card-ad">{NOFIG_WORD} buildings publish no rent figure here and are excluded when a rent range is set.</p>''')}
  <button type="button" class="fbtn" data-fbtn="more" data-label="More filters" data-fmodal-open>
    <span data-fbtn-label>More filters</span>
  </button>
 </form>
 <div class="rail-float">
   <button class="rail-btn prev sm" data-rail-prev aria-label="Scroll filters left"></button>
   <button class="rail-btn next sm" data-rail-next aria-label="Scroll filters right"></button>
 </div>

 <dialog class="fmodal" data-fmodal aria-labelledby="fmodal-t">
  <div class="fmodal-h">
    <h2 id="fmodal-t">More filters</h2>
    <button type="button" class="fmodal-x" data-fmodal-close aria-label="Close filters">
      <svg viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13"/></svg>
    </button>
  </div>
  <div class="fmodal-b">
    <div class="fgrp">
      <h3>Minimum size</h3>
      <label class="vh" for="sqmin">Minimum square feet</label>
      <select class="sel" id="sqmin" name="sqmin" style="max-width:240px"><option value="">Any size</option>{sq}</select>
    </div>
    <div class="fgrp"><h3>Amenities</h3><div class="fgrid">{amen}</div></div>
    <div class="fgrp"><h3>Home features</h3><div class="fgrid">{feat}</div></div>
  </div>
  <div class="fmodal-f">
    <button type="button" class="lnk-clear" data-clearall>Clear all filters</button>
    <button type="button" class="btn-apply" data-fmodal-apply>Show <span data-count>0</span> buildings</button>
  </div>
 </dialog>
</div>"""


def build_results():
    return """<div class="sresults">
  <p class="scount"><b data-count>0</b> buildings</p>
  <div class="chips" data-chips></div>
  <p class="snote">Snapshot of the live leasing feed &middot; the building's own page has today's availability</p>
  <button type="button" class="lnk-clear" data-clearall hidden>Clear all</button>
  <div class="sright">
    <div class="vtog" role="group" aria-label="List or map">
      <button type="button" data-view="list" aria-pressed="true">List</button>
      <button type="button" data-view="map" aria-pressed="false">Map</button>
    </div>
    <label for="sort">Sort</label>
    <select class="sel" id="sort" name="sort">
      <option value="no">Recommended</option>
      <option value="priceup">Rent, low to high</option>
      <option value="pricedown">Rent, high to low</option>
      <option value="beds">Most bedrooms</option>
      <option value="sqft">Largest</option>
      <option value="name">Name A&ndash;Z</option>
      <option value="area">Neighbourhood</option>
    </select>
  </div>
</div>"""


def price_label(p):
    """FACT-CHECK: Motor Tides' rent range must not be published anywhere."""
    if p["no"] in NO_RENT:
        return "Now leasing"
    if p.get("priceMin") is None:
        return "Call for details"
    if p.get("priceMax") and p["priceMax"] > p["priceMin"]:
        return money(p["priceMin"]) + "–" + money(p["priceMax"])
    return "From " + money(p["priceMin"])


def card(p, tag_labels):
    tags = [tag_labels[t] for t in p["tags"][:3] if t in tag_labels]
    price = price_label(p)
    beds = (p.get("beds") or "—").replace(" Beds", " bed").replace(" Bed", " bed")
    baths = (p.get("baths") or "—").replace(" Baths", " bath").replace(" Bath", " bath")
    sqft = (p.get("sqft") or "").replace(" Sq. Ft.", "")
    fx = " &middot; ".join(x for x in [beds, baths, (sqft + " sq ft") if sqft and sqft != "—" else ""] if x)
    rent = ""
    if p.get("priceMin") is not None and p["no"] not in NO_RENT:
        rent = f' data-rent="{int(p["priceMin"])}"'
    sq = ""
    if p.get("sqftMax"):
        sq = f' data-sqft="{int(p["sqftMax"])}"'
    return f"""<article class="card" data-card data-row data-no="{E(p['no'])}" data-area="{E(p['areaKey'])}"
  data-arealabel="{E(p['area'])}" data-name="{E(p['short'])}" data-street="{E(p['street'])}"
  data-bedsmin="{p.get('bedsMin') if p.get('bedsMin') is not None else ''}"
  data-bedsmax="{p.get('bedsMax') if p.get('bedsMax') is not None else ''}"
  data-bathsmin="{p.get('bathsMin') if p.get('bathsMin') is not None else ''}"
  data-bathsmax="{p.get('bathsMax') if p.get('bathsMax') is not None else ''}"{rent}{sq}
  data-tags="{E('|'.join(p['tags']))}">
  <a class="card-img" href="buildings/{E(p['path'])}.html" tabindex="-1" aria-hidden="true">
    <img src="{E(p['thumb'])}" alt="" width="600" height="400" loading="lazy" decoding="async">
  </a>
  <button type="button" class="card-fav" data-fav="{E(p['no'])}" aria-pressed="false"
          aria-label="Save {E(p['short'])}">{HEART}</button>
  <div class="card-b">
    <p class="card-price tnum">{E(price)}</p>
    <p class="card-fx">{fx}</p>
    <h3 class="card-nm"><a href="buildings/{E(p['path'])}.html">{E(p['short'])}</a></h3>
    <p class="card-ad">{E(p['streetLine'] if 'streetLine' in p else p['address'].split(',')[0])} &middot; {E(p['area'])}{(' &middot; <b>' + str(p['availableNow']) + ' available now</b>') if p.get('availableNow') else ''}</p>
    {'<p class="card-tags">' + ''.join(f'<span>{t}</span>' for t in tags) + '</p>' if tags else ''}
  </div>
</article>"""


NO_RENT = {"071"}   # Motor Tides: FACT-CHECK forbids publishing its rent range


def build(direction, data):
    path = os.path.join(ROOT, direction, "search.html")
    if not os.path.exists(path):
        path = os.path.join(ROOT, direction, "search.html")   # pre-rename fallback
    if not os.path.exists(path):
        return 0
    src = open(path, encoding="utf-8").read()
    if "<!--SEARCH-->" not in src or "<!--/SEARCH-->" not in src:
        print("  %-10s no <!--SEARCH--> markers, skipped" % direction)
        return 0

    tag_labels = dict(AMENITIES + FEATURES)
    props = data["properties"]
    cards = "\n".join(card(p, tag_labels) for p in props)
    nofig = no_figure_count(props)
    nofig_word = WORDS.get(nofig, str(nofig))

    body = f"""<!--SEARCH-->
<div data-search>
{build_bar(data['areas'], nofig)}
{build_results()}
<div class="split" data-split>
  <div class="slist">
    <div class="cards" data-cards>
{cards}
    </div>
    <div class="sempty" data-empty hidden>
      <h3>No building matches those filters.</h3>
      <p>Try widening the rent range or adding a neighbourhood. {nofig_word} buildings publish no rent
         figure here, so they drop out whenever a rent range is set.</p>
      <p>Availability moves faster than this page. The leasing line has today's list.</p>
      <form onsubmit="return false">
        <label class="vh" for="notify">Email address</label>
        <input id="notify" type="email" placeholder="Email address" autocomplete="email">
        <button type="submit" class="btn-apply">Notify me</button>
      </form>
      <p class="card-ad">Demo form &mdash; it does not send anything.</p>
    </div>
  </div>
  <div class="smap" id="search-map" data-theme="light"></div>
</div>
</div>
<!--/SEARCH-->"""

    out = re.sub(r"<!--SEARCH-->.*?<!--/SEARCH-->", lambda m: body, src, flags=re.S)
    open(path, "w", encoding="utf-8").write(out)
    print("  %-10s %d cards, %d filters" % (direction, len(props), len(AMENITIES) + len(FEATURES) + 4))
    return 1


if __name__ == "__main__":
    data = json.load(open(DATA))
    targets = sys.argv[1:] or [d for d in sorted(os.listdir(ROOT))
                               if os.path.isdir(os.path.join(ROOT, d))
                               and (os.path.exists(os.path.join(ROOT, d, "search.html"))
                                    or os.path.exists(os.path.join(ROOT, d, "search.html")))]
    n = sum(build(t, data) for t in targets)
    print("%d availability pages rebuilt" % n)
