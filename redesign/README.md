# Motor Tides by Wiseman — Website Redesign Concepts

Pitch materials for [Motor Tides](https://motortides.wisemanresidential.com/) (3557 Motor Avenue,
Los Angeles — a 107-residence Wiseman Residential lease-up on the Culver City border): six live
redesign directions, a shared AI leasing-concierge chat widget, and a stakeholder-facing hub.

All content — copy, floor plans, pricing, photography, links — is real, sourced from the live site
and recorded in [`CONTENT.md`](CONTENT.md). Wiseman branding (three-bars mark, teal palette) is preserved.

## Live URLs

**Hub / concept selector:** https://motor-tides-concepts.vercel.app

| # | Concept | URL | Character |
|---|---------|-----|-----------|
| 01 | Resort Immersive | https://motor-tides-concept-e.vercel.app | The flagship. Cinematic pinned chapters, damped scroll, six switchable color & type themes |
| 02 | Pacific Nocturne | https://motor-tides-concept-nocturne.vercel.app | After-dark resort film — acts, title sequence, traveling iris reveals |
| 03 | Living Monogram | https://motor-tides-concept-monogram.vercel.app | Fashion-house typography — giant Bodoni words filled with imagery |
| 04 | The Grand Tour | https://motor-tides-concept-grandtour.vercel.app | Sunrise to midnight — the palette shifts with time of day as you scroll |
| 05 | Riviera Journal | https://motor-tides-concept-riviera.vercel.app | Sun-drenched travel magazine — masthead, postcards, folios |
| 06 | Voyage | https://motor-tides-concept-voyage.vercel.app | Feadship-inspired journey with a progress rail through six legs |

Also live: **current-site replica** with the concierge bot attached —
https://motor-tides-current.vercel.app (`option-current/`).

**Archived explorations** (linked quietly from the hub): Coastal Editorial
(`option-a`, https://motor-tides-concept-a.vercel.app), Architectural Dark
(`option-c`, https://motor-tides-concept-c.vercel.app), Modern Platform
(`option-b`, https://motor-tides-concept-b.vercel.app), and Estate Green
(a shared Claude artifact — no local source).

## Structure

```
redesign/
├── index.html            hub page (numbered concept cards with live-site preview thumbnails)
├── CONTENT.md            source of truth: address, plans, pricing, amenities, real URLs
├── DEMO-SCRIPT.md        talk track for the owner meeting
├── option-e/             flagship — 4 pages (home, residences, experience, location)
│                         plus shared style.css + app.js (the one concept not fully inline)
├── option-nocturne/      \
├── option-monogram/       |  each: 4 pages (home, residences, floorplans, experience),
├── option-grandtour/      |  self-contained HTML with inline CSS + JS
├── option-riviera/        |
├── option-voyage/        /
├── option-a|b|c/         archived single-page concepts
├── option-current/       replica of the current live site + concierge bot
├── assets/
│   ├── chat.js           shared "Maya · Leasing Concierge" widget, themed per concept
│   ├── img/              property photography + floor-plan drawings (RentCafe CDN originals)
│   │   ├── plans-trim/   margin-trimmed plan drawings used by the plan modals
│   │   └── previews/     hub thumbnails (headless screenshots of each concept)
└── scripts/prep_deploy.py   builds deploy/ bundles for every Vercel project
```

## How it's built

Vanilla HTML, CSS, and JavaScript — no build step, no framework. Shared conventions:

- **Smooth scroll** via [Lenis](https://github.com/darkroomengineering/lenis) from a CDN, one
  `requestAnimationFrame` loop per page, `IntersectionObserver` for reveals.
- **Scroll choreography** with `clip-path`, `background-clip: text`, and transform/opacity only.
- **`prefers-reduced-motion`** disables pinning, parallax, and traversal on every page.
- **Chat widget** (`assets/chat.js`) is shared by all concepts and themed through `--mtc-*`
  custom properties. Scripted flows cover pricing, tours, pets, amenities, neighborhood, and apply.
- **Plan modals** open the real drawing for each of the seven plans; Apply / availability /
  resident-login links point at the property's live SecureCafe and RentCafe endpoints.

## Deploying

Each concept is its own Vercel project. Images resolve through `vercel.json` rewrites to the
property's RentCafe CDN, so the deploy bundles stay small.

```bash
python3 scripts/prep_deploy.py                 # regenerate deploy/ for every project
cd deploy/<key>                                # e.g. deploy/voyage, deploy/hub
vercel link --yes --project motor-tides-concept-<key> --scope <scope>
vercel deploy --prod --yes
```

`deploy/` is generated output and is not tracked in git — always run `prep_deploy.py` before deploying.

## Notes

- Floor-plan drawing ↔ plan-name mapping is inferred from bedroom and unit-stack counts;
  it has not been confirmed by Wiseman.
- The bot is referred to as an "AI leasing concierge" in all feature and marketing copy;
  the "Maya" persona appears only inside live demo conversations.
- The property has no pool, and appliances are stainless with quartz counters — copy and imagery
  across all concepts are kept consistent with `CONTENT.md`.
