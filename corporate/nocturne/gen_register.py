#!/usr/bin/env python3
"""Generate NOCTURNE — nocturne/index.html, buildings.html, neighborhoods.html,
search.html (the ILS shell). Run:

    python3 nocturne/gen_register.py

Every plate, row and reel frame is real, static, crawlable HTML that agrees with
its siblings on every number, name, street and photograph. Photography for the
reel and the plates comes from data/plates.json (one measured, high-resolution
curated frame per building) and the twelve features from data/artdirection.json
('selected'); the reel frames are asked of the CDN at the width they are painted
and never upscaled past native (SPEC risk 4). FACT-CHECK §2: no Motor Tides rent
figure is published anywhere, in any view.
"""
import json, os, re, sys, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")
PLATES = os.path.join(ROOT, "data", "plates.json")
ARTDIR = os.path.join(ROOT, "data", "artdirection.json")
SHELL = os.path.join(HERE, "templates", "_shell.html")

VER = "19"
SNAPSHOT = "11 September 2026"
TOTAL = 72
FLAG_NO = "071"          # Motor Tides — FACT-CHECK §2
LEASING_TEL = "+1 310-473-3000"

AREA_ORDER = ["west-la", "beverly-grove", "brentwood", "hollywood", "venice", "palms", "glendale"]
AREA_LABEL = {
    "west-la": "West Los Angeles", "beverly-grove": "Beverly Grove",
    "brentwood": "Brentwood", "hollywood": "Hollywood", "venice": "Venice",
    "palms": "Palms · Motor Avenue", "glendale": "Glendale",
}

WORD = {0: "studio", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def esc(s):
    return _html.escape("" if s is None else str(s), quote=True)


def money(n):
    return None if n is None else "$" + format(int(round(n)), ",d")


def street_line(p):
    return p["address"].split(",")[0].strip()


def beds_short(p):
    lo, hi = p.get("bedsMin"), p.get("bedsMax")
    if lo is None and hi is None:
        return ""
    lo = int(lo or 0); hi = int(hi if hi is not None else lo)
    if lo == hi:
        return "Studio" if lo == 0 else str(lo)
    return ("Studio" if lo == 0 else str(lo)) + "–" + str(hi)


def bed_meta(p):
    """A short bedroom clause for a reel caption."""
    lo, hi = p.get("bedsMin"), p.get("bedsMax")
    if lo is None and hi is None:
        return ""
    lo = int(lo or 0); hi = int(hi if hi is not None else lo)
    if lo == hi:
        return "studios" if lo == 0 else "%s bedroom%s" % (WORD.get(lo, lo), "" if lo == 1 else "s")
    if lo == 0:
        return "studios to %s bedrooms" % WORD.get(hi, hi)
    return "%s–%s bedrooms" % (lo, hi)


def price_shown(p):
    if p["no"] == FLAG_NO:
        return "Now leasing"
    if p.get("priceMin") is None:
        return "Call for details"
    if p.get("priceMax") and p["priceMax"] > p["priceMin"]:
        return money(p["priceMin"]) + "–" + money(p["priceMax"])
    return "From " + money(p["priceMin"])


# ---------------------------------------------------------------- photography
class Plates(object):
    def __init__(self, path):
        d = json.load(open(path, encoding="utf-8"))
        self.cdn = d["cdn"]; self.hero = d["hero"]; self.p = d["plates"]

    def dims(self, no):
        v = self.p[no]; return v["w"], v["h"]

    def cover(self, no, w, h, base="../"):
        """A cropped frame at (w x h), asked of the CDN at a width never above the
        master (so it is served at the size it is painted, never upscaled)."""
        v = self.p[no]
        if v["local"]:
            return base + v["src"]
        rw = min(w, v["w"])
        rh = int(round(rw * h / w))
        return "%sq_auto,f_auto,w_%d,h_%d,c_fill,g_auto/%s" % (self.cdn, rw, rh, v["src"])

    def wide(self, no, w, base="../"):
        v = self.p[no]
        if v["local"]:
            return base + v["src"]
        rw = min(w, v["w"])
        return "%sq_auto,f_auto,w_%d/%s" % (self.cdn, rw, v["src"])


# ---------------------------------------------------------------- furniture
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
        "footer": one(r'<footer class="ft".*?</footer>', "footer"),
        "mnav": one(r'<nav class="mnav".*?</nav>', "mobile menu"),
        "curtain": one(r'<div class="pt" aria-hidden="true">.*?\n</div>', "curtain"),
    }


