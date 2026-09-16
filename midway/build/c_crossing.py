# -*- coding: utf-8 -*-
"""Concept B — THE CROSSING.

The organising idea is a fact about the site: Motor Avenue runs at an angle to
the Los Angeles street grid, and 3657 sits where it cuts across. That diagonal
is the concept. It appears as a drawn street plan, as the rule-work between
sections, and as the reason the Walk 89 number is what it is.

The register is architectural — a drawing set rather than a brochure. Mono
annotations carry the measured facts (square feet, distances, floors); the
serif carries the names. Nothing decorative claims anything the property has
not published.
"""
import data as D
import chrome as C
import pages as P

slug = "crossing"
name = "The Crossing"
css = "crossing.css"
number = "02"
tagline = "A drawing set. Motor Avenue's diagonal as the organising line."
summary = ("Motor Avenue runs at an angle to every street it meets, and 3657 is the building at "
           "the crossing. This direction treats the site like an architect's drawing set — a "
           "drawn street plan, mono annotations carrying the measured facts, and the building "
           "read floor by floor from the roof down to the garage.")
poster = "exterior-sign"

# The building read top down. Only facts the property publishes.
#
# The marker used to be the floor letter set beside the floor name, so the row
# read "ROOF / ROOF" — the same word twice. It is an icon now, and the floor
# range lives in the description where it is useful.
_ICON = {
 "roof": '<circle cx="18.6" cy="5.2" r="2.3"/><path d="M3 10.4h18"/>'
         '<path d="M6.5 10.4V7.6M10.5 10.4V7.6M14.5 10.4V7.6"/>'
         '<path d="M4.5 20h15"/><path d="M6.5 20v-9.6M17.5 20v-9.6"/>',
 "res":  '<rect x="4.2" y="3.2" width="15.6" height="17.6" rx="1.2"/>'
         '<path d="M8 7.4h3M13 7.4h3M8 11.4h3M13 11.4h3M8 15.4h3M13 15.4h3"/>',
 "ground": '<path d="M3 9.2h18"/><path d="M3 9.2 5 5h14l2 4.2"/>'
           '<path d="M5.2 9.2V20h13.6V9.2"/><path d="M9.4 20v-5.6h5.2V20"/>',
 "garage": '<path d="M4 15.8l1.7-5.3A2.1 2.1 0 0 1 7.7 9h8.6a2.1 2.1 0 0 1 2 1.5l1.7 5.3"/>'
           '<path d="M4 15.8h16"/><path d="M5.8 15.8v2.4M18.2 15.8v2.4"/>'
           '<circle cx="7.9" cy="15.8" r="1.3"/><circle cx="16.1" cy="15.8" r="1.3"/>',
}

STACK = [
    ("roof",   "Roof",       "Rooftop deck, pergola, the city on every side", "amenities.html"),
    ("res",    "Residences", "Floors 2&ndash;7. Two- and three-bedroom homes, 692&ndash;909 sq ft, a patio "
                             "on every one &mdash; behind a controlled door, with an elevator and "
                             "on-site management", "floorplans.html"),
    ("ground", "Ground",     "Commercial space &mdash; essential services an elevator ride away", "map.html"),
    ("garage", "Garage",     "Resident parking, bike racks, recycling", "amenities.html"),
]


def body_class(page):
    return "cr" + (" cr-home" if page == "index" else "")


def phero(page, *, kick, title, lede):
    sheet = {"floorplans": "A-201", "amenities": "A-301", "gallery": "A-401",
             "tours": "A-402", "map": "A-101", "contact": "A-001"}.get(page, "A-000")
    return f"""<section class="phero cr-phero">
  <div class="wrap">
    <div class="cr-sheet"><span>Sheet</span><b>{sheet}</b></div>
    <p class="kick rv">{kick}</p>
    <h1 class="rv d1">{title}</h1>
    <p class="lede rv d1">{lede}</p>
  </div>
</section>"""


