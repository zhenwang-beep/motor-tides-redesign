# -*- coding: utf-8 -*-
"""The six interior pages.

Content and information architecture are identical across the three concepts —
the same plans, the same amenities, the same 47 photographs — because the
client asked for the concepts to differ in design, not in what they say. Each
concept supplies its own page hero through `c.phero(...)` and restyles the
shared blocks through its own stylesheet.
"""
import data as D
import chrome as C



def map_block(*, note_prefix="") -> str:
    """The neighbourhood map: a MapLibre canvas and, beside it, the same
    places as a list. The list is the content — it reads and works with the
    map switched off, and the pins are wired to it rather than the reverse."""
    rows = []
    for i, (name, note, lat, lon, mi) in enumerate(D.NEARBY, 1):
        rows.append(
            f'<li><button type="button" data-place="{name}" data-num="{i:02d}" '
            f'data-lat="{lat}" data-lon="{lon}" aria-current="false">'
            f'<span class="m-num">{i:02d}</span>'
            f'<span class="m-name">{name}</span>'
            f'<span class="m-note">{note}</span>'
            f'<span class="m-dist">{mi} mi</span></button></li>')
    return f"""<div class="map-layout">
  <div class="map-frame rv">
    <div class="map-canvas" id="map-canvas"
         data-style="../assets/maps/midway-positron.json"
         data-lat="{D.HOME[0]}" data-lon="{D.HOME[1]}" data-label="{D.HOME_LABEL}"
         role="application" aria-label="Map of {D.FULL} and what is nearby"></div>
  </div>
  <div>
    <ul class="map-list">{''.join(rows)}</ul>
    <div class="map-toolbar">
      <button type="button" id="map-reset">Recentre on the building</button>
      <a class="tlink" href="{D.DIRECTIONS}" target="_blank" rel="noopener">Directions</a>
    </div>
  </div>
</div>
<p class="fine map-note">{note_prefix}{D.DISTANCE_NOTE}</p>"""


# ── Floor plans ─────────────────────────────────────────────────────────────
def floorplans(c) -> str:
    cards = []
    for i, p in enumerate(D.PLANS):
        cards.append(f"""
      <article class="plan rv" data-plan data-beds="{p['beds']}">
        <div class="plan-draw">{C.img(p['img'], f"{p['name']} floor plan — {p['beds']} bedroom, {p['baths']} bath, {p['sqft']} square feet", sizes="(max-width:820px) 100vw, 40vw")}</div>
        <div class="plan-body">
          <div class="plan-head">
            <h2>{p['name']}</h2>
            <p class="plan-price"><small>From / month</small>${p['price']:,}</p>
          </div>
          <p class="plan-blurb">{p['blurb']}</p>
          <dl class="plan-spec">
            <div><dt>Bedrooms</dt><dd>{p['beds']}</dd></div>
            <div><dt>Bathrooms</dt><dd>{p['baths']}</dd></div>
            <div><dt>Square feet</dt><dd>{p['sqft']}</dd></div>
            <div><dt>Available</dt><dd>{p['avail']}</dd></div>
          </dl>
          <p class="plan-meta"><span class="badge">{D.PLAN_SPECIALS}</span> <span class="fine">{D.PLAN_DEPOSIT}</span></p>
          <p class="plan-note fine">{p['note']}</p>
          <div class="actions">
            <a class="btn" href="{D.APPLY}" target="_blank" rel="noopener">Check availability</a>
            <a class="btn outline" href="contact.html">Ask about {p['name']}</a>
          </div>
        </div>
      </article>""")

    return f"""<main id="main">
{c.phero('floorplans',
         kick='Availability',
         title='Floor <em>plans</em>',
         lede='Four plans. Two and three bedrooms, 692 to 909 square feet, '
              'a bathroom for every bedroom and a patio on every one of them.')}

<section class="sec-tight">
  <div class="wrap">
    <div class="plan-toolbar">
      <div class="gal-filter" data-plan-filter role="group" aria-label="Filter plans by bedrooms">
        <button type="button" data-beds="all" aria-pressed="true">All plans</button>
        <button type="button" data-beds="2" aria-pressed="false">2 bedrooms</button>
        <button type="button" data-beds="3" aria-pressed="false">3 bedrooms</button>
      </div>
      <p class="fine" data-plan-count>{len(D.PLANS)} plans</p>
    </div>
    <div class="plan-grid" data-plans>{''.join(cards)}</div>
    <p class="fine utilities">{D.UTILITIES_NOTE}</p>
  </div>
</section>

<section class="sec dark" data-hd="inv">
  <div class="wrap">
    <p class="kick rv">Named for the neighbourhood</p>
    <h2 class="section-title rv d1">Dunn, Venice, Sony, <em>Regent.</em></h2>
    <p class="lede rv d1">Every plan here is named for something within walking distance &mdash;
      a street one over, a boulevard to the north, the studio lot half a mile south.
      It is a small thing, and it is the whole idea of the building: you are in the middle of it.</p>
    <div class="actions rv d2">
      <a class="btn" href="map.html">See where they are</a>
      <a class="btn outline" href="tours.html">Walk through one</a>
    </div>
  </div>
</section>

</main>"""


