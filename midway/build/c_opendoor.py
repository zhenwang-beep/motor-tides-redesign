# -*- coding: utf-8 -*-
"""Concept C — OPEN DOOR.

The organising idea comes from the amenity list: *Patio / Balcony* is on every
residence, not a subset. In a 692-square-foot two-bedroom, the patio is not a
feature — it is the extra room, and it is what living here actually feels like.

So the page is built on the threshold. Its recurring device is a diptych: the
room on the left, what the room opens onto on the right, a hairline between
them that widens as the pair enters the viewport. Warm, domestic, human scale
— deliberately less monumental than Tides, because Midway is the smaller and
more intimate building and pretending otherwise would be the wrong sell.
"""
import data as D
import chrome as C

slug = "open-door"
name = "Open Door"
css = "opendoor.css"
number = "03"
tagline = "Built on the threshold — every residence here opens onto its own patio."
summary = ("Patio/Balcony is on every residence, not a subset — in a 692-square-foot two-bedroom "
           "that patio is the extra room. This direction is built on the threshold: paired "
           "photographs of the room and what the room opens onto, a hairline between them that "
           "widens as you scroll. Domestic and human-scale rather than monumental.")
poster = "u17-patio"

# Each diptych: (inside slug, inside alt, inside label,
#                outside slug, outside alt, outside label, caption)
PAIRS = [
    ("u704-kdl-patio", "Open-concept kitchen, dining and living room with patio", "The living room",
     "u17-patio", "A balcony with a couch and a plant, overlooking the city", "opens onto the patio",
     "Room for a sofa and a plant, on every plan in the building."),
    ("u703-bed-curtains", "Large bedroom with vinyl flooring, recessed lighting and patio", "The bedroom",
     "u703-patio", "Large patio", "opens onto its own",
     "Several plans put a second door on the bedroom side."),
    ("u708-kitchen", "Kitchen and dining space", "The kitchen",
     "u708-lr-patio", "Dining and living room with in-suite washer and dryer and patio", "opens onto the room",
     "Full-size, stainless, energy-efficient, and open to where everyone is."),
]


def body_class(page):
    return "od" + (" od-home" if page == "index" else "")


def _pair(i, ins, ins_alt, ins_lbl, out, out_alt, out_lbl, note):
    return f"""
  <div class="od-pair rv" data-pair="{i}">
    <figure class="od-in">
      <div class="fig">{C.img(ins, ins_alt, sizes='(max-width:820px) 100vw, 48vw')}</div>
      <figcaption class="cap">{ins_lbl}</figcaption>
    </figure>
    <span class="od-thresh" aria-hidden="true"></span>
    <figure class="od-out">
      <div class="fig">{C.img(out, out_alt, sizes='(max-width:820px) 100vw, 48vw')}</div>
      <figcaption class="cap">{out_lbl}</figcaption>
    </figure>
    <p class="od-pair-note">{note}</p>
  </div>"""


def phero(page, *, kick, title, lede):
    return f"""<section class="phero od-phero">
  <div class="wrap">
    <p class="kick rv">{kick}</p>
    <h1 class="rv d1">{title}</h1>
    <p class="lede rv d1">{lede}</p>
  </div>
</section>"""


