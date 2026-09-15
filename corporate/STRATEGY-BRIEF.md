# Wiseman Residential — Strategy Brief

**Prepared for:** corporate site rebuild
**Working data:** `/Users/wangzhen/Documents/wiseman website/corporate/data/wiseman.json` (72 properties, verified below)
**Date:** 10 September 2026

---

## 1. Positioning

The current site says nothing a template couldn't say: a welcome paragraph, a photo slider, two nav items, and two claims — "over 45 years" and "over 100+ apartment communities" — that are both contradicted by the client's own archived pages and by their own property feed. The new site has to stop making claims about *time* and start making a claim about *place*, because place is the only thing here that is both true and unmatched.

**Wiseman is a street company, not a portfolio company.** Read the data and the differentiator is obvious: 27 buildings in West LA sitting on Brockton, Colby, Purdue, Butler, Armacost, Beloit, Barrington, Bentley, Selby, Kelton, Ohio, Federal, Overland, Amherst, McClellan, Westgate and Louisiana; 13 in Brentwood; 14 in Beverly Grove. The buildings are *named after the streets they stand on* — Brockton Manor, Beloit at Ohio, Armacost Manor, Amherst Rochester, Penmar Superba, McClellan Corner. That is not a portfolio, it is a street atlas, and no REIT and no Douglas Emmett page can produce it. Second true claim, layered on top: Wiseman builds and rents the apartments the Westside doesn't otherwise have — the data shows homes up to five bedrooms, and their own site has advertised "rare and highly coveted 3 and 4 bedroom floor plans" since at least 2014. Third: they build what they manage, with a verifiable current pipeline in Palms, Venice and Sawtelle.

So the site's argument is: *these specific streets, these specific buildings, this many bedrooms, and we are still building here.* That argument is checkable line by line, which is precisely why it's persuasive — and it routes around every landmine the brand research turned up. Heritage, stewardship, "preserving neighborhoods," "generations of residents," "45 years" are all off the table: there is a published appellate opinion on Ellis Act/Airbnb class allegations against the principals, press tying the company to rent-controlled evictions and demolitions, and a Wayback trail showing the company said "over 25 years" as recently as September 2025. Puffery invites a search that ends badly. Specificity doesn't.

One more thing the site must carry that the current one doesn't: **the on-site manager.** Every positive review names a person and cites speed; every negative review names the corporate office and cites a security deposit. The site should put the building's own office, hours and manager on every building page, and should answer the deposit question in plain English on its own page. That converts the single genuine operational strength into the site's spine, and pre-empts the single most repeated complaint.

---

## 2. Information architecture

Wiseman currently has a two-item nav. Every credible peer at this size has five blocks: finder, place hierarchy, residents, company, careers. Here is the full map. **E** = essential for the demo build, **S** = secondary (structure the site for it, stub or omit in the demo).

### Primary

| Slug | Page | Contents | |
|---|---|---|---|
| `/` | Home | Signature moment; the count ("72 buildings on 41 streets in 7 parts of Los Angeles"); the Selected twelve; neighborhood entry; rare-large-homes claim; what we're building now; residents strip; one leasing number | **E** |
| `/buildings/` | The Register | The full 72 as a typographic index. Three peer views at real URLs (`?view=register` default, `?view=atlas`, `?view=plates`), sort controls, neighborhood grouping. No prices, no badges. See §3. | **E** |
| `/buildings/<slug>/` | Building page ×72 | Number, name, street address, neighborhood, bed/bath/sqft ranges, 4-image gallery, community + apartment amenity lists, map, this building's office and phone, status caption, Availability + Schedule a Tour + Apply | **E** (3 built, 69 generated) |
| `/buildings/selected/<slug>/` | Selected twelve | Same template, longer photography, a paragraph of real writing per building. The URL tier encodes curation (6a pattern). | **S** |
| `/availability/` | Availability | The transactional door, deliberately separate from the Register (Rudin pattern). Table: building, neighborhood, beds, baths, sqft, rent, available date, apply. Filters live *here* only. Interest-list form when filters return nothing. | **E** |
| `/neighborhoods/` | Neighborhoods index | Seven cards with counts, street lists, a map | **E** |
| `/neighborhoods/west-la/` | West Los Angeles · Sawtelle (27) | Place writing, street list, map, the buildings, link into filtered Register | **E** |
| `/neighborhoods/brentwood/` | Brentwood (13) | as above | **E** |
| `/neighborhoods/beverly-grove/` | Beverly Grove (14) | as above | **S** |
| `/neighborhoods/hollywood/` | Hollywood (13) | as above | **S** |
| `/neighborhoods/venice/` | Venice (2) | as above | **S** |
| `/neighborhoods/palms/` | **Palms · Motor Avenue** (2) | **Rename required.** The data calls this "Culver City"; 3557 S Motor Ave 90034 is City of LA / Palms. Say "minutes from Culver City." Palms is also where the entire pipeline is and it is missing from the current homepage. | **E** |
| `/neighborhoods/glendale/` | Glendale (1) | as above; separate rent-control jurisdiction | **S** |