def header_for(header, href, over):
    """Mark the nav item for the page, and set the transparent-over-hero / solid class."""
    header = header.replace('class="hd wrap wrap-n"',
                            'class="hd %s wrap wrap-n"' % ("over" if over else "solid"))
    if href:
        pat = '<a href="%s"' % href
        if pat in header:
            header = header.replace(pat, pat + ' aria-current="page"', 1)
    return header


# ---------------------------------------------------------------- head / tail
FONTS = ('<link rel="preconnect" href="https://resource.rentcafe.com">'
         '\n<link rel="preconnect" href="https://fonts.googleapis.com">'
         '\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..500;1,6..96,400&family=Manrope:wght@400;500&display=swap">')

FAVICON = ("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'"
           "%3E%3Crect%20width='100'%20height='100'%20fill='%230F0E0C'/%3E%3Cg%20fill='%23EFE8DB'%3E"
           "%3Cpolygon%20points='14,18%2034,18%2034,74%2014,80'/%3E%3Cpolygon%20points='40,18%2060,18%2060,71%2040,77'/"
           "%3E%3Cpolygon%20points='66,18%2086,18%2086,68%2066,74'/%3E%3C/g%3E%3C/svg%3E")


def head(title, desc, img, extra="", body_class=""):
    return """<!doctype html>
<html lang="en" data-base="" data-data="../data/wiseman.json" data-index="../data/index.json">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0F0E0C">
<link rel="icon" type="image/svg+xml" href="{fav}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wiseman Residential">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:image" content="{img}">
{fonts}
<link rel="stylesheet" href="../core/base.css?v={v}">
<link rel="stylesheet" href="../core/map.css?v={v}">{extra}
<link rel="stylesheet" href="style.css?v={v}">
<script>(function(d){{var r=d.documentElement;r.classList.add('js');if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{r.classList.add('js-pt');setTimeout(function(){{r.classList.remove('js-pt');}},1500);}}}})(document);</script>
</head>
<body{bodyc}>
""".format(title=title, desc=esc(desc), fav=FAVICON, img=esc(img), fonts=FONTS,
           v=VER, extra=extra, bodyc=(' class="%s"' % body_class) if body_class else "")


TAIL = """
{footer}

{mnav}

{curtain}

<script src="../core/core.js?v=%s" defer></script>
<script src="../core/map.js?v=%s" defer></script>
<script src="../core/rail.js?v=%s" defer></script>{extra}
<script src="app.js?v=%s" defer></script>{boot}
</body>
</html>
""" % (VER, VER, VER, VER)


AV_BOOT = """
<script>
/* search.html boots the shared ILS module after the deferred scripts have run.
   Nocturne runs the map theme:'dark' (Esri imagery). */
document.addEventListener('DOMContentLoaded', function () {
  WR.rails();
  var bar = document.querySelector('.sbar [data-rail-track]');
  if (bar && bar.tagName === 'FORM') bar.setAttribute('role', 'search');
  [].forEach.call(document.querySelectorAll('[data-card]'), function (c) {
    if (c.dataset.bedsmin === '') c.dataset.bedsmin = 'na';
    if (c.dataset.bedsmax === '') c.dataset.bedsmax = 'na';
  });
  [].forEach.call(document.querySelectorAll('[data-fmenu] h4'), function (h) { h.setAttribute('role', 'presentation'); });
  WR.searchPage({});
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
      el: '#search-map', pins: 'price', theme: 'dark',
      points: d.properties.map(function (p) {
        return { no: p.no, lat: p.lat, lng: p.lng, name: p.short, street: p.street,
                 area: p.areaKey, areaLabel: p.area, beds: p.beds,
                 img: p.thumb, url: 'buildings/' + p.path + '.html', pinLabel: p.no === '071' ? 'New' : '' };
      }),
      areas: Object.fromEntries(Object.entries(d.areas).map(function (e) { return [e[0], { name: e[1].name, count: e[1].count }]; }))
    });
    if (WR.searchApply) WR.searchApply(false);
  });
});
</script>"""


