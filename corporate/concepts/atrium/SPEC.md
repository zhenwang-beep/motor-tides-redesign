# CLERESTORY — build spec (fourth direction · working key `atrium`)

The authoritative brief for Wiseman Residential's **fourth** website direction. Build it as a real,
complete direction at `corporate/atrium/` on the shared core. The rendered concept board is the visual
target: `corporate/concepts/atrium/index.html` (open it in the browser). This document is the authority
on name, IA, copy, tokens, type, layout, motion and every page. `CONVENTIONS.md` and `FACT-CHECK.md`
remain binding; `ELEVATE.md` binds except where this spec deliberately departs (noted inline).

The other three live directions are portfolio-first. **Clerestory is corporate / culture-first** — it
models the IA of morgangroup.com (About / Live-at / Work-at / Track Record) and translates it to what
Wiseman can *truthfully* say. Nothing here is invented; every unverifiable claim renders as a visible
`[CLIENT]` chip.

## Name
**Clerestory** — the high band of windows that brings daylight down into a hall. It names the look
(bright, top-lit, open) and the argument (a company you can see straight through: it builds, owns and
runs its own buildings, and puts a named office in each one). Working key stays `atrium` in the build
system and URLs; the interface wordmark is plain "Wiseman Residential", and "Clerestory" is the internal
codename only (as Tideline / The Plates / Nocturne are).

## One line
Los Angeles light, brought inside — the bright, culture-first corporate face of a company that builds,
owns and manages every home it rents.

## Idea
Where the three portfolio directions open on a photograph and sell a home, Clerestory opens on the
**company** and earns the home second. The ground is a bright, cool-leaning limestone; warmth comes
from the architecture in the photographs and one teal accent, never from a saturated cream. The grammar
is the premium-developer / annual-report register — a split editorial masthead (a mission statement set
large in the light beside one tall architectural frame), hairline rules that draw themselves, generous
vertical air, and numerals set in the display face. Luxury is space and precision, not gold or gloss.
The whole site argues one true, checkable thing: **Wiseman owns, develops and manages all 72 of its
buildings, and keeps a named office, leasing line and maintenance team inside each one.** That vertical
integration is the differentiator no Westside competitor can copy, and it is the spine of the copy.

## Typography (Google Fonts only — none reused from the other three)
- **Display: Newsreader** (`opsz 18–72`, wght 400/500, + 400/500 italic). A refined transitional
  editorial serif — institutional and calm, not the soft old-style of Tideline's Fraunces nor the
  Didone hairlines of Nocturne's Bodoni, and never a wedding Garamond. Hero `clamp(2.55rem, 5.4vw,
  5.35rem)/1.0`, weight 500, `-0.022em`. Section heads `clamp(1.9rem, 3.4vw, 3.1rem)/1.05`, 500,
  `-0.016em`. Display numerals (the stats ribbon) `clamp(2.6rem, 5.2vw, 4.6rem)`, tabular. One italic
  clause per key moment (the tagline eyebrow; the emphasised word in the mission line and the on-site
  statement) in 500 italic. Never below ~18px; the bright ground carries the contrast, so no text-shadow
  is needed off photography — but any Newsreader set *over* an image uses `paint-order: stroke fill`
  hairline per CONVENTIONS §8.
- **Text: Hanken Grotesk** (400 body, 500 UI/meta, 600 labels/buttons/wordmark). A clean humanist
  grotesk with real tabular numerals — bright and legible, distinct from Archivo / Manrope / Libre
  Franklin / IBM Plex. Body `1.0625rem/1.62`, measure ≤ 68ch. Meta/caption `0.85rem`. Labels
  `0.72rem` / `0.2em` / uppercase. Buttons `0.82rem` / `0.02em`. Facts, rents, counts and bed ranges in
  Hanken **tabular-nums**; only the large "hero" numerals move to Newsreader.

Two families, contrast axis (editorial serif + humanist grotesk), preconnected, `display=swap`.

## Palette (tokens — bright, one sparing accent)
Named by role, not by material (per the anti-cream discipline): the ground is a genuinely bright,
near-neutral limestone that leans faintly cool, not a warm cream.
```
--bg        #F4F3EE   bright limestone ground (cooler + brighter than Tideline's #F2EFE7)
--bg-2      #ECEBE4   one step down — alternating "stone" bands (on-site model, about)
--raised    #FBFAF7   near-white for the frosted header and raised surfaces
--ink       #191A19   cool near-black (neutral, not brown) — headings, wordmark
--ink-2     #3D3F3A   body copy — 9.6:1 on --bg
--ink-3     #63645B   meta, captions, labels — 5.4:1 on --bg (passes AA for small text)
--teal      #1C6775   THE accent (brand) — decorative surfaces/marks only (2.99:1: never body text)
--teal-ink  #0C6C79   teal as TEXT / links on the light ground — 5.5:1 (the readable teal)
--teal-deep #0E7C8B   teal button hover
--line      rgba(25,26,25,.13)   every hairline
--line-2    rgba(25,26,25,.07)   the quieter hairline / inset frame keyline
--scrim     linear-gradient(to top, rgba(18,19,17,.58), rgba(18,19,17,.10) 46%, transparent 66%)
--map-tint  var(--bg)            core/map.js theme:'light', OSM colour tiles, teal dot pins
```
**Teal budget: four uses per page, maximum** — the italic tagline eyebrow, the "Find a home" button,
one keyline/active state, and the ordered-pillar indices (or the stat unit). Body teal only ever in
`--teal-ink`. No gold, no metallic, no gradient except the photo scrim, zero radius everywhere (the only
round things are map pins and the on-site status dot). Themed scrollbar: `scrollbar-color:#c7c6bd var(--bg)`.

