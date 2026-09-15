#!/usr/bin/env python3
"""Generate the repetitive pages of each Wiseman direction from data/wiseman.json.

Each direction folder may contain `templates/building.html` and `templates/neighborhood.html`.
Rendered output lands in `<direction>/buildings/<nnn>-<slug>.html` and
`<direction>/neighborhoods/<key>.html`, so every building and neighbourhood has a real,
linkable, crawlable URL with its own <title> and meta description.

Template syntax (deliberately tiny):
    {{ key }}                 escaped value
    {{{ key }}}               raw value
    {{# list }} ... {{/ list }}   loop; inside, `{{ .field }}` is the current item,
                                  `{{ @index }}` / `{{ @n }}` the 0/1-based position,
                                  `{{ @first }}` / `{{ @last }}` are truthy strings
    {{^ key }} ... {{/ key }} inverted section: renders when key is falsy/empty
    {{? key }} ... {{/ key }} section: renders when key is truthy (non-list)
Dotted lookups work: {{ p.name }}, {{ .gallery.0 }}.
"""
import json, os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")

TOKEN = re.compile(r"\{\{\s*([#^?/{]?)\s*([@\w.\-]+)\s*\}?\}\}")


def lookup(ctx, key):
    if key.startswith("@"):
        return ctx.get(key)
    cur = ctx
    if key.startswith("."):
        # inside a loop: `.field` resolves against the current item
        cur = ctx.get(".")
        key = key[1:]
        if not key:
            return cur
    for part in key.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, (list, tuple)):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
        if cur is None:
            return None
    return cur


def render(tpl, ctx):
    out, i = [], 0
    for m in TOKEN.finditer(tpl):
        if m.start() < i:
            continue
        sigil, key = m.group(1), m.group(2)
        if sigil in ("#", "^", "?"):
            close = find_close(tpl, m.end(), key)
            if close is None:
                raise ValueError("unclosed section {{%s %s}}" % (sigil, key))
            body = tpl[m.end():close[0]]
            out.append(tpl[i:m.start()])
            val = lookup(ctx, key)
            if sigil == "#":
                items = val or []
                if isinstance(items, dict):
                    items = [dict(v, key=k) if isinstance(v, dict) else {"key": k, "value": v}
                             for k, v in items.items()]
                n = len(items)
                for idx, item in enumerate(items):
                    sub = dict(ctx)
                    sub["."] = item
                    if isinstance(item, dict):
                        sub.update({("." + k): v for k, v in item.items()})
                    else:
                        sub["."] = item
                    sub["@index"] = idx
                    sub["@n"] = idx + 1
                    sub["@first"] = "first" if idx == 0 else ""
                    sub["@last"] = "last" if idx == n - 1 else ""
                    sub["@odd"] = "odd" if idx % 2 else "even"
                    out.append(render(body, sub))
            elif sigil == "?":
                if val:
                    out.append(render(body, ctx))
            else:  # ^
                if not val:
                    out.append(render(body, ctx))
            i = close[1]
            continue
        if sigil == "/":
            continue
        out.append(tpl[i:m.start()])
        raw = m.group(0).startswith("{{{")
        if key == ".":
            val = ctx.get(".")
        else:
            val = lookup(ctx, key)
        if val is None or val is False:
            val = ""
        s = str(val)
        out.append(s if raw else html.escape(s, quote=True))
        i = m.end()
    out.append(tpl[i:])
    return "".join(out)


def find_close(tpl, start, key):
    depth, pos = 1, start
    while True:
        m = TOKEN.search(tpl, pos)
        if not m:
            return None
        if m.group(2) == key:
            if m.group(1) in ("#", "^", "?"):
                depth += 1
            elif m.group(1) == "/":
                depth -= 1
                if depth == 0:
                    return (m.start(), m.end())
        pos = m.end()


# ---------------------------------------------------------------- view models

def money(n):
    return None if n is None else "$" + format(int(round(n)), ",d")


def price_label(p):
    if p.get("priceMin") is None:
        return "Call for details"
    if p.get("priceMax") and p["priceMax"] > p["priceMin"]:
        return money(p["priceMin"]) + "–" + money(p["priceMax"])
    return "From " + money(p["priceMin"])