### Residents

| Slug | Page | | |
|---|---|---|---|
| `/residents/` | Residents hub — five doors, not one login link | **E** |
| `/residents/maintenance/` | Request flow + a **separate, always-visible 24/7 emergency phone path** (nobody with a flooding unit should be asked to log in) | **E** |
| `/residents/deposits/` | **The objection page.** How deposits are held, the California 21-day itemized-statement timeline, how roommate turnovers and partial move-outs work, who to contact, named escalation path. | **E** |
| `/residents/moving-in/` | Utilities with real LADWP / SoCalGas / Spectrum links, renters insurance and how to submit proof, parking, packages, building access | **S** |
| `/residents/rights-and-resources/` | Links out to LAHD's RSO, Renter Protections and Right to Counsel pages, plain-language explanation, scoped per jurisdiction, explicit note that unit-specific disclosures come with the lease | **S** |
| `/residents/pay-rent` | Redirect to the RentCafe portal | **E** (link) |

### Company

| Slug | Page | | |
|---|---|---|---|
| `/company/` | About — what we do, where, how the on-site model works, the numbers we can actually prove | **E** |
| `/company/building/` | **Development / owner side.** Completed and in-progress projects, sourced to trade press. This is Sentral's "For Owners & Developers" block, given its own room so it never intrudes on the renter path. | **E** |
| `/company/building/motor-tides/` | Case study: 104 apartments + 3 ADUs, seven storeys, Uriu & Associates, completing 2026 | **S** |
| `/company/history/` | Blocked on client confirmation of a founding year. Ship `/company/how-we-work/` instead until then. | **S** |
| `/company/leadership/` | Blocked — only Isaac Cohanzad is publicly verifiable as founder, with no stated title | **S** |
| `/careers/` | Real openings or nothing. A stale careers page is worse than none. | **S** |
| `/news/` | Secondary, only with a content owner | **S** |

### Utility

`/contact/` **E** — routed by intent (leasing / current resident / maintenance emergency / owner & development / careers / press), with the corporate address, hours, and **one** central leasing number. `/legal/accessibility/` **S**, `/legal/privacy/` **S**. Footer = full site map with all 72 enumerated by neighborhood, Equal Housing Opportunity mark as a real `<img alt="Equal Housing Opportunity">` sized no smaller than the Wiseman mark, and the broker entity + DRE number **once the client confirms which entity that is**. Spanish paths `/es/...` for search, building, contact and residents — structure for it now, ship later, never machine-translate disclosure text.

**Demo build = 12–14 pages.** Home, Register (3 views), 3 building pages, 2 neighborhood pages, Availability, Residents hub, Deposits, Company, Building/Development, Contact.

---

## 3. The portfolio problem

**The question:** how do 72 buildings on ordinary Westside streets read as a curated collection rather than a spreadsheet?

**The wrong answer, which every AI tool and every mediocre property site converges on:** a responsive grid of 72 photo cards with a 16px radius and a filter sidebar. A card grid stops working at about thirty items. OMA puts 591 projects on one page because the default view is *text*.

**The answer: the Register.** Four moves.

### 3.1 Give every building a permanent number

We do not have acquisition or construction years, and the award-craft research is right that a date is what makes an index read as an archive. Getting years is the highest-value content ask in §4. In the meantime the number itself does most of the work, because a number asserts that the collection is finite, ordered and stewarded.

Assign **001–072 once, in geographic block order, never reassigned**:

```
001–027  West Los Angeles · Sawtelle      (27)
028–040  Brentwood                        (13)
041–054  Beverly Grove                    (14)
055–067  Hollywood                        (13)
068–069  Venice                            (2)
070–071  Palms · Motor Avenue              (2)
072      Glendale                          (1)
```

Alphabetical by street within each block. New acquisitions take 073, 074 and so on — the block structure describes the founding register, not a rule. The number goes in the URL: `/buildings/004-brockton-manor/`. It appears in a left gutter set in a mono with `font-variant-numeric: tabular-nums`. Motor Tides is 070 or 071 — the newest entry in a sequence, not an outlier the other 71 have to live up to.

### 3.2 The Register is a text list, and it is the default view

Row = `NUMBER · NAME · STREET · NEIGHBOURHOOD · BEDS · status`. Five columns, one hairline between rows, no card, no border-box, no radius, no coloured pill. Status is a lowercase caption in small type — *now leasing* / *waitlist* / *fully leased* — borrowed from Aman's property lines and Cleveland Museum's "On View" filter. Rows are grouped under neighbourhood headings with a running count ("West Los Angeles · Sawtelle — twenty-seven buildings"). `content-visibility: auto` on the row groups keeps 72 rows cheap.

