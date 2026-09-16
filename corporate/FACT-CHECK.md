# Fact check — what the new site may and may not claim

Compiled 10 September 2026 from a verified research sweep (sources in `RESEARCH-STREAMS.json`).
Read this before writing a single line of copy. Where a claim is flagged **[CLIENT]**, the demo
renders a visible chip rather than plausible-looking fiction.

---

## 1. Two claims on the client's current homepage that we could not verify

### "over 45 years"
The live site says *"Wiseman Residential has proudly served Los Angeles renters for over 45 years."*
Public sources do not support it, and the client's own archived pages contradict it:

| Source | Says |
|---|---|
| wisemanresidential.com, Wayback captures Feb 2014 · Aug 2018 · Feb 2025 · **7 Sep 2025** | "over **25** years of experience" |
| wisemanresidential.com, Wayback capture Nov 2023 | "over **30** years of experience" |
| wisemanresidential.com, capture Mar 2026 → today | "over **45** years" |
| Wiseman's own Archinect firm profile | "Established in **1985** by Isaac W. Cohanzad" |
| BBB profile, *Wiseman Development & Management, Inc.* | business start date **6/28/1987** |
| CSLB licence #417744, COBUILD INC, qualifier Isaac Wise Cohanzad | issued **02/03/1982** |

The figure jumped roughly twenty years between September 2025 and March 2026. **Ask the client to
confirm a founding year in writing.** Defensible alternatives in order of strength:

1. "Building and managing Los Angeles apartments since **1985**" — their own stated founding year.
2. "Licensed to build in California since **1982**" — anchored to the active CSLB licence.
3. Drop the number: "Four decades of Los Angeles apartments."

**How the demo handles it:** the site does not lead with a year. Where the client's own sentence is
quoted verbatim it is marked. Everywhere else the argument is made with checkable facts —
72 buildings, 7 areas, 52 streets, homes up to five bedrooms.

### "over 100+ apartment communities"
Their own RentCafe search returns **72**. The Real Deal counted "nearly 70" in June 2024 and
"around 30" in 2022; CBS News and a 2019 court filing say 35 buildings. Nothing supports 100+.

**How the demo handles it:** every count on the site is computed from the live feed
(`data/wiseman.json`), so it is right today and self-corrects. If the client wants a bigger number,
"1,000+ homes built" is the claim their own Archinect profile makes — still theirs to confirm.

---

## 2. Claims the site must not make

| Do not say | Why |
|---|---|
| A founding year as fact | 1982, 1985, 1987 and 1980 all appear in public sources; they cannot all be right |
| "Continuously family-owned since 19XX" | The brand spans at least four legal entities (Wiseman Development & Management Inc., Wiseman Management LLC, COBUILD INC, Copac Corp) |
| Any executive name or title except "founder Isaac Cohanzad" | No public source states a current title for anyone |
| "Licensed brokerage", "our licensed agents", a DRE number | Every principal's DRE licence is **expired**; no company DRE record exists. Confirm the responsible broker entity with the client before putting a licence number in the footer |
| AAGLA / CAA / NMHC / IREM membership, any award, any certification | No evidence for any of them |
| A BBB rating or badge | BBB lists the business as **not accredited** and "not rated" |
| A star rating or review count as a selling point | Google aggregates to **3.2 across 233 reviews** |
| "We preserve LA's character", "stewards of the neighbourhood", "restoring historic buildings" | The trade press reports the company has been criticised by preservation advocates for demolitions; the development model is teardown-and-rebuild |
| "Residents stay for generations", "a home for life", "we never displace anyone" | The Real Deal, citing the LA Times, reports evictions from rent-controlled properties; there is a published appellate opinion on Ellis Act / Airbnb class allegations against the principals |
| Any reference to litigation, including a rebuttal | Live litigation. Nothing about it belongs on a marketing site |
| "Motor Tides is in Culver City" | 3557 Motor Ave, 90034 is in the **City of Los Angeles (Palms)**, adjacent to Culver City. Say "minutes from Culver City" |
| A Motor Tides rent range | The only sourced figure mixes market-rate and deed-restricted units and goes stale fast |
| Unit counts, employee counts, dollars reinvested | Unverified |
| Any social follower count | Unverified, and the accounts are split across duplicate handles |

