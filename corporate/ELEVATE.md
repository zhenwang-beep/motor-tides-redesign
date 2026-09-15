# Elevation brief — image-forward, high-end, and a real map

The client has seen the first build and asked for three things. This brief is now senior to the
original direction specs wherever they disagree. `CONVENTIONS.md` and `FACT-CHECK.md` still bind.

> *"Please ensure the site looks cool and elegant and high-end, luxury; make use of the images,
> rather than a lot of text; for the map, please embed real map properly."*

---

## 1. Image-forward. Text earns its place.

The library is 288 real photographs plus 20 better frames from the client's own homepage.
`data/artdirection.json` is a hand-curated manifest — **use it, do not pick images by filename.**
It names the seven hero-grade frames with focal points, the eight atmosphere frames, a hero per
neighbourhood, twelve selected buildings, and eight images to avoid because they are interiors
mislabelled as exteriors, mid-construction, or flat documentation with no light.

Rules:

- **Every home page opens on a full-bleed photograph**, not on type over paper. The headline sits
  inside the image, low and left, over a gradient scrim — never over a flat overlay.
- **A section that could be an image should be an image.** Replace explanatory paragraphs with one
  photograph and one line. Where a paragraph survives, cut it to two sentences.
- **Body copy budget per page: 180 words above the fold, 700 words total.** Count it. If a page is
  over, cut — the photograph already said it.
- **Crop with intent.** Tall crops (4:5, 3:4) for a single building. Wide (21:9) only for streets and
  skies. Never letterbox a building into a 16:9 card.
- **Ask the CDN for the size you paint**: `w_2400` full-bleed, `w_1400` half, `w_700` plate,
  `w_420` row — always with `q_auto,f_auto`. Set `width`/`height` or `aspect-ratio` on every image,
  and `loading="lazy"` below the fold.
- **Scrims are gradients**: `linear-gradient(to top, color-mix(in srgb, var(--deep) 74%, transparent) 0%, transparent 58%)`.
  Never a flat 40% black sheet across a whole frame.

## 2. High-end, not decorated

Luxury in this category is **scale, space, stillness and precision** — not gold, not gloss.

- **Push the type scale up.** Display headlines `clamp(2.6rem, 7.2vw, 8.5rem)` with
  `line-height: 0.94` and optical tracking (`-0.02em` at the top of the scale, `0` at the bottom).
  Small type gets the opposite treatment: `0.7rem` at `0.22em` tracking, uppercase, for labels only.
- **Push the space up.** Section rhythm `clamp(96px, 14vh, 220px)`. Generous is the point.
- **One accent, used four times a page at most.** Everything else lives on the ink/paper alpha ladder.
- **Hairlines, not boxes.** No card with a 16px radius. If two things need separating, use a 1px rule
  at 12% ink or a 4% background shift — then stop.
- **Numerals are typography.** Register numbers, counts, rents and bed counts all use
  `font-variant-numeric: tabular-nums` and sit in the display face where they are large.
- **Detail passes people notice**: a 1px rule that draws itself on reveal; a caption that fades in
  after its image; an image that scales 1.00 → 1.04 across a full viewport of scroll; a hover that
  moves an arrow 4px and nothing else.

## 3. A real map, properly embedded