# ── Amenities ───────────────────────────────────────────────────────────────
def amenities(c) -> str:
    comm = "".join(f"<li class='rv'><h3>{n}</h3><p>{b}</p></li>" for n, b in D.COMMUNITY_AMENITIES)
    apt = "".join(f"<li class='rv'><h3>{n}</h3><p>{b}</p></li>" for n, b in D.APARTMENT_AMENITIES)
    pets = "".join(f"<p>{line}</p>" for line in D.PET_POLICY)

    return f"""<main id="main">
{c.phero('amenities',
         kick='Beyond your front door',
         title='The roof is the <em>best room.</em>',
         lede='An open deck above the intersection with the city on every side of it. Below it: '
              'the fitness center, garage parking, racks for the bikes, and a controlled door '
              'between the street and the stairs.')}

<section class="sec-tight">
  <div class="wrap">
    <div class="am-showcase">
      <figure class="fig rv">{C.img('dusk-05', 'Entertainment area with pergola and sunset views from the rooftop deck', sizes='(max-width:900px) 100vw, 62vw')}
        <figcaption class="fig-over">Rooftop &middot; Golden hour</figcaption></figure>
      <figure class="fig rv d1">{C.img('gym-3', 'Fitness center with resistance bands, free weights, treadmills and universal equipment', sizes='(max-width:900px) 100vw, 36vw')}
        <figcaption class="fig-over">Fitness center</figcaption></figure>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="kick rv">In the building</p>
    <h2 class="section-title rv d1">Community amenities</h2>
    <ul class="amlist">{comm}</ul>
  </div>
</section>

<section class="sec dark" data-hd="inv">
  <div class="wrap">
    <p class="kick rv">In the apartment</p>
    <h2 class="section-title rv d1">Every residence, <em>as standard.</em></h2>
    <ul class="amlist">{apt}</ul>
  </div>
</section>

<section class="sec">
  <div class="wrap pet">
    <div>
      <p class="kick rv">Pet policy</p>
      <h2 class="section-title rv d1">Cats and dogs <em>welcome.</em></h2>
      <div class="lede rv d1 pet-copy">{pets}</div>
      <div class="actions rv d2"><a class="btn outline" href="contact.html">Ask the resident manager</a></div>
    </div>
    <figure class="fig rv d1">{C.img('u17-patio', 'A balcony with a couch and a plant, overlooking the city', sizes='(max-width:820px) 100vw, 44vw')}</figure>
  </div>
</section>

</main>"""