def home():
    pairs = "".join(_pair(i, *p) for i, p in enumerate(PAIRS))

    return f"""<main id="main">

<!-- ── Threshold hero ──────────────────────────────────────────────────────
     The hero IS the concept rather than type floating over a photograph:
     the room on the left, what it opens onto on the right, the threshold
     drawn between them. It also solves a real problem — Midway's interiors
     are bright and white-walled, and light type over them needs a scrim so
     heavy it erases the photograph. Here nothing sits on the image at all. -->
<section class="od-hero">
  <div class="od-hero-inside">
    <p class="od-eyebrow">{D.LOCALE} &middot; Now leasing</p>
    <h1 class="od-title">Every home here<br><em>opens.</em></h1>
    <p class="od-sub">Two- and three-bedroom apartments at {D.ADDRESS_1}, each one with its own
      private patio &mdash; and a rooftop deck above them all.</p>
    <div class="actions">
      <a class="btn" href="floorplans.html">Find your floor plan</a>
      <a class="btn outline" href="contact.html">Plan a visit</a>
    </div>
    <p class="od-call">Leasing &middot; <a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a></p>
  </div>
  <span class="od-hero-thresh" aria-hidden="true"></span>
  <figure class="od-hero-outside">
    {C.img('u17-patio', 'A Motor Midway balcony with a sofa and a plant, looking out over the city',
           sizes='(max-width:900px) 100vw, 52vw', priority=True, cls='od-hero-img')}
    <figcaption>The patio &middot; every residence has one</figcaption>
  </figure>
</section>

<!-- ── Manifesto ───────────────────────────────────────────────────────── -->
<section class="sec od-mani">
  <div class="wrap">
    <p class="kick rv">The extra room</p>
    <p class="od-big rv d1">In a 692-square-foot two-bedroom, the patio is not a feature.
      It is <em>the room you actually live in</em> nine months of the year.</p>
    <p class="lede rv d1">Brand-new construction in Palms, on the Culver City line. Two and
      three bedrooms, 692 to 909 square feet &mdash; and <em>Patio / Balcony</em> on every
      plan in the building, not on a lucky few.</p>
  </div>
</section>

<!-- ── The diptychs ────────────────────────────────────────────────────── -->
<section class="sec-tight od-pairs">
  <div class="wrap">{pairs}</div>
</section>

<!-- ── The shared one ──────────────────────────────────────────────────── -->
<section class="od-shared dark" data-hd="inv" id="rooftop">
  <div class="od-shared-media">
    {C.img('dusk-05', 'Entertainment area with pergola and sunset views from the rooftop deck', sizes='100vw', cls='od-shared-img')}
    <span class="od-shared-scrim" aria-hidden="true"></span>
  </div>
  <div class="wrap od-shared-copy">
    <p class="kick rv plain">And one everybody shares</p>
    <h2 class="od-shared-title rv d1">The roof.</h2>
    <p class="lede rv d1">An open deck above the intersection with a pergola over the long
      tables and the city on every side. The patio you do not have to keep tidy.</p>
    <div class="actions rv d2">
      <a class="btn" href="amenities.html">See the amenities</a>
      <a class="btn outline" href="gallery.html">More of the roof</a>
    </div>
  </div>
</section>

<!-- ── Plans ───────────────────────────────────────────────────────────── -->
<section class="sec od-plans" id="plans">
  <div class="wrap">
    <p class="kick rv">Find your fit</p>
    <h2 class="section-title rv d1">Four plans. <em>Four doors.</em></h2>
    <p class="lede rv d1">Dunn, Venice, Sony and Regent &mdash; named for the streets and
      landmarks around the building. Two and three bedrooms, 692 to 909 square feet, and a
      patio on all four.</p>
    <div class="od-plan-cards rv d2">
      {''.join(f'''
      <a class="od-plan-card" href="floorplans.html">
        <span class="od-pc-top"><b>{p['name']}</b><i>{p['avail']} available</i></span>
        <span class="od-pc-fig">{C.img(p['img'], f"{p['name']} floor plan", sizes='(max-width:700px) 90vw, 24vw')}</span>
        <span class="od-pc-spec">{p['beds']} bed &middot; {p['baths']} bath &middot; {p['sqft']} sq ft</span>
        <span class="od-pc-price">From ${p['price']:,}<small>/ month</small></span>
      </a>''' for p in D.PLANS)}
    </div>
    <div class="actions rv">
      <a class="btn" href="{D.APPLY}" target="_blank" rel="noopener">Check availability</a>
      <a class="btn outline" href="floorplans.html">Compare all four</a>
    </div>
    <p class="fine od-util">{D.PLAN_SPECIALS} &middot; {D.PLAN_DEPOSIT} &middot; {D.UTILITIES_NOTE}</p>
  </div>
</section>

<!-- ── Amenities ───────────────────────────────────────────────────────── -->
<section class="sec od-amen">
  <div class="wrap od-amen-grid">
    <div>
      <p class="kick rv">Downstairs</p>
      <h2 class="section-title rv d1">What is <em>under</em> the roof.</h2>
      <ul class="od-amen-list rv d1">
        {''.join(f'<li>{n}</li>' for n, _b in D.COMMUNITY_AMENITIES)}
      </ul>
      <div class="actions rv d2"><a class="btn outline" href="amenities.html">All the amenities</a></div>
    </div>
    <div class="od-amen-figs">
      <figure class="fig rv d1">{C.img('gym-5', 'Well-equipped fitness center with medicine balls, free weights and treadmills', sizes='(max-width:900px) 50vw, 26vw')}</figure>
      <figure class="fig rv d2">{C.img('corridor', 'A corridor with wood panelling and the elevator', sizes='(max-width:900px) 50vw, 26vw')}</figure>
    </div>
  </div>
</section>

<!-- ── Outside the door ────────────────────────────────────────────────── -->
<section class="sec od-place dark" data-hd="inv">
  <div class="wrap">
    <p class="kick rv">Outside the front one</p>
    <h2 class="section-title rv d1">What is <em>within reach.</em></h2>
    <p class="lede rv d1">Downtown Culver City, two studio lots and Apple TV+&rsquo;s campus and a Metro stop are all
      inside a mile of the front door. Palms station on the E Line is the closest of them,
      and the Ballona Creek Trail carries on west to the ocean.</p>
    <div class="stats">
      {''.join(f"<div class='rv'><b>{n}</b><span>{lbl}</span><p>{note}</p></div>" for n, lbl, note in D.SCORES)}
    </div>
    <div class="actions rv d2"><a class="btn outline" href="map.html">Open the map</a></div>
  </div>
</section>

</main>"""
