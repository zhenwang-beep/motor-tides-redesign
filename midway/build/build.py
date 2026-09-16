#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the three Motor Midway concept sites plus the hub.

    python3 midway/build/build.py

Writes 21 pages (3 concepts x 7) and one hub page. Run it from anywhere; paths
resolve relative to this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import data as D          # noqa: E402
import chrome as C        # noqa: E402
import pages as P         # noqa: E402
import c_golden, c_crossing, c_opendoor   # noqa: E402

CONCEPTS = [c_golden, c_crossing, c_opendoor]

TITLES = {
    "index":      ("{n} by Wiseman | Apartments in Los Angeles, CA",
                   "Two- and three-bedroom apartments at 3657 Motor Ave. in Palms, on the Culver "
                   "City border. Rooftop deck, fitness center, private patio on every residence."),
    "floorplans": ("Floor Plans &amp; Availability | {n} by Wiseman",
                   "Four floor plans from $3,395 a month. Two and three bedrooms, 692 to 909 "
                   "square feet, with current availability and move-in specials."),
    "amenities":  ("Amenities | {n} by Wiseman",
                   "Rooftop deck, fitness center, garage parking, controlled access, elevator, "
                   "bike racks — and in-suite washer and dryer in every residence."),
    "gallery":    ("Photo Gallery | {n} by Wiseman",
                   "{count} photographs of the residences, kitchens, bedrooms, patios, the "
                   "rooftop at dusk and the fitness center."),
    "tours":      ("360&deg; Tours | {n} by Wiseman",
                   "Seven Matterport walkthroughs of the residences at Motor Midway. In-person "
                   "and virtual tours available by appointment."),
    "map":        ("Map &amp; Directions | {n} by Wiseman",
                   "3657 Motor Ave., Los Angeles, CA 90034. Walk Score 89, Bike Score 82, "
                   "Transit Score 61, with directions and what is nearby."),
    "contact":    ("Contact Us | {n} by Wiseman",
                   "Plan a visit to Motor Midway. Leasing office +1 310-853-1532, open Monday "
                   "to Friday 9 AM to 5 PM and weekends 11 AM to 4 PM."),
}

PAGE_BUILDERS = {
    "floorplans": P.floorplans,
    "amenities":  P.amenities,
    "gallery":    P.gallery,
    "tours":      P.tours,
    "map":        P.map_page,
    "contact":    P.contact,
}

CTA = {"index": ("Plan a visit", "contact.html"),
       "floorplans": ("Check availability", D.APPLY),
       "gallery": ("Plan a visit", "contact.html"),
       "amenities": ("Plan a visit", "contact.html"),
       "tours": ("Plan a visit", "contact.html"),
       "map": ("Plan a visit", "contact.html"),
       "contact": ("Call leasing", D.PHONE_TEL)}


def build_concept(c):
    out = os.path.join(ROOT, c.slug)
    os.makedirs(out, exist_ok=True)
    written = []

    for key, (title_t, desc) in TITLES.items():
        fname = f"{key}.html"
        title = title_t.format(n=D.NAME)
        desc = desc.format(count=D.GALLERY_COUNT) if "{count}" in desc else desc
        cta_label, cta_href = CTA[key]

        body = c.home() if key == "index" else PAGE_BUILDERS[key](c)

        # The map page always draws a map; The Crossing also draws one on its
        # home page, where the real street geometry IS the concept.
        needs_map = key == "map" or (key == "index" and c.slug == "crossing")

        html = (
            C.head(title=title, desc=desc, concept_css=f"../assets/{c.css}",
                   body_class=c.body_class(key),
                   extra_head=C.MAP_HEAD if needs_map else "")
            + C.header(fname, cta_label=cta_label, cta_href=cta_href)
            + body
            + C.footer(c.name, c.slug, page=fname,
                       extra_scripts=C.map_scripts() if needs_map else "")
        )
        path = os.path.join(out, fname)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(html)
        written.append((fname, len(html)))
    return written


HUB_CSS = """
:root{--paper:#F3F0E7;--ink:#074B4D;--deep:#04343A;--accent:#9A5A2B;--sun:#E8C08F;
 --tide:#A8C9CE;--muted:#4E5E62;--rule:rgba(7,75,77,.2);--rule-d:rgba(239,234,221,.22);
 --serif:'Newsreader',Georgia,serif;--sans:'Montserrat',sans-serif;--mono:'IBM Plex Mono',monospace;
 --ease:cubic-bezier(.22,.61,.36,1);--pad:clamp(22px,4vw,80px)}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.6;
 -webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit}
:where(a,button):focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:1240px;margin-inline:auto;padding-inline:var(--pad)}
/* The brand mark is a CSS mask filled with currentColor (same as base.css).
   The hub carries its own self-contained stylesheet, so when MARK changed
   from an inline <svg> to a masked <span> this rule had to come with it —
   without it the span has no background and no mask, and renders as nothing. */
.wiseman-mark{display:block;background:currentColor;
 -webkit-mask:url("assets/img/wiseman-symbol.svg") center/contain no-repeat;
 mask:url("assets/img/wiseman-symbol.svg") center/contain no-repeat}
.mk{width:30px;height:21px;flex:none}
header{padding-top:clamp(34px,5vw,60px)}
.brand{display:flex;align-items:center;gap:13px;text-decoration:none}
.brand b{font-size:.84rem;letter-spacing:.3em;text-transform:uppercase;font-weight:600}
.brand i{display:block;font-style:normal;font-size:.5rem;letter-spacing:.46em;text-transform:uppercase;
 opacity:.72;margin-top:3px;font-weight:500}
.hero{padding-block:clamp(46px,7vw,86px) clamp(34px,5vw,54px);border-bottom:1px solid var(--rule)}
.kick{font-size:.72rem;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:var(--accent);
 display:flex;align-items:center;gap:14px;margin-bottom:20px}
.kick::before{content:"";width:30px;height:1px;background:currentColor}
h1{font-family:var(--serif);font-weight:300;font-size:clamp(2.5rem,6.6vw,5.4rem);line-height:1.02;
 letter-spacing:-.012em;max-width:16ch}
h1 em{font-style:italic;color:var(--accent)}
.hero p{max-width:66ch;margin-top:24px;line-height:1.9;color:var(--muted)}
.facts{display:flex;flex-wrap:wrap;gap:10px 26px;margin-top:28px;font-size:.82rem;
 font-family:var(--mono);letter-spacing:.04em}
.facts span{display:flex;align-items:center;gap:9px}
.facts span::before{content:"";width:5px;height:5px;background:var(--accent)}
.grid{display:grid;gap:clamp(22px,3vw,34px);padding:clamp(40px,6vw,66px) 0}
.card{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(24px,4vw,58px);
 align-items:center;padding-bottom:clamp(34px,5vw,54px);border-bottom:1px solid var(--rule);
 text-decoration:none}
.card:last-of-type{border-bottom:0}
.card .shot{aspect-ratio:16/11;overflow:hidden;background:#E9E4D6;order:2}
.card:nth-child(even) .shot{order:0}
.card .shot img{width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease)}
.card:hover .shot img{transform:scale(1.04)}
.num{font-family:var(--mono);font-size:.72rem;letter-spacing:.2em;color:var(--accent);margin-bottom:14px}
.card h2{font-family:var(--serif);font-weight:300;font-size:clamp(2rem,4.6vw,3.6rem);line-height:1.04;
 text-transform:uppercase;letter-spacing:-.01em}
.card .tag{margin-top:12px;font-style:italic;font-family:var(--serif);font-size:1.12rem;color:var(--accent)}
.card p{margin-top:18px;font-size:.92rem;line-height:1.9;color:var(--muted);max-width:52ch}
.go{margin-top:22px;display:inline-flex;align-items:center;gap:10px;font-size:.8rem;font-weight:600;
 letter-spacing:.14em;text-transform:uppercase;border-bottom:1px solid currentColor;padding-bottom:6px}
.go::after{content:"→";transition:transform .3s}
.card:hover .go::after{transform:translateX(5px)}
.pages{margin-top:18px;display:flex;flex-wrap:wrap;gap:7px}
.pages a{font-size:.7rem;letter-spacing:.08em;padding:6px 11px;border:1px solid var(--rule);
 text-decoration:none;transition:background-color .25s,color .25s,border-color .25s}
.pages a:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
@media(max-width:820px){.card,.card:nth-child(even) .shot{grid-template-columns:1fr}
 .card .shot,.card:nth-child(even) .shot{order:0;aspect-ratio:16/10}}
.notes{background:var(--deep);color:var(--paper);padding:clamp(44px,6vw,74px) 0}
.notes h2{font-family:var(--serif);font-weight:300;font-size:clamp(1.6rem,3.4vw,2.6rem);
 text-transform:uppercase;margin-bottom:26px}
.notes h2 em{font-style:italic;color:var(--sun)}
.ncols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));
 gap:clamp(24px,3vw,44px)}
.ncols h3{font-size:.7rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
 color:var(--tide);margin-bottom:12px}
.ncols p,.ncols li{font-size:.86rem;line-height:1.9;color:#C9D6D8}
.ncols ul{list-style:none}
.ncols li{padding-left:16px;position:relative}
.ncols li::before{content:"";position:absolute;left:0;top:.75em;width:6px;height:1px;background:var(--sun)}
.ncols a{color:var(--sun)}
.flag{margin-top:26px;padding:16px 18px;border-left:2px solid var(--sun);background:rgba(232,192,143,.1);
 font-size:.86rem;line-height:1.85;color:#DCE6E7}
footer{padding-block:clamp(30px,4vw,48px);font-size:.76rem;color:var(--muted);display:flex;
 flex-wrap:wrap;gap:10px 26px;justify-content:space-between}
"""


def build_hub():
    cards = []
    for c in CONCEPTS:
        pages_links = "".join(
            f'<a href="{c.slug}/{h}">{t}</a>' for h, t in C.NAV if h != "index.html")
        cards.append(f"""
      <a class="card" href="{c.slug}/index.html">
        <div class="shot">{C.img(c.poster, f'{c.name} — {c.tagline}', sizes='(max-width:820px) 100vw, 48vw')}</div>
        <div>
          <p class="num">Direction {c.number}</p>
          <h2>{c.name}</h2>
          <p class="tag">{c.tagline}</p>
          <p>{c.summary}</p>
          <span class="go">Open the site</span>
        </div>
      </a>""")

    # the page links sit outside the <a> cards so they are not nested anchors
    page_rows = "".join(f"""
      <div class="pages-row">
        <h3>{c.name}</h3>
        <div class="pages">{''.join(f'<a href="{c.slug}/{h}">{t}</a>' for h, t in C.NAV)}</div>
      </div>""" for c in CONCEPTS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Motor Midway by Wiseman — Three Redesign Directions</title>
<meta name="description" content="Three complete, browsable redesign directions for Motor Midway by Wiseman at 3657 Motor Ave., Los Angeles — built on the Motor Tides design system.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="{C.FAVICON_HUB}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://resource.rentcafe.com" crossorigin>
<link href="{C.FONTS}" rel="stylesheet">
<style>{HUB_CSS}
.pages-row{{display:grid;grid-template-columns:150px minmax(0,1fr);gap:12px 22px;align-items:baseline;
 padding:16px 0;border-bottom:1px solid var(--rule)}}
.pages-row h3{{font-family:var(--serif);font-size:1.15rem;text-transform:uppercase;font-weight:400;
 letter-spacing:.02em}}
@media(max-width:620px){{.pages-row{{grid-template-columns:1fr;gap:10px}}}}
.allpages{{padding-block:clamp(34px,5vw,54px)}}
.allpages>p.kick{{margin-bottom:22px}}
</style>
</head>
<body>

<header class="wrap">
  <a class="brand" href="index.html">{C.MARK}<span><b>Motor Midway</b><i>By Wiseman</i></span></a>
</header>

<section class="wrap hero">
  <p class="kick">Three redesign directions</p>
  <h1>One property, one house style, <em>three ideas.</em></h1>
  <p>Three complete seven-page websites for {D.FULL} at {D.ADDRESS_ONE} &mdash; each built on the
     same Wiseman system that runs Motor Tides, so the two properties read as one operator. They
     carry the property&rsquo;s real content: the four current floor plans and their rents, every
     published amenity, the pet policy, all {D.GALLERY_COUNT} photographs, the seven Matterport tours
     and the live application portal. They differ in exactly one thing &mdash; the idea that
     carries them.</p>
  <div class="facts">
    <span>3 directions</span><span>21 pages</span><span>4 floor plans</span>
    <span>{D.GALLERY_COUNT} photographs</span><span>7 360&deg; tours</span><span>0 invented facts</span>
  </div>
</section>

<main class="wrap">
  <div class="grid">{''.join(cards)}</div>
</main>

<section class="wrap allpages">
  <p class="kick">Every page, direct</p>
  {page_rows}
</section>

<section class="notes">
  <div class="wrap">
    <h2>How these were <em>built</em></h2>
    <div class="ncols">
      <div>
        <h3>Inherited, not invented</h3>
        <p>All three use the Motor Tides design system &mdash; the cream paper, the teal ink,
           Newsreader over Montserrat, the squared buttons and letterspaced labels. The single
           value that changes is the accent, from Tides&rsquo; cool coastal tone to a burnt ochre
           that agrees with Midway&rsquo;s golden-hour photography. It is measured at 4.76:1 on
           cream, so it passes AA as body text.</p>
      </div>
      <div>
        <h3>Content is the live site&rsquo;s</h3>
        <ul>
          <li>Four plans, real rents and real availability</li>
          <li>Every community and apartment amenity, verbatim</li>
          <li>Pet policy, weight limit and breed restrictions, verbatim</li>
          <li>Utilities note carried on every plan page</li>
          <li>SecureCAFE apply and resident portals, live</li>
        </ul>
      </div>
      <div>
        <h3>Photography</h3>
        <p>No image is re-hosted. Every photograph is served from the property&rsquo;s own
           RentCafe library &mdash; the same origin the live site uses &mdash; with Cloudinary
           generating a real <code>srcset</code>. The whole deployed bundle is a few hundred
           kilobytes of HTML and CSS.</p>
      </div>
      <div>
        <h3>Two things to confirm</h3>
        <p>The live homepage gives the leasing number as <b>(760) 212-6707</b>, while the contact
           page and the footer both give <b>+1 310-853-1532</b>. These concepts use the 310
           number throughout.</p>
        <p style="margin-top:12px">The photo gallery captions name three plans &mdash; Madison,
           Overland and Palm &mdash; that are not on the availability page.</p>
      </div>
    </div>
    <p class="flag">These are design concepts. The contact forms are not wired to a mailbox, and
       the map is an OpenStreetMap embed rather than the property&rsquo;s mapping vendor. Everything
       else &mdash; plans, rents, amenities, photography, tours, the apply and resident portals
       &mdash; points at the real thing.</p>
  </div>
</section>

<footer class="wrap">
  <span>&copy; 2026 {D.OPERATOR} &middot; design concepts, not a live property site</span>
  <span><a href="{D.WISEMAN}" target="_blank" rel="noopener">wisemanresidential.com</a></span>
</footer>

</body>
</html>
"""
    path = os.path.join(ROOT, "index.html")
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(html)
    return len(html)


def main():
    total = 0
    for c in CONCEPTS:
        rows = build_concept(c)
        total += len(rows)
        print(f"\n  {c.number} {c.name}  ({c.slug}/)")
        for fname, size in rows:
            print(f"      {fname:<18} {size/1024:6.1f} KB")
    size = build_hub()
    print(f"\n  hub  index.html         {size/1024:6.1f} KB")
    print(f"\n  {total} concept pages + 1 hub\n")


if __name__ == "__main__":
    main()
