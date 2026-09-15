# Build spec — shared across the directions

Read `CONVENTIONS.md` and `FACT-CHECK.md` first. They are not optional.

Root: `/Users/wangzhen/Documents/wiseman website/corporate/`

```
data/wiseman.json      the whole portfolio (72 buildings, 7 areas, company block)
data/index.json        compact index for typeahead / atlas pins
core/base.css          shared reset, .wrap gutter, reveals, header/menu/curtain shells
core/core.js           shared spine — see the API below
scripts/build_site.py  generates buildings/*.html and neighborhoods/*.html from templates
assets/img/            wiseman-logo.png and 20 downloaded homepage photographs (wr01–wr20.jpg)
```

Run `python3 scripts/build_site.py <direction>` after writing templates.

## Pages every direction ships

| File | What |
|---|---|
| `index.html` | Home. The signature moment lives here and **only** here. |
| `buildings.html` | All 72 buildings, three peer views (`?view=register\|atlas\|plates`), sort-don't-filter. No visible numbering — the client's rule. |
| `buildings/<slug>.html` | 72 generated from `templates/building.html`: hero, facts, action row, today's floor plans, gallery, listing copy, amenity icons, office hours, map, nearby. |
| `neighborhoods.html` | Seven areas with counts, street lists, a map. |
| `neighborhoods/<key>.html` | 7 generated from `templates/neighborhood.html`. |
| `search.html` | The transactional door. This is the only page with filters. |
| `residents.html` | Five doors: pay rent, maintenance (with a 24/7 path that needs no login), deposits, moving in, rights & resources. |
| `company.html` | What Wiseman does, where, how the on-site model works, and the pipeline. |
| `contact.html` | Routed by intent. One leasing number. Corporate address. |
| `style.css`, `app.js` | Direction-specific. `app.js` calls `WR.boot()`. |
| `templates/building.html`, `templates/neighborhood.html` | For the generator. |

Relative paths from a direction root: `../core/base.css`, `../core/core.js`, `../data/wiseman.json`.
From `buildings/` or `neighborhoods/` one level deeper: `../../core/base.css` etc.

## core.js API

```js
WR.reduce                 // boolean, prefers-reduced-motion
WR.onScroll(fn)           // ONE rAF-gated dispatcher. fn(scrollY, viewportH). Never add another rAF loop.
WR.through(el)            // 0→1 as el crosses the viewport
WR.pinned(el)             // 0→1 progress of a tall section with a sticky child
WR.clamp01(v) WR.smooth(t) WR.lerp(a,b,t)
WR.reveals()              // .rv (text, threshold .14) and .rvi (images, threshold .001) → .in
WR.header({heroEnd:110})  // transparent over hero, .up on scroll-down, .frost on scroll-up, .inv over [data-hd="dark"]
WR.menu()                 // .mbtn + .mnav, inert background, focus return, Escape
WR.transition()           // .pt curtain; intercepts same-origin relative links only
WR.load(url)              // memoised fetch of wiseman.json
WR.register({list,flatLabel})  // sort controls [data-sort], specimen plate [data-plate], hover AND focus
WR.atlas({el, points})    // drawn-SVG fallback for WR.map; dots as pins; syncs .lit with rows
WR.map({el, points, theme, tiles, pins, onSelect})  // core/map.js — Leaflet over colour tiles; pins 'dot' | 'price'
WR.filters({form,rows,count,empty})  // availability filters, URL-encoded state
WR.typeahead({input,out,items})      // items: {hay, no, name, sub, url}
WR.favourites()           // [data-fav="<no>"] toggles, localStorage 'wr-saved'
WR.boot({header:{heroEnd:N}, transition:true})
WR.priceLabel(p) WR.bedLabel(p) WR.money(n)
```

## Register markup contract (so `WR.register` and `WR.atlas` work)

`data-no` is an internal id (favourites, map↔row sync, rent suppression for 071). It never appears in
visible text, captions, titles, ordinals ("001 / 072") or URLs — the client rejected numbering twice.

```html
<div data-register data-mode="grouped">
  <section data-group="west-la">
    <h2><span data-grouplabel>West Los Angeles · Sawtelle</span> <span class="tnum">27</span></h2>
    <div data-rows>
      <div data-row data-no="001" data-name="Amherst Rochester" data-street="Amherst"
           data-area="west-la" data-arealabel="West Los Angeles" data-bedsmax="4"
           data-rent="4895" data-img="…w_900 gallery image…">
        <a href="buildings/amherst-rochester.html">…</a>
      </div>
    </div>
  </section>
</div>
<aside data-plate>
  <img src="" alt=""><span data-plateno></span><span data-platename></span><span data-platestreet></span>
</aside>
<button data-sort="area">Neighbourhood</button> <button data-sort="no">Recommended</button> …
```

Rows must be **complete and usable with the plate absent**. The plate is an enhancement.

## The brand mark — inline SVG, `currentColor`, so it inverts on dark

```html
<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">
  <polygon points="14,18 34,18 34,74 14,80"/>
  <polygon points="40,18 60,18 60,71 40,77"/>
  <polygon points="66,18 86,18 86,68 66,74"/>
</svg>
```

## Equal Housing Opportunity mark — required in every footer

```html
<p class="eho">
  <svg viewBox="0 0 12 10.608" role="img" aria-label="Equal Housing Opportunity" fill="currentColor" focusable="false"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.95263 1.07242L0 4.00926V5.38295H0.663158V9.51979H11.2026V5.38295H11.9921V4.00926L5.95263 1.07242ZM9.9 8.27242H1.95789V4.49874L5.95263 2.44611L9.9 4.49874V8.27242Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 5.82505H4.08947V4.49874H7.77632V5.82505Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 7.73558H4.08947V6.40926H7.77632V7.73558Z"/></svg>
  <span>Equal Housing Opportunity</span>
</p>
```

## Footer contract

The brand mark AND the "Wiseman Residential" wordmark together (never the mark alone), the full site
map (all seven neighbourhoods with counts, Buildings, Find a home, Residents, Company, Contact), the corporate address `1520 Federal Ave, Los Angeles, CA 90025`, one leasing number
`+1 310-473-3000`, resident and applicant login links, the three social links, the EHO mark, and
`© 2026 Wiseman Residential`. No DRE number — see FACT-CHECK §2.

Resident portal: `https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx`
Applicant portal: `https://wisemanresidential.securecafe.com/onlineleasing/apartmentsforrent/guestlogin.aspx`

## Copy rules

- Every count comes from the data. 72 buildings · 7 areas · 52 named streets · homes to five bedrooms.
- 17 buildings offer four bedrooms or more; 5 go to five. 24 offer studios.
- Never invent. Anything the client must confirm renders as a visible `[CLIENT]` chip:
  `<span class="chip">[CLIENT]</span>` — styled small, monospace, boxed, in the accent colour.
- Sentence case in body copy. No exclamation marks. No "elevated", "curated", "nestled",
  "boasts", "seamless", "unparalleled", "vibrant tapestry".
- A building page says what the building is and where it stands. It does not sell a lifestyle.

## Anti-slop list — refuse all of these

Grey card with a 16px radius around every item · a filter sidebar in front of the collection ·
72 photo cards in a responsive grid · a purple-to-blue gradient · Inter/Roboto/Open Sans headlines ·
SVG wave dividers or any literal wave shape · a WebGL water shader · saturated cyan as a surface
colour · animated counters · a carousel of 72 · an obligatory cinematic entrance that blocks search ·
the same fade-in on every element · hover states that do nothing · a map with 72 undifferentiated
pins and no regional aggregation · identical "luxury" descriptions.