**Sort, don't filter.** Controls are `Number | Street A–Z | Neighbourhood | Bedrooms | Year` (Year appears when the client supplies dates). Sorting reorders a complete list; filtering hides things and makes the visitor do inventory work before they've been given a reason to care. There is **no filter sidebar on the Register.** Filtering is the job of `/availability/`, which is a different door.

### 3.3 The specimen plate

This is the mechanic that makes a text list feel expensive. On desktop, the right third of the viewport is a fixed **plate**: one photograph, the building number, the name, the street. Hovering *or keyboard-focusing* a row swaps the plate. The swap uses a same-document View Transition with `view-transition-name` on the plate image and on the number (Baseline since 2025-10-14 — Chrome 111 / Firefox 144 / Safari 18, safe to ship). Clicking the row navigates to the building page, and because the same `view-transition-name` exists on the building page's hero and number, the plate *becomes* the building page. Under 900px the plate collapses to a sticky 40vh strip above the list; under 640px it disappears and rows carry a 64px thumbnail. The list is complete and fully usable with the plate absent — it is an enhancement, never the path to inventory.

All 72 buildings have a 4-image gallery in the data (288 images total), so the plate has real material on day one.

### 3.4 Three peer views, and a separate door for transactions

`?view=register` (default, typographic), `?view=atlas` (map), `?view=plates` (image grid, for the people who came to look at apartments). Real URLs, crawlable, back-button safe, works without JS. The Atlas is not a stock map widget: we have lat/lng for all 72, so it is a drawn SVG of the actual Westside street grid with **numbers as pins, not dots**, and hovering a pin highlights its row. Below the Register, one link: *"Looking for something available now? → Availability."* That page carries the beds / price / move-in / pets / parking / laundry filters, the URL-encoded filter state, the compare tray, and the interest-list capture.

The effect of all this: the Portfolio is permanent, dated, photographed and priceless. The Availability list is a utility. Rudin — a 1925 family owner with 32 properties — ships exactly that split, with "Portfolio," "All Availabilities" and "View Map" as three peer nav items.

### 3.5 Curation on top

Twelve **Selected** buildings at `/buildings/selected/<slug>/`, chosen by hand, with longer photography and a paragraph of real writing each. Everything else is one click away at the complete Register. Curation is a decision a person made, and visitors can feel the difference between a chosen dozen and a filtered result set. It is the cheapest available fix for "this feels like a database."

---

## 4. Content inventory

### What we already have, verified in the repo

- **72 properties**, complete: name, short name, slug, street, full address, ZIP, area, neighbourhood, **lat/lng on all 72**, bed/bath/sqft/price ranges as both strings and numbers, phone, RentCafe URL, hero image, thumb, category, areaKey.
- **288 gallery images** — 72/72 have galleries (66 have four images, 4 have three, 2 have two).
- **Amenities**: 69/72 community lists, 66/72 apartment lists. Top signals: vinyl flooring 51, patio/balcony 48, elevator 42, energy-efficient appliances 39, in-suite alarm 33, gated resident garage 29, in-suite washer/dryer 27 (+24 more under a variant spelling), bike racks 26, central HVAC 23, courtyard 18, fireplace 14, rooftop deck 8, fitness centre 7. **These strings need normalising** — "In-Suite Washer & Dryer" / "In-Suite Washer and Dryer" and three spellings of walk-in closets are the same amenity and currently split the count.
- **Seven neighbourhood editorial blocks** in `areas.json` with a lead, body, street list, map centre and price band each.
- Pricing on 67/72, sqft on 59/72, bed ranges on 71/72, descriptions on 62/72.
- Brand assets: the three-bar mark as inline SVG polygons using `currentColor`, colour values, social links, resident/applicant portal URLs.
- Verified development pipeline from Urbanize/TRD: 3659 Motor (68 units, built), 3557 Motor / Motor Tides (104 + 3 ADUs, completing 2026), 3418 Motor (200 proposed, 22 ELI set-aside), 9000 Venice (490 proposed, 64 ELI), 1600 E Venice (77), 11261 Santa Monica (119), 1808 Lincoln (50).

### What we must get from the client — and what we will otherwise be tempted to invent

