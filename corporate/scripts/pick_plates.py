#!/usr/bin/env python3
"""Pick one photographic plate per building and write data/plates.json.

Why this exists
---------------
`data/artdirection.json` is the hand-curated judgement about WHICH frames carry the
brand. It was compiled by looking at the 72 *community* photographs. Those frames are
the right pictures — but most of them are tiny: 44 of the 72 community masters are
under 1200px wide and one (015) is 200x150. A plate book cannot be built out of
upscaled 500px JPEGs, so this script measures the real pixel dimensions of every
candidate frame the feed publishes for a building and picks the largest one that is
sharp enough to paint at plate size.

The rule, in order:
  1. Never a dead URL (the feed publishes several that 404 at every transform).
  2. Never the community photograph of a building on artdirection.json's `avoid`
     list — those are the interiors mislabelled as exteriors, the mid-construction
     frames and the flat documentation shots.
  3. Prefer a frame that reads as an elevation (street / exterior / facade in the
     source path) when it is at least 1200px wide.
  4. Otherwise the widest frame the feed has for that building.

`big` is true only when the master is at least 1600px wide. The plate sequence only
puts a `big` frame in a full-bleed or a tall slot; everything else is painted at
half width or smaller, where its master is sufficient.

Dimensions are read from the JPEG SOF header of the first few KB of
`q_auto,f_jpg,w_3000,c_limit/<path>` — c_limit means Cloudinary never upscales, so
what comes back is the true master size.

    python3 scripts/pick_plates.py            # re-probe the CDN and rewrite
    python3 scripts/pick_plates.py --check    # report without writing
"""
import json
import os
import re
import struct
import sys
import urllib.request
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")
ART = os.path.join(ROOT, "data", "artdirection.json")
OUT = os.path.join(ROOT, "data", "plates.json")

CDN = "https://resource.rentcafe.com/image/upload/"
SRC = re.compile(r"/image/upload/[^/]+/(.+)$")
DEAD_TAIL = re.compile(r"%20\.(jpe?g|png)$", re.I)
DEAD_PATHS = frozenset(["s3/2/9707/rsz_1338_formosa_ave_exteriors-1.jpg"])
ELEVATION = re.compile(r"exterior|exteriors|facade|street|elevation", re.I)

BIG_W = 1600          # sharp enough for a full-bleed or a tall plate
ELEVATION_W = 1200    # sharp enough to be preferred for being an elevation

# --------------------------------------------------------------------- looked at
# Everything that lands in a full-bleed slot was downloaded and looked at before it
# was chosen; the automatic rule above is only trusted for the small slots. Two
# things it gets wrong on its own, both found by looking:
#   * 025's "10473 santa monica bl exteriors-03.jpg" is a corridor. The filename lies.
#   * the frames artdirection.json praises are often the community photograph, and
#     44 of those 72 masters are under 1200px. Where the client's own homepage
#     carries the SAME scene at 1800px (assets/img/wr*.jpg), that file is used
#     instead — same picture, four times the pixels.
# `kind` is the slot this frame has earned in the plate sequence. Anything not named
# here is laid out at half width or as a 3:4 tall, where a 1600px master is ample.
VERIFIED = {
    "001": ("bleed", "s3/2/9707/1331%20amherst%20ave%20exteriors%20-22.jpg",
            "Clean four-storey elevation, deep sky, no signage."),
    "022": ("wide", "s3/2/9707/1500purdue-106%20(3).jpg",
            "3000x1252. Symmetrical twin elevation behind queen palms - the one "
            "frame in the library that is genuinely a 21:9 street."),
    "024": ("bleed", "s3/2/9707/image0.jpeg",
            "3000x2000. Curved corner mass at Purdue and Santa Monica."),
    "030": ("bleed", "s3/2/9707/darlington%20legacy%20-%20exterior%20edited.jpg",
            "Sea-glass balconies stacked against a clean sky."),
    "033": ("tall", "s3/2/9707/12017%20goshen%20ave%20%20exterior-11(1).jpg",
            "Twin bungalow-court blocks either side of a stair, one tall palm."),
    "037": ("bleed", "local:assets/img/wr12.jpg",
            "artdirection.json's Brentwood hero. The community master is 500px; the "
            "client's own homepage carries the same courtyard stair at 1800px."),
    "046": ("bleed", "s3/2/9707/409%20n%20hayworth%20ave%20exterior-01.jpg",
            "Painted geometric planters, bottlebrush in flower, hard Californian sun."),
    "051": ("bleed", "s3/3/1030854/100sorlando-105.jpg",
            "artdirection.json's 'navy and white, crisp light'. 1600x1200 master."),
    "057": ("bleed", "s3/2/9707/sunset%20rise%20-%20exterior%203(1).jpg",
            "Five storeys, glass balustrades, one palm at the left edge."),
    "061": ("bleed", "s3/2/9707/old%20hawthorn%20exterior_final.jpg",
            "Wide-angle corner, blue-and-brown balconies over a tiled plinth."),
    "066": ("tall", "s3/2/9707/850%20wilcox%20ave%20exteriors-7.jpg",
            "Warm timber and orange elevation under street trees."),
    "069": ("bleed", None,
            "Venice has two buildings and no sharp elevation. The 2048px coastal "
            "kitchen is the best frame the area has."),
    "071": ("bleed", None,
            "The flagship, 3000x2001. Staged living room open to a balcony and sky."),
    "072": ("wide", "s3/3/119320/220_east_broadway_exterior.jpg",
            "artdirection.json's most cinematic frame - blue hour, starburst street "
            "lights, traffic streaks. Master is only 960px, so it is never painted "
            "wider than a contained 21:9 band."),
}