## Layout
One gutter `--pad: clamp(20px, 4vw, 72px)` shared by header and content; content capped `1580px`. A
12-col mental grid; the recurring split is roughly `1.05fr / 0.95fr` (copy / frame). Header 70px, sticky,
**never retracts**: transparent over the limestone masthead (dark ink on light — legible), then frosts
to `--raised` at 88% with a `blur(14px)` backdrop and a bottom hairline on scroll (`.frost`). Left: the
inline-SVG mark + letterspaced "WISEMAN RESIDENTIAL". Centre: the five nav words. Right: a solid teal
**Find a home** button. Below 1080px the nav collapses to a Menu button (`inert` background, focus
return, Escape) and the header CTA hides. Section rhythm `clamp(72px, 11vh, 148px)`, one step tighter
below 740px. Photographs: `4:5` and `3:4` tall crops for single buildings and the masthead frame; `21:9`
only for streets/skies; every frame carries a `1px --line-2` inset keyline and `aspect-ratio` so nothing
shifts on load. Cards are avoided — the featured-communities module is an image-forward editorial grid
(tall frame, hairline caption, from-rent) with zero chrome, not a boxed card grid. Z-index scale:
header 30 · sticky 20 · (dialogs/menu from core). `overflow-x: clip` on html/body; every `100vh` gets an
`svh` twin.

## Signature moment — the split masthead + the drawn hairline
Two quiet, ownable devices instead of a photographic spectacle:
1. **The clerestory masthead.** The home (and every top-level page) opens not on a full-bleed photo but
   on a split: the mission statement set large in Newsreader in the bright left column, one tall `4:5`
   architectural frame in the right, a `3px` teal **keyline** drawing itself down the frame's leading
   edge on load, and a measured caption beneath ("Owner · developer · manager of 72 Los Angeles
   buildings"). This is the grammar change that separates Clerestory from the three photo-first
   directions and from Morgan's own full-bleed home. *(Deliberate departure from ELEVATE's "every home
   opens full-bleed"; justified because this is the corporate/culture door, not the portfolio door. The
   **Live at Wiseman** landing — the portfolio door — does open full-bleed per ELEVATE.)*
2. **The measured hairline.** Section rules and figure keylines draw themselves `scaleX(0→1)` from the
   left on reveal, and key captions carry one real fact from the feed ("Studios to five bedrooms",
   "72 buildings · 7 areas · 52 streets"). Cheap, fair-housing-safe, memorable.

## Motion
One curve `--ease: cubic-bezier(.22,.61,.36,1)`; two clocks (UI 280ms, reveals 850–1100ms). Everything
subscribes to `WR.onScroll` — no second rAF loop; transform/opacity/clip-path only.
- **Page load (after `document.fonts.ready`):** the masthead frame scales `1.03→1.00` and the teal
  keyline draws down; the tagline, headline, sub and CTAs rise `18px` and fade, staggered 80/160/240/320ms.