def home():
    stack = "".join(f"""
      <li class="rv">
        <a href="{href}">
          <span class="lvl" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="1.25" stroke-linecap="round"
            stroke-linejoin="round">{_ICON[icon]}</svg></span>
          <span class="nm">{nm}</span>
          <span class="ds">{ds}</span>
        </a>
      </li>""" for icon, nm, ds, href in STACK)

    plans = "".join(f"""
      <tr class="rv">
        <th scope="row">{p['name']}</th>
        <td>{p['beds']} bd / {p['baths']} ba</td>
        <td>{p['sqft']} sq ft</td>
        <td>${p['price']:,}</td>
        <td>{p['avail']} avail.</td>
        <td class="t-act"><a class="tlink" href="floorplans.html">Plan</a></td>
      </tr>""" for p in D.PLANS)

    return f"""<main id="main">

<!-- ── Title block ─────────────────────────────────────────────────────── -->
<section class="cr-hero" data-hd="inv">
  <div class="cr-hero-media">
    {C.img('exterior-street-1', '', sizes='100vw', priority=True, cls='cr-hero-img')}
    <span class="cr-hero-scrim" aria-hidden="true"></span>
    <span class="cr-hero-rule" aria-hidden="true"></span>
  </div>
  <div class="wrap cr-hero-copy">
    <div class="cr-titleblock">
      <div><span>Project</span><b>Motor Midway</b></div>
      <div><span>Operator</span><b>Wiseman Residential</b></div>
      <div><span>Location</span><b>Palms, Los Angeles</b></div>
      <div><span>Status</span><b>Now leasing</b></div>
    </div>
    <h1 class="cr-title"><span>Motor</span><span class="i">Midway</span></h1>
    <p class="cr-addr"><b>{D.ADDRESS_1}</b> &middot; {D.ADDRESS_2}</p>
    <div class="actions">
      <a class="btn" href="floorplans.html">View the plans</a>
      <a class="btn outline" href="contact.html">Plan a visit</a>
    </div>
  </div>
  <p class="cr-hero-note" aria-hidden="true">{abs(D.HOME[0]):.4f}&deg;N &nbsp;{abs(D.HOME[1]):.4f}&deg;W</p>
</section>

<!-- ── The line ────────────────────────────────────────────────────────── -->
<section class="sec cr-thesis">
  <div class="wrap">
    <p class="kick rv">The organising line</p>
    <h2 class="cr-big rv d1">Motor Avenue runs at an angle to every street it meets.
      Midway is the building <em>at the crossing.</em></h2>
    <p class="lede rv d1">That angle is why the Walk Score is 89 and the Bike Score is 82.
      A diagonal meets more of the grid than a straight line does, so more is close in more
      directions &mdash; downtown Culver City, three studio lots, the E Line, the Ballona
      Creek Trail, and on-ramps for both the 10 and the 405.</p>
  </div>
</section>

<!-- ── Site plan ───────────────────────────────────────────────────────────
     This was a schematic drawing of the street grid. A real basemap makes the
     same argument better: the diagonal is not a graphic device here, it is
     what Motor Avenue actually does, and a survey-accurate map proves it
     where a diagram only asserts it. The frame and the sheet annotation stay,
     so it still reads as a drawing set. -->
<section class="sec cr-site dark" data-hd="inv" id="site">
  <div class="wrap">
    <div class="cr-site-head">
      <div>
        <p class="kick rv">Site plan</p>
        <h2 class="section-title rv d1">Where it <em>sits.</em></h2>
      </div>
      <p class="lede rv d1">On the east side of Motor, in Palms. The four floor plans are
        named for what surrounds it &mdash; Dunn Drive one street over, Venice Boulevard
        north, Sony Pictures half a mile south, Regent Street at the end of the block.
        Motor Avenue is the line running corner to corner.</p>
    </div>
    {P.map_block(note_prefix="Sheet A-101 &middot; ")}
  </div>
</section>

<!-- ── Section through the building ────────────────────────────────────── -->
<section class="sec cr-stack" id="stack">
  <div class="wrap">
    <p class="kick rv">Section</p>
    <h2 class="section-title rv d1">Read it from the <em>roof down.</em></h2>
    <div class="cr-stack-grid">
      <ol class="cr-levels">{stack}</ol>
      <figure class="fig rv d1 cr-stack-fig">{C.img('dusk-06', 'Rooftop deck with entertainment area', sizes='(max-width:900px) 100vw, 44vw')}
        <figcaption class="fig-over">Roof &middot; Deck</figcaption></figure>
    </div>
  </div>
</section>

<!-- ── Residences ──────────────────────────────────────────────────────── -->
<section class="sec cr-res">
  <div class="wrap">
    <p class="kick rv">Residences</p>
    <h2 class="section-title rv d1">Squared to <em>the street.</em></h2>
    <p class="lede rv d1">Open-concept two- and three-bedroom homes with a bathroom for every
      bedroom, a washer and dryer in the unit, full-size kitchens with energy-efficient
      stainless appliances, central heating and air, vinyl flooring, mirrored closets and a
      private patio on every plan.</p>
    <div class="cr-res-grid">
      <figure class="fig rv">{C.img('u703-kdl-patio', 'Open-concept kitchen, dining, living room and patio', sizes='(max-width:900px) 100vw, 50vw')}<figcaption class="cap">01 &middot; Living</figcaption></figure>
      <figure class="fig rv d1">{C.img('u708-kitchen', 'Kitchen and dining space', sizes='(max-width:900px) 100vw, 25vw')}<figcaption class="cap">02 &middot; Kitchen</figcaption></figure>
      <figure class="fig rv d2">{C.img('u704-bed-patio', 'Large bedroom with mirrored closet, built-in organizers and a patio', sizes='(max-width:900px) 100vw, 25vw')}<figcaption class="cap">03 &middot; Bedroom</figcaption></figure>
      <figure class="fig rv d3">{C.img('u703-patio', 'Large patio', sizes='(max-width:900px) 100vw, 25vw')}<figcaption class="cap">04 &middot; Patio</figcaption></figure>
      <figure class="fig rv d4">{C.img('u702-bath', 'Bathroom with glass-door shower-bath and vanity cabinet storage', sizes='(max-width:900px) 100vw, 25vw')}<figcaption class="cap">05 &middot; Bath</figcaption></figure>
    </div>
    <div class="actions rv"><a class="btn outline" href="gallery.html">All {D.GALLERY_COUNT} photographs</a></div>
  </div>
</section>

<!-- ── Schedule of plans ───────────────────────────────────────────────── -->
<section class="sec cr-schedule dark" data-hd="inv" id="schedule">
  <div class="wrap">
    <p class="kick rv">Schedule</p>
    <h2 class="section-title rv d1">Four plans, named for<br><em>what is around them.</em></h2>
    <div class="cr-table-wrap rv d1">
      <table class="cr-table">
        <caption class="sr-only">Floor plans, sizes, starting rents and current availability</caption>
        <thead><tr><th scope="col">Plan</th><th scope="col">Type</th><th scope="col">Area</th>
          <th scope="col">From / month</th><th scope="col">Availability</th><th scope="col"><span class="sr-only">Detail</span></th></tr></thead>
        <tbody>{plans}</tbody>
      </table>
    </div>
    <p class="cr-note rv">{D.PLAN_SPECIALS} on all plans &middot; {D.PLAN_DEPOSIT} &middot; {D.UTILITIES_NOTE}</p>
    <div class="actions rv d2">
      <a class="btn" href="{D.APPLY}" target="_blank" rel="noopener">Check availability</a>
      <a class="btn outline" href="floorplans.html">See the drawings</a>
    </div>
  </div>
</section>

<!-- ── Measured ────────────────────────────────────────────────────────── -->
<section class="sec cr-measured">
  <div class="wrap">
    <p class="kick rv">Measured</p>
    <h2 class="section-title rv d1">Measured from <em>the door.</em></h2>
    <div class="stats">
      {''.join(f"<div class='rv'><b>{n}</b><span>{lbl}</span><p>{note}</p></div>" for n, lbl, note in D.SCORES)}
    </div>
    <ul class="cr-dist rv">
      {''.join(f'<li><span>{n}</span><i></i><b>{mi} mi</b></li>'
               for n, _note, _la, _lo, mi in D.NEARBY)}
    </ul>
    <p class="cr-note rv">{D.DISTANCE_NOTE}</p>
    <div class="actions rv"><a class="btn outline" href="map.html">Map &amp; directions</a></div>
  </div>
</section>

</main>"""
