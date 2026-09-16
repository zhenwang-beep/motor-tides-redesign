# -*- coding: utf-8 -*-
"""Concept A — GOLDEN HOUR.

The organising idea: Motor Midway's one unforgettable asset is a rooftop at
dusk, and there are ten frames of it. So the whole home page is edited as a
single evening. Photography is sequenced by the hour — daylight interiors,
afternoon patios, the roof at golden hour, the building lit after dark — and
the page's palette travels with it, cream paper warming into deep dusk.

A fixed rail on the left marks the hour you are currently reading in. It is
the only chrome the concept adds, and it is decorative: every chapter is a
normal section that reads correctly with CSS and JS both switched off.
"""
import data as D
import chrome as C

slug = "golden-hour"
name = "Golden Hour"
css = "golden.css"
number = "01"
tagline = "The property edited as a single evening, cream paper warming into dusk."
summary = ("Ten frames of the rooftop at golden hour are the best thing this property owns, so "
           "the page is sequenced by the clock — daylight interiors, afternoon patios, the roof "
           "at sunset, the building lit after dark — and the palette travels with it. A fixed "
           "hour rail marks where in the evening you are reading.")
poster = "dusk-05"

HOURS = [("4:40", "Daylight"), ("6:10", "Afternoon"),
         ("7:25", "Golden hour"), ("8:50", "Evening")]


def body_class(page):
    return "gh" + (" gh-home" if page == "index" else "")


def rail():
    items = "".join(
        f'<li data-hour="{i}"><span class="t">{t}</span><span class="l">{lbl}</span></li>'
        for i, (t, lbl) in enumerate(HOURS))
    return f'<div class="hour-rail" aria-hidden="true"><ol>{items}</ol></div>'


def phero(page, *, kick, title, lede):
    return f"""<section class="phero gh-phero">
  <div class="wrap">
    <p class="kick rv">{kick}</p>
    <h1 class="rv d1">{title}</h1>
    <p class="lede rv d1">{lede}</p>
  </div>
  <span class="gh-phero-glow" aria-hidden="true"></span>
</section>"""


