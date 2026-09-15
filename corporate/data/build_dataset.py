#!/usr/bin/env python3
"""Merge the scraped RentCafe listing rows + JSON-LD coordinates into one dataset."""
import json, re, os, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
CDN  = "https://resource.rentcafe.com/image/upload/"

AREA_KEY = {
    "West Los Angeles": "west-la", "Brentwood": "brentwood", "Beverly Grove": "beverly-grove",
    "Hollywood": "hollywood", "Venice": "venice", "Palms": "palms", "Glendale": "glendale",
}

ZIP_AREA = {
    "90291": ("Venice", "Venice"),
    "90025": ("West Los Angeles", "West LA · Sawtelle"),
    "90064": ("West Los Angeles", "Rancho Park"),
    "90049": ("Brentwood", "Brentwood"),
    "90034": ("Palms", "Palms · Motor Avenue"),
    "90035": ("Beverly Grove", "Pico–Robertson"),
    "90036": ("Beverly Grove", "Miracle Mile"),
    "90048": ("Beverly Grove", "Beverly Grove"),
    "90069": ("Hollywood", "West Hollywood"),
    "90046": ("Hollywood", "Fairfax · Sunset"),
    "90038": ("Hollywood", "Hollywood"),
    "90004": ("Hollywood", "Hancock Park"),
    "91205": ("Glendale", "Glendale"),
}