# ================================================================ pieces
def reel_frame(no, by_no, plates, base=""):
    p = by_no[no]
    area = p["areaKey"]
    w, h = plates.dims(no)
    src = plates.cover(no, 640, 800, base=base + "../")
    meta = "%s · %s" % (esc(street_line(p)), bed_meta(p))
    if no == FLAG_NO:
        meta += " · completing 2026"
    cap = "%s · %s" % (AREA_LABEL[area].split(" · ")[0], p["short"])
    return """        <li class="frame" data-area="{area}">
          <a href="{base}buildings/{path}.html">
            <figure>
              <img src="{src}" alt="{alt}" width="640" height="800" loading="lazy" decoding="async">
              <figcaption>{cap}</figcaption>
            </figure>
            <span class="fcap">
              <span class="area">{arealabel}</span>
              <span class="name">{name}</span>
              <span class="meta">{meta}</span>
            </span>
          </a>
        </li>""".format(area=area, base=base, path=p["path"], src=esc(src),
                        alt=esc("%s, %s" % (p["short"], street_line(p))), cap=esc(cap),
                        arealabel=esc(AREA_LABEL[area]), name=esc(p["short"]), meta=meta)


def area_hero_img(key, artdir, by_no, plates):
    """The area's hero building frame (artdirection areaHero), 4:5."""
    no = (artdir.get("areaHero", {}).get(key) or {}).get("no")
    if not no or no not in plates.p:
        # fall back to the first building in the area
        for k, p in by_no.items():
            if p["areaKey"] == key:
                no = p["no"]; break
    return plates.cover(no, 720, 900), no


def reg_row(p, plates):
    beds = beds_short(p) or "—"
    if p["no"] == FLAG_NO:
        fig = '<span class="reg-flag">Now leasing</span>'
    elif p.get("priceMin") is None:
        fig = '<span class="reg-rent tnum none">—</span>'
    else:
        fig = '<span class="reg-rent tnum">%s</span>' % money(p["priceMin"])
    rent = "" if (p.get("priceMin") is None or p["no"] == FLAG_NO) else str(int(p["priceMin"]))
    thumb = (p.get("thumb") or "").replace("w_600,h_400", "w_160,h_160")
    plate = plates.wide(p["no"], 900)
    return """            <div class="reg-row" data-row data-no="{no}" data-name="{name}" data-street="{street}"
                 data-area="{area}" data-arealabel="{arealabel}" data-bedsmax="{bmax}" data-rent="{rent}" data-img="{img}">
              <a href="buildings/{path}.html">
                <img class="reg-thumb" src="{thumb}" alt="" width="56" height="56" loading="lazy" decoding="async">
                <span><span class="reg-name">{name}</span><span class="reg-street">{street}</span></span>
                <span class="reg-beds tnum">{beds}</span>
                {fig}
              </a>
            </div>""".format(
        no=p["no"], name=esc(p["short"]), street=esc(p["street"]), area=p["areaKey"],
        arealabel=esc(AREA_LABEL[p["areaKey"]]), bmax="" if p.get("bedsMax") is None else int(p["bedsMax"]),
        rent=rent, img=esc(plate), path=p["path"], thumb=esc(thumb), beds=beds, fig=fig)


def reg_block(key, rows, areas, plates):
    a = areas[key]
    body = "\n".join(reg_row(p, plates) for p in rows)
    return """        <section class="reg-block" id="{key}" data-group="{key}" aria-labelledby="h-{key}">
          <h2 id="h-{key}"><span data-grouplabel>{label}</span> <span class="tnum">{n}</span></h2>
          <p class="reg-sub">{sub}</p>
          <div class="reg-rows" data-rows>
{body}
          </div>
        </section>""".format(key=key, label=esc(AREA_LABEL[key]), n=len(rows),
                             sub=esc(a["sub"]), body=body)