def trim(s, suffix):
    s = (s or "").strip()
    return re.sub(suffix, "", s).strip() or "—"


# --------------------------------------------------- view-model additions
# The RentCafe feed carries URLs whose filename ends in a space before the
# extension ("... living room .jpg" -> "...%20.jpg"). Every one of them 404s.
# Filter before publishing, and top a short list back up with the community
# image so a gallery never collapses to a single frame.
DEAD_IMG = re.compile(r"%20\.(jpe?g|png)$", re.I)
# One more the rule above cannot see: this source path 404s at every transform.
# Verified against the CDN on 10 September 2026; re-sweep after a feed refresh.
DEAD_PATHS = frozenset(["s3/2/9707/rsz_1338_formosa_ave_exteriors-1.jpg"])
_SRC = re.compile(r"/image/upload/[^/]+/(.+)$")


def dead_image(u):
    if not u or DEAD_IMG.search(u):
        return True
    m = _SRC.search(u)
    return bool(m) and m.group(1) in DEAD_PATHS


def _tx(u, transform):
    """Swap the Cloudinary-style transform segment of a RentCafe CDN URL, so a
    page asks for the width it will actually paint."""
    if not u:
        return ""
    return re.sub(r"(/image/upload/)[^/]+/", r"\g<1>" + transform + "/", u, count=1)


def _src_path(u):
    m = _SRC.search(u or "")
    return m.group(1) if m else (u or "")


def _live_gallery(urls, extra):
    out, seen = [], set()
    for u in (urls or []):
        if dead_image(u) or _src_path(u) in seen:
            continue
        seen.add(_src_path(u))
        out.append(u)
    # top a short list back up with the community image, unless that is the
    # same photograph at a different width
    if extra and not dead_image(extra) and _src_path(extra) not in seen and len(out) < 4:
        out.append(extra)
    return out


def bed_parts(p):
    """Neutral pieces for a bedroom cell, so a template can set the DIGITS in a
    display face without putting the word "Studio" in it too."""
    lo, hi = p.get("bedsMin"), p.get("bedsMax")
    if lo is None and hi is None:
        return {"bedsNone": True, "bedsStudio": False, "bedsDash": False,
                "bedsNum": "", "bedsAny": False}
    lo = int(lo or 0)
    hi = int(hi if hi is not None else lo)
    studio = lo == 0
    if studio:
        num = str(hi) if hi > 0 else ""
    else:
        num = str(lo) if hi == lo else "%d\u2013%d" % (lo, hi)
    return {"bedsNone": False, "bedsStudio": studio, "bedsDash": studio and hi > 0,
            "bedsNum": num, "bedsAny": True}


