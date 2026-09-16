# Wiseman Residential — corporate site

Two complete, browsable website directions for **Wiseman Residential**, the family-run Los Angeles
apartment owner, developer and manager behind Motor Tides. Each direction is a real 86-page site
built on the company's live portfolio — 72 buildings, real addresses, real floor plans as advertised
today, real rents, 288 of their own photographs, and a real map of every building.

**Start here: `hub/index.html`** — presents both. (A third direction, `fivebed/`, was retired by the
client on 2026-09-11; it is kept on disk for the record and linked from the hub as an archive.)

---

## The two directions

| | | |
|---|---|---|
| **01 · Tideline** `tideline/` | Los Angeles light and water as the measure of a portfolio. The company name cut out of a single photograph; a tideline travelling the page. | Fraunces · Archivo |
| **02 · The Plates** `register/` | The portfolio as a catalogue: every building presented as a large-format plate with an index rail. | Libre Franklin · IBM Plex Mono |

Both share the same spine: the same data, sort-don't-filter on the portfolio pages, a real embedded
colour map, an ILS-style search page (dropdown filters, a More-filters modal, chips, a live map), and
building pages with today's floor plans and amenity icons. Buildings are never numbered in anything a
visitor sees — the register numbers in `data/register-lock.json` are an internal id only (favourites,
map↔row sync), and URLs are `buildings/<slug>.html`.

Each direction ships: `index.html`, `buildings.html` (all buildings, three views), 72 generated
building pages, `neighborhoods.html` + 7 generated area pages, `search.html`, `residents.html`,
`company.html`, `contact.html`.

---

## Layout

```
corporate/
  hub/index.html            the presentation hub
  tideline/  register/            (fivebed/ — retired, kept for the record)
      index.html … contact.html      hand-authored pages
      style.css  app.js              the direction's design system
      templates/                     building.html + neighborhood.html
      buildings/  neighborhoods/     generated — do not hand-edit
  core/
      base.css   reset, gutter, reveals, header/menu/curtain shells
      core.js    one rAF scroll dispatcher, reveals, header, menu, register,
                 filters, typeahead, favourites, SVG atlas fallback
      map.js     real map — Leaflet over OpenStreetMap colour tiles (keyless; Esri topo / streets /
                 aerial / grey as one-line options), dot pins, price pills on search, filter sync
      map.css    map skin, driven by each direction's palette tokens
      search.js/.css  the shared ILS search: filter bar, floating popovers, More-filters dialog
      rail.js/.css    arrow-driven horizontal rails with hidden scrollbars
      icons.svg  the amenity icon sprite used on building pages
  data/
      wiseman.json        the whole portfolio, built from the sources below
      index.json          compact index for typeahead and map pins
      properties.psv      the 72 listings as scraped from the live feed
      coords.psv          lat/lng from the site's own JSON-LD
      details.psv         descriptions, unit counts, amenity indices
      galleries.psv       4 photographs per building
      availability.psv    every building's advertised floor plans (plan, sq ft, rent, deposit,
                          count available, office hours) scraped 2026-09-11 from the live feed
      amenities.dict      the amenity vocabulary
      areas.json          neighbourhood editorial
      artdirection.json   hand-curated image manifest — which photo goes where
      register-lock.json  stable internal building ids; a feed change never re-keys them
      build_dataset.py    merges all of the above into wiseman.json
  scripts/
      build_site.py       generates the 79 repetitive pages per direction
      gen_search.py       the shared ILS search UI, spliced into each search.html
      gen_editorial.py    image-led company / residents / contact pages, all directions
      prep_deploy.py      bundles each direction for Vercel
```

## Documents

| | |
|---|---|
| `FACT-CHECK.md` | **Read before writing copy.** What the site may and may not claim, with sources. |
| `CONVENTIONS.md` | The trap list. Every item cost a debugging session on the Motor Tides project. |
| `BUILD-SPEC.md` | Pages, core.js API, markup contracts, footer, copy rules, anti-slop list. |
| `ELEVATE.md` | The image-forward / real-map brief, senior to the original direction specs. |
| `STRATEGY-BRIEF.md` | Positioning, IA, the portfolio problem, three directions, build plan. |
| `CODEX-CONSULT.md` | Independent outside consult. |
| `RESEARCH-STREAMS.json` | The five raw research streams with every source URL. |

## Working on it

```bash
# rebuild the dataset after editing anything in data/*.psv
python3 data/build_dataset.py

# regenerate the 79 repetitive pages for one direction, or all
python3 scripts/build_site.py tideline
python3 scripts/build_site.py

# then, per direction: python3 gen_register.py; then from corporate/:
python3 scripts/gen_search.py && python3 scripts/gen_editorial.py

# serve locally (sends Cache-Control: no-store, so a bumped ?v= is never stale)
python3 scripts/serve.py            # from corporate/, port 8899

# bundle for deployment, then deploy each one
python3 scripts/prep_deploy.py
cd deploy/tideline && vercel link --yes --project wiseman-tideline --scope <scope> && vercel deploy --prod --yes
```

Vanilla HTML, CSS and JS. No framework, no build step, no package manager. Leaflet is the only
third-party script and it loads on demand with a drawn-SVG fallback.

## Where the content came from

Everything is the client's own. The 72 listings, addresses, bed/bath/sq-ft ranges, rents, leasing
phone numbers, amenity lists, descriptions and today's floor plans were read out of their live
RentCafe feed; the coordinates out of the JSON-LD their own search page publishes; the 288
photographs are hotlinked from their CDN. Map tiles come from OpenStreetMap's community server —
fine for a pitch; a launched site should swap in a keyed provider (MapTiler, Stadia) serving the same
style, which is one URL in `core/map.js`. The brand mark and its colour `#1C6775` come from their logo file.

Two claims on their current homepage — "over 45 years" and "over 100+ apartment communities" — could
not be verified and are contradicted by the company's own archived pages and their own feed. Neither
site repeats them. See `FACT-CHECK.md`.