# ================================================================ build
def main():
    data = json.load(open(DATA, encoding="utf-8"))
    props = data["properties"]
    areas = {k: dict(v, key=k) for k, v in data["areas"].items()}
    for a in areas.values():
        a["countWord"] = "building" if a.get("count") == 1 else "buildings"
    plates = Plates(PLATES)
    artdir = json.load(open(ARTDIR, encoding="utf-8"))
    F = lift_furniture()
    by_no = {p["no"]: p for p in props}
    groups = {k: [p for p in props if p["areaKey"] == k] for k in AREA_ORDER}

    # reel selection: artdirection 'selected', large-enough curated frames
    selected = [no for no in artdir.get("selected", []) if no in plates.p][:12]

    priced = [p for p in props if p.get("priceMin") is not None]
    streets_total = len({p["street"] for p in props if p["street"]})

    # ============================================================ index.html
    HERO = "wr13.jpg"     # Motor Tides flagship exterior, 1800x1348 — a genuinely
                          # unused dark-capable exterior (not the retired fivebed wr04,
                          # not Tideline wr14, not The Plates wr05)
    reel_frames = "\n".join(reel_frame(no, by_no, plates) for no in selected)

    # seven areas: an inset frame + a list; the frame swaps to the row's building on hover
    default_hero_img, default_hero_no = area_hero_img(AREA_ORDER[0], artdir, by_no, plates)
    arows = []
    for key in AREA_ORDER:
        a = areas[key]
        img, _no = area_hero_img(key, artdir, by_no, plates)
        arows.append(
            '        <li><a class="arow" href="neighborhoods/{key}.html" data-areaimg="{img}">'
            '<span class="an">{name}</span><span class="ac tnum">{n}</span>'
            '<span class="as">{sub}</span>'
            '<svg class="aa" viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></a></li>'.format(
                key=key, img=esc(img), name=esc(AREA_LABEL[key]), n=len(groups[key]), sub=esc(a["sub"])))
    arows = "\n".join(arows)

    # available tonight: the six buildings with the most homes listed today
    live = sorted([p for p in props if (p.get("availableNow") or 0) > 0],
                  key=lambda p: (-int(p["availableNow"]), p["no"]))[:6]
    trows = []
    for p in live:
        n = int(p["availableNow"])
        price = ('<span class="flag">Now leasing</span>' if p["no"] == FLAG_NO
                 else (money(p.get("priceMin")) or "—"))
        trows.append(
            '        <li><a class="trow" href="buildings/{path}.html">'
            '<span class="tprice tnum">{price}</span>'
            '<span class="tbody"><span class="tn">{name}</span><span class="tmeta">{street} · {area}</span></span>'
            '<span class="tav tnum">{n} available now</span>'
            '<svg class="aa" viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></a></li>'.format(
                path=p["path"], price=price, name=esc(p["short"]), street=esc(street_line(p)),
                area=esc(AREA_LABEL[p["areaKey"]].split(" · ")[0]), n=n))
    trows = "\n".join(trows)

    obm_img = plates.cover("071", 720, 900) if "071" in plates.p else default_hero_img

    page = head(
        "Wiseman Residential &mdash; Los Angeles living, managed wisely",
        ("Wiseman Residential owns, develops and manages 72 apartment buildings across seven parts "
         "of Los Angeles and Glendale. Studios to five-bedroom homes; the portfolio as a reel of "
         "photographs through the dark."),
        "../assets/img/" + HERO,
        extra='\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % VER)
    page += F["skip"] + "\n\n" + header_for(F["header"], None, over=True) + "\n"

    page += """
<main id="main">

  <section class="hero" id="home" aria-labelledby="hero-h" data-hd="dark">
    <figure class="hero-fig">
      <img src="../assets/img/{hero}" width="1800" height="1348" alt="A Wiseman apartment building on Motor Avenue at dusk, glass balconies lit against a deep sky" fetchpriority="high" decoding="async">
    </figure>
    <p class="hero-cred a"><b>Motor Avenue, at dusk</b><br>One of seventy-two buildings</p>
    <div class="hero-in">
      <div class="hero-wrap">
        <div class="hero-copy">
          <p class="tag a a1">Los Angeles living, managed wisely.</p>
          <h1 class="t-hero a a2" id="hero-h">Come home to the city at dusk.</h1>
          <p class="hero-sub a a3">Studios to five-bedroom homes in {total} buildings across seven parts of Los Angeles, each with its own office and its own leasing&nbsp;line.</p>
        </div>
        <form class="srch a a4" action="search.html" method="get" role="search" aria-label="Find a home">
          <label class="cell"><span class="l">Where</span><span class="v"><input type="search" name="q" placeholder="Building, street or neighbourhood" autocomplete="off" data-typeahead role="combobox" aria-expanded="false" aria-controls="hero-ta" aria-autocomplete="list"></span></label>
          <label class="cell"><span class="l">Bedrooms</span><span class="v"><select name="beds" aria-label="Bedrooms"><option value="">Any</option><option value="0">Studio</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg></span></label>
          <label class="cell"><span class="l">Monthly rent</span><span class="v"><select name="pmax" aria-label="Maximum rent"><option value="">Any</option><option value="2500">Up to $2,500</option><option value="3500">Up to $3,500</option><option value="4500">Up to $4,500</option><option value="6000">Up to $6,000</option></select><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg></span></label>
          <a class="cell more" href="search.html"><span class="v">More filters</span></a>
          <button class="go" type="submit">Search <svg viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></button>
          <ul class="ta" id="hero-ta" role="listbox" aria-label="Matching buildings" data-typeahead-out hidden></ul>
        </form>
      </div>
    </div>
  </section>

  <div class="wrap wrap-n">
    <p class="facts rv">
      <span><b class="tnum">{total}</b>buildings<span class="sep">·</span><b class="tnum">7</b>areas<span class="sep">·</span><b class="tnum">{streets}</b>named streets<span class="sep">·</span>homes to five bedrooms</span>
      <span>Every figure read {snapshot} from the live leasing feed</span>
    </p>
  </div>

  <!-- THE REEL — the signature -->
  <section class="reel-sec" aria-labelledby="reel-h">
    <div class="wrap wrap-n reel-head">
      <div>
        <p class="kicker rv"><span class="tick"></span>The portfolio</p>
        <h2 class="t-2 rv rv-d1" id="reel-h">Seventy-two buildings, <em>one frame at a time.</em></h2>
        <p class="lede rv rv-d2">Twelve frames that carry the portfolio. The reel runs the length of the page on the buildings page, grouped by area, the frame at the gate lit and the rest waiting in the dark.</p>
      </div>
      <div class="rnav" aria-label="Reel controls">
        <button class="rbtn prev" type="button" aria-label="Previous frames"><svg viewBox="0 0 20 12" aria-hidden="true"><path d="M20 6H2M7 1 2 6l5 5"/></svg></button>
        <button class="rbtn next" type="button" aria-label="Next frames"><svg viewBox="0 0 20 12" aria-hidden="true"><path d="M0 6h18M13 1l5 5-5 5"/></svg></button>
      </div>
    </div>
    <div class="reel" data-reel>
      <span class="gate top" aria-hidden="true"></span><span class="gate btm" aria-hidden="true"></span>
      <div class="reel-stage">
        <ul class="reel-track" data-reel-track aria-label="Twelve buildings">
{reel}
        </ul>
      </div>
    </div>
    <div class="wrap wrap-n reel-foot">
      <span class="small tnum">Twelve of seventy-two</span>
      <span class="reel-bar"><span class="reel-fill"></span></span>
      <a class="lnk" href="buildings.html?view=reel">All 72 buildings <svg viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></a>
    </div>
  </section>

  <!-- SEVEN PARTS OF LOS ANGELES -->
  <section class="wrap wrap-n n-sec" aria-labelledby="areas-h">
    <div class="areas">
      <figure class="areas-fig rvi" data-areafig>
        <img src="{areaimg}" width="720" height="900" alt="A Wiseman building in West Los Angeles" loading="lazy" decoding="async">
        <figcaption>Seven parts of Los Angeles</figcaption>
      </figure>
      <div>
        <p class="kicker rv"><span class="tick"></span>Seven parts of Los Angeles</p>
        <h2 class="t-2 rv rv-d1" style="margin-top:18px;max-width:12ch">Where the buildings stand.</h2>
        <ul class="areas-list rv rv-d2">
{arows}
        </ul>
      </div>
    </div>
  </section>

  <!-- AVAILABLE TONIGHT -->
  <section class="wrap wrap-n n-sec" aria-labelledby="tonight-h">
    <p class="kicker rv"><span class="tick"></span>Available tonight</p>
    <h2 class="t-2 rv rv-d1" id="tonight-h" style="max-width:16ch">The buildings with the most homes listed.</h2>
    <ul class="tonight-list rv rv-d2">
{trows}
    </ul>
    <p class="reel-foot"><a class="lnk" href="search.html">See everything available <svg viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></a></p>
  </section>

  <!-- OWNER · BUILDER · MANAGER -->
  <section class="wrap wrap-n n-sec" aria-labelledby="obm-h">
    <div class="obm">
      <figure class="obm-fig rvi">
        <img src="{obmimg}" width="720" height="900" alt="Motor Tides, the newest Wiseman building on Motor Avenue" loading="lazy" decoding="async">
      </figure>
      <div class="obm-body">
        <p class="kicker rv"><span class="tick"></span>Owner · builder · manager</p>
        <h2 class="t-2 rv rv-d1" id="obm-h">One company, all seventy-two.</h2>
        <p class="lede rv rv-d2">One Los Angeles company owns every building on this site, builds the new ones, and runs the day-to-day of each.</p>
        <p class="obm-p rv rv-d2">Wiseman develops as well as owns — most recently along the Motor Avenue corridor in Palms, minutes from Culver City. Every building page carries that building&rsquo;s own leasing number, and the repair path starts there, with no login.</p>
        <p class="reel-foot rv rv-d2"><a class="lnk" href="company.html">About the company <svg viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></a></p>
      </div>
    </div>
  </section>

</main>
""".format(hero=HERO, total=TOTAL, streets=streets_total, snapshot=SNAPSHOT,
           reel=reel_frames, areaimg=esc(default_hero_img), arows=arows,
           trows=trows, obmimg=esc(obm_img))
    page += TAIL.format(footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"], extra="", boot="")
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)

    # ============================================================ buildings.html
    all_frames = "\n".join(reel_frame(no, by_no, plates)
                           for key in AREA_ORDER for no in [p["no"] for p in groups[key]])
    chap_ticks = "".join('<span class="reel-chap" title="%s"></span>' % esc(AREA_LABEL[k]) for k in AREA_ORDER)
    blocks = "\n".join(reg_block(k, groups[k], areas, plates) for k in AREA_ORDER)
    first = props[0]
    fw, fh = plates.dims(first["no"])
    atlas_key = "".join('<span>%s <span class="tnum">%d</span></span>' % (esc(AREA_LABEL[k]), len(groups[k]))
                        for k in AREA_ORDER)

    page = head(
        "Every building &mdash; all 72 Wiseman buildings in Los Angeles",
        ("All 72 Wiseman Residential apartment buildings, grouped by neighbourhood. Run the portfolio "
         "as a reel, read it as an index beside a specimen plate, or place it on a dark map."),
        first["image"],
        extra='\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % VER)
    page += F["skip"] + "\n\n" + header_for(F["header"], "buildings.html", over=False) + "\n"

    page += """
<main id="main">

  <section class="pagehead wrap wrap-n">
    <p class="kicker rv"><span class="tick"></span>Every building · <span class="tnum">72 buildings</span> · compiled {snapshot}</p>
    <h1 class="t-hero rv rv-d1" style="font-size:clamp(2.4rem,5.2vw,4.6rem)">Every building Wiseman owns.</h1>
    <p class="pagehead-sub rv rv-d2">Seventy-two buildings in seven areas, in full. Nothing hidden behind a filter — run it as a reel, an index, or a map.</p>
  </section>

  <div class="toolbar wrap wrap-n">
    <div class="views" role="tablist" aria-label="View">
      <span class="tb-label" aria-hidden="true">View</span>
      <a class="view-btn" role="tab" href="?view=reel" data-viewbtn="reel" aria-selected="true">Reel</a>
      <a class="view-btn" role="tab" href="?view=index" data-viewbtn="index" aria-selected="false">Index</a>
      <a class="view-btn" role="tab" href="?view=atlas" data-viewbtn="atlas" aria-selected="false">Map</a>
    </div>
    <div class="sorts" role="group" aria-label="Sort the index">
      <span class="tb-label" aria-hidden="true">Sort</span>
      <button class="sort-btn" type="button" data-sort="area" aria-pressed="true">Neighbourhood</button>
      <button class="sort-btn" type="button" data-sort="no" aria-pressed="false">Recommended</button>
      <button class="sort-btn" type="button" data-sort="street" aria-pressed="false">Street A&ndash;Z</button>
      <button class="sort-btn" type="button" data-sort="beds" aria-pressed="false">Bedrooms</button>
      <button class="sort-btn" type="button" data-sort="rent" aria-pressed="false">Rent</button>
    </div>
  </div>

  <!-- REEL VIEW -->
  <section class="view-pane bview-reel" data-viewpane="reel" role="tabpanel" aria-label="The reel">
    <section class="reel-sec" aria-label="All 72 buildings as a reel">
      <div class="wrap wrap-n reel-head">
        <div>
          <p class="kicker rv"><span class="tick"></span>The reel</p>
          <h2 class="t-2 rv rv-d1">All seventy-two, grouped by area.</h2>
        </div>
        <div class="rnav" aria-label="Reel controls">
          <button class="rbtn prev" type="button" aria-label="Previous frames"><svg viewBox="0 0 20 12" aria-hidden="true"><path d="M20 6H2M7 1 2 6l5 5"/></svg></button>
          <button class="rbtn next" type="button" aria-label="Next frames"><svg viewBox="0 0 20 12" aria-hidden="true"><path d="M0 6h18M13 1l5 5-5 5"/></svg></button>
        </div>
      </div>
      <div class="reel" data-reel data-reel-pin>
        <span class="gate top" aria-hidden="true"></span><span class="gate btm" aria-hidden="true"></span>
        <div class="reel-stage">
          <ul class="reel-track" data-reel-track aria-label="All 72 buildings">
{allframes}
          </ul>
        </div>
      </div>
      <div class="wrap wrap-n reel-foot">
        <span class="small tnum">All 72 buildings</span>
        <span class="reel-bar"><span class="reel-fill"></span></span>
        <span class="reel-chaps" aria-hidden="true">{chaps}</span>
      </div>
    </section>
  </section>

  <!-- INDEX VIEW -->
  <section class="view-pane" data-viewpane="index" role="tabpanel" aria-label="The index" hidden>
    <div class="regwrap wrap wrap-n">
      <div class="reg-groups" data-register data-mode="grouped">
{blocks}
        <p class="reg-legend">
          <span>Seventy-two buildings in seven areas, set out west to east.</span>
          <span>Rent is the lowest figure a building lists on {snapshot}; an em dash means no price today. Motor Tides leases through the live system.</span>
        </p>
      </div>
      <aside class="plate" data-plate data-cur="{fno}" aria-hidden="true">
        <div class="plate-frame"><img src="{pimg}" alt="{fname}" width="720" height="900" loading="lazy" decoding="async"></div>
        <div class="plate-cap">
          <span class="plate-name" data-platename>{fname}</span>
          <span class="plate-street" data-platestreet>{fstreet} · {farea}</span>
        </div>
        <p class="plate-foot"><span>Specimen plate</span><span>Follows the row under your pointer</span></p>
      </aside>
    </div>
  </section>

  <!-- ATLAS VIEW -->
  <section class="view-pane" data-viewpane="atlas" role="tabpanel" aria-label="The map" hidden>
    <div class="wrap wrap-n">
      <div class="atlas-map" id="buildings-atlas" data-map='{{"scope":"all","theme":"dark","label":"Map of all 72 Wiseman buildings in Los Angeles"}}'></div>
      <p class="atlas-key"><span><span class="tnum">72</span> buildings</span>{atlaskey}</p>
    </div>
  </section>

  <p class="avail-line wrap wrap-n">
    For what is available this week, see <a href="search.html">Find a home</a>.
    <span class="avail-sub">The live leasing system is the authority on availability and&nbsp;price.</span>
  </p>

</main>
""".format(snapshot=SNAPSHOT, allframes=all_frames, chaps=chap_ticks, blocks=blocks,
           fno=first["no"], pimg=esc(plates.wide(first["no"], 900)), fname=esc(first["short"]),
           fstreet=esc(first["street"]), farea=esc(AREA_LABEL[first["areaKey"]]), atlaskey=atlas_key)
    page += TAIL.format(footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"], extra="", boot="")
    open(os.path.join(HERE, "buildings.html"), "w", encoding="utf-8").write(page)

    # ============================================================ neighborhoods.html
    nblocks = []
    for key in AREA_ORDER:
        a = areas[key]
        img, _no = area_hero_img(key, artdir, by_no, plates)
        streets = " · ".join(sorted({p["street"] for p in groups[key] if p["street"]}))
        lo, hi = money(a.get("priceLow")), money(a.get("priceHigh"))
        rent = ("%s to %s" % (lo, hi)) if lo and hi else (lo or "Call for details")
        nblocks.append("""    <div class="nblock" id="{key}">
      <figure class="nblock-fig rvi"><img src="{img}" width="720" height="900" alt="A Wiseman building in {name}" loading="lazy" decoding="async"><figcaption>{name}</figcaption></figure>
      <div>
        <p class="kicker rv"><span class="tick"></span>{sub}</p>
        <h2 class="t-2 rv rv-d1">{name}</h2>
        <p class="nbody rv rv-d2">{lead}</p>
        <p class="nstreets rv rv-d2">{streets}</p>
        <div class="nspec rv rv-d2">
          <div><span class="l">Buildings</span><span class="v tnum">{n}</span></div>
          <div><span class="l">Rent, low to high</span><span class="v tnum">{rent}</span></div>
        </div>
        <p class="reel-foot rv rv-d2"><a class="lnk" href="neighborhoods/{key}.html">The {n} {word} in {name} <svg viewBox="0 0 16 12" aria-hidden="true"><path d="M0 6h14M9 1l5 5-5 5"/></svg></a></p>
      </div>
    </div>""".format(key=key, img=esc(img), name=esc(AREA_LABEL[key]), sub=esc(a["sub"]),
                     lead=esc(a["lead"]), streets=esc(streets), n=len(groups[key]),
                     rent=esc(rent), word=a["countWord"]))
    nblocks = "\n".join(nblocks)

    page = head(
        "Neighbourhoods &mdash; the seven parts of Los Angeles where Wiseman owns",
        ("The 72 Wiseman Residential buildings stand in seven parts of Los Angeles and Glendale. "
         "Counts, rents, streets and a dark map of the whole portfolio."),
        "../assets/img/wr14.jpg")
    page += F["skip"] + "\n\n" + header_for(F["header"], "neighborhoods.html", over=False) + "\n"
    page += """
<main id="main" class="wrap wrap-n">

  <section class="pagehead">
    <p class="kicker rv"><span class="tick"></span>Neighbourhoods · <span class="tnum">7 areas</span> · <span class="tnum">72 buildings</span></p>
    <h1 class="t-hero rv rv-d1" style="font-size:clamp(2.4rem,5.2vw,4.6rem)">Seven parts of Los Angeles.</h1>
    <p class="pagehead-sub rv rv-d2">Wiseman owns and manages in seven parts of the city, set out below largest first, over a map of the whole portfolio.</p>
  </section>

  <section class="bmap-sec" aria-labelledby="map-h">
    <p class="kicker rv"><span class="tick"></span>The map</p>
    <h2 class="t-3 rv rv-d1" id="map-h">Where they all stand.</h2>
    <div class="nbh-map" id="portfolio-map" data-map='{{"scope":"all","theme":"dark","label":"Map of all 72 Wiseman buildings in Los Angeles"}}'></div>
    <p class="nbh-map-foot"><span><span class="tnum">72</span> buildings · one dot per building</span><span>The list below is complete with the map switched off.</span></p>
  </section>

{nblocks}

  <p class="avail-line">
    For what is available this week, see <a href="search.html">Find a home</a>.
    <span class="avail-sub">The live leasing system is the authority on availability and&nbsp;price.</span>
  </p>

</main>
""".format(nblocks=nblocks)
    page += TAIL.format(footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"], extra="", boot="")
    open(os.path.join(HERE, "neighborhoods.html"), "w", encoding="utf-8").write(page)

    # ============================================================ search.html
    av = head(
        "Find a home &mdash; search 72 Wiseman buildings in Los Angeles",
        ("Search 72 Wiseman apartment buildings in Los Angeles. Filter by neighbourhood, bedrooms, "
         "baths, rent, size and amenities, then open the live leasing listing. A snapshot of the feed "
         "on %s." % SNAPSHOT),
        by_no[FLAG_NO]["image"],
        extra=('\n<link rel="stylesheet" href="../core/search.css?v=%s">'
               '\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % (VER, VER)),
        body_class="search-page")
    av += F["skip"] + "\n\n" + header_for(F["header"], "search.html", over=False) + "\n"
    av += """
<main id="main">

  <section class="shead wrap wrap-n">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Find a home</span></nav>
    <h1 class="shead-h">Find a home in Los Angeles.</h1>
    <p class="shead-sub">Studios to five-bedroom homes in 72 buildings across seven parts of the city · {npriced} list a rent&nbsp;today.</p>
  </section>

  <h2 class="vh">Filters and results</h2>
<!--SEARCH-->
<!--/SEARCH-->

  <p class="avail-line wrap wrap-n">
    Apply, pay and renew in the <a href="https://wisemanresidential.securecafe.com/onlineleasing/apartmentsforrent/guestlogin.aspx" rel="noopener">live leasing&nbsp;system</a>.
    <span class="avail-sub">Or call the leasing office on {tel}. Saved buildings are kept in this browser only. Wiseman Residential is an equal housing opportunity&nbsp;provider.</span>
  </p>

</main>
""".format(npriced=len(priced), tel=LEASING_TEL)
    av += TAIL.format(footer=F["footer"], mnav=F["mnav"], curtain=F["curtain"],
                      extra=('\n<script src="../core/search.js?v=%s" defer></script>' % VER),
                      boot=AV_BOOT)
    open(os.path.join(HERE, "search.html"), "w", encoding="utf-8").write(av)

    print("nocturne  index + buildings + neighborhoods + search")
    print("reel      %d selected  /  full reel %d frames" % (len(selected), len(props)))
    print("areas     " + "  ".join("%s %d" % (k, len(groups[k])) for k in AREA_ORDER))
    print("available " + "  ".join("%s:%d" % (p["no"], int(p["availableNow"])) for p in live))
    print("priced    %d / %d" % (len(priced), len(props)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