# ---------------------------------------------------------------- the lede
# The feed's own `description` is RentCafe marketing copy: "nestled in the
# heart of", "your premier destination", "the pinnacle of modern living in the
# prestigious Palms area". BUILD-SPEC bans that vocabulary outright and says a
# building page states what the building is and where it stands rather than
# selling a lifestyle; several feed entries also file a building in a different
# neighbourhood from the one the portfolio puts it in ("Edinburgh Courtyard ...
# located in West Hollywood"). So the lede is generated from the numbers,
# never quoted. Additive: `description` is untouched for any direction still
# rendering it.
WORD = {0: "studio", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def homes_line(p):
    """A plain sentence about the homes, built only from the feed's numbers."""
    lo, hi = p.get("bedsMin"), p.get("bedsMax")
    if lo is None and hi is None:
        return "Floor plans and bedroom counts for this building are held in the live leasing system."
    lo = int(lo or 0)
    hi = int(hi if hi is not None else lo)
    if lo == hi:
        n = "Studio apartments" if lo == 0 else "%s-bedroom apartments" % WORD[lo].capitalize()
    elif lo == 0:
        n = "Apartments from studios to %s bedrooms" % WORD[hi]
    elif hi - lo == 1:
        n = "%s- and %s-bedroom apartments" % (WORD[lo].capitalize(), WORD[hi])
    else:
        n = "Apartments of %s to %s bedrooms" % (WORD[lo], WORD[hi])
    sq = (p.get("sqft") or "").strip()
    sq = re.sub(r"\s*Sq\.\s*Ft\.$", "", sq).strip()
    if sq and sq not in ("-", "\u2013", "\u2014"):
        return "%s, %s square feet." % (n, sq.replace(" to ", "\u2013"))
    return "%s." % n


def fact_lede(p, d):
    # "in Palms \u00b7 Motor Avenue." reads as two places inside a sentence;
    # the compound area labels keep their first half in running prose.
    where = d["areaName"].split(" \u00b7 ")[0]
    return "%s stands at %s in %s. %s" % (
        p["short"], d["streetLine"].rstrip("."), where, homes_line(p))


# FACT-CHECK §2 — no Motor Tides rent figure may be published anywhere on the
# site. 071 is the only flagged property; templates print the leasing flag in
# place of a figure. Keep this list here, not in a template: it is a compliance
# rule, and it must hold for every direction that renders a price.
NO_RENT = frozenset(["071"])


ICON_FOR = [
    ("i-laundry", ("washer", "dryer", "laundry")), ("i-parking", ("parking", "garage", "carport")),
    ("i-elevator", ("elevator",)), ("i-fitness", ("fitness", "weights")), ("i-rooftop", ("rooftop", "roof deck")),
    ("i-courtyard", ("courtyard",)), ("i-pool", ("pool",)), ("i-gated", ("gated", "controlled access", "alarm")),
    ("i-ac", ("air condition", "central ac", "central air", "heating", "thermostat")), ("i-dishwasher", ("dishwasher", "appliance", "range", "microwave", "refrigerator", "stove", "disposal")),
    ("i-patio", ("patio", "balcony", "view")), ("i-closet", ("closet", "storage", "cabinet")), ("i-fireplace", ("fireplace",)),
    ("i-floor", ("flooring", "hardwood", "carpet", "ceiling", "shades", "window", "cable", "wired")), ("i-ev", ("electric vehicle",)),
    ("i-package", ("package", "amazon", "locker")), ("i-bike", ("bike",)), ("i-manager", ("on-site management", "child care")),
    ("i-townhome", ("townhouse", "floor plan")), ("i-wheelchair", ("wheelchair",)), ("i-recycle", ("recycling",)),
]
def icon_for(label):
    l = label.lower()
    for icon, needles in ICON_FOR:
        if any(n in l for n in needles):
            return icon
    return "i-generic"

def clean_amenity(a):
    """Feed strings carry footnotes and typos ('In-Suite Alram System', '*Coming Soon')."""
    a = re.sub(r"\s*\*\s*(coming soon|in select units|terms apply)\s*$", "", a, flags=re.I).strip()
    a = a.replace("Alram", "Alarm").replace("VInyl", "Vinyl").replace("Gated Residents' Garage", "Gated Resident Garage")
    a = re.sub(r"\s+More info on .*$", "", a)
    return a

def plan_rows(p):
    rows = []
    for x in p.get("plans", []):
        r = dict(x)
        r["rentLabel"] = ("Now leasing" if p["no"] in NO_RENT else (("$%s/mo" % format(x["rent"], ",d")) if x.get("rent") else "Ask"))
        r["sqftLabel"] = ("%s sq ft" % format(x["sqft"], ",d")) if x.get("sqft") else ""
        r["availLabel"] = ("%d available" % x["available"]) if x.get("available") else ""
        r["depositLabel"] = ("$%s deposit" % format(x["deposit"], ",d")) if x.get("deposit") and p["no"] not in NO_RENT else ""
        # Four studio plans arrive with beds=null and only the name saying
        # "Studio, 1 Bath"; read the word from the name so the row never
        # prints "\u00b7 1 bath" with an empty bedroom cell.
        _beds = x.get("beds")
        if _beds is None and re.match(r"\s*studio\b", x.get("name") or "", re.I):
            _beds = 0
        r["bedsLabel"] = "Studio" if _beds == 0 else ("%d bed" % _beds if _beds else "")
        r["bathsLabel"] = ("%g bath" % x["baths"]) if x.get("baths") else ""
        rows.append(r)
    return rows

def decorate(p, areas):
    a = areas[p["areaKey"]]
    d = dict(p)
    d["areaName"] = a["name"]
    d["areaSub"] = a["sub"]
    d["areaCount"] = a["count"]
    d["priceLabel"] = price_label(p)
    d["bedsShort"] = trim(p.get("beds"), r"\s*Beds?$")
    d["bathsShort"] = trim(p.get("baths"), r"\s*Baths?$")
    d["sqftShort"] = trim(p.get("sqft"), r"\s*Sq\. Ft\.$")
    d["cityLine"] = re.sub(r"^[^,]+,\s*", "", p["address"])
    d["streetLine"] = p["address"].split(",")[0]
    d["gallery"] = _live_gallery(p.get("gallery"), p.get("image"))
    d["galleryThumb"] = _live_gallery(p.get("galleryThumb"), p.get("thumb"))
    d["hero"] = (d["gallery"] or [p.get("image")])[0]
    d["shots"] = d["gallery"][:4]
    # ---- image-forward additions (ELEVATE) ---------------------------------
    # A page that opens on a 100svh photograph must ask the CDN for the width
    # it actually paints. The community exterior is kept separately: it is the
    # building's identity shot, but it is also the smallest file in the feed,
    # so it is never the one blown up full-bleed.
    d["heroWide"] = _tx(d["hero"], "q_auto,f_auto,w_1800")
    d["exterior"] = p.get("image") or d["hero"]
    # the four frames that are NOT already the hero, topped up with the
    # exterior so a gallery never collapses to two plates
    rest = d["gallery"][1:]
    ext = p.get("image")
    if len(rest) < 4 and ext and not dead_image(ext) and \
            _src_path(ext) not in {_src_path(u) for u in d["gallery"]}:
        rest = rest + [ext]
    d["shots4"] = rest[:4] or d["shots"]
    # ELEVATE §1 — ask the CDN for the size you paint. A full-bleed room
    # strip paints one frame per screen width, so it asks for w_2000.
    d["shotsWide"] = [re.sub(r"(/image/upload/)[^/]+/", r"\g<1>q_auto,f_auto,w_2000/", u, count=1)
                      for u in d["shots"]]
    d["city"] = d["cityLine"].split(",")[0].strip()
    d["bedsMinN"] = "" if p.get("bedsMin") is None else int(p["bedsMin"])
    d["bedsMaxN"] = "" if p.get("bedsMax") is None else int(p["bedsMax"])
    d["rentN"] = "" if p.get("priceMin") is None else int(p["priceMin"])
    d.update(bed_parts(p))
    d["mapUrl"] = "https://maps.google.com/?q=%s,%s" % (p["lat"], p["lng"])
    d["telHref"] = "tel:" + re.sub(r"[^\d+]", "", p.get("phone") or "")
    d["hasAmen"] = bool(p.get("community") or p.get("apartment"))
    seen = set(); d["amenIcons"] = []
    for a in (p.get("community") or []) + (p.get("apartment") or []):
        lab = clean_amenity(a)
        if not lab or lab.lower() in seen: continue
        seen.add(lab.lower()); d["amenIcons"].append({"icon": icon_for(lab), "label": lab, "where": "building" if a in (p.get("community") or []) else "apartment"})
    d["buildingIcons"] = [x for x in d["amenIcons"] if x["where"] == "building"]
    d["apartmentIcons"] = [x for x in d["amenIcons"] if x["where"] == "apartment"]
    d["planRows"] = plan_rows(p)
    d["hasPlans"] = bool(d["planRows"])
    d["availLine"] = ("%d apartment%s available now" % (p["availableNow"], "" if p["availableNow"] == 1 else "s")) if p.get("availableNow") else "Nothing advertised today"
    d["officeHours"] = p.get("officeHours") or ""
    d["unitsLine"] = ("%d apartments" % p["units"]) if p.get("units") else ""
    # ---- additive display values (THE REGISTER direction) -------------------
    # Existing keys are untouched. These add en-dashed ranges, a bare rent
    # figure for a tabular column, a 160px row thumbnail, and the FACT-CHECK
    # price suppression above.
    d["bathsRange"] = d["bathsShort"].replace("-", "\u2013")
    d["sqftRange"] = d["sqftShort"].replace(" to ", "\u2013")
    d["thumb160"] = (p.get("thumb") or "").replace("w_600,h_400", "w_160,h_160")
    # ELEVATE §1 — never letterbox a building into a 16:9 card. A specimen
    # plate is a tall crop, asked of the CDN at the size it is painted.
    d["plateImg"] = re.sub(r"(/image/upload/)[^/]+/", r"\g<1>q_auto,f_auto,w_560,h_700,c_fill,g_auto/",
                           (d["galleryThumb"] or [p.get("thumb") or ""])[0] or "", count=1)
    d["nowLeasing"] = "Now leasing" if p["no"] in NO_RENT else ""
    d["rentShown"] = "" if p["no"] in NO_RENT else (money(p.get("priceMin")) or "")
    d["priceShown"] = "Now leasing" if p["no"] in NO_RENT else d["priceLabel"]
    # FACT-CHECK §2: a suppressed price must stay suppressed in the meta
    # description too, or the figure leaks into search results and link cards.
    # A building the feed has no beds/baths for (023) must not advertise
    # "—, —" in a search result either: drop the clause instead.
    _sizes = [v for v in (p.get("beds"), p.get("baths"))
              if v and v.strip() and v.strip() not in ("-", "\u2013", "\u2014")]
    _bits = ["%s, %s" % (p["short"], d["streetLine"].rstrip("."))]
    if _sizes:
        _bits.append(", ".join(_sizes))
    _bits.append(d["priceShown"])
    _bits.append("Managed by Wiseman Residential")
    d["metaDesc"] = ". ".join(_bits) + "."
    # A sortable rent for a data-* attribute that honours the same
    # suppression: blank reads as "no published figure" to WR.register and
    # WR.filters alike, so 071 behaves exactly like the five buildings that
    # quote on request instead of leaking its figure through sort order.
    d["rentSort"] = "" if p["no"] in NO_RENT else d["rentN"]
    d["factLede"] = fact_lede(p, d)
    return d


def _priced(members):
    return [m for m in members
            if m.get("priceMin") is not None and m["no"] not in NO_RENT]


def _area_low(members):
    vals = [m["priceMin"] for m in _priced(members)]
    return min(vals) if vals else None


def _area_high(members):
    vals = [(m.get("priceMax") or m["priceMin"]) for m in _priced(members)]
    return max(vals) if vals else None


def build(direction, data, quiet=False):
    dirpath = os.path.join(ROOT, direction)
    tdir = os.path.join(dirpath, "templates")
    if not os.path.isdir(tdir):
        return 0
    # Per-direction copy overlay. data/wiseman.json is shared by all three
    # directions, so a direction that has settled on a house style — British
    # spelling, typographic apostrophes — patches the area prose through its
    # own copy.json rather than editing the shared feed under the other two.
    areas = {k: dict(v) for k, v in data["areas"].items()}
    overlay_path = os.path.join(dirpath, "copy.json")
    if os.path.exists(overlay_path):
        with open(overlay_path, encoding="utf-8") as fh:
            overlay = json.load(fh)
        for key, patch in (overlay.get("areas") or {}).items():
            if key in areas:
                areas[key].update(patch)
    # "All 1 buildings in Glendale" is the kind of thing a client reads first.
    for a in areas.values():
        a["countWord"] = "building" if a.get("count") == 1 else "buildings"
    props = [decorate(p, areas) for p in data["properties"]]
    by_area = {}
    for p in props:
        by_area.setdefault(p["areaKey"], []).append(p)
    made = 0

    bt = os.path.join(tdir, "building.html")
    if os.path.exists(bt):
        tpl = open(bt).read()
        out = os.path.join(dirpath, "buildings")
        os.makedirs(out, exist_ok=True)
        for p in props:
            sibs = [s for s in by_area[p["areaKey"]] if s["no"] != p["no"]]
            i = by_area[p["areaKey"]].index(p)
            nxt = by_area[p["areaKey"]][(i + 1) % len(by_area[p["areaKey"]])]
            ctx = {"p": p, "company": data["company"], "area": areas[p["areaKey"]],
                   "nearby": sibs[:4], "next": nxt, "total": len(props)}
            open(os.path.join(out, p["path"] + ".html"), "w").write(render(tpl, ctx))
            made += 1

    nt = os.path.join(tdir, "neighborhood.html")
    if os.path.exists(nt):
        tpl = open(nt).read()
        out = os.path.join(dirpath, "neighborhoods")
        os.makedirs(out, exist_ok=True)
        for key, a in areas.items():
            members = by_area.get(key, [])
            # "1 buildings" is the kind of thing a client reads first.
            ctx = {"area": dict(a, key=key), "company": data["company"],
                   "properties": members, "count": len(members),
                   "countWord": "building" if len(members) == 1 else "buildings",
                   "propsByBeds": sorted(members, key=lambda m: (-(m.get("bedsMax") or 0), m["no"])),
                   "streetList": sorted({m["street"] for m in members}),
                   "others": [dict(v, key=k) for k, v in areas.items() if k != key],
                   # FACT-CHECK §2: recompute the area range from the members the
                   # site is allowed to price. Identical to the stored figures
                   # today, because 070 sets both ends in Palms — but a feed
                   # refresh that moved either end onto 071 would otherwise
                   # publish a Motor Tides rent through the aggregate.
                   "priceLow": money(_area_low(members)),
                   "priceHigh": money(_area_high(members)),
                   # The real embedded map (core/map.js) reads the same array the
                   # drawn-SVG fallback does, so it carries enough to draw a
                   # popup as well as a pin. Additive: WR.atlas ignores the
                   # extra keys. No rent is ever passed — FACT-CHECK §2 bans a
                   # Motor Tides figure anywhere, and a popup is anywhere.
                   "points": json.dumps([{
                       "no": p["no"], "lat": p["lat"], "lng": p["lng"],
                       "name": p["short"], "street": p["street"],
                       "areaLabel": a["name"],
                       "beds": ("" if p["bedsShort"] == "—"
                                else p["bedsShort"].replace("-", "–") + " bed"),
                       "img": (p["galleryThumb"] or [p.get("thumb") or ""])[0],
                       "url": "../buildings/" + p["path"] + ".html",
                   } for p in members], separators=(",", ":"))}
            open(os.path.join(out, key + ".html"), "w").write(render(tpl, ctx))
            made += 1

    if not quiet:
        print("%-12s %3d pages" % (direction, made))
    return made


def write_index(data):
    """Compact index for typeahead, atlas pins and client-side sorting."""
    idx = []
    for p in data["properties"]:
        # FACT-CHECK §2: no Motor Tides rent figure may be published anywhere.
        # index.json feeds the typeahead AND the map popups, so the suppression
        # has to happen here, not in each direction's JavaScript.
        quiet = p["no"] in NO_RENT
        idx.append({
            "no": p["no"], "n": p["short"], "s": p["street"], "a": p["areaKey"],
            "lat": p["lat"], "lng": p["lng"], "u": p["path"],
            "bmin": p["bedsMin"], "bmax": p["bedsMax"],
            "pmin": None if quiet else p["priceMin"],
            "pmax": None if quiet else p["priceMax"],
            "img": p["thumb"],
        })
    out = {"areas": {k: {"name": v["name"], "count": v["count"]} for k, v in data["areas"].items()},
           "p": idx}
    path = os.path.join(ROOT, "data", "index.json")
    json.dump(out, open(path, "w"), separators=(",", ":"), ensure_ascii=False)
    print("index.json  %d entries, %.0f KB" % (len(idx), os.path.getsize(path) / 1024))


if __name__ == "__main__":
    data = json.load(open(DATA))
    write_index(data)
    targets = sys.argv[1:] or [d for d in sorted(os.listdir(ROOT))
                               if os.path.isdir(os.path.join(ROOT, d, "templates"))]
    total = sum(build(t, data) for t in targets)
    print("total %d generated pages" % total)
