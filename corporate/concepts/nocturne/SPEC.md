# NOCTURNE — build spec (third direction)

The judged, structured concept for Wiseman Residential's third website direction. Build it as a real,
complete direction at `corporate/nocturne/` on the shared core. The rendered concept board is the
visual target: `corporate/concepts/nocturne/index.html` (open it in the browser). This document is the
authority on tokens, type, layout, motion and every page.

## One line
Los Angeles after dark: a night ground where the photographs are the only light, and the portfolio
runs as a reel of film through a lit gate.

## Idea
Nocturne treats the site as a screening room. The ground is a warm near-black (never #000); the
photographs are the only bright surfaces, and everything else — type, hairlines, the search strip, the
map — is drawn in cream at falling alphas like light on a cinema wall. One weight, hierarchy by size and
tracking, zero radius, one accent (brass) spent only where money changes hands. A Didone display face
whose hairlines catch the light; a geometric grotesk set small and tracked for labels. Brass appears at
most four times a page: the Search button, the "available now" status, the reel's gate ticks, and the
primary Apply button. Film grain (an SVG turbulence layer ~8.5%, soft-light, no JS) and a radial
vignette give atmosphere; no gradients except the scrim, no shadows, no radius. Photographs sit inset
inside the gutter on every page except the home hero; the building's own night/dusk frame glows out of
the dark like a lit window. Place is conveyed by facts the data already holds (area, street, bedrooms,
sq ft, plans, office hours, the building's own line) — the fair-housing-safe route.

## Typography (Google Fonts only)
- **Display: Bodoni Moda** (variable opsz 6–96, wght 400–500, + 400 italic). Hero: opsz 40, weight 460,
  letter-spacing −0.028em, a 34px soft text-shadow so hairlines survive over a photograph — never opsz
  96 over an image, never below 20px. Hero size clamp(3rem, 7.4vw, 7.6rem)/0.96. Section & building
  names clamp(2rem, 4.3vw, 4.4rem)/1.0, opsz 48, −0.018em. Sub-heads 1.5–2rem opsz 48. Numerals (rents,
  sq ft, counts) in Bodoni tabular at 1.25–1.9rem. Tagline + one italic clause per section in 400 italic
  opsz 24.
- **Text: Manrope** (400; 500 on buttons and the header). Body 15px/1.6 at cream 72%; UI/facts 13px;
  labels 10.5–11px uppercase 0.22em weight 500; buttons 11.5px uppercase 0.22em. Two families, three
  weights, preconnected, font-display: swap.

## Palette (tokens)
`--night #0F0E0C` ground · `--night-2 #151310` (footer, popovers, reservation column) · `--night-3
#1C1915` (hover) · `--cream #EFE8DB` = ink at 100%, with an alpha ladder `--c86/--c72/--c56/--c40/--c24`
via color-mix · `--line rgba(cream,.14)` and `--line-2 rgba(cream,.08)` (every hairline; no boxes, no
shadows) · `--brass #C9A468` the single accent, `--brass-ink #181206` for text on it, hover `#D6B378` ·
`--focus #1C6775` (the brand teal survives only as the focus ring and the mark's own colour) ·
`--scrim linear-gradient(to top, rgba(15,14,12,.88) 0%, rgba(15,14,12,.46) 34%, transparent 66%)` + a
radial vignette on the hero · `--map-tint var(--night)`; every map runs core/map.js `theme:'dark'` (Esri
imagery + road/place overlays) with 8px brass dots ringed 1px cream, price pills cream-on-night on
search only. Body cream 72% over night ≈ 8:1; labels cream 56% pass AA for 11px caps. No gold gradient,
no metallic, no purple, no cyan surface.

## Layout
One gutter `--pad: clamp(20px, 4.2vw, 64px)` shared by header and content; content capped 1600px. A
12-col grid from 1060px: building page splits 7/5 (inset frame / sticky reservation column), areas beat
5/7, the reel is edge-to-edge with captions on the gutter. Header 60px, never retracts: transparent over
the hero, night at 100% with a hairline elsewhere; mark + letterspaced wordmark + "72 buildings" left,
five nav words centre, a hairline "Find a home" button right; 52px on search.html. Vertical rhythm on an
8px base: sections clamp(88px, 12vh, 176px), one step tighter below 740px. Zero radius everywhere; the
only round things are the 6px status dot and the map pins. Photographs inset inside the gutter except the
home hero and one night frame per page; frames 4:5 in the reel, 3:2 for the inset building-page frame,
21:9 only for streets/skies; galleries are fixed-height contact strips with natural widths. The search
entry is a hairline row: a 66px strip inside the hero, cells separated by 1px cream 24%, backdrop-blurred,
one brass button — never a box, never a pill. Reading measure 640px on company/residents/contact.
Z-index: header 30 · popovers 40 · bottom bar 50 · dialogs 60 · grain 60 (pointer-events none).

## Signature moment — The Reel
The portfolio runs across the page like film through a projector gate, not stacked down it. Home: twelve
selected frames; buildings.html: all 72 grouped by area. Tall 4:5 frames glide horizontally on the night
ground with an AREA eyebrow, the name in Bodoni, the street beneath. The frame at the gate is lit (full
brightness, its atmosphere caption fading in on a bottom scrim, its eyebrow turning brass); every other
frame waits at 42% brightness. Two brass ticks above/below mark the gate and travel with the lit frame; a
hairline progress rule fills brass, the seven areas as chapter markers on the full reel. Desktop: a 300vh
runway with a sticky 100vh stage, WR.pinned mapping vertical scroll to translateX, arrows/arrow-keys step
one frame. Below 900px and under reduced motion it is core/rail.js's plain arrow rail with the same
lit-frame logic on scroll, no pinning on touch. No numbers — only "Six of seventy-two" / "All 72
buildings".

## Motion
One curve, `--ease cubic-bezier(.22,.61,.36,1)`; two clocks (UI 280ms, reveals 900–1200ms). Load, after
document.fonts.ready: hero image scales 1.06→1.00 over 1.2s; tagline/headline/sub/search arrive
opacity 0→1, translateY 14→0, blur(8px)→0 over 0.9s, staggered 150/260/400/580ms; the photo credit fades
last. The search strip is usable at first paint (only opacity animates). Section entry: text rises 18px
and fades 0.9s with 100/200ms sibling delays; images reveal by clip-path inset(0 0 8% 0)→inset(0) over
1.1s; hairlines draw scaleX(0→1) from the left; IntersectionObserver threshold 0.02 so no blank band sits
under the header. Reel: transform-only, scroll-driven; lit-frame brightness + caption crossfade 0.5–0.6s.
Hover: row bg +4%, arrow +4px, a dim frame brightens to 100% over 0.6s, the brass button warms one step.
Reduced motion: every mechanic branches to its static end state, the reel becomes the arrow rail. No
GSAP, Lenis, custom cursor, preloader, or counters.

## Pages
- **HOME** — (1) a dark 1800px frame full-bleed 100svh under the transparent header (use a genuinely
  unused dark exterior; verify it is NOT the retired fivebed opener); tagline "Los Angeles living,
  managed wisely." in Bodoni italic as the eyebrow; headline "Come home to the city at dusk." low-left
  over the scrim; one facts sentence; the hairline search strip (Where · Bedrooms · Monthly rent · More
  filters · Search) → search.html with URL state. (2) facts line: 72 buildings · 7 areas · 52 named
  streets · homes to five bedrooms + the feed timestamp. (3) The Reel, twelve selected frames. (4) Seven
  parts of Los Angeles: an inset 4:5 frame beside a list — name in Bodoni, count, sub-streets in caps, an
  arrow — hover swaps the frame to the area's hero building. (5) Available tonight: the six buildings with
  the most homes listed, hairline rows, price first, "N available now" in brass. (6) Owner · builder ·
  manager: one inset frame + two sentences. (7) Footer. Under 5,400px at 1440.
- **BUILDINGS** — opens `?view=reel` (all 72 by area, chapter markers); `?view=index` the region-grouped
  list (AREA eyebrow, name, street, "to N bedrooms", the data-plate 4:5 frame on hover AND on first paint
  — the specimen must show a building before hover); `?view=atlas` the dark Esri map with brass dot pins
  + area aggregation below zoom 13; sort-don't-filter as hairline text buttons. On wide screens the view
  switch and the sort buttons share ONE row.
- **BUILDING PAGE** — breadcrumb; a 7/5 split: left the building's best frame inset at 3:2 with a
  fixed-height contact strip of its gallery + a caps caption; right a **sticky reservation column**:
  AREA · street eyebrow, name in Bodoni, address link, three facts (bedrooms, sq ft, monthly rent from)
  in Bodoni numerals, "Rents from the leasing feed, not a quote", the brass status "N homes available
  now", then three PRIMARY buttons stacked full-width — **Check availability & apply** (brass, → the
  building's RentCafe `p.url`, new tab, rel=noopener), **Inquire about this building** (cream outline, →
  `contact.html?building=<slug>`; app.js prefills the contact form and shows "About <name>"), **Call**
  (hairline, `tel:`, number visible) — office hours + feed timestamp. Then Today's floor plans as
  bedroom-tabbed hairline rows (plan · sq ft · rent · deposit · available · Apply; Motor Tides 071 →
  "Call for today's rents" / status "Now leasing", never a figure); amenities as 36px stroke icons from
  core/icons.svg in a hairline grid; two sentences of listing copy; the dark map at zoom 15; a mini-reel
  of nearby buildings. Below 1060 the column becomes a sticky bottom bar of the three buttons, with
  `env(safe-area-inset-bottom)`.
- **SEARCH** — the shared core/search.js and core/map.js byte-for-byte, re-skinned by tokens only: 52px
  header, the filter bar as the hairline strip with 11px caps labels and one brass Search, chips as
  hairline ovals, the More-filters dialog on night-2 zero-radius with "Show N buildings", a bottom sheet
  below 740; results as hairline rows with a 4:5 thumb, price first, a tabular facts line, AREA · name,
  "N available now" in brass; the dark map right of 1060px with cream price pills degrading to dots under
  crowding (core map.js `crowd()`); list-first below with a floating "Map" toggle.
- **NEIGHBOURHOOD PAGE** — the area's hero building inset 3:2 with the area name in Bodoni + its count;
  the streets as a caps list; one paragraph of place facts (transit, streets, parks — never who lives
  there); the dark map of that area; a reel of its buildings.
- **COMPANY** — one inset frame per beat: owner · builder · manager, where (the seven areas), the on-site
  model (each building's own office and line), the pipeline (Urbanize LA / The Real Deal citations); no
  year, no count above 72, no awards.
- **FOOTER** — night-2 with a top hairline: mark + wordmark, the tagline in italic, address + the one
  leasing number; Areas with counts; Site (Find a home, Buildings 72, Neighbourhoods 7, Residents,
  Company, Contact); Accounts (resident + applicant logins, Facebook, Instagram, Yelp); the EHO mark at
  22px beside the 18px Wiseman mark, © 2026, and the point-in-time feed line.
- **RESPONSIVE AT 360** — `--pad` 20px; hero headline floors 2.85rem with `text-wrap: balance` (no
  single-word last line); the search strip collapses to one "Where" field over a full-width brass Search
  that opens the filter sheet; nav becomes a Menu button, the header CTA hides; the reel is a 76vw arrow
  rail; the areas list stacks; the building page stacks, facts in two columns, plan rows wrap to two
  columns with column labels drawn in; every target ≥44px; no horizontal overflow at 360/390/768/1024/1366.

## How it differs (do not drift toward either existing direction)
Tideline is warm paper #F2EFE7, Fraunces+Archivo, a soft serif over a full-bleed photo, light and
lyrical. The Plates is white #FBFAF7, Libre Franklin + IBM Plex Mono, a catalogue of plates with mono
captions and ink rules. Nocturne inverts the ground to warm near-black, lets the photographs be the only
light, swaps to a Didone + geometric grotesk at one weight, moves the portfolio from vertical stacks to a
horizontal reel with a lit gate, opens building pages on an inset glowing frame with a sticky reservation
column, replaces teal with brass and paper hairlines with cream-at-14% rules, and adds grain + vignette.
Same spine underneath: core/search.js, core/map.js (theme:'dark'), core/rail.js, base.css, the
generators; only style.css, app.js and the two templates change.

## Risks to engineer around (all binding)
1. Dark can read heavy — keep it residential, not nightlife; a documented fallback is one token swap to a
   cool off-white, keeping the Didone/reel/inset frames/brass. (Do not build the fallback; note it.)
2. Bodoni hairlines thin fast — opsz 40 / weight 460 / soft shadow at hero; never <20px, never opsz 96
   over a photo.
3. A colour map on black looks like an embed — every map runs `theme:'dark'` (Esri imagery, already the
   core default for dark hosts).
4. Only the twenty 1800px `assets/img/wrNN.jpg` frames + a few RentCafe exteriors survive a large crop;
   most community thumbnails are ~500×340. Cap reel 4:5 frames at ~420px wide; do not upscale past native.
5. The scroll-driven reel must degrade to core/rail.js on touch and under reduced motion (a pinned runway
   would otherwise leave a blank band).
6. Grain + backdrop-filter cost paint — grain is one fixed pseudo-element, blur is confined to the 66px
   search strip.
7. Enforce the four-uses-per-page brass budget in the templates (Search, status, gate ticks, Apply).
8. Cream 56% on night passes AA for 11px caps; the 40% step is decorative only and must never carry
   information.
