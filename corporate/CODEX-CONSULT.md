**Wiseman should present itself as a collection of Los Angeles addresses, backed by one accountable owner.** The buildings supply the character. The company supplies continuity. Geography connects them.

I would ship **The Street Atlas**, the second direction below. Preserve the sensuality the client liked in Motor Tides through photography and restrained motion, while giving the parent company its own organizing idea.

**1. Diagnosis: the site wastes the advantage of owning a collection**

The strategic miss is that Wiseman presents its buildings as interchangeable inventory and its management experience as introductory copy. Those two things should reinforce each other: **find a particular place; understand who stands behind it.**

Five specific failures:

- **Geography is buried.** The search page puts Brentwood, Hollywood, Venice and West LA under “Specialty,” alongside Affordable and Student. Local knowledge becomes a miscellaneous database attribute. Geography should structure the entire collection. [Current search page](https://www.wisemanresidential.com/searchlisting)
- **The photography has no argument.** A sequence of attractive rooms demonstrates access to photographs. A named building, its street, its entrance and its courtyard establish a place someone can recognize and choose.
- **The company’s three roles are indistinct.** Owning, developing and managing explain why Wiseman has a continuing relationship with its buildings. Repeated assurances about experience do not show that relationship.
- **Motor Tides sets an unrepresentative expectation.** Give the flagship prominence, but frame it explicitly as the latest addition. Its scale and amenities cannot become the implied standard for the smaller buildings.
- **The site drops renters between inspiration and evaluation.** “Good living” leads into database controls. There is no intermediate layer explaining where the buildings are, what distinguishes them, or which alternatives deserve comparison.

Two content corrections precede design:

**Separate portfolio size from searchable inventory.** The homepage says “100+ apartment communities”; your working inventory contains 72 listings. Those counts describe different things until verified. Never animate either into a universal portfolio statistic. [Current homepage](https://www.wisemanresidential.com/)

**Separate building characteristics from available apartments.** A building-wide studio–five-bedroom range and a displayed rent do not establish an available studio at that rent. The present listing format makes that distinction unclear. A new interface must make it explicit. [Current listing format](https://www.wisemanresidential.com/searchlisting)

Keep **“Los Angeles Living, Managed Wisely.”** It connects place and operational competence. Replace the long welcome passage with a concise statement:

> Family-run apartment owners, developers and managers. Rooted in Los Angeles for over 45 years.

Luxury should come from attention, proportion and specificity. Applying resort language to every building will undermine trust.

**2. The collection problem: two different browsing systems**

Curation requires **an intelligible order, visible distinctions and a reason to look closer**. It does not require hiding most of the portfolio.

Both systems need two immediate entry points: **Choose an area** and **Set your budget**. Neither requires finishing the homepage animation.

**A. The Neighborhood Atlas — spatial browsing**

Best for renters choosing between locations.

**Opening state**

On desktop, use a roughly 55/45 split: a geographic overview on the left, six named area rows on the right. Show the actual distribution of buildings and a count for each area. Do not begin with 72 overlapping pins.

Use your six groups as browsing regions, not as assertions about neighborhood boundaries. “Beverly Grove / Hollywood” is a collection region; individual addresses still need precise neighborhood labels. “Culver City corridor” must not silently become “City of Culver City.”

**Interaction**

1. Clicking an area fits the map to its buildings and opens that area’s editorial introduction.
2. Show one representative building prominently, then a complete, ordered list. State why the lead building is featured; “Newest addition” is meaningful, “Featured” alone is not.
3. Each listing contains a real exterior, full name, address, bedroom information, price/status and save control.
4. Hovering or focusing a listing highlights its map marker. Selecting a marker reveals the corresponding listing without unexpectedly scrolling the whole page.
5. Opening a property and returning restores the area, filters and list position.

**Budget-first entry**

A maximum-rent field and bedroom selector update the six area counts before the user chooses a region. Keep zero-match regions visible and labeled. Never quietly widen the budget.

With only aggregate building data, label results as **buildings to check**, not confirmed available apartments. Exact bedroom-plus-budget matching requires apartment-level availability.

**Vanilla implementation**

One property dataset, one filter-state object, one selected property ID. Map and list derive from the same filtered IDs. Store area, budget, bedrooms and view in the URL.

A lightweight SVG overview can use real geographic coordinates; load the detailed map only when requested. Close markers must expand or cluster at detail scale. On mobile, default to the list with an explicit Map toggle.

**Why it feels authored:** Wiseman’s distribution becomes legible. Twenty-five West LA buildings communicate depth in a place instead of twenty-five more search results.

**B. The Street Index — typographic browsing**

Best for discovering individual buildings and returning to a remembered address.

**Opening state**

A large photographic panel occupies the left half of the desktop viewport. The right half contains a neighborhood chapter and a compact list of streets:

> Armacost Avenue  
> Brockton Avenue  
> Colby Avenue  
> Purdue Avenue

Each street expands into its actual buildings. The photography changes with the selected building; the address and practical facts remain attached to it.

**Interaction**

1. Select a neighborhood from a persistent chapter rail.
2. Expand a street to reveal all its buildings.
3. Hover or keyboard-focus a building to preview its photograph. Click its name to open its page.
4. Save buildings into a persistent shortlist. Compare up to three across the same fields: location, available bedroom types, current rent, square footage and verified practical features.
5. A separate name/address search finds buildings directly, without knowing their chapter.

Organize streets by **verified address**, not poetic property name. The names are memorable, but they are not reliable geocodes.

Budget filtering leaves the chapter-and-street hierarchy intact, hiding nonmatching buildings and updating counts. Provide “Price: low to high” as a plain alternative view.

**Vanilla implementation**

Use native `<details>` elements for street groups, ordinary property links and a sticky image stage with two overlapping `<img>` elements. Crossfade previews over approximately 180 milliseconds; preload only the next likely images. No hover-dependent access to information.

On mobile, use compact rows with visible thumbnails. The oversized sticky photograph disappears. Store shortlist IDs locally; no account wall.

**Why it feels authored:** the names become the interface. Small buildings acquire individual presence without forcing the renter through 72 full-screen presentations.

Useful precedents: [The Modern House](https://themodernhouse.com/) places editorial attention beside explicit property facts; [The Landmark Trust](https://www.landmarktrust.org.uk/) offers location, building character and an A–Z directory as parallel ways into a collection. Borrow those principles, not their visual identities.

**3. Three site directions**

**Direction A — Pacific Light**

*One-line idea:* Los Angeles living, connected by light.

*Organizing metaphor:* A photographic journey from open sky into the places people live.

This carries the water lineage through pacing, luminous photography and a continuous horizon. It does not turn every Wiseman building into a coastal property.

| Role | Specification |
|---|---|
| Background | Bone `#F2F0E9` |
| Primary text | Deep pine `#173D37` |
| Secondary surface | Pale mineral `#DCE7E3` |
| Brand accent | Wiseman teal `#169BAC` |
| Secondary text | Slate `#52635F` |
| Google Fonts | **Bodoni Moda**, 500/600 for display; **Manrope**, 400/500/600 for text and controls |

Use teal sparingly. Keep body copy and control labels in dark ink.

**Signature scroll: the horizon handoff**

A desktop section is `220svh` tall, containing a sticky `100svh` photographic stage. Start with a real rooftop or terrace image. Use two additional actual-property photographs selected for compatible horizon placement.

Calculate local progress as:

`p = clamp(-sectionTop / (sectionHeight - viewportHeight), 0, 1)`

Across three intervals, replace the photograph through a **straight horizontal clipped reveal**. Incoming images translate vertically by no more than 4%; outgoing images remain still. Names and addresses change with the image.

The effect is a tide-like rise and release, achieved entirely with photographs. No rippling pixels, wave outlines, masked typography or fabricated moving water.

The sequence releases into the Neighborhood Atlas. Mobile uses three normal image blocks. Reduced-motion mode removes pinning and translation.

**Homepage sequence**

Brand and immediate apartment search → horizon sequence → six-area atlas → three named buildings with distinct character → Motor Tides as the newest addition → owner/developer/manager statement → resident access and corporate contact.

**Risk**

It can become a boutique-hotel advertisement. Control that by naming every property image and keeping search visible from the first screen. The available photography must support the sequence; unrelated atmospheric images are not a substitute.

---

**Direction B — The Street Atlas**

*One-line idea:* Find your place in the Los Angeles Wiseman knows.

*Organizing metaphor:* A contemporary city atlas organized into areas, streets and addresses.

This makes the actual shape of the business the brand expression.

| Role | Specification |
|---|---|
| Background | Chalk `#F4F2EB` |
| Primary text | Asphalt `#252B2A` |
| Secondary surface | Pale teal `#DCEBEC` |
| Brand accent | Wiseman teal `#169BAC` |
| Rules and boundaries | Stone `#C8CEC8` |
| Secondary text | Gray-green `#58645F` |
| Google Fonts | **DM Serif Display**, 400 for chapter titles; **DM Sans**, 400/500/600 for navigation, facts and body |

Keep the existing logo intact. Set street names generously, but retain compact, highly readable listing facts.

**Signature scroll: the address register**

The homepage contains a desktop introduction with three editorial beats, each about `65svh` tall, beside a sticky photograph and small geographic locator.

As a beat crosses a fixed activation line around 45% of the viewport:

- Its street name becomes active.
- The corresponding real-property photograph crossfades over 220 milliseconds.
- The locator highlights that building’s actual position.
- Its neighborhood, address and property link update together.

Use three selected buildings from different areas. Clearly label the group “Selected addresses”; it is an introduction to the collection, not a purported trip between adjacent streets.

Implement activation using measured section positions or `IntersectionObserver`, with click and keyboard selection available independently. Do not scroll-jack. The full six-area browser follows immediately.

**Homepage sequence**

“Los Angeles Living, Managed Wisely” with area/budget controls → three-address register → full collection browser → brief statement of ownership, development and management → Motor Tides → resident utility strip → contact/footer.

The neighborhood pages use the Street Index. An optional map supplies geographic comparison.

**Risk**

It can become an architectural directory with little warmth. Counter that with inhabited spaces, planting, daylight and tactile building details. Do not add cartographic decoration to compensate for weak photographs.

**This is the direction I would ship.**

It turns the hardest problem—many small buildings—into the distinctive feature. It gives street names a useful role, supports both renter entry paths and works with uneven photography. It also lets Motor Tides retain its stronger individual personality.

---

**Direction C — Places That Last**

*One-line idea:* Distinct buildings, with a continuing owner behind them.

*Organizing metaphor:* A working architectural record: what Wiseman creates, owns and looks after.

This is the strongest corporate positioning. The other directions lead with discovery; this one leads with stewardship.

| Role | Specification |
|---|---|
| Background | Plaster `#EEE9DF` |
| Primary text | Brown-black `#302E29` |
| Secondary surface | Limestone `#D9D1C4` |
| Brand accent | Wiseman teal `#169BAC` |
| Editorial accent | Terracotta `#A45B43` |
| Secondary text | Warm gray `#635F56` |
| Google Fonts | **Marcellus**, 400 for display; **Source Sans 3**, 400/500/600 for body and controls |

Avoid sepia grading, ornamental borders and fabricated archival material. Forty-five years of operation does not require a nostalgia costume.

**Signature scroll: three scales of a place**

Use one well-documented property with three real images: street-facing exterior, entrance/shared space, interior.

Inside a `200svh` section, a sticky editorial spread contains three overlapping rectangular image layers. During the first half of progress, the exterior slides left inside the fixed frame, revealing the entrance. During the second half, the entrance slides right, revealing the interior.

Captions connect each view to documented decisions or visible features. No simulated floor plans, exploded building diagrams or unsupported claims about maintenance.

The mechanism changes the viewer’s scale of attention: street → building → home. Use ordinary transforms and overflow clipping. Mobile presents the three photographs in sequence.

**Homepage sequence**

Search and a concise ownership proposition → three-scale property study → browse the collection → owning/developing/managing explained separately → Motor Tides development profile → resident services → corporate contact.

**Risk**

The evidence burden is highest. The current asset set supports photographic observation, but not a detailed account of development decisions or management performance. Without verified project facts, this becomes expensive-looking corporate prose. That makes it the wrong first release.

**4. Information architecture: build the corporate layer the portfolio needs**

Primary navigation:

**Find an Apartment · Neighborhoods · About Wiseman · Residents**

Keep **Applicant Login** and **Contact** in utility navigation. A global “Apply Now” button is wrong when the user has not selected a property.

| Page | Purpose |
|---|---|
| `/` | Establish the company and provide immediate area/budget entry. |
| `/apartments` | Complete searchable collection; list/map views; visible active filters and result counts. |
| `/neighborhoods` | Six browsing regions with their geographic relationship explained. |
| `/neighborhoods/{area}` | Short local introduction, accurate map, street index and complete relevant collection. |
| `/apartments/{property}` | Corporate property profile: actual photographs, name, address, distinguishing details, practical facts and direct leasing handoff. |
| `/saved` | Persistent shortlist and comparison across buildings. No registration required. |
| `/about` | Family-run ownership, 45+ years, and the relationship between owning, developing and managing. |
| `/development` | Verified development work, beginning with Motor Tides. No invented pipeline or project history. |
| `/residents` | Resident portal, maintenance routing, management contact and published emergency instructions. |
| `/leasing` | General leasing process and FAQs; property-specific terms remain with the relevant property. |
| `/contact` | Separate prospective-renter, resident and corporate routes. Show the Federal Avenue office and corporate phone. |
| Utility pages | Privacy, accessibility and applicable housing disclosures using approved content. |

Do not launch thin neighborhood subpages purely for search traffic. Start with six substantive regional pages; split further when both inventory and useful local content justify it.

**Corporate site owns discovery and comparison.**

It should explain the collection, preserve the shortlist, establish Wiseman’s identity and show alternatives when a building has no matching apartment.

**RentCafe property subdomains own the transaction.**

They remain authoritative for unit availability, floor plans, lease-term pricing, fees, applications, tour booking where configured, and resident/applicant accounts.

A corporate property page needs a specific handoff:

> View floor plans & availability at Brockton Manor

Link directly to the relevant destination, not another generic property homepage. Preserve the corporate browse state when the renter returns.

Keep corporate profiles editorial and comparative; keep subdomain pages operational. Copying the same long description across both creates duplicate maintenance and a confusing experience.

**The data contract determines what the design can promise.**

Maintain one record per building with a stable ID, actual address, coordinates, browsing region, official name, image provenance, leasing phone and destination URLs. Separate:

- Building facts.
- Apartment-level availability and pricing.
- Editorial descriptions and selection order.

The existing price and bedroom ranges support an initial catalogue. They do not establish exact available-unit matches. Obtain a supported feed before promising those matches; otherwise show clearly dated building-level information and “Check availability.”

Vanilla HTML/CSS/JS is sufficient. Generate real, linkable HTML pages from shared data; do not maintain 72 hand-copied pages. Keep any feed credentials off the client.

**5. Traps: what to refuse**

- **The luxury starter kit:** cream background, giant serif, “Elevated living,” three amenity icons and rounded cards. No amount of whitespace makes that specific to Wiseman.
- **Ocean footage as universal property evidence.** It suggests a coastal experience the portfolio does not consistently provide.
- **Literal waves, facade illustrations and another photograph-filled wordmark.** The client has already supplied the answer.
- **An obligatory cinematic entrance.** Search, resident access and direct links must work immediately.
- **A 72-slide carousel or forced horizontal journey.** That is inventory with worse navigation.
- **A map with 72 undifferentiated pins.** Regional aggregation must precede individual markers.
- **A fullscreen card for every building.** Reserve editorial scale for introductions. Keep evaluation compact.
- **Identical “luxury” descriptions.** Write one specific, verifiable sentence about each building. When the evidence is limited, say less.
- **AI-enhanced property photography that changes the building.** No invented landscaping, removed neighboring buildings, expanded views or amenities.
- **Invented founding dates, founder stories, team portraits, awards or unit totals.** “45+ years” is sufficient.
- **Price bait caused by aggregate data.** A building containing studios does not mean its displayed minimum rent buys an available studio.
- **An empty Journal or third-party management sales page.** Neither follows from the supplied business or content.
- **Animation on every component.** One signature sequence, simple transitions elsewhere. Lenis stays restrained; touch scrolling stays native; reduced-motion mode remains complete.
- **Typography that sacrifices utility.** Use display faces for names and statements. Prices, addresses, filters and phone numbers need immediate legibility.

Judge the design by a concrete task: **can someone find three plausible buildings, understand their differences and reach the correct leasing destination without losing their place?** That is where the art direction earns its keep.