| Needed | Why it blocks work | The invention risk if we don't get it |
|---|---|---|
| **Founding year, in writing** | Gates `/company/history/`, any "since" line, the whole legacy frame | Four different years appear in public records: 1982 (CSLB licence), 1985 (their own Archinect bio), 1987 (BBB start date), 1980 (aggregators). **Do not pick one.** And **do not repeat "45 years"** — their own site said "over 25 years" on 7 September 2025. |
| **Unit counts** | Only 18/72 buildings have a unit count (427 units across those 18) | The temptation is to extrapolate to ~1,700 and put it in a stats bar. Don't. Their Archinect profile claims "1000+ residential units built" — that's the only unit number with a source. |
| **Year built or acquired, per building** | This is the field that turns the Register into an archive and unlocks "Sort by year" and year-grouped headings | We will be tempted to infer vintage from architecture in the photos. Absolutely not — and note that Presidio-style "HISTORIC / POST-WWII" tagging is only available to us if the client confirms the dates. |
| **One central leasing number** | The data contains **31 distinct phone numbers** across 72 buildings, including area codes 984 (North Carolina), 760, 714 and 619 (San Diego / Orange County). This actively undermines the local-operator claim. | We will be tempted to just render what's in the feed. Flag it to the client as a defect. |
| **Portfolio count to publish** | Homepage says "100+ communities," feed says 72, TRD counted "nearly 70" in 2024, court filings said 35 in 2019 | Use the live count from the feed, rendered dynamically. 72. |
| **DRE broker entity + licence number** | Footer disclosure | Every principal's DRE licence is expired and no company DRE record exists. **Do not put a DRE number in the footer or imply licensed brokerage** until the client names the licensed entity. |
| **Deposit process, in their words** | The `/residents/deposits/` page is the highest-conversion page on the site and it cannot be written by us | We will be tempted to write a generic "we follow California law" paragraph. That's worthless — the page only works if it names the timeline, the roommate-turnover procedure, and a role to escalate to. |
| **On-site manager model** | Building pages, and the trust argument | Reviews name Limberth, Josh, Yassine, Dianne. **Do not publish employee names from reviews.** We need the client's permission and their own list. |
| **Maintenance and leasing response commitments** | Replaces "professional, communicative, and proactive" — three adjectives with nothing testable behind them | Only publish a number they will actually hold to. |
| **Leadership names and titles** | `/company/leadership/` | Only Isaac Cohanzad as founder is verifiable, with no stated title. Michael and Benjamin's roles come from a BBB entry and a lawsuit. Publish nothing without sign-off, and never use names scraped from ZoomInfo/RocketReach. |
| **Careers openings** | `/careers/` | Ship nothing rather than a stale page. |
| **Which address is correct** | The site says 1520 Federal Ave / 310-473-3000; CSLB, BBB, Archinect and Birdeye all say 11601 Santa Monica Blvd / 310-914-5555 | NAP inconsistency is a real findability problem — flag as a launch task. |
| **Affordable set-asides** | 22 ELI units at 3418 Motor and 64 at 9000 Venice are conditions of the density-bonus incentives | State factually. Concealing income-restricted inventory creates fair-housing exposure; framing it as philanthropy is spin. |

### Content already in the repo that needs a provenance check

The seven `areas.json` neighbourhood write-ups read as project-authored, not client-supplied. Before any of it ships: fact-check every claim (Expo Line stops, distances, named businesses), and run every line against the **California** protected-class list, which is broader than federal. Neighbourhood pages are the single highest fair-housing-risk surface on a portfolio site — characterising an area's "character" or "vibe" in demographic terms is textbook steering. Restrict the copy to verifiable non-demographic facts: transit, distances, named businesses, parks, walk times.

### The standing rules (carried from `CONTENT.md`)

Never invent prices, unit counts, availability or contact info; the live leasing system is the authority and we link out to SecureCafe rather than restating. Never say "No Section 8" or build income-qualifier logic that ignores the voucher portion — source of income is a FEHA protected class. Never write copy that describes the imagined occupant ("perfect for young professionals," "ideal for singles," "great for empty nesters"). Audit the 288-image library **in aggregate** for human-model representation, not shot by shot. Build to WCAG 2.1 AA in code and do not install an accessibility overlay widget. Never claim an award, a BBB rating, a trade-association membership, or a star rating — none are supported.

---

## 5. Three design directions

Each has a different **primary axis** for the 72, which is what makes them structurally different rather than three skins: Tideline organises by **place**, Register by **street and number**, Five Bedrooms by **size of home**.

---

### Direction A — **TIDELINE**

**One sentence:** Los Angeles light and water, used as the measure of a portfolio rather than as decoration — surf photography lives *inside* the wordmark, and a tideline travels across the page as you read.

**Metaphor:** the tide. Chosen deliberately over "the wave": a wave is an event and belongs to one building; a tide is portfolio-scale, place-scale and time-scale — it returns, it covers ground, it measures. It is the only one of the three metaphors that a single lease-up building cannot own, which is exactly the parent-versus-Motor-Tides problem we have to solve.