def slugify(s):
    s = s.replace(" by Wiseman", "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def street_of(addr):
    m = re.match(r"^\s*[\d\-]+\s+(.+?),", addr or "")
    if not m: return ""
    st = m.group(1)
    st = re.sub(r"\b(N\.?|S\.?|E\.?|W\.?|North|South|East|West)\s+", "", st, flags=re.I)
    st = re.sub(r"\s+(Ave\.?|Avenue|Blvd\.?|Boulevard|St\.?|Street|Dr\.?|Drive|Pl\.?|Place|Rd\.?|Road|Way|Court|Ct\.?|Terrace)\s*$", "", st, flags=re.I)
    return st.strip()

def num_range(s, unit):
    """'650 to 1,657 Sq. Ft.' -> (650, 1657); 'Studio-5 Beds' -> (0, 5)"""
    if not s or s == "—": return (None, None)
    nums = [float(x.replace(",", "")) for x in re.findall(r"[\d,]+(?:\.\d+)?", s)]
    if unit == "beds" and re.search(r"studio", s, re.I):
        nums = [0.0] + nums
    if not nums: return (None, None)
    return (min(nums), max(nums))

TAGS = [
    ("in-unit-laundry", ("washer", "dryer")),
    ("parking",         ("parking", "garage", "carport")),
    ("elevator",        ("elevator",)),
    ("fitness",         ("fitness", "free weights")),
    ("rooftop",         ("rooftop", "roof deck")),
    ("courtyard",       ("courtyard",)),
    ("pool",            ("pool",)),
    ("gated",           ("gated", "controlled access")),
    ("air-conditioning",("air condition", "central ac", "central air", "central heating & air",
                         "central heating and air", "air conditioner")),
    ("dishwasher",      ("dishwasher",)),
    ("patio-balcony",   ("patio", "balcony")),
    ("walk-in-closets", ("walk-in closet",)),
    ("fireplace",       ("fireplace",)),
    ("hardwood",        ("hardwood",)),
    ("ev-charging",     ("electric vehicle",)),
    ("package-locker",  ("package locker", "amazon locker")),
    ("bike-storage",    ("bike rack",)),
    ("on-site-manager", ("on-site management",)),
    ("townhome",        ("townhouse",)),
    ("wheelchair",      ("wheelchair",)),
]


def tags_for(rec):
    """Normalised filter vocabulary, derived from the feed's own amenity strings."""
    hay = " | ".join(rec.get("community", []) + rec.get("apartment", [])).lower()
    out = [key for key, needles in TAGS if any(n in hay for n in needles)]
    if (rec.get("bedsMax") or 0) >= 4:
        out.append("four-plus-bedrooms")
    if rec.get("bedsMin") == 0:
        out.append("studio")
    return out


coords = {}
with open(os.path.join(HERE, "coords.psv")) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        n, la, lo = line.split("|")
        coords[n.lower()] = (float(la), float(lo))

amen = [l.rstrip("\n") for l in open(os.path.join(HERE, "amenities.dict")) if l.strip()]

details = {}
with open(os.path.join(HERE, "details.psv")) as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip(): continue
        parts = (line.split("~") + ["", "", "", ""])[:5]
        nm, desc, units, cam, aam = parts
        pick = lambda s: [amen[int(i)] for i in s.split(",") if i.strip().isdigit() and int(i) < len(amen)]
        seen, cam_l = set(), []
        for a in pick(cam):
            if a.lower() not in seen: seen.add(a.lower()); cam_l.append(a)
        seen, aam_l = set(), []
        for a in pick(aam):
            if a.lower() not in seen: seen.add(a.lower()); aam_l.append(a)
        details[nm.lower()] = {"description": desc.strip(), "units": units.strip(),
                               "community": cam_l, "apartment": aam_l}

galleries = {}
with open(os.path.join(HERE, "galleries.psv")) as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip(): continue
        bits = line.split("~")
        galleries[bits[0].lower()] = [b for b in bits[1:] if b.strip() and "ERR" not in b]

WORDNUM = {"eight":8,"nine":9,"ten":10,"eleven":11,"fifteen":15,"sixteen":16,"eighteen":18,
           "twenty-six":26,"thirty":30,"thirty-six":36,"thirty-nine":39,"forty":40,"forty-six":46,"fifty-one":51}

props = []
with open(os.path.join(HERE, "properties.psv")) as f:
    header = f.readline()
    for line in f:
        line = line.rstrip("\n")
        if not line.strip(): continue
        (name, category, beds, baths, sqft, address, price, phone, path, image) = line.split("|")
        zipc = (re.search(r"(\d{5})\s*$", address) or [None, ""])[1]
        area, hood = ZIP_AREA.get(zipc, ("Los Angeles", "Los Angeles"))
        la, lo = coords.get(name.lower(), (None, None))
        pmin, pmax = num_range(price, "price")
        bmin, bmax = num_range(beds, "beds")
        smin, smax = num_range(sqft, "sqft")
        props.append({
            "name": name,
            "short": name.replace(" by Wiseman", ""),
            "slug": slugify(name),
            "street": street_of(address),
            "address": address,
            "zip": zipc,
            "area": area,
            "neighborhood": hood,
            "lat": la, "lng": lo,
            "beds": beds, "bedsMin": bmin, "bedsMax": bmax,
            "baths": baths,
            "sqft": sqft, "sqftMin": smin, "sqftMax": smax,
            "price": price, "priceMin": pmin, "priceMax": pmax,
            "phone": phone,
            "url": "https://www.wisemanresidential.com/apartments/" + path if path else "",
            "image": (CDN + "q_auto,f_auto,w_1200/" + image) if image else "",
            "thumb": (CDN + "q_auto,f_auto,w_600,h_400,c_fill,g_auto/" + image) if image else "",
            "category": category,
        })
        d = details.get(name.lower(), {})
        g = galleries.get(name.lower(), [])
        rec = props[-1]
        rec["areaKey"] = AREA_KEY.get(area, "west-la")
        rec["description"] = d.get("description", "")
        u = d.get("units", "")
        rec["units"] = WORDNUM.get(u.lower()) if u and not u.isdigit() else (int(u) if u.isdigit() else None)
        rec["community"] = d.get("community", [])
        rec["apartment"] = d.get("apartment", [])
        bmin, bmax = num_range(baths, "baths")
        rec["bathsMin"], rec["bathsMax"] = bmin, bmax
        rec["gallery"] = [CDN + "q_auto,f_auto,w_1400/" + x for x in g]
        rec["galleryThumb"] = [CDN + "q_auto,f_auto,w_700,h_500,c_fill,g_auto/" + x for x in g]
        if not rec["image"] and g:
            rec["image"] = CDN + "q_auto,f_auto,w_1200/" + g[0]
            rec["thumb"] = CDN + "q_auto,f_auto,w_600,h_400,c_fill,g_auto/" + g[0]
        rec["tags"] = tags_for(rec)

areas = {}
for p in props:
    areas.setdefault(p["area"], []).append(p["short"])

# Register numbers are PERMANENT. They were assigned once (geographic block order,
# alphabetical by street) and are pinned in register-lock.json; favourites, URLs and the
# rent-suppression rule all key off them, so a feed change must never renumber anything.
# A building new to the feed takes the next free number and is appended to the lock.
LOCK_PATH = os.path.join(HERE, "register-lock.json")
try:
    LOCK = json.load(open(LOCK_PATH))
except (OSError, ValueError):
    LOCK = {}
BLOCKS = ["west-la", "brentwood", "beverly-grove", "hollywood", "venice", "palms", "glendale"]
n = max([int(v) for v in LOCK.values()] or [0])
order = []
for blk in BLOCKS:
    order += sorted([x for x in props if x["areaKey"] == blk],
                    key=lambda x: (x["street"].lower(), x["short"].lower()))
order += [x for x in props if x not in order]
new_entries = 0
for m in order:
    if m["slug"] in LOCK:
        m["no"] = LOCK[m["slug"]]
    else:
        n += 1
        m["no"] = "%03d" % n
        LOCK[m["slug"]] = m["no"]
        new_entries += 1
    m["path"] = m["slug"]   # URLs carry the name only; the number is an internal id
if new_entries:
    json.dump(LOCK, open(LOCK_PATH, "w"), indent=1, sort_keys=True)
    print("register-lock.json: %d new building(s) numbered" % new_entries)
props.sort(key=lambda x: x["no"])

# ---- currently advertised floor plans, read from each building's live availability card ----
PLANS, HOURS = {}, {}
with open(os.path.join(HERE, "availability.psv")) as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip(): continue
        bits = (line.split("~") + [""] * 8)[:8]
        nm, plan, avail, sqft, dep, rent, link, hours = bits
        if hours.strip(): HOURS[nm.lower()] = hours.strip()
        if plan.strip() in ("", "NONE"): continue
        bm = re.match(r"(Studio|\d+)\s*Beds?", plan); ba = re.search(r"([\d.]+)\s*Baths?", plan)
        beds = 0 if (bm and bm.group(1) == "Studio") else (int(bm.group(1)) if bm else None)
        PLANS.setdefault(nm.lower(), []).append({
            "name": plan.strip(), "beds": beds, "baths": float(ba.group(1)) if ba else None,
            "sqft": int(sqft.replace(",", "")) if sqft.strip() else None,
            "deposit": int(dep.replace(",", "")) if dep.strip() else None,
            "rent": int(rent.replace(",", "")) if rent.strip() else None,
            "available": int(avail) if avail.strip().isdigit() else None,
            "url": link.strip(),
        })
for p in props:
    p["plans"] = sorted(PLANS.get(p["short"].lower(), []), key=lambda x: (x["beds"] if x["beds"] is not None else 99, x["rent"] or 0))
    p["availableNow"] = sum(x["available"] or 0 for x in p["plans"])
    p["officeHours"] = HOURS.get(p["short"].lower(), "")

with open(os.path.join(HERE, "areas.json")) as f:
    AREAS = json.load(f)
for key, a in AREAS.items():
    members = [x for x in props if x["areaKey"] == key]
    a["key"] = key
    a["count"] = len(members)
    lows  = [x["priceMin"] for x in members if x["priceMin"]]
    highs = [x["priceMax"] or x["priceMin"] for x in members if (x["priceMax"] or x["priceMin"])]
    a["priceLow"], a["priceHigh"] = (min(lows) if lows else None), (max(highs) if highs else None)
    a["image"] = next((x["image"] for x in members if x["image"]), "")

out = {
    "company": {
        "name": "Wiseman Residential",
        "tagline": "Los Angeles Living, Managed Wisely.",
        "years": 45,
        "address": "1520 Federal Ave, Los Angeles, CA 90025",
        "phone": "+1 310-473-3000",
        "brandColor": "#169BAC",
        "residentLogin": "https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx",
        "applicantLogin": "https://wisemanresidential.securecafe.com/onlineleasing/apartmentsforrent/guestlogin.aspx",
        "social": {
            "facebook": "https://www.facebook.com/Officialwisemanresidential/",
            "instagram": "https://www.instagram.com/officialwisemanresidential",
            "yelp": "https://www.yelp.com/biz/wiseman-residential-los-angeles-2",
        },
    },
    "areas": AREAS,
    "counts": {"properties": len(props), "areas": {k: len(v) for k, v in sorted(areas.items(), key=lambda kv: -len(kv[1]))}},
    "properties": props,
}

tmp = os.path.join(HERE, "wiseman.json.tmp")
with open(tmp, "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
os.replace(tmp, os.path.join(HERE, "wiseman.json"))   # atomic: a reader never sees a partial file

missing_coords = [p["short"] for p in props if p["lat"] is None]
missing_img = [p["short"] for p in props if not p["image"]]
print(json.dumps({"withDescription": sum(1 for x in props if x["description"]),
                  "withGallery": sum(1 for x in props if x["gallery"]),
                  "withUnits": sum(1 for x in props if x["units"]),
                  "properties": len(props), "areas": out["counts"]["areas"],
                  "missing_coords": missing_coords, "missing_image": missing_img,
                  "price_range": [min(p["priceMin"] for p in props if p["priceMin"]),
                                  max(p["priceMax"] for p in props if p["priceMax"])]}, indent=1))