def home():
    return f"""<main id="main">
{rail()}

<!-- ── The hour the property is famous for ─────────────────────────────── -->
<section class="gh-hero" data-hd="inv" data-chapter="0">
  <div class="gh-hero-media">
    {C.img('dusk-02', '', sizes='100vw', priority=True, cls='gh-hero-img')}
    <span class="gh-hero-scrim" aria-hidden="true"></span>
  </div>
  <div class="wrap gh-hero-copy">
    <p class="gh-eyebrow">{D.LOCALE} &middot; Now leasing</p>
    <h1 class="display gh-title"><span>Motor</span><span>Midway</span></h1>
    <p class="gh-sub">Two- and three-bedroom apartments at {D.ADDRESS_1},
      with a rooftop deck over the intersection.</p>
    <div class="actions gh-actions">
      <a class="btn" href="floorplans.html">Find your floor plan</a>
      <a class="btn outline" href="contact.html">Plan a visit</a>
    </div>
    <p class="gh-call">Leasing &middot; <a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a></p>
  </div>
  <span class="gh-scroll" aria-hidden="true"><i></i></span>
</section>

<!-- ── Manifesto ───────────────────────────────────────────────────────── -->
<section class="sec gh-mani" data-chapter="0">
  <div class="wrap">
    <p class="kick rv">Where the Westside crosses</p>
    <p class="gh-big rv d1">Motor Avenue runs at an angle to every street it meets.
      Midway is the building <em>at the crossing</em> &mdash; and the best room in it
      has no ceiling.</p>
    <p class="lede rv d1">Brand-new construction in Palms, on the Culver City line. Open-concept
      two- and three-bedroom residences with a washer and dryer in the unit, full-size kitchens
      with energy-efficient stainless appliances, central air and heat, and a private patio on
      every single one. Commercial space on the ground floor, so essential services are an
      elevator ride away.</p>
  </div>
</section>

<!-- ── 4:40 · Daylight ─────────────────────────────────────────────────── -->
<section class="sec gh-chapter" data-chapter="0" id="daylight">
  <div class="wrap">
    <header class="gh-head">
      <p class="kick rv">4:40 &middot; Daylight</p>
      <h2 class="section-title rv d1">Rooms that keep <em>the afternoon.</em></h2>
      <p class="lede rv d1">Open layouts, recessed lighting, vinyl flooring through the living
        space and the bedrooms, and a wall of glass onto the patio. 692 to 909 square feet.</p>
    </header>
    <div class="gh-grid">
      <figure class="fig rv g1">{C.img('u704-kdl-patio', 'Open-concept kitchen, dining and living room with patio', sizes='(max-width:900px) 100vw, 58vw')}<figcaption class="cap">Living &middot; Kitchen &middot; Patio</figcaption></figure>
      <figure class="fig rv d1 g2">{C.img('u709-kitchen', 'Open-concept kitchen with stainless-steel appliances', sizes='(max-width:900px) 100vw, 38vw')}<figcaption class="cap">Full-size kitchens</figcaption></figure>
      <figure class="fig rv d2 g3">{C.img('u17-bed-closet', 'Large bedroom with a mirrored closet, recessed lighting and vinyl flooring', sizes='(max-width:900px) 100vw, 38vw')}<figcaption class="cap">Mirrored closets</figcaption></figure>
      <figure class="fig rv d3 g4">{C.img('u702-bath', 'Bathroom with glass-door shower-bath and vanity cabinet storage', sizes='(max-width:900px) 100vw, 58vw')}<figcaption class="cap">A bath for every bedroom</figcaption></figure>
    </div>
    <div class="actions rv"><a class="btn outline" href="gallery.html">See all {D.GALLERY_COUNT} photographs</a></div>
  </div>
</section>

<!-- ── 6:10 · Afternoon ────────────────────────────────────────────────── -->
<section class="sec gh-chapter gh-warm" data-chapter="1" id="afternoon">
  <div class="wrap gh-split">
    <div class="gh-split-copy">
      <p class="kick rv">6:10 &middot; Afternoon</p>
      <h2 class="section-title rv d1">Every residence <em>opens.</em></h2>
      <p class="lede rv d1">Not a French balcony and not a fire escape &mdash; a patio with room
        for a sofa and a plant, off the living room or the bedroom, on every plan in the
        building. It is the reason the afternoons here are worth something.</p>
      <div class="actions rv d2"><a class="btn outline" href="floorplans.html">Compare the plans</a></div>
    </div>
    <figure class="fig rv d1">{C.img('u17-patio', 'A balcony with a couch and a plant, overlooking the city', sizes='(max-width:820px) 100vw, 46vw')}
      <figcaption class="fig-over">Private patio</figcaption></figure>
  </div>
</section>

<!-- ── 7:25 · Golden hour — the peak ───────────────────────────────────── -->
<section class="gh-peak" data-chapter="2" data-hd="inv" id="golden-hour">
  <div class="gh-peak-media">
    {C.img('dusk-07', 'Sunset from the rooftop deck', sizes='100vw', cls='gh-peak-img')}
    <span class="gh-peak-scrim" aria-hidden="true"></span>
  </div>
  <div class="wrap gh-peak-copy">
    <p class="kick rv plain">7:25 &middot; Golden hour</p>
    <h2 class="gh-peak-title rv d1">The roof is<br>the <em>best room.</em></h2>
    <p class="lede rv d1">An open deck above the intersection, pergola over the long tables,
      the city on every side of it. This is the hour it was built for.</p>
    <div class="actions rv d2">
      <a class="btn" href="amenities.html">See the amenities</a>
      <a class="btn outline" href="gallery.html">More of the roof</a>
    </div>
  </div>
</section>

<section class="sec gh-strip dark" data-chapter="2" data-hd="inv">
  <div class="gh-strip-rail">
    <figure class="fig rv">{C.img('dusk-01', 'Rooftop deck with entertainment area and pergola', sizes='40vw')}</figure>
    <figure class="fig rv d1">{C.img('dusk-09', 'Sunset views from the rooftop deck', sizes='40vw')}</figure>
    <figure class="fig rv d2">{C.img('dusk-10', 'Rooftop deck with entertainment area', sizes='40vw')}</figure>
    <figure class="fig rv d3">{C.img('roof-pergola', 'A rooftop patio with wooden floors and benches under a metal pergola', sizes='40vw')}</figure>
  </div>
</section>

<!-- ── Plans ───────────────────────────────────────────────────────────── -->
<section class="sec gh-plans dark" data-chapter="3" data-hd="inv" id="plans">
  <div class="wrap">
    <p class="kick rv">Find your fit</p>
    <h2 class="section-title rv d1">Four plans, four names<br>from <em>around here.</em></h2>
    <p class="lede rv d1">Dunn, Venice, Sony and Regent are streets and landmarks this building
      sits among. They are also its floor plans &mdash; two and three bedrooms, 692 to 909
      square feet, from ${min(p['price'] for p in D.PLANS):,} a month.</p>
    <ol class="gh-plan-index rv d2">
      {''.join(f'<li><a href="floorplans.html"><b>{p["name"]}</b>'
               f'<span>{p["beds"]} bd &middot; {p["baths"]} ba &middot; {p["sqft"]} sq ft</span>'
               f'<em>${p["price"]:,}</em></a></li>' for p in D.PLANS)}
    </ol>
    <div class="actions rv d2">
      <a class="btn" href="floorplans.html">View all floor plans</a>
      <a class="btn outline" href="{D.APPLY}" target="_blank" rel="noopener">Check availability</a>
    </div>
  </div>
</section>

<!-- ── 8:50 · Evening ──────────────────────────────────────────────────── -->
<section class="sec gh-chapter gh-night dark" data-chapter="3" data-hd="inv" id="evening">
  <div class="wrap gh-split reverse">
    <figure class="fig rv">{C.img('exterior-sign', 'The building on Motor Avenue, the address set on the frontage', sizes='(max-width:820px) 100vw, 46vw')}
      <figcaption class="fig-over">3657 Motor Avenue</figcaption></figure>
    <div class="gh-split-copy">
      <p class="kick rv">8:50 &middot; Evening</p>
      <h2 class="section-title rv d1">The rest of the evening<br>is <em>outside.</em></h2>
      <p class="lede rv d1">Downtown Culver City, three studio lots and a Metro stop are all
        inside a mile. Palms station on the E Line is the closest, four tenths of a mile up
        Motor Avenue; the 10 and the 405 are both a short drive; and the Ballona Creek Trail
        carries on west to the ocean.</p>
      <ul class="score-notes rv d2">
        {''.join(f'<li><b>{lbl}</b><span>{note}</span></li>' for _n, lbl, note in D.SCORES)}
      </ul>
      <div class="actions rv d2"><a class="btn outline" href="map.html">Open the map</a></div>
    </div>
  </div>
</section>

</main>"""