# The home page opens on this. artdirection.json nominates 072 and 025; 072's only
# master is 960px and goes visibly soft at 100svh, and 025's community master is
# 540px. assets/img/wr05.jpg is 025 - the same Century City Icon the manifest
# praises for "the only frame with real sunset colour" - at 1800x1200.
HERO = {"no": "025", "src": "assets/img/wr05.jpg", "local": True,
        "w": 1800, "h": 1200, "pos": "42% 46%", "dark": True}

# Local masters used as plates, measured from the files in assets/img.
LOCAL_DIMS = {"assets/img/wr12.jpg": (1800, 1013)}


def src_path(u):
    m = SRC.search(u or "")
    return m.group(1) if m else ""


def jpeg_dims(b):
    i = 2
    while i < len(b) - 9:
        if b[i] != 0xFF:
            i += 1
            continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        if i + 4 > len(b):
            return None
        i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None


def measure(path):
    url = CDN + "q_auto,f_jpg,w_3000,c_limit/" + path
    try:
        req = urllib.request.Request(url, headers={"Range": "bytes=0-6000"})
        d = jpeg_dims(urllib.request.urlopen(req, timeout=30).read())
        return (path, d[0], d[1]) if d else (path, 0, 0)
    except Exception:
        return (path, 0, 0)


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    art = json.load(open(ART, encoding="utf-8"))
    avoid = set(art.get("avoid") or [])

    jobs, meta = [], {}
    for p in data["properties"]:
        seen = set()
        cands = []
        for u in [p.get("image")] + (p.get("gallery") or []):
            sp = src_path(u)
            if not sp or sp in seen or sp in DEAD_PATHS or DEAD_TAIL.search(u or ""):
                continue
            # rule 2: the condemned frame is the building's community photograph
            if p["no"] in avoid and u == p.get("image"):
                continue
            seen.add(sp)
            cands.append(sp)
        meta[p["no"]] = cands
        jobs.extend(cands)

    jobs = sorted(set(jobs))
    print("measuring %d frames for %d buildings…" % (len(jobs), len(meta)))
    with cf.ThreadPoolExecutor(16) as ex:
        dims = {path: (w, h) for path, w, h in ex.map(measure, jobs)}

    out, soft, elev = {}, [], 0
    for p in data["properties"]:
        best = None
        for sp in meta[p["no"]]:
            w, h = dims.get(sp, (0, 0))
            if not w:
                continue
            is_el = bool(ELEVATION.search(sp))
            # rule 3 beats rule 4: an elevation that is sharp enough wins outright
            rank = (1 if (is_el and w >= ELEVATION_W) else 0, w)
            if best is None or rank > best[0]:
                best = (rank, sp, w, h, is_el)
        if best is None:
            raise SystemExit("no usable frame for %s" % p["no"])
        _r, sp, w, h, is_el = best
        rec = {"src": sp, "w": w, "h": h, "local": False,
               "elevation": bool(is_el and w >= ELEVATION_W)}

        if p["no"] in VERIFIED:
            kind, override, why = VERIFIED[p["no"]]
            rec["kind"] = kind
            rec["why"] = why
            if override and override.startswith("local:"):
                lp = override.split(":", 1)[1]
                rec.update(src=lp, local=True,
                           w=LOCAL_DIMS[lp][0], h=LOCAL_DIMS[lp][1])
            elif override:
                if override not in dims:
                    dims[override] = measure(override)[1:]
                rec.update(src=override, w=dims[override][0], h=dims[override][1])
        out[p["no"]] = rec
        rec["big"] = rec["w"] >= BIG_W
        if rec["w"] < BIG_W:
            soft.append((p["no"], rec["w"]))
        if rec["elevation"]:
            elev += 1

    print("elevations chosen: %d   masters >= %dpx: %d   soft: %d   looked at: %d"
          % (elev, BIG_W, sum(1 for v in out.values() if v["big"]), len(soft),
             len(VERIFIED)))
    if soft:
        print("  soft masters (never painted above half width):",
              " ".join("%s(%d)" % s for s in soft))
    if "--check" in sys.argv:
        return 0
    json.dump({"_note": "Generated by scripts/pick_plates.py. Native master sizes "
                        "measured against the CDN; see the module docstring. `kind` "
                        "is set only for frames a human looked at.",
               "cdn": CDN, "hero": HERO, "plates": out},
              open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote data/plates.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