---

## 3. Fair housing — non-negotiable

- Copy describes **the apartment, never the household.** No "perfect for young professionals",
  "ideal for families", "great for roommates", "a quiet building for quiet people".
- No voucher-exclusion language anywhere, including in form dropdowns, income calculators or any
  chatbot pre-qualification logic. Source of income is a protected class under California FEHA.
- Neighbourhood copy stays on verifiable non-demographic facts: transit, distance, named
  businesses, parks, streets. Never on who lives there.
- Equal Housing Opportunity mark in every footer as a real element with
  `alt="Equal Housing Opportunity"`, no smaller than the Wiseman mark.
- Build to WCAG 2.1 AA in code. Do **not** install a third-party accessibility overlay widget —
  they measurably increase litigation risk.
- Audit the photo library in aggregate for representation across all 72 buildings, not shot by shot.

---

## 4. Facts that are verified and safe to use

- **Corporate office** 1520 Federal Ave, Los Angeles, CA 90025 · +1 310-473-3000 *(note: the address
  of record on CSLB, BBB and Archinect is still 11601 Santa Monica Blvd / (310) 914-5555 — a NAP
  consistency task for the client, not a copy problem)*
- **Portfolio today:** 72 buildings, 7 areas, 52 named streets — computed from their own feed.
- **Areas:** West Los Angeles · Sawtelle (27), Beverly Grove (14), Brentwood (13), Hollywood (13),
  Venice (2), Palms · Motor Avenue (2), Glendale (1).
- **Rare large homes.** The data shows apartments up to five bedrooms. Their own site has advertised
  "rare and highly coveted 3 and 4 bedroom floor plans" since at least 2014. This is real, checkable,
  and no Westside competitor matches it. 17 buildings offer four bedrooms or more; 5 go to five.
- **Motor Tides:** 3557 Motor Avenue, Los Angeles CA 90034; seven storeys; 104 apartments plus three
  ADUs (107 homes); architect Uriu & Associates; 1–4 bedrooms; rooftop deck; fitness centre; pet
  friendly; leasing (833) 521-3999; completing 2026. *(Urbanize LA, 12 May 2026.)*
- **Pipeline, sourced to trade press:** 68 apartments at 3659 S Motor Ave (built); 200 proposed at
  3418–3554 S Motor Ave with 22 units set aside for extremely-low-income households; 490 filed at
  9000–9020 Venice Blvd with 64 set aside; 119 at 11261 Santa Monica Blvd; 77 at 1600 E Venice Blvd;
  50 at 1808 Lincoln Blvd. Cite Urbanize LA / The Real Deal on the page.
- **Their own words**, quotable verbatim: "Los Angeles Living, Managed Wisely."; "As locals with
  deep roots in the city, we develop and manage apartments with your needs at the heart of
  everything we do."; "smart development, well-run properties, and communities people are proud to
  call home."; "Experience That Shows."
- **Brand colour** #1C6775 — **supplied by the client** on 15 September 2026, together with the
  logo file. It supersedes #169BAC, which an earlier pass had sampled from a low-resolution
  logo PNG and which was markedly brighter and greener than the real mark. The lockup is three
  tapered bars above a letterspaced "WISEMAN", both in the brand colour; the horizontal
  arrangement used in the site header is ours, the stacked one in the footer is theirs.

---

## 5. The operational truth the site should be built around

Across Google, Yelp and VeryApt the pattern is consistent and worth designing for:

- **What residents praise:** the named on-site manager, speed of repairs, large three- and
  four-bedroom floor plans, walkable Westside locations, pet friendliness.
- **What residents complain about:** the corporate office — specifically security-deposit refunds
  (multi-month delays) and roommate-turnover paperwork; and uneven maintenance responsiveness
  between buildings.

So: put the building's own office and phone on every building page, make the maintenance path
visible without a login, and answer the deposit question in plain English on its own page
(California requires an itemised statement within 21 days of move-out). That converts the one
genuine operational strength into the site's spine and pre-empts the single most repeated
objection. **The body copy of the deposits page is the client's to write — the demo ships the
structure with a `[CLIENT COPY]` chip.**
