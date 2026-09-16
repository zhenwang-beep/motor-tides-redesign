# -*- coding: utf-8 -*-
"""Shared page chrome — head, header, footer, image helpers.

Every concept renders the same header and footer so the three directions read
as one property. Only the body between them differs.

IMAGES: these pages do not re-host any photography. Every <img> points at the
property's own RentCafe/Cloudinary bucket — the same origin motormidway.
wisemanresidential.com already serves them from — with Cloudinary transforms
generating a real srcset. That keeps the deploy bundles at a few hundred KB
and leaves the image rights exactly where they already are.
"""
import hashlib
import os
import urllib.parse
import data as D

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
_VER_CACHE = {}


def v(rel: str) -> str:
    """`../assets/base.css` -> `../assets/base.css?v=ab12cd34`.

    Filenames here never change, so without this a redeploy leaves whoever
    already opened the page on their cached stylesheet — which is exactly how
    a corrected logo and a corrected nav contrast both went on looking broken
    after they had been fixed and shipped. The query is a hash of the file, so
    it changes when, and only when, the file does."""
    name = rel.split("/assets/", 1)[-1]
    if name not in _VER_CACHE:
        path = os.path.join(_ASSETS, name)
        try:
            with open(path, "rb") as fp:
                _VER_CACHE[name] = hashlib.sha256(fp.read()).hexdigest()[:8]
        except OSError:
            _VER_CACHE[name] = "0"
    return f"{rel}?v={_VER_CACHE[name]}"

CDN = "https://resource.rentcafe.com/image/upload/{t}/s3/2/9707/{f}"
WIDTHS = (600, 1000, 1600, 2200)


def _cdn(fname: str, transform: str) -> str:
    return CDN.format(t=transform, f=urllib.parse.quote(fname, safe=""))


def src(slug: str, w: int = 1600) -> str:
    """Single URL at a given width."""
    kind, fname = D.IMAGES[slug]
    if kind == D.PLAN:
        return _cdn(fname, "q_auto,f_auto,c_limit,w_1400")
    if kind == D.LOGO:
        return _cdn(fname, "q_auto,f_auto,c_limit,w_400")
    return _cdn(fname, f"q_auto,f_auto,c_limit,w_{w}")


def srcset(slug: str) -> str:
    kind, fname = D.IMAGES[slug]
    if kind != D.PHOTO:
        return ""
    return ", ".join(f"{_cdn(fname, f'q_auto,f_auto,c_limit,w_{w}')} {w}w" for w in WIDTHS)


def img(slug, alt, *, sizes="100vw", cls="", loading="lazy",
        w=None, h=None, priority=False, full=False) -> str:
    """<img> with a real srcset. `priority` marks the LCP image."""
    kind, _ = D.IMAGES[slug]
    bits = [f'src="{src(slug)}"']
    ss = srcset(slug)
    if ss:
        bits.append(f'srcset="{ss}"')
        bits.append(f'sizes="{sizes}"')
    if full and kind == D.PHOTO:
        bits.append(f'data-full="{src(slug, 2200)}"')
    bits.append(f'alt="{alt}"')
    if cls:
        bits.append(f'class="{cls}"')
    if w and h:
        bits.append(f'width="{w}" height="{h}"')
    if priority:
        bits.append('fetchpriority="high" decoding="async"')
    else:
        bits.append(f'loading="{loading}" decoding="async"')
    return "<img " + " ".join(bits) + ">"


# ── Brand mark ──────────────────────────────────────────────────────────────
# The real Wiseman symbol (assets/img/wiseman-symbol.svg, 1162x799), drawn as a
# CSS mask filled with currentColor so it takes the header's or the footer's
# colour without a second file. This replaces a hand-drawn approximation whose
# bar widths and slope were both wrong.
MARK = '<span class="mk wiseman-mark" aria-hidden="true"></span>'

EHO = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
       '<path d="M12 3 2 10.2h2.6V21h5.1v-5.6h4.6V21h5.1V10.2H22L12 3Zm0 2.5 6.4 4.6V19h-1.1v-5.6H7.7V19H6.6'
       'v-8.9L12 5.5Z"/></svg>')

# ── Navigation ─────────────────────────────────────────────────────────────
NAV = [
    ("index.html",      "Home"),
    ("floorplans.html", "Floor Plans"),
    ("amenities.html",  "Amenities"),
    ("gallery.html",    "Photos"),
    ("tours.html",      "Tours"),
    ("map.html",        "Map"),
    ("contact.html",    "Contact"),
]

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;"
         "1,6..72,300;1,6..72,400&"
         "family=Montserrat:wght@400;500;600&"
         "family=IBM+Plex+Mono:wght@400;500&display=swap")

# MapLibre is only pulled in by the pages that draw a map (the map page on all
# three concepts, plus The Crossing's home page). Everything else never pays
# for it. Pinned rather than floating so a major release cannot change the
# rendering of a concept nobody is rebuilding.
# 5.6.1, from jsDelivr. cdnjs lists 6.10.0 and serves its stylesheet, but
# 404s the matching maplibre-gl.min.js — which is why the map rendered as an
# empty box. Both files below were checked for a 200 before being pinned.
MAPLIBRE_VER = "5.6.1"
MAPLIBRE_BASE = f"https://cdn.jsdelivr.net/npm/maplibre-gl@{MAPLIBRE_VER}/dist"
MAP_HEAD = (f'<link rel="stylesheet" href="{MAPLIBRE_BASE}/maplibre-gl.css">\n'
            '<link rel="preconnect" href="https://tiles.openfreemap.org" crossorigin>\n')