**Palette** — two hexes plus an alpha ladder, plus two accents (ERA Residence's structure). No cyan anywhere; the evidence from every credible water brand is sand and slate.

```
--paper     #F2EFE7   warm stucco / bone paper
--paper-2   #E6E1D5
--ink       #16242A   wet slate — deliberately not black
--slate     #5D7076   4pm marine layer
--sand      #CBB69B   accent 1, dry sand
--salt      #A8B8B2   accent 2, sea glass
```
Both `--ink` and `--paper` declared at 0 / 5 / 10 / 30 / 60 / 100% alpha via `color-mix()`, giving twelve values that cover every hairline, scrim, divider and tint on the site.

**Typefaces (Google Fonts):** **Fraunces** — variable, with `opsz`, `wght`, `SOFT` and `WONK` axes; an old-style display serif with real lineage, set at `opsz 144, wght 900, SOFT 0, WONK 0` for the masked lockup and `opsz 72, wght 500, WONK 1` for section heads. **Archivo** — variable grotesque for all text, data and the Register, with `font-variant-numeric: tabular-nums` on every number column.

**Signature mechanic — two devices, one metaphor.**

1. **The masked lockup.** Ported from `option-monogram`. A single element with `background-clip: text` containing two block-level spans — `WISEMAN` / `RESIDENTIAL` — over one Santa Monica Bay photograph, so the photo is painted once across the whole lockup and clipped to every glyph; the two lines read as windows onto one continuous seascape, with no per-word alignment maths. Scroll-scrubbed across a 340vh runway with a sticky 100svh stage: `p < 0.30` scales 0.94 → 1.02 while drifting `background-position` 38% → 57.8% *inside* the letters; `0.30–0.66` smoothsteps the scale to peak (7.2 desktop, **4.8 under 700px** — a 7× clipped-text texture is too much for a mid-range phone to rasterise) while the identical photograph fades up full-bleed behind at a staggered offset so there is never a gap; `p ≥ 0.66` holds peak and pushes the full frame 1.00 → 1.06. **Scale never decreases on either element** — a contraction undoes the reveal it just paid off. Mandatory `@supports not (background-clip:text)` fallback resetting `color`, `background` and `-webkit-text-fill-color`. Reduced motion keeps the photograph in the letters as a static piece of art and deletes only the bloom. **One instance, on the home page only** — not on 72 building pages.

2. **The tideline rule.** ERA Residence's scroll indicator, rotated to horizontal. One JS-set `--tide` custom property (0–100%) drives two complementary clips on a shared 1px rule — `clip-path: rect(0 calc(var(--tide) - 14px) 100% 0)` on the fill, `clip-path: rect(0 100% 100% calc(var(--tide) + 14px))` on the track — so a 28px gap travels left to right along the rule as the section crosses the viewport. Zero libraries, one property write. The same `--tide` drives each neighbourhood photograph's `mask-image: linear-gradient(0deg, #fff <tide>, transparent <tide + 18%>)`, so images fill from the bottom like water rising. **No wave shapes, no SVG dividers, no shader.** The water is real footage and real photography; Seasats and Feadship both ship dozens of looping MP4s and zero WebGL.

**Homepage sequence:**
1. Hero — one still frame, low horizon, the wordmark small in the corner, a single typeahead ("Search by street, neighbourhood or building name") and one line: *Seventy-two buildings on forty-one streets in seven parts of Los Angeles.*
2. **The masked lockup** — the 340vh payoff, blooming into full-bleed water.
3. **The count** — three facts on a tideline rule: 72 buildings · 7 neighbourhoods · homes up to five bedrooms.
4. **Selected** — twelve buildings as a horizontal rail of large plates, number and street only.
5. **The neighbourhoods** — seven bands, each a photograph filling from the bottom on `--tide`, with the street list set small underneath.
6. **Rare large homes** — the four- and five-bedroom claim, with the buildings that have them.
7. **Still building here** — the Palms and Venice pipeline, sourced to trade press.
8. **Residents** — four doors including the 24/7 maintenance line.
9. Footer as full site map, all 72 by neighbourhood, EHO mark.

**Wins the client who** already told us the tides-and-waves concept was their favourite, and who wants the corporate site to feel like a place rather than a product.

**Risks:** the water metaphor is one bad decision away from kitsch, and the boundary is thin — the moment anyone adds a cyan, a gradient or an SVG wave divider, it collapses. It is also the direction that most depends on photography we don't yet own: the RentCafe gallery is daylight interiors, and a credible tideline needs real Santa Monica Bay footage, colour-graded to the palette. Budget a shoot or a licence, or the hero is the weakest thing on the page. Finally, "coastal" is a claim Venice and Brentwood can carry and Glendale and Hollywood cannot — the metaphor has to be about *light*, not literal proximity, or it strains across the portfolio.

---

### Direction B — **THE REGISTER**

**One sentence:** The site as a surveyor's index of Los Angeles — numbered, ruled, alphabetised, almost imageless, and completely uninterested in selling you anything.

**Metaphor:** the Thomas Guide. A register of streets, with the buildings as entries. The reference set is Herzog & de Meuron's project index, OMA's 591-row list, Kononenko's "Index, Work, About, Contact," and museum collection browsers.

**Palette:**
```
--paper     #FBFAF7   index card
--paper-2   #EFEDE6
--ink       #141414   press black
--rule      #B9B4A8   hairline
--blueline  #2E4A7D   accent 1, survey blue — links, active states
--flag      #C1502E   accent 2, terracotta — used *only* for "now leasing"
```

**Typefaces (Google Fonts):** **Libre Franklin** — the Franklin Gothic lineage, American institutional printing, variable, used for absolutely everything textual. **IBM Plex Mono** — the left gutter, the numbers, the coordinates, the street index, all with tabular figures. Two families, no display face. The restraint *is* the design.

**Signature mechanic — the plate and the ruler.**
The Register (§3) is not a page here, it *is* the site: the home page opens directly into it, with the company material as short interstitial texts between neighbourhood blocks. Three devices:

1. **The specimen plate** — fixed right third, swaps on hover or keyboard focus via a same-document View Transition, with `view-transition-name` on both the image and the number so the plate literally becomes the building page on click. 160ms crossfade, one registered easing curve.
2. **The ruler** — a fixed horizontal scale above the register drawn with `repeating-linear-gradient`, ticked by street initial or by neighbourhood, with a travelling caret bound to scroll position. It tells you where in the collection you are the way a map margin does. Tabular numerals so digits never jitter.
3. **The Atlas** — a hand-built SVG of the real Westside street grid from our lat/lng, pins rendered as three-digit numbers rather than dots, hover syncs to the row. Never a stock map widget.

**Homepage sequence:**
1. A masthead: `WISEMAN RESIDENTIAL — A REGISTER OF SEVENTY-TWO BUILDINGS IN LOS ANGELES`, one rule, one date line.
2. The count, stated flat: buildings, neighbourhoods, streets. No animated counters.
3. **West Los Angeles · Sawtelle — twenty-seven** — full register block, plate live.
4. A short text: how the on-site model works. One column, 62 characters.
5. **Brentwood — thirteen.**
6. A short text: what we are building now.
7. **Beverly Grove — fourteen**, **Hollywood — thirteen**, **Venice — two**, **Palms — two**, **Glendale — one.**
8. Availability as a single line of type: *For what is available this week, see Availability.*
9. Colophon-style footer: address, hours, one leasing number, EHO mark, the full index again.

**Wins the client who** wants to be taken seriously by owners, lenders, brokers and city planners — the client who reads the Douglas Emmett site and thinks "we should look more serious than that." It is also the cheapest direction to build well and the fastest to load.

**Risks:** it is cold. Renters searching for a two-bedroom in Sawtelle at 11pm do not want a surveyor's index, and this direction asks the Availability page to carry the entire commercial burden alone. It also strands 288 photographs in a thumbnail-sized plate — we'd be buying restraint with an asset we already own. And an all-type site is unforgiving: if the typography is a millimetre off, there is nothing else on the page to look at.

---

### Direction C — **FIVE BEDROOMS**

**One sentence:** The portfolio organised by the size of the home, leading with the one product claim no Westside competitor can match — Wiseman rents three, four and five bedroom apartments in neighbourhoods where those effectively don't exist.

**Metaphor:** the count of rooms. Warm, domestic, plainly useful. Where Tideline is about light and Register is about geography, this is about the apartment itself.

**Palette:**
```
--paper     #FAF4EA   warm plaster
--paper-2   #F0E6D6
--ink       #2A211B   warm brown-black
--rule      #C7B7A2
--terra     #A8562F   accent 1
--olive     #6B6F4B   accent 2
```

**Typefaces (Google Fonts):** **Young Serif** — a single-weight chunky serif with big, confident shapes, used *only* for the giant numerals and for the building numbers. **Work Sans** — variable, for everything else. Two families, cleanly separated by job.

**Signature mechanic — the count.**
The home page is a vertical run of five enormous numerals — **1 2 3 4 5** — each set in Young Serif at `clamp(8rem, min(44vw, 62vh), 30rem)`, each pinned in a sticky 100svh stage. Each numeral uses the same single-element `background-clip: text` technique as Tideline's lockup, but with a *different* photograph per numeral, so the photo appears inside the glyph's strokes and counters. As a numeral scrolls through its stage, the clipped photograph drifts `background-position` across the glyph and the numeral scales forward from 0.96 to 1.10 — **forward-only, never contracting** — then hands off to the next. Beneath each: a plain line — *four bedrooms · nine buildings · West LA, Brentwood, Beverly Grove* — linking into the Register pre-sorted by bedroom count.

Second device: **room strips.** On a building page the gallery is a horizontal `scroll-snap-type: x mandatory` rail, one photograph per room, each with a small set-in-type room label. A progress rule under the rail uses `animation-timeline: view()` **gated behind `@supports (animation-timeline: view())`** with a fully-styled static fallback — Firefox has no implementation at all and an ungated version ships broken content.

**Homepage sequence:**
1. Hero — one warm interior, and the line *We build apartments with more rooms than the Westside usually gets.*
2. **The count** — the five sticky numerals, 1 through 5.
3. **Where the large homes are** — the buildings that carry four and five bedrooms, as plates.
4. **The Register** — the full 72, in the §3 form, sorted by bedrooms by default with a sort control.
5. **The neighbourhoods** — seven bands with street lists.
6. **How a Wiseman building works** — on-site management, the maintenance path, the deposit page linked by name.
7. **Still building here** — the pipeline.
8. Footer as full site map, EHO mark.

**Wins the client who** looks at the reviews and the data and concludes the strongest thing they have is the product, not the story — and who wants a site that converts roommate households and larger families rather than one that impresses their peers.

**Risks:** two, and both are real. First, **fair housing.** Organising a site around bedroom count is safe; organising it around *who lives in those bedrooms* is steering. Every line has to describe the apartment, never the household — no "perfect for roommates," no "ideal for growing families" — and the photography must not settle into a single demographic across 72 buildings. This direction needs a formal copy and image review, in writing, before launch. Second, it is the direction closest to a listings site. Lead with bedroom counts and the visual grammar drifts toward a portal; the Register and the restraint of the numerals are the only things holding it away from Zillow, and they have to be held hard.

---

### Recommendation: **TIDELINE**, with the Register as its spine

Three reasons.

**It is the one the client already chose.** Of six Motor Tides concepts they picked the tides-and-waves one. Directors who ignore a signal that clear are usually about to lose an argument they didn't need to have. The job is not to find a new metaphor, it is to prove the metaphor scales from one building to a parent company — and the tide does, because it is the one water idea that is about *return and coverage* rather than a single event.

**It solves the positioning problem the other two don't.** Register is credible but silent about place-feeling; Five Bedrooms is commercially sharp but says nothing about Los Angeles. Tideline can carry both the light and the street atlas at once: the masked lockup does the identity work in twenty seconds, and the Register underneath does the seventy-two-buildings work. Neither of the other directions gets both.

**We have already built and debugged the hard part.** The mask mechanic exists, its phase maths is verified over a 41-point monotonic sweep, its mobile peak-scale cap and `@supports` fallback and reduced-motion collapse are already written, and the commit history documents every trap. Tideline is the only direction where the signature moment is a port rather than an invention.

**What to take from the others regardless of direction:** the Register, the specimen plate, the permanent number, the sort-don't-filter rule, and the Portfolio/Availability split are not Direction B — they are the answer to §3 and they ship in all three. And Direction C's insight about large homes is a *content* insight, not a design one: the four-and-five-bedroom claim belongs on the Tideline homepage as section 6 whatever we pick.

---

## 6. Build plan

### Demo-complete, per direction

Same page count for all three so they can be compared honestly. **13 pages:**

| Page | Real | Stubbed |
|---|---|---|
| Home | full sequence, signature mechanic working, real photography from the 288-image library | — |
| `/buildings/` Register, all three views | all 72 rows from real data, numbers assigned, plate live, sort working, View Transitions on | Atlas SVG drawn for the West LA / Brentwood extent only; other areas fall back to a numbered list |
| 3 × building page | 004 Brockton Manor (full depth: gallery, amenities, map, office block), plus one Brentwood and one Palms/Motor Tides | 69 others generated from the same template, reachable, unphotographed beyond the four gallery images |
| 2 × neighbourhood page | West LA (27) and Palms (2) with real street lists, maps and building lists | copy marked `[CLIENT REVIEW]` inline |
| `/availability/` | real filter UI over the live dataset, URL-encoded state, compare tray, interest-list form | form posts nowhere |
| `/residents/` | five doors, real portal deep links, 24/7 emergency path | — |
| `/residents/deposits/` | full page structure, California 21-day timeline | body copy marked `[CLIENT COPY REQUIRED]` — do not write it for them |
| `/company/` | what we do, where, how the on-site model works | every number that isn't 72 or 7 marked `[CLIENT]` |
| `/company/building/` | real pipeline, sourced to Urbanize/TRD with citations visible | — |
| `/contact/` | intent routing, corporate address, **one** leasing number | form posts nowhere; the 31-number problem written up as a flagged note |

Everything the client has not confirmed renders as a visible `[CLIENT]` chip in the demo rather than as plausible-looking fiction. That is a feature in the review meeting, not a defect — it turns the presentation into a content-gathering session.

### Technical approach

Vanilla HTML / CSS / JS, no framework, no build step, no package manager — the house stack. Start from `option-e`, the only concept with externalised `style.css` (579 lines) and `app.js` (438 lines); a 72-page site cannot carry an inlined stylesheet per page. Keep the generic spine (Lenis setup, anchor interception, page-transition curtain, the two reveal observers, the accessible fullscreen menu with `inert` and focus return, the smart header, the section stepper, the single per-frame scroll handler) and delete the concept-specific halves (hero letter-splitter, chapter sweep, sliders, tours strip, plan preview, map interactions, experience rail, and the theme-switcher swatch control, which is a concept-review tool and must not ship).

Generate the 72 building pages and the 7 neighbourhood pages from `wiseman.json` with a small Python generator alongside `build_dataset.py`, writing static HTML — no runtime templating, no client-side data fetching for content that should be crawlable.

**Before the second page is written, put a `CONVENTIONS.md` at the root** with the trap list, every item of which cost a debugging session already:

- `overflow-x: clip` on `html` and `body`, **never** `hidden` — `hidden` creates a scroll container that silently kills `position: sticky`, and every pinned stage depends on it.
- `padding-top` / `padding-bottom` **longhand** on any element that also carries `.wrap`; shorthand zeroes the `var(--pad)` gutter and text runs to the viewport edge. Full-bleed sections use shorthand plus a nested `<div class="wrap">`.
- Every `vh` paired with an `@supports (height: 100svh)` twin via `--vh100`. The mask stage in `option-monogram` is the one place this is missing today — fix it in the port.
- Flex buttons: `flex: 1 1 auto; min-width: max-content`, never a pixel `min-width`.
- `overflow: hidden` line masks extended `.14em` with an equal negative margin, and the start offset pushed to 125%, or descenders clip.
- Two-token accents (`--x` decorative, `--x-ink` text-safe); body copy always on the AA neutral.
- Dark themes need an explicit ~15-rule hover sweep, not just a token flip.
- `.js` class gating in `<head>` so content is visible if scripts fail.
- `pageshow` + `e.persisted` reset on the transition curtain, and a modifier-key bail (`metaKey || ctrlKey || shiftKey || defaultPrevented`) on intercepted links — `option-e`'s version lacks it and swallows cmd-click.
- `absTop()` (offsetTop/offsetParent walk) for all scroll-spy and anchor maths, never `getBoundingClientRect().top + scrollY` — reveal transforms corrupt rects before reveal. Carry the deep-link correction with its `hashDone` wheel/touch guard; a 72-building site gets deep-linked heavily and its imagery shifts layout late.
- `data-sec="light|dark"` on every top-level section from day one. Retrofitting it across 70+ pages later is far more work than writing it as you go.
- Check the header at 375px on day one. It is the repo's most reliable regression.

**Motion:** one registered easing curve as the global default; every reveal `start: 'top 85%', once: true`, `stagger: { each: 0.06 }`; `clamp()` trigger syntax near document edges; hover animations gated behind `(hover: hover) and (pointer: fine)`; an explicit `prefers-reduced-motion` branch everywhere that keeps the composition and deletes only the choreography. GSAP 3.15 + ScrollTrigger + CustomEase + Lenis 1.3 is available and free including all former Club plugins, but the two signature devices here need neither — the mask is 35 lines of vanilla scroll maths and the tideline is one custom property.

**Platform gates, verified today:** same-document View Transitions are safe (Baseline 2025-10-14). `@property`, `color-mix()`, relative colors, masks, `:has()`, subgrid, container queries and `content-visibility` are all safe. **Scroll-driven animations are not** — Baseline limited with no Firefox implementation at all; any use must sit inside `@supports (animation-timeline: view())` with a fully-styled static fallback. Cross-document view transitions are enhancement only.

**Chat widget:** the existing `assets/chat.js` re-scripts as a portfolio concierge without touching the engine — roughly 600 of its 778 lines are unchanged. The work is adding one piece of conversation state (a selected building), a `flowFindHome()` that filters the 72 by neighbourhood / beds / budget through the existing `.mtc-card` renderer, and threading each building's own phone and RentCafe path in place of the single hardcoded constants. Add a neighbourhood branch to the router ladder ahead of the generic location match. ~150–200 lines.

**Deploy:** extend `scripts/prep_deploy.py` rather than replacing it — make `ROOT` repo-relative instead of the hardcoded absolute path, generalise the image `MAP` to read from the dataset (note the `image` column spans multiple s3 buckets while the current CDN template hardcodes `s3/2/9707`), and stamp `?v=` cache-bust params from a content hash instead of leaving them hand-maintained. Keep the `(` / `)` percent-encoding in the Vercel rewrite destinations and keep the post-build sanity grep. Regenerate `deploy/` before every push — it is gitignored. New Vercel projects must be created via the CLI; the MCP token can't create them.

**Before showing the client:** render the home page at 200px wide, black on white, beside Douglas Emmett, Essex, Kilroy and two LA competitors. If the Wiseman silhouette isn't immediately identifiable, the layout is structurally generic regardless of how good the photography is — and we rebuild the sequence, not the palette.