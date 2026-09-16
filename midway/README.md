# Motor Midway by Wiseman — three redesign directions

Three complete seven-page websites for **Motor Midway by Wiseman**, 3657 Motor Ave.,
Los Angeles — built on the same design system that runs
[Motor Tides](https://wiseman-dev.unitpulse.ai/), so the two properties read as one
operator rather than two vendors.

**▶ [motor-midway-concepts.vercel.app](https://motor-midway-concepts.vercel.app)** — the hub.

| | Direction | The one idea |
|---|---|---|
| 01 | [Golden Hour](https://motor-midway-concepts.vercel.app/golden-hour/index.html) | The property edited as a single evening. Photography sequenced by the clock and the palette travelling with it, cream paper into dusk. |
| 02 | [The Crossing](https://motor-midway-concepts.vercel.app/crossing/index.html) | A drawing set. Motor Avenue's diagonal as the organising line, read off a real basemap rather than a diagram. |
| 03 | [Open Door](https://motor-midway-concepts.vercel.app/open-door/index.html) | The threshold. Every residence here has a patio, so the page is built on paired inside/outside photographs. |

Each direction carries all seven pages: home, floor plans, amenities, photo gallery,
360° tours, map & directions, contact.

---

## What they inherit, and what differs

All three use Motor Tides' system unchanged — cream `#F3F0E7` paper, teal `#074B4D`
ink, Newsreader over Montserrat, squared 48px buttons, letterspaced micro-labels.

**One token differs.** Tides runs a cool coastal accent; Midway runs burnt ochre
`#9A5A2B`, because Midway's best photography is ten frames of a rooftop at golden hour
and the palette should agree with it. It measures **4.76:1 on cream**, so it passes AA
as body text. A tone light enough to *read* as golden hour cannot clear 3:1 on cream
(`#C97F5C` measures 2.76:1), so the warmth lives in the photography and in the dark
sections, never in the accent on paper.

---

## Content

`build/data.py` is the source of truth. Every string in it was read off
motormidway.wisemanresidential.com on 2026-09-15 — four plans with real rents and
availability, every published community and apartment amenity, the pet policy and
breed restrictions verbatim, the utilities note, the live SecureCAFE apply and
resident portals, all 47 gallery photographs and all seven Matterport tours.

Nothing is invented. If a fact is not in `data.py`, the pages do not claim it.

### The map

Every map is MapLibre GL over a Positron basemap retoned for this property
(`assets/maps/midway-positron.json`), with tiles, glyphs and sprites from OpenFreeMap's
public endpoints — no key, no account. The pins are ordinary DOM buttons wired to the
list beside them, so they take the site's focus ring and the list still reads and works
with the map switched off.

Coordinates are cached at build time, never geocoded in the browser: the building came
from Nominatim, the station and studio lots from Overpass. Distances are straight-line
from those coordinates and are labelled as such on the page, because a straight line is
not a walking route.

The Crossing originally argued its thesis with a hand-drawn schematic of the street
grid. A survey-accurate basemap makes the same argument better — the diagonal is not a
graphic device, it is what Motor Avenue does — so the schematic went and the drawing-set
framing (bordered field, sheet number) stayed.

### Three things for the client to confirm

1. **The leasing number is inconsistent on the live site.** The homepage body copy
   gives **(760) 212-6707**; the contact page and the site-wide footer both give
   **+1 310-853-1532**. These concepts use the 310 number throughout.
2. **The photo gallery names three plans that are not on the availability page** —
   Madison, Overland and Palm. Recorded in `data.py` as `ARCHIVE_PLAN_NAMES` so
   nobody later assumes they were dropped by mistake.
3. **The nearest E Line stop is Palms, not Culver City.** Palms is 0.4 mi up Motor
   Avenue; Culver City station is 1.1 mi. Listings for this stretch routinely name
   Culver City, and it is the weaker of the two facts.

---

## Photography

**No image is re-hosted.** Every `<img>` points at the property's own
RentCafe/Cloudinary bucket — the same origin the live site already serves them from —
with Cloudinary transforms generating a real `srcset` at 600/1000/1600/2200px.

That was deliberate. A mirrored copy of this photography exists elsewhere in the
Wiseman repos with **reuse rights still unverified**; pointing at the client's own CDN
leaves that question exactly where it already sits, and keeps the whole deployed
bundle at **589 KB**.

All 56 CDN filenames were verified to return HTTP 200 before being built against.
Note the source filenames are inconsistently spaced (`exterior-1.jpg` but
`exterior -04.jpg`, `mm - unit 17` but `mm- unit 17`) — `data.py` has them exact.

---

## Build

Pages are generated, not hand-written, so the four plans and the amenity lists cannot
drift apart across three concepts.

```bash
python3 midway/build/build.py          # 21 concept pages + hub
python3 midway/scripts/prep_deploy.py  # stage midway/deploy/
```

```
build/
  data.py       content source of truth
  chrome.py     head / header / footer / image helpers  (shared by all three)
  pages.py      the six interior pages                  (shared by all three)
  c_golden.py   ─┐
  c_crossing.py  ├ per-concept home page + page-hero treatment
  c_opendoor.py ─┘
  build.py      the generator
assets/
  base.css      the Wiseman system — tokens, header, footer, buttons, type
  site.js       reveal, menu, gallery filter + lightbox, plan filter, tour loading
  map.js        MapLibre renderer, DOM pins, list ↔ map selection
  maps/         the retoned Positron basemap + its licences
  img/          the Wiseman symbol and wordmark (the only local images)
  golden.css / crossing.css / opendoor.css
```

Each concept supplies a `phero()` and a `home()`; the interior pages are shared and
restyled through the concept stylesheet. Content and IA are identical across all
three because the brief was for the concepts to differ in design, not in what they say.

## Deploy

One Vercel project holds the hub and all three concepts — they are a single tree of
relative links, and with no image rewrites to configure there is nothing to give a
separate project.

```bash
cd midway/deploy && vercel deploy --prod --yes
```

`prep_deploy.py` refuses to stage a bundle that references build tooling, a local
image path, or localhost. `midway/deploy/` is generated and gitignored.

---

## Verified

All 21 pages were swept in-browser at 1440×900 for broken images, horizontal overflow,
heading-order skips, duplicate ids, controls with no accessible name, clipped text, and
computed colour contrast against the effective background — **21/21 clean**, no console
errors. A second sweep measured the vertical gap between every pair of stacked siblings
and flagged labels touching their headings and any chasm over 220px — also clean. Interactions were tested rather than assumed: gallery filter (47 → 11 rooftop →
5 fitness → 47), lightbox open/advance/close at `w_2200`, plan filter (3 bd → Regent,
2 bd → Venice/Dunn/Sony), and the Matterport tours, which load only on click so seven
heavy embeds never land on first paint. All 49 deployed URLs return 200.

Contrast over photography was set by eye against the actual frames rather than
computed, since the pixels behind the type cannot be sampled from a cross-origin image.

## These are concepts

The contact forms are not wired to a mailbox, and the maps are OpenFreeMap rather than
the property's mapping vendor. Everything else — plans, rents, amenities, photography,
tours, and the apply and resident portals — points at the real thing. Every page ships
`noindex, nofollow`.