- **Section entry:** text rises `18px`/fades `0.9s`; images reveal `clip-path: inset(0 0 9% 0)→inset(0)`
  `1.1s`, ~120ms behind the text; hairlines `scaleX(0→1)` `0.85s`; IntersectionObserver threshold ~0.12
  with a small negative bottom margin so no blank band sits under the header.
- **Hover:** featured frame scales `1.00→1.045` over `1.1s`; the nav underline wipes in from the left;
  a button arrow translates `4px`; nothing else.
- **Reduced motion:** every mechanic branches to its static end state (all `.rv/.rvi/.rvl` visible, no
  transition) and composition is preserved. Because reveals are `.js .rv{opacity:0}`, content is fully
  visible if the script fails (CONVENTIONS §21). *(Note for the board renderer: `loading="lazy"` frames
  and scroll-reveals mean a one-shot full-page screenshot must step-scroll the page first to trigger
  both — see `concepts/atrium` shoot script.)*

## Pages
- **HOME** — (1) the clerestory masthead: italic tagline eyebrow "Los Angeles living, managed wisely.",
  mission headline "We build the buildings we run, and stay to run them *well*.", one facts sentence
  (72 buildings · 7 parts of LA · own office/leasing/maintenance), **Inside Wiseman** (solid ink) +
  **Find a home** (line) CTAs, the `4:5` frame + caption. (2) **Stats ribbon** — 72 buildings · 7 areas ·
  52 streets · to 5 beds, Newsreader tabular, hairline-divided, every count from `data/wiseman.json`.
  (3) **What Wiseman does** — four *ordered* pillars (numbering earned because it is a real end-to-end
  sequence): 01 Develop · 02 Build · 03 Own · 04 Manage on-site, beside a sticky `3:4` frame. (4)
  **The on-site model** — a stone (`--bg-2`) band: the statement "Repairs and questions go to the
  building's *own office* — not a call centre in another city." + one trust line + a `4:5` courtyard
  frame. (5) **Live at Wiseman** — the featured six (below). (6) **Portfolio map** — the whole portfolio
  on `core/map.js` (`theme:'light'`, OSM colour tiles, teal dot pins, area bubbles below zoom 13,
  scroll-zoom off until clicked). (7) **About Wiseman** — the family-run intro (founder Isaac Cohanzad
  named) + a three-cell **core values** row, each a `[CLIENT]` stub. (8) **Track Record** teaser —
  Motor Tides (107 homes, Palms, minutes from Culver City, now leasing) + one pipeline line citing
  Urbanize LA / The Real Deal; every quantitative total a `[CLIENT]` chip; **never a Motor Tides rent**.
  (9) **Company history** — a timeline rendered entirely as `[CLIENT]` (no invented dates). (10) Footer.
- **ABOUT WISEMAN** (`about.html` / mapped from the shared company page) — the corporate/culture story:
  *What we do* (owner · developer · manager, vertically integrated), *The on-site model* (each building
  its own office/line/maintenance — the genuine differentiator), *Where* (the seven areas with counts),
  *Founder* (Isaac Cohanzad — the only nameable person), *Motor Avenue development*. *History*,
  *Leadership beyond the founder*, *Core values*, and any *Gives Back* content render as clearly-marked
  `[CLIENT]` sections — no founding year, no years-in-business, no advisory board, no awards.
- **LIVE AT WISEMAN** (`live.html`) — the portfolio landing and the one page that **opens full-bleed**
  (ELEVATE): a hero photograph, then a funnel into the shared **Buildings** (`buildings.html`, three
  views), **Neighbourhoods** (`neighborhoods.html` + 7 area pages) and **Search** (`search.html`). Reuses
  `core/search.js`, `core/map.js`, `core/rail.js` and the generated building/area pages byte-for-byte,
  re-skinned by tokens only. Featured-communities modules reuse the home grid.
- **WORK AT WISEMAN** (`work.html`) — careers, culture-forward, built on the existing careers content:
  the roles Wiseman verifiably staffs (on-site management, maintenance, leasing, the corporate office at
  1520 Federal Ave), a short "what it's like to work in the building you manage" note, and an application
  route. Open roles, benefits and EEO wording are `[CLIENT]` stubs. No invented headcount or perks.