def map_scripts() -> str:
    return (f'<script id="maplibre-js" defer src="{MAPLIBRE_BASE}/maplibre-gl.js"></script>\n'
            f'<script src="{v("../assets/map.js")}" defer></script>\n')

FAVICON = "../assets/img/wiseman-symbol.svg"       # from a concept page
FAVICON_HUB = "assets/img/wiseman-symbol.svg"      # from the hub at the root


def head(*, title, desc, concept_css, body_class="", extra_head="") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{src('dusk-05', 1600)}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://resource.rentcafe.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{v('../assets/base.css')}">
<link rel="stylesheet" href="{v(concept_css)}">
{extra_head}</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(current: str, *, cta_label="Plan a visit", cta_href="contact.html") -> str:
    links = "".join(
        f'<a href="{h}"{" aria-current=\'page\'" if h == current else ""}>{t}</a>'
        for h, t in NAV if h != "index.html"
    )
    mlinks = "".join(
        f'<a href="{h}"{" aria-current=\'page\'" if h == current else ""}>{t}</a>'
        for h, t in NAV
    )
    return f"""<header class="hd" id="hd">
  <a class="brand" href="index.html" aria-label="{D.FULL} — home">
    {MARK}<span><b>Motor Midway</b><i>By Wiseman</i></span>
  </a>
  <nav class="hnav" aria-label="Primary">{links}</nav>
  <a class="cta" href="{cta_href}"><span>{cta_label}</span></a>
  <button class="mbtn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
      <path d="M3 6h18M3 12h18M3 18h18"/></svg>
  </button>
</header>
<div class="mnav" id="mnav">
  <nav aria-label="All pages">{mlinks}</nav>
  <div class="msub">
    <a class="btn" href="{D.APPLY}" target="_blank" rel="noopener">Check availability</a>
    <a class="btn outline" href="contact.html">Plan a visit</a>
  </div>
  <p class="mcall">Leasing &middot; <a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a></p>
</div>
"""


def footer(concept_name: str, concept_slug: str, extra_scripts: str = "") -> str:
    hours = "".join(f"<li>{d} &middot; {t}</li>" for d, t in D.HOURS)
    return f"""<footer class="ft dark" data-hd="inv">
<div class="wrap">
  <div class="ft-cta">
    <h2>Ready to <em>experience</em> good living?</h2>
    <div class="actions" style="margin:0">
      <a class="btn" href="{D.APPLY}" target="_blank" rel="noopener">Check availability</a>
      <a class="btn outline" href="contact.html">Plan a visit</a>
    </div>
  </div>

  <div class="ft-grid">
    <div>
      <div class="ft-brand">{MARK}<span><b>Motor Midway</b><i>By Wiseman</i></span></div>
      <p class="ft-addr">
        {D.ADDRESS_1}<br>{D.ADDRESS_2}<br>
        <a href="{D.DIRECTIONS}" target="_blank" rel="noopener">Get directions</a><br>
        <a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>
      </p>
    </div>
    <div>
      <h3>Explore</h3>
      <ul>
        <li><a href="floorplans.html">Floor plans</a></li>
        <li><a href="amenities.html">Amenities</a></li>
        <li><a href="gallery.html">Photo gallery</a></li>
        <li><a href="tours.html">360&deg; tours</a></li>
        <li><a href="map.html">Map &amp; directions</a></li>
      </ul>
    </div>
    <div>
      <h3>Residents</h3>
      <ul>
        <li><a href="{D.APPLY}" target="_blank" rel="noopener">Apply now</a></li>
        <li><a href="{D.RESIDENT}" target="_blank" rel="noopener">Resident login</a></li>
        <li><a href="contact.html">Contact us</a></li>
        <li><a href="{D.WISEMAN}" target="_blank" rel="noopener">Wiseman Residential</a></li>
      </ul>
    </div>
    <div>
      <h3>Office hours</h3>
      <ul class="ft-addr" style="list-style:none">{hours}</ul>
      <h3 style="margin-top:22px">Follow</h3>
      <ul>
        <li><a href="{D.INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="{D.FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{D.YELP}" target="_blank" rel="noopener">Yelp</a></li>
      </ul>
    </div>
  </div>

  <div class="ft-bottom">
    <span>&copy; 2026 {D.OPERATOR}. All rights reserved.</span>
    <nav aria-label="Legal">
      <a href="{D.TERMS}" target="_blank" rel="noopener">Terms &amp; conditions</a>
      <a href="{D.PRIVACY}" target="_blank" rel="noopener">Privacy policy</a>
      <a href="{D.ACCESS}" target="_blank" rel="noopener">Accessibility</a>
    </nav>
    <span class="eho">{EHO} Equal Housing Opportunity</span>
  </div>

  <p class="concept-note">
    Design concept &mdash; <b>{concept_name}</b> &middot;
    <a href="../index.html">View all three directions</a> &middot;
    Photography served from the property&rsquo;s own RentCafe library.
  </p>
</div>
</footer>
<script src="{v('../assets/site.js')}" defer></script>
{extra_scripts}</body>
</html>
"""