# ── Gallery ─────────────────────────────────────────────────────────────────
def gallery(c) -> str:
    groups = [g for g, _ in D.GALLERY]
    buttons = ['<button type="button" data-group="all" aria-pressed="true">All</button>']
    buttons += [f'<button type="button" data-group="g{i}" aria-pressed="false">{g}</button>'
                for i, g in enumerate(groups)]
    figs = []
    total = 0
    for i, (_g, items) in enumerate(D.GALLERY):
        for slug, alt in items:
            total += 1
            # A <figure> is not focusable and announces nothing, so the
            # full-size view of all 47 photographs was mouse-only. The real
            # control is a button; site.js still delegates from .gal.
            figs.append(f'<figure data-group="g{i}">'
                        f'<button class="gal-open" type="button">'
                        f'{C.img(slug, alt, sizes="(max-width:560px) 100vw, (max-width:960px) 50vw, 33vw", full=True)}'
                        f'<span class="sr-only">Open photograph: {alt}</span>'
                        f'</button></figure>')

    return f"""<main id="main">
{c.phero('gallery',
         kick=f'{total} photographs',
         title='The <em>gallery</em>',
         lede='Residences, kitchens, bedrooms, patios, the rooftop at dusk, the fitness center '
              'and the building on Motor Avenue.')}

<section class="sec-tight">
  <div class="wrap">
    <div class="gal-filter" role="group" aria-label="Filter photographs">{''.join(buttons)}</div>
    <div class="gal">{''.join(figs)}</div>
  </div>
</section>

<dialog class="lb" aria-label="Photograph">
  <div class="lb-inner">
    <img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="">
    <p class="lb-cap"></p>
  </div>
  <button class="lb-close" type="button" aria-label="Close">&times;</button>
  <button class="lb-prev" type="button" aria-label="Previous photograph">&#8249;</button>
  <button class="lb-next" type="button" aria-label="Next photograph">&#8250;</button>
</dialog>

</main>"""


# ── Tours ───────────────────────────────────────────────────────────────────
def tours(c) -> str:
    cards = []
    posters = ['u704-kdl-patio', 'u703-kdl-patio', 'u708-lr-patio', 'u710-dl-patio',
               'u709-lr-patio', 'u17-kdlr', 'u702-kitchen']
    for i, (mid, label) in enumerate(D.TOURS):
        cards.append(f"""
      <article class="tour rv">
        <div class="frame">{C.img(posters[i], f'Still from {label.lower()}', sizes='(max-width:700px) 100vw, 33vw', cls='tour-poster')}</div>
        <div class="meta">
          <b id="tour-{i}">{label}</b>
          <button class="btn outline" type="button" data-tour="{mid}"
                  aria-label="Start {label}">Start tour</button>
        </div>
      </article>""")

    return f"""<main id="main">
{c.phero('tours',
         kick='Walk through it',
         title='360&deg; <em>tours</em>',
         lede='Seven Matterport walkthroughs of the residences. Each one loads only when you '
              'start it. In-person and virtual tours are also available by appointment.')}

<section class="sec-tight">
  <div class="wrap">
    <div class="tour-grid">{''.join(cards)}</div>
    <p class="fine utilities">Tours open inside the page. Use the arrow keys or drag to look around;
      click the floor to move. For an in-person visit, <a class="tlink" href="contact.html">book a time</a>
      or call <a class="tlink" href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>.</p>
  </div>
</section>

</main>"""


# ── Map & directions ────────────────────────────────────────────────────────
def map_page(c) -> str:
    stats = "".join(f"<div class='rv'><b>{n}</b><span>{lbl}</span><p>{note}</p></div>"
                    for n, lbl, note in D.SCORES)

    return f"""<main id="main">
{c.phero('map',
         kick='Map &amp; directions',
         title='In the <em>middle</em> of it.',
         lede='3657 Motor Avenue sits in Palms, on the Culver City border. Motor Avenue runs at '
              'an angle to the grid around it, which is why so much is close in so many directions.')}

<section class="sec-tight">
  <div class="wrap">
    <div class="stats">{stats}</div>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap">
    <p class="kick rv">Close by</p>
    <h2 class="section-title rv d1">What is <em>around it.</em></h2>
    {map_block()}
  </div>
</section>

<section class="sec dark" data-hd="inv">
  <div class="wrap">
    <p class="kick rv">Getting around</p>
    <h2 class="section-title rv d1">The nearest E Line stop is <em>Palms.</em></h2>
    <p class="lede rv d1">Four tenths of a mile up Motor Avenue &mdash; closer than Culver City
      station, which most listings for this stretch name instead. From Palms the E Line runs
      west to Santa Monica and east to Downtown LA. The 10 and the 405 are both a short drive,
      and the Ballona Creek Trail carries on west to the ocean.</p>
    <div class="actions rv d2">
      <a class="btn" href="{D.DIRECTIONS}" target="_blank" rel="noopener">Open in Google Maps</a>
      <a class="btn outline" href="contact.html">Plan a visit</a>
    </div>
  </div>
</section>

</main>"""