- **TRACK RECORD** (`track.html`) — the development pipeline, honest and short: Motor Tides (3557 Motor
  Ave, 90034, Palms — "minutes from Culver City"; seven storeys; 107 homes; 1–4 bedrooms; rooftop deck;
  now leasing) plus the sourced pipeline (68 built at 3659 S Motor; 200 proposed at 3418–3554 S Motor
  with 22 ELI set-asides; 490 filed at 9000–9020 Venice with 64 set-asides; 119 / 77 / 50 on the named
  sites), each **cited to Urbanize LA / The Real Deal on the page**. Any total not in the public record
  (dollars invested, jobs, unit counts beyond the cited filings) is a `[CLIENT]` chip. Never a Motor
  Tides rent.
- **CONTACT / RESIDENTS / legal** — carry over from `scripts/gen_editorial.py` (routed contact, one
  leasing number, corporate address; the five resident doors incl. the deposits page with its
  `[CLIENT COPY]` chip; Privacy / Accessibility / Your Privacy Choices), re-skinned by tokens.
- **BUILDING & NEIGHBOURHOOD pages** — generated by `scripts/build_site.py atrium` from
  `atrium/templates/building.html` + `neighborhood.html`; the shared contract (hero, facts, Apply /
  Inquire / Call, today's floor plans, gallery, amenity icons, office hours, `core/map.js` at zoom 15,
  nearby). No property numbered anywhere. Motor Tides 071 → "Call for today's rents", never a figure.

## Live at Wiseman — the featured six (on the board, real data)
Six real buildings spanning six of the seven areas, each an image-forward editorial cell (`4:5` frame,
area eyebrow, name in Newsreader, bed range + from-rent in Hanken tabular), funnelling to Find a home /
All 72. Board uses: Santa Monica Federal (West L.A.·Sawtelle, Studio–3, from $4,995) · Kiowa Grand
(Brentwood, Studio–2, from $3,450) · Croft Retreat (Beverly Grove, Studio–4, from $4,495) · Wilcox
Melrose (Hollywood, 3 beds, from $3,895) · Venice Wave (Venice, 1–2, from $3,045) · Broadway Glendale
(Glendale, 1–3, from $3,450). Rents flagged "point-in-time snapshot from the live leasing feed, not a
quote". In the built direction the six are data-driven, not hard-coded.

## `[CLIENT]` chips — render, never invent
Company **founding year / years-in-business / any date on the history timeline**; **milestones / "our
story" arc**; **leadership beyond founder Isaac Cohanzad** (names, titles, bios); **core-values wording**;
**Gives Back / philanthropy**; **open roles, benefits, EEO statement** (Work at Wiseman); **any
quantitative development total** not in the cited public record (dollars, jobs, units beyond 72 / the
cited filings); the **deposits page body copy** (`[CLIENT COPY]`). Chip style per CONVENTIONS: small,
monospace, boxed, in the teal accent.

## Not applicable for Wiseman (and why) — Morgan sections we do NOT copy
- **Advisory Board** — no verifiable board exists. Omit (or a single `[CLIENT]` stub if the client
  insists); never list names.
- **Executive / leadership team grid with titles** — FACT-CHECK allows only "founder Isaac Cohanzad".
  No other name or title. Render as `[CLIENT]`, not a fabricated team page.
- **Awards / certifications / memberships (AAGLA, CAA, NMHC, IREM), BBB rating, star ratings** — none
  verified (BBB "not accredited / not rated"; Google 3.2/233). Omit entirely — not even a `[CLIENT]`
  badge wall.
- **"Acquisitions" pillar / investor / fund pages** — Wiseman is an owner-operator that builds and holds,
  not a fund that buys to flip. Replace Morgan's Development·Construction·Acquisitions·Management with
  the true **Develop · Build · Own · Manage-on-site**. No returns, no AUM, no fund language.
- **Founding-year hero / "over 45 years" / "100+ communities"** — unverifiable and self-contradicted
  (FACT-CHECK §1). The site never leads with a year; every count is computed from the feed (72 / 7 / 52).
- **Any dollar / unit / headcount figure, litigation, preservation or tenure claims** — barred by
  FACT-CHECK §2. Not present in any form.

## Footer (atrium style, on `--ink`)
The inline-SVG mark **and** the "Wiseman Residential" wordmark, the italic tagline, the corporate address
`1520 Federal Ave, Los Angeles, CA 90025` + the one leasing number `+1 310-473-3000`; a **Company** column
(About Wiseman · Live at Wiseman · Work at Wiseman · Track Record · Contact · Residents); a
**Neighbourhoods** column (all seven with counts: West L.A.·Sawtelle 27 · Beverly Grove 14 · Brentwood
13 · Hollywood 13 · Venice 2 · Palms·Motor Ave 2 · Glendale 1); an **Accounts** column (resident login,
applicant login, Find a home, Facebook, Instagram, Yelp); the new **Equal Housing Opportunity**
house-and-equals SVG (`alt="Equal Housing Opportunity"`, no smaller than the Wiseman mark) beside the
socials; `© 2026 Wiseman Residential`. No DRE number (FACT-CHECK §2).

## How it differs (do not drift toward the other three)
Tideline is warm paper `#F2EFE7`, Fraunces + Archivo, a soft serif over a full-bleed photo, portfolio-
first and lyrical. The Plates is white `#FBFAF7`, Libre Franklin + IBM Plex Mono, a mono catalogue of
plates. Nocturne inverts to warm near-black, Bodoni + Manrope, brass, a photographic reel. **Clerestory**
is the only **corporate / culture-first** direction: a bright cool limestone ground, Newsreader +
Hanken Grotesk (an editorial serif + a humanist grotesk, both unused elsewhere), a **split editorial
masthead** instead of a full-bleed hero, an ordered "what we do" argument, a stone on-site-model band,
teal (not brass, not paper hairlines) as the single accent, and Morgan's IA translated honestly. Same
spine underneath: `core/search.js`, `core/map.js` (`theme:'light'`), `core/rail.js`, `base.css`, the
generators; only `atrium/style.css`, `atrium/app.js` and the two templates change.

## Risks to engineer around (binding)
1. **The bright warm-neutral ground must not read as cream/Tideline.** Keep it cool-leaning and bright
   (`--bg #F4F3EE`), carry all warmth through imagery + teal, and separate hard via the corporate grammar
   (split masthead, ordered argument) — not via material names. Never a saturated cream.
2. **Contrast is verified, keep it.** Body `--ink-2` 9.6:1, meta/labels `--ink-3` 5.4:1, links `--teal-ink`
   5.5:1. Raw `--teal` is 2.99:1 — decorative only, never body text or a small label.
3. **Newsreader over photography** uses the CONVENTIONS §8 stroke, not an offset shadow; on the bright
   ground no shadow is needed. Never set display below ~18px.
4. **Only the twenty `assets/img/wrNN.jpg` (1800px) + a few RentCafe exteriors survive a large crop**
   (art-direction manifest). The masthead frame and any full-bleed use those; featured/community frames
   cap at plate size (`4:5`, ≤ ~760px) and never upscale past native.
5. **The teal budget (four/page)** is enforced in the templates, or the "sparing accent" becomes decoration.
6. **The masthead's deliberate non-bleed** applies to the corporate pages only; the Live-at-Wiseman
   portfolio door opens full-bleed per ELEVATE, so the two grammars must be kept straight across templates.
7. **Every unverifiable Morgan-style section is a `[CLIENT]` chip or omitted** — history dates, leadership,
   values, Gives Back, open roles, dollar/unit totals. The generator must never print a Motor Tides rent,
   a founding year, or any count above 72.
8. **Reveals are `.js`-gated and lazy images abound** — content is visible without JS; the full-page
   board/QA screenshot must step-scroll first to fire lazy-load + IntersectionObserver.

## Regeneration (from `corporate/`, `?v=18` on every ref, matching the site)
```
python3 scripts/build_site.py atrium
(cd atrium && python3 gen_register.py)
python3 scripts/gen_search.py atrium
python3 scripts/gen_editorial.py atrium          # pass atrium explicitly — its default omits new directions
```
Add `atrium` to any direction list in the shared generators; never break tideline / register / nocturne /
fivebed. Dev server: http://127.0.0.1:8899/ (no-store).