`core/map.js` + `core/map.css` are built and tested. Leaflet 1.9.4 from cdnjs over **OpenStreetMap's
own colour cartography** (keyless, native tiles to z19), loaded on demand with a drawn-SVG fallback if
the CDN is unreachable. `WR.tiles` / the `tiles:` option switch to Esri's `topo`, `streets`, aerial
`imagery` (the default for a `theme:'dark'` host, with Esri's road and place-name overlays) or the
Canvas greys `light` / `dark`.

> **Tile provider, corrected 11 Sep 2026.** This brief originally specified CARTO, then Esri Canvas
> grey. CARTO's keyless `basemaps.cartocdn.com` stamps **"API KEY REQUIRED"** across every tile; the
> Esri Canvas grey was clean but the client called it "so grey" and asked for a more visual map, so
> the default is now OpenStreetMap standard. Its community tile server has a usage policy
> (operations.osmfoundation.org/policies/tiles) — fine for a pitch, not for a launched site with 72
> building pages: swap in a keyed provider serving the same style (MapTiler, Stadia, Thunderforest);
> it is one URL in `core/map.js`.

```html
<link rel="stylesheet" href="../core/map.css">
<script src="../core/map.js" defer></script>
```
```js
fetch('../data/wiseman.json').then(r => r.json()).then(d => {
  WR.map({
    el: '#portfolio-map',
    theme: 'light',
    points: d.properties.map(p => ({
      no: p.no, lat: p.lat, lng: p.lng, name: p.short, street: p.street,
      area: p.areaKey, areaLabel: p.neighborhood, beds: p.beds, rent: p.price,
      img: p.thumb, url: 'buildings/' + p.path + '.html'
    })),
    areas: Object.fromEntries(Object.entries(d.areas).map(([k, v]) => [k, {name: v.name, count: v.count}]))
  });
});
```

It gives you: numbered pins instead of teardrops, area bubbles with counts when zoomed out (below
zoom 13) so 72 pins never pile up, a photo popup, two-way highlight with any
`[data-row][data-no]` in the page, scroll-wheel zoom disabled until the map is clicked so it never
steals the page scroll, and a whisper of the page's paper over the tiles so the cartography belongs to the
design. Pins are plain dots everywhere (no tails, no numbers, no count bubbles — the client rejected
both) and flat price pills on the search map; pills that would collide draw as dots until zoom or hover
makes room (`crowd()` in map.js).

Put a real map on: `neighborhoods.html` (whole portfolio), every generated neighbourhood page (that
area only, `points` is already in the template context), `buildings.html` under `?view=atlas`, and
every building page (that one building, zoom 15, no area bubbles). **Delete the drawn-SVG atlas from
the page bodies** — it stays only as the automatic fallback inside `map.js`.

Set `--map-tint` in each direction's stylesheet to its own `--paper`.

## 4. Motion

One registered curve, `--ease: cubic-bezier(.22,.61,.36,1)`, on everything. Then exactly these:

| Where | What | Duration |
|---|---|---|
| Page load | The hero image scales 1.06 → 1.00 and its scrim fades; the headline rises in two masked lines, 90ms apart | 1.2s / 0.9s |
| Section entry | Text rises 18px and fades; images reveal by `clip-path: inset(0 0 8% 0)` → `inset(0)`, 120ms behind the text | 0.9s / 1.1s |
| Full-bleed images | Scale 1.00 → 1.04 across one viewport of scroll, transform only | — |
| Row / plate hover | Background shifts 4%, an arrow translates 4px, the plate crossfades | 0.28s |
| Rules | `transform: scaleX(0 → 1)` from the left on reveal | 0.8s |
| Page change | The existing `.pt` curtain | 0.62s |

Nothing else animates. Every mechanic branches on `WR.reduce` to a static end state. All motion is
`transform` and `opacity` only; no second `requestAnimationFrame` loop — subscribe to `WR.onScroll`.

## 5. Per-direction changes

**TIDELINE** — keep the masked lockup, it is the strongest thing built. But the page must now open on
a full-bleed photograph with the search inside it, and the lockup becomes the second beat rather than
the first image on the page. Make the neighbourhood bands full-bleed and much taller. Cut the copy.

**THE REGISTER** — re-cast. The all-type index conflicts with the brief. Keep the spine — permanent
numbers, neighbourhood grouping, sort-don't-filter, the specimen plate — and invert the ratio: the
plate becomes the page. Think a photographic plate book with an index rail, not a directory. Rename
it in the interface to **THE PLATES**. The index stays available as a dense view for people who want
it, but the default is large photography with the number and street set small beneath.

**FIVE BEDROOMS** — the full-bleed hero is right but the frame is wrong: it is cropped into a
television. Use the manifest. Keep the numeral mechanic; make the photographs inside the numerals the
best frames in the library, and give each numeral section a full-bleed photograph behind it at low
opacity so the page never goes flat between beats.