# ── Contact ─────────────────────────────────────────────────────────────────
def contact(c) -> str:
    hours = "".join(f"<p>{d} &middot; {t}</p>" for d, t in D.HOURS)
    return f"""<main id="main">
{c.phero('contact',
         kick='Plan a visit',
         title='Come and <em>see it.</em>',
         lede='In-person and virtual tours are available by appointment. Send a note and the '
              'leasing office will come back to you, or call during office hours.')}

<section class="sec-tight">
  <div class="wrap contact-grid">
    <form class="contact-form rv" data-demo method="post" action="#" novalidate aria-labelledby="ct-form-h">
      <h2 class="sr-only" id="ct-form-h">Send the leasing office a message</h2>
      <div class="form-grid">
        <div class="field"><label for="fn">First name</label><input id="fn" name="fn" autocomplete="given-name" required></div>
        <div class="field"><label for="ln">Last name</label><input id="ln" name="ln" autocomplete="family-name" required></div>
        <div class="field"><label for="em">Email address</label><input id="em" name="em" type="email" autocomplete="email" required></div>
        <div class="field"><label for="ph">Phone number</label><input id="ph" name="ph" type="tel" autocomplete="tel" required></div>
        <div class="field full"><label for="pl">Plan of interest</label>
          <select id="pl" name="pl">
            <option value="">No preference</option>
            {''.join(f'<option>{p["name"]} &middot; {p["beds"]} bed &middot; {p["sqft"]} sq ft</option>' for p in D.PLANS)}
          </select></div>
        <div class="field full"><label for="ms">Message</label>
          <textarea id="ms" name="ms" maxlength="512" placeholder="When would you like to visit?"></textarea>
          <span class="hint">512 characters maximum.</span></div>
        <label class="check"><input type="checkbox" name="sms">
          <span>Yes, I&rsquo;d be happy to receive text messages about my enquiry.</span></label>
      </div>
      <div class="actions">
        <button class="btn" type="submit">Send my message</button>
        <a class="btn outline" href="{D.APPLY}" target="_blank" rel="noopener">Apply online</a>
      </div>
      <p class="form-note fine" data-demo-note tabindex="-1" hidden></p>
      <noscript><p class="form-note fine">This is a design concept &mdash; the form is not wired to a mailbox. Please call <a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a> during office hours.</p></noscript>
    </form>

    <aside class="contact-info rv d1" aria-labelledby="ct-info-h">
      <h2 class="sr-only" id="ct-info-h">Leasing office details</h2>
      <ul class="info-list">
        <li><h3>Call the leasing office</h3><a href="{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a></li>
        <li><h3>Office hours</h3><div class="hours">{hours}</div></li>
        <li><h3>Address</h3><p>{D.FULL}<br>{D.ADDRESS_1}<br>{D.ADDRESS_2}</p>
            <a href="{D.DIRECTIONS}" target="_blank" rel="noopener">Get directions</a></li>
        <li><h3>Residents</h3><a href="{D.RESIDENT}" target="_blank" rel="noopener">Resident login</a></li>
      </ul>
      <figure class="fig contact-fig">{C.img('address-wall', 'The lobby wall at 3657 Motor Avenue', sizes='(max-width:900px) 100vw, 38vw')}</figure>
    </aside>
  </div>
</section>

</main>"""
