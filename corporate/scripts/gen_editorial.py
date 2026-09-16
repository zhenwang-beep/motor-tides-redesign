#!/usr/bin/env python3
"""Image-led company / residents / contact pages for every direction.

The copy is shared (same company, same facts, FACT-CHECK applies); each direction keeps
its own <head>, header, footer and tokens, and core/editorial.css renders the bands in that
direction's type and palette. Splices between <main id="main"> and </main>.

    python3 scripts/gen_editorial.py            # all directions
    python3 scripts/gen_editorial.py tideline
"""
import json, os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V = "18"   # fallback only — splice() reads the page's own ?v= so a direction
           # that has bumped never gets a stale core link written into it
E = lambda s: html.escape(str(s), quote=True)
DATA = json.load(open(os.path.join(ROOT, "data", "wiseman.json")))
P = {p["slug"]: p for p in DATA["properties"]}
AREAS = DATA["areas"]

def gal(slug, i=0, w=1400):
    """A building's own photograph at a width the CDN can honour (originals are 2048px+)."""
    u = P[slug]["gallery"][i]
    return re.sub(r"/upload/[^/]+/", "/upload/q_auto,f_auto,w_%d/" % w, u)

def local(name):
    return "../assets/img/" + name

ARROW = '<svg viewBox="0 0 26 8" aria-hidden="true"><path d="M0 4h24M20 1l4 3-4 3"/></svg>'
def link(href, text):
    return f'<a class="ed-link" href="{href}">{text} {ARROW}</a>'

def fig(src, alt, pos="50% 50%", ar=None, cap=None, wide=False, w=1400, h=933):
    style = f' style="--pos:{pos}{(";--ar:"+ar) if ar else ""}"'
    c = f"<figcaption>{E(cap)}</figcaption>" if cap else ""
    return (f'<figure class="ed-fig{" wide" if wide else ""} rvi"{style}>'
            f'<img src="{src}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">{c}</figure>')

def hero(img, alt, eyebrow, h1, lede, pos="50% 50%", cred=None):
    return f"""
  <section class="ed-hero" data-hd="dark" style="--pos:{pos}">
    <figure class="ed-img"><img src="{img}" alt="{E(alt)}" width="1800" height="1200" fetchpriority="high" decoding="async"></figure>
    <div class="ed-body wrap wrap-n">
      <p class="ed-eyebrow">{eyebrow}</p>
      <h1 class="ed-h1">{h1}</h1>
      <p class="ed-lede">{lede}</p>
    </div>
    {f'<p class="ed-cred">{cred}</p>' if cred else ''}
  </section>"""

def band(figure, eyebrow, h2, paras, flip=False, cta=None):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f"""
    <div class="ed-band{' flip' if flip else ''}">
      {figure}
      <div class="ed-copy rv">
        <p class="ed-eyebrow">{eyebrow}</p>
        <h2 class="ed-h2">{h2}</h2>
        {body}
        {cta or ''}
      </div>
    </div>"""

def doc_row(title, paras, tag=None):
    """A ruled row for a text-led page (services pillars, careers roles, legal sections):
    heading in the left column, prose in the right, an optional short label at the end."""
    body = "".join(f"<p>{p}</p>" for p in paras)
    t = f'<span class="ed-state">{tag}</span>' if tag else ""
    return f'<li class="ed-row"><h3>{title}</h3><div>{body}</div>{t}</li>'

def doc(eyebrow, h2, rows, lede=None, banner=None):
    """A flowing text document (careers / privacy / accessibility): one section, a heading,
    an optional draft banner, and a ruled list of doc_row sections."""
    ban = f'<p class="ed-note" style="margin-bottom:34px">{banner}</p>' if banner else ""
    ld = f'<p class="ed-lede" style="margin-top:16px">{lede}</p>' if lede else ""
    return f"""
  <section class="ed-sec wrap wrap-n">
    {ban}
    <p class="ed-eyebrow">{eyebrow}</p>
    <h2 class="ed-h2">{h2}</h2>
    {ld}
    <ul class="ed-rows rv" style="margin-top:32px">{''.join(rows)}</ul>
  </section>"""

# --------------------------------------------------------------------------- company
def company():
    n = DATA["counts"]["properties"]
    areas = sorted(AREAS.values(), key=lambda a: -a["count"])
    four = sum(1 for p in DATA["properties"] if (p["bedsMax"] or 0) >= 4)
    five = sum(1 for p in DATA["properties"] if (p["bedsMax"] or 0) >= 5)
    streets = len({p["street"] for p in DATA["properties"] if p["street"]})
    stats = f"""
  <section class="ed-stats wrap wrap-n">
    <div class="rv"><p class="ed-num tnum">{n}</p><span>Buildings owned and managed</span></div>
    <div class="rv rv-d1"><p class="ed-num tnum">{len(areas)}</p><span>Parts of Los Angeles</span></div>
    <div class="rv rv-d2"><p class="ed-num tnum">{streets}</p><span>Named streets</span></div>
    <div class="rv rv-d3"><p class="ed-num tnum">{four}</p><span>Buildings with four bedrooms or more</span></div>
  </section>"""
    pipeline = [
        ("3557 Motor Avenue", "Motor Tides — seven storeys, 104 apartments plus three accessory units, one to four bedrooms, a rooftop deck and a fitness centre. Architect: Uriu &amp; Associates.", "Completing 2026", "Urbanize LA, 12 May 2026"),
        ("3659 South Motor Avenue", "Sixty-eight apartments, a block north on the same street.", "Built", "Urbanize LA"),
        ("3418–3554 South Motor Avenue", "Two hundred apartments proposed, twenty-two set aside for extremely-low-income households.", "Proposed", "Urbanize LA"),
        ("9000–9020 Venice Boulevard", "Four hundred and ninety apartments filed, sixty-four of them set aside.", "Filed", "Urbanize LA / The Real Deal"),
        ("11261 Santa Monica Boulevard", "One hundred and nineteen apartments. Current status to confirm. <span class=\"chip\">[CLIENT]</span>", "Reported", "Urbanize LA / The Real Deal"),
        ("1600 East Venice Boulevard", "Seventy-seven apartments. Current status to confirm. <span class=\"chip\">[CLIENT]</span>", "Reported", "Urbanize LA / The Real Deal"),
        ("1808 Lincoln Boulevard", "Fifty apartments. Current status to confirm. <span class=\"chip\">[CLIENT]</span>", "Reported", "Urbanize LA / The Real Deal"),
    ]
    rows = "".join(f'<li class="ed-row"><h3>{a}</h3><p>{d}</p><span class="ed-state">{s}</span><span class="ed-cite">{c}</span></li>' for a, d, s, c in pipeline)
    where = "".join(f'<li class="ed-row"><h3>{E(a["name"])}</h3><p>{E(a["sub"])}</p><span class="ed-state tnum">{a["count"]} building{"s" if a["count"]!=1 else ""}</span></li>' for a in areas)
    pillars = [
        ("Own", ["Every building is held and listed here &mdash; the whole portfolio, not a selection from it."], f"{n} buildings"),
        ("Develop", ["New apartments, most recently along the Motor Avenue corridor in Palms, minutes from Culver City. The company was founded by Isaac Cohanzad."], "Motor Avenue"),
        ("Manage", ["Leasing, rent and repairs. Every building runs its own office and leasing line."], "On site"),
    ]
    services = f"""
  <section class="ed-sec wrap wrap-n" id="what-we-do" style="padding-bottom:clamp(40px,6vh,72px)">
    <p class="ed-eyebrow">What we do</p>
    <h2 class="ed-h2">Owned, built and run in-house.</h2>
    <p class="ed-lede" style="margin-top:16px">One Los Angeles company owns, develops and manages all {n} buildings &mdash; each with its own on-site office and leasing line.</p>
    <ul class="ed-rows rv" style="margin-top:32px">{''.join(doc_row(t, d, s) for t, d, s in pillars)}</ul>
  </section>"""
    return hero(local("wr03.jpg"), "A Wiseman building on a corner in West Los Angeles, palms against a deep blue sky.",
                "The company", "Owner. Builder.<br>Manager.",
                f"One Los Angeles company holds all {n} buildings, builds the new ones, and runs the day-to-day of every one.",
                pos="50% 48%", cred="West Los Angeles") + services + stats + f"""
  <section class="ed-sec wrap wrap-n">
    {band(fig(local("wr11.jpg"), "A tree-lined Wiseman building in Brentwood.", "50% 50%", cap="Brentwood"),
          "01 — Owns", "Every building is listed.",
          [f"All {n} buildings are listed on this site, each with its street, its neighbourhood and its own leasing line. It is the whole portfolio, not a selection from it."],
          cta=link("buildings.html", "Every building"))}
  </section>
  <section class="ed-sec wrap wrap-n">
    {band(fig(local("wr13.jpg"), "Motor Tides, the newest Wiseman building, on Motor Avenue.", "50% 44%", cap="Motor Tides · Palms"),
          "02 — Builds", "New apartments on Motor Avenue.",
          ["Wiseman develops as well as owns — most recently along the Motor Avenue corridor in Palms, minutes from Culver City. The company was founded by Isaac Cohanzad."],
          flip=True, cta=link("#pipeline", "What is under way"))}
  </section>
  <section class="ed-sec wrap wrap-n">
    {band(fig(local("wr06.jpg"), "A planted courtyard at a Wiseman building in the morning.", "50% 50%", cap="A Wiseman courtyard"),
          "03 — Manages", "Leasing, rent and repairs.",
          ["Every building page carries that building's own leasing number, and the repair path starts there — no login needed."],
          cta=link("residents.html", "How repairs work"))}
  </section>
  <section class="ed-sec wrap wrap-n" id="on-site">
    {band(fig(local("wr14.jpg"), "A Wiseman apartment building on a residential Westside street.", "50% 50%", cap="On site"),
          "The on-site model", "The manager is in the building.",
          [f"Each of the {n} buildings runs its own office, leasing number and maintenance path — no login, no ticket queue. A named manager on site, and repairs that move.",
           "The corporate office at 1520 Federal Ave stands behind them; the day-to-day starts at the building."],
          flip=True, cta=link("residents.html", "How repairs work"))}
    <p class="ed-note" style="margin-top:28px">Most of these roles are hired locally, building by building.</p>
    {link("careers.html", "Work at Wiseman")}
  </section>
  <section class="ed-bleed" data-hd="dark" style="--pos:50% 46%">
    <figure class="ed-img"><img src="{local('wr19.jpg')}" alt="A modern Wiseman elevation with blue glass balconies." width="1800" height="1200" loading="lazy" decoding="async"></figure>
    <div class="ed-body wrap wrap-n"><p class="ed-eyebrow">Where</p><h2 class="ed-h2">Concentrated, not spread.</h2>
      <p class="ed-lede">Twenty-seven buildings stand in West Los Angeles alone. The rest reach from Brentwood to Hollywood, Venice and Glendale.</p></div>
  </section>
  <section class="ed-sec wrap wrap-n">
    <ul class="ed-rows rv">{where}</ul>
    {link("neighborhoods.html", "All seven neighbourhoods")}
  </section>
  <section class="ed-sec wrap wrap-n" id="pipeline">
    <p class="ed-eyebrow">Still building here</p>
    <h2 class="ed-h2">What is under way, and who reported it.</h2>
    <p class="ed-lede" style="margin-top:16px">Every line is as the trade press reported it; the citation stays on the line.</p>
    <ul class="ed-rows rv" style="margin-top:32px">{rows}</ul>
  </section>
  <section class="ed-sec wrap wrap-n" id="about">
    <p class="ed-eyebrow">Still to come from Wiseman</p>
    <h2 class="ed-h2" id="client-gaps">The parts only the company can write.</h2>
    <p class="ed-lede" style="margin-top:16px">Rather than invent a team page, a founding date or a set of values, the demo marks them. Each is the company's to confirm in writing.</p>
    <ul class="ed-rows rv" style="margin-top:32px">
      {doc_row("Leadership", ["The company was founded by Isaac Cohanzad. Any other name, title or biography is the company's to supply. <span class=\"chip\">[CLIENT]</span>"], "Founder named")}
      {doc_row("Our history", ["The year the company was founded, the years it has been in business and the number of homes it has built to date are not stated here until Wiseman confirms them in writing. <span class=\"chip\">[CLIENT]</span>"], "No dates yet")}
      {doc_row("What we value", ["Two lines are the company's own and quotable today: &ldquo;Los Angeles Living, Managed Wisely.&rdquo; and &ldquo;Experience That Shows.&rdquo; Any further statement of values is the company's to write. <span class=\"chip\">[CLIENT]</span>"], "In their words")}
    </ul>
  </section>"""

# --------------------------------------------------------------------------- residents
def residents():
    doors = [
        ("Pay rent", "Rent and your account history, in the resident portal.", "https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx", gal("brockton-manor", 0), "Login"),
        ("Security deposits", "California gives a landlord twenty-one days to send an itemised statement.", "#deposits", local("wr16.jpg"), "Twenty-one days"),
        ("Moving in", "Keys, utilities, parking and who to call in the first week.", "#moving", local("wr17.jpg"), "The first week"),
        ("Rights &amp; resources", "Los Angeles and Glendale are different jurisdictions. Both, linked at source.", "#rights", local("wr09.jpg"), "Where the rules live"),
    ]
    tiles = "".join(f"""
      <a class="ed-door rv" href="{h}"{' rel="noopener"' if h.startswith('http') else ''}>
        <span class="ed-tag">{E(t)}</span>{fig(i, n, w=1400, h=1867).replace(' rvi', '')}
        <h3>{n}</h3><p>{d}</p></a>""" for n, d, h, i, t in doors)
    return hero(local("wr01.jpg"), "A living room under arched windows in a Wiseman apartment.",
                "Residents", "The urgent door needs no login.",
                "Rent lives behind a password because it has to. A broken pipe does not.", pos="50% 50%") + f"""
  <section class="ed-sec wrap wrap-n">
    <div class="ed-urgent rv">
      <div>
        <p class="ed-eyebrow">Maintenance · any hour</p>
        <h2 class="ed-h2">Report a repair.</h2>
        <p style="margin-top:14px">Call the building's own office, or the main line.</p>
        <a class="ed-tel tnum" href="tel:+13104733000">+1 310-473-3000</a>
        <p class="ed-note" style="margin-top:18px">The after-hours number belongs here, larger than anything else on the page. <span class="chip">[CLIENT]</span></p>
      </div>
      <ol>
        <li><b>1</b><div><p><strong>Anyone in danger</strong> — call 911 first. If you smell gas, leave and call from outside.</p></div></li>
        <li><b>2</b><div><p><strong>Cannot wait</strong> — water that will not stop, no heat or power, a door that will not lock. Call the building; if no answer, the main line.</p></div></li>
        <li><b>3</b><div><p><strong>Can wait until morning</strong> — call the building's office in working hours. Its number is on its page.</p></div></li>
      </ol>
    </div>
  </section>
  <section class="ed-sec wrap wrap-n">
    <p class="ed-eyebrow">Everything else</p>
    <h2 class="ed-h2">Four more doors.</h2>
    <div class="ed-doors" style="margin-top:32px">{tiles}</div>
  </section>
  <section class="ed-sec wrap wrap-n" id="deposits">
    {band(fig(gal("rimini", 1), "Dining and living room opening onto a patio at Rimini.", "50% 50%", cap="Rimini · Beverly Grove"),
          "Security deposits", "Twenty-one days, in writing.",
          ["No later than twenty-one calendar days after you move out, the landlord must send an itemised statement of any deduction and return the balance. It is California law, statewide — Civil Code §1950.5.",
           "How Wiseman handles it — when the statement is sent, what is normally deducted, who to ask — is the company's to write. <span class=\"chip\">[CLIENT COPY]</span>"],
          cta='<a class="ed-link" href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1950.5" rel="noopener">Read §1950.5 ' + ARROW + '</a>')}
  </section>
  <section class="ed-sec wrap wrap-n" id="moving">
    {band(fig(gal("santa-monica-breeze", 2), "Living room and patio at Santa Monica Breeze.", "50% 50%", cap="Santa Monica Breeze · West LA"),
          "Moving in", "The first week.",
          ["In the City of Los Angeles, water and power come from LADWP and gas from SoCalGas; the Glendale building is served by Glendale Water &amp; Power. Which utilities the rent includes is in your lease. <span class=\"chip\">[CLIENT]</span>",
           "Walk the apartment with whoever hands over the keys and note anything already marked, in writing. It is the same list that decides a deduction at the other end."],
          flip=True, cta=link("buildings.html", "Find your building"))}
  </section>
  <section class="ed-sec wrap wrap-n" id="rights">
    {band(fig(local("wr20.jpg"), "A shaded patio lounge at a Wiseman building.", "50% 50%"),
          "Rights &amp; resources", "Where the rules actually live.",
          ["One building is in Glendale, a separate city with its own rules. The rest carry Los Angeles addresses; the LA Housing Department publishes the Rent Stabilization Ordinance and renter protections, and the disclosures for your own unit come with your lease."],
          cta='<a class="ed-link" href="https://housing.lacity.gov/residents" rel="noopener">LA Housing Department ' + ARROW + '</a>')}
  </section>"""

# --------------------------------------------------------------------------- contact
def contact():
    routes = [
        ("Leasing", "You want to see an apartment, or ask what is free and what it costs.", "The leasing office for that building calls you back.", "search.html", "What is available"),
        ("Current resident", "Rent, a document, a lease question, a renewal.", "Rent goes to the portal; everything else to your building's own office.", "residents.html", "Residents"),
        ("Maintenance emergency", "Water that will not stop, no heat, a door that will not lock.", "You call rather than write. If anyone is in danger, 911 first.", "tel:+13104733000", "Call now"),
        ("Owner &amp; development", "A site, a building, a partnership on a project.", "Goes to the development side of the company. Named contact <span class=\"chip\">[CLIENT]</span>", "company.html#pipeline", "What is under way"),
        ("Careers", "On-site management, maintenance, leasing, the office.", "The roles behind the on-site model, and how to apply.", "careers.html", "Work at Wiseman"),
        ("Press", "A reporter on deadline, or a number to check before it prints.", "Press contact <span class=\"chip\">[CLIENT]</span>. Every figure on this site is computed from the live feed.", "company.html", "The portfolio in numbers"),
    ]
    rows = "".join(f'<li class="ed-row"><h3>{n}</h3><p>{w}<br><span style="color:var(--ed-mute)">{x}</span></p><a class="ed-state" href="{h}">{t} →</a></li>' for n, w, x, h, t in routes)
    return hero(local("wr07.jpg"), "The entrance of a Wiseman building, dark timber and terracotta.",
                "Contact", "One number. Six routes.",
                "Each route says where it goes and who answers, before you spend a call finding out.", pos="50% 50%") + f"""
  <section class="ed-sec wrap wrap-n">
    <div class="ed-office rv">
      <div class="ed-addr">
        <p class="ed-eyebrow">The office</p>
        <p class="ed-big">1520 Federal Ave<br>Los Angeles, CA 90025</p>
        <p style="margin-top:16px"><a class="ed-tel tnum" href="tel:+13104733000" style="font-size:clamp(1.5rem,2.6vw,2.2rem)">+1 310-473-3000</a></p>
        <p>One number for leasing and the corporate office. Office hours <span class="chip">[CLIENT]</span></p>
        <p style="margin-top:14px"><a class="ed-link" href="https://maps.google.com/?q=1520+Federal+Ave,+Los+Angeles,+CA+90025" rel="noopener">Directions {ARROW}</a></p>
      </div>
      <div class="ed-map" id="office-map" data-theme="light"></div>
    </div>
  </section>
  <section class="ed-sec wrap wrap-n">
    <p class="ed-eyebrow">Routed by what you need</p>
    <h2 class="ed-h2">Six ways in.</h2>
    <ul class="ed-rows rv" style="margin-top:32px">{rows}</ul>
  </section>
  <section class="ed-sec wrap wrap-n">
    <div class="ed-write">
      {fig(local("wr12.jpg"), "A planted courtyard stair with birds of paradise at a Wiseman building.", "50% 54%")}
      <div class="ed-writebody rv">
        <p class="ed-eyebrow">Or write it down</p>
        <h2 class="ed-h2">Send it in writing.</h2>
        <p>Slower than the phone, and better when you need a record of what you asked. An emergency should never go through a form.</p>
        <form class="ed-form" onsubmit="return false">
          <div class="ed-two">
            <label>Your name<input type="text" name="name" autocomplete="name"></label>
            <label>Email<input type="email" name="email" autocomplete="email"></label>
          </div>
          <div class="ed-two">
            <label>Phone (optional)<input type="tel" name="tel" autocomplete="tel"></label>
            <label>Building or street (optional)<input type="text" name="building"></label>
          </div>
          <label>What is this about
            <select name="topic"><option>Leasing — I am looking at an apartment</option><option>I am a current resident</option><option>Maintenance — not an emergency</option><option>A security deposit</option><option>Owner &amp; development</option><option>Careers</option><option>Press</option></select>
          </label>
          <label>Message<textarea name="message"></textarea></label>
          <button type="submit">Send — demo only</button>
          <p class="ed-note">This form posts nowhere in the demo. Before launch it needs a monitored inbox and an acknowledgement. <span class="chip">[CLIENT]</span></p>
        </form>
      </div>
    </div>
  </section>"""

# --------------------------------------------------------------------------- careers
def careers():
    n = DATA["counts"]["properties"]
    areas = len(AREAS)
    roles = [
        ("On-site management", ["Resident managers who run a single building's office: leasing enquiries, the day-to-day questions, and the first call when something needs fixing."], "In the building"),
        ("Maintenance &amp; make-ready", ["The crews who handle repairs and turn an apartment over between residents."], "Hands on"),
        ("Leasing", ["Showing apartments, answering what is available and what it costs, and taking an application through."], "Front of house"),
        ("Corporate office", ["Accounting, operations and the support behind the buildings, from the office at 1520 Federal Ave."], "1520 Federal Ave"),
    ]
    return hero(local("wr04.jpg"), "A Wiseman apartment building on a tree-lined Westside street.",
                "Careers", "Work at Wiseman.",
                "The people who run a building and fix what breaks are the ones residents actually deal with. Those are the jobs.",
                pos="50% 50%") + f"""
  <section class="ed-sec wrap wrap-n">
    <p class="ed-eyebrow">What we hire for</p>
    <h2 class="ed-h2">Four kinds of work.</h2>
    <p class="ed-lede" style="margin-top:16px">No invented titles, counts or salaries &mdash; the open roles and the terms are the company's to publish.</p>
    <ul class="ed-rows rv" style="margin-top:32px">{''.join(doc_row(t, d, s) for t, d, s in roles)}</ul>
  </section>
  <section class="ed-sec wrap wrap-n">
    {band(fig(local("wr18.jpg"), "A planted walkway alongside a Wiseman building.", "50% 50%", cap="Neighbourhood-based"),
          "How the work is shaped", "Seventy-two offices, not one.",
          [f"Wiseman runs {n} buildings across {areas} parts of Los Angeles, each with its own office and leasing line. Most roles are tied to a building and a neighbourhood, not a single headquarters."],
          cta=link("buildings.html", "Every building"))}
    {link("neighborhoods.html", "The seven areas")}
  </section>
  <section class="ed-sec wrap wrap-n">
    <p class="ed-eyebrow">How to apply</p>
    <h2 class="ed-h2">How to reach us.</h2>
    <p style="margin-top:18px">Wiseman does not publish an open-roles list or an application portal today. Until it does, send a note through the contact page and mark it for careers, or write to the careers inbox. <span class="chip">[CLIENT]</span></p>
    {link("contact.html", "Contact &mdash; careers")}
    <p class="ed-note" style="margin-top:28px">Wiseman Residential is an equal-opportunity employer. The exact wording of that statement is the company's to confirm. <span class="chip">[CLIENT]</span></p>
  </section>"""

# --------------------------------------------------------------------------- privacy policy
DRAFT = 'This is a draft for the client&rsquo;s counsel to confirm before launch. <span class="chip">[CLIENT]</span>'
PORTAL_LINK = ('<a class="ed-link" href="https://wisemanresidential.securecafe.com/residentservices/apartmentsforrent/userlogin.aspx" '
               'target="_blank" rel="noopener">The resident &amp; applicant portal ' + ARROW + '</a>')

def privacy():
    rows = [
        doc_row("Who we are", ["This policy covers this website, published by Wiseman Residential, 1520 Federal Ave, Los Angeles, CA 90025.",
                               "It does not cover the separate resident and applicant portal, which a third-party vendor (SecureCafe / RentCafe) runs for Wiseman under its own privacy policy." + PORTAL_LINK]),
        doc_row("Information we collect", ["<strong>What you give us.</strong> When you use the leasing or contact form: your name, email, phone, and the building or street you ask about.",
                                           "<strong>What we collect automatically.</strong> Standard device and usage information, and cookies where the launched site uses them.",
                                           "<strong>From the leasing system.</strong> Enquiries and applications you start reach us through the live leasing system."]),
        doc_row("How we use it", ["To answer your enquiries, process rental applications, operate and maintain the buildings, and meet our legal obligations."]),
        doc_row("Cookies &amp; analytics", ["The analytics, advertising and cookie tools the launched site runs are confirmed before launch. This demo runs no analytics and sets no advertising cookies. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("Sharing", ["We share information with the service providers who make the site and the buildings work &mdash; the leasing and portal vendor, and maintenance vendors &mdash; under contract.",
                            "Whether any disclosure is a &ldquo;sale&rdquo; or &ldquo;share&rdquo; as the CPRA defines those terms is being confirmed with counsel. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("Your California privacy rights", ["If you live in California, you have the right to know, to delete, to correct, to opt out of the sale or sharing of personal information, to limit the use of sensitive personal information, and not to be treated differently for exercising these rights.",
                                                    link("privacy-choices.html", "Your privacy choices")], "CCPA / CPRA"),
        doc_row("Fair housing", ["Rental applications are handled consistent with the federal Fair Housing Act and California's FEHA. Source of income is a protected class in California."]),
        doc_row("Children", ["This site is not directed to children and does not knowingly collect information from them."]),
        doc_row("Security", ["We take reasonable measures to protect the information we hold. No method of transmission or storage is completely secure."]),
        doc_row("Retention", ["How long each kind of information is kept is set with counsel before launch. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("Changes", ["We may update this policy. The effective date below marks the current version."]),
        doc_row("Contact", ["Questions about privacy go to 1520 Federal Ave, Los Angeles, CA 90025, or +1 310-473-3000. A dedicated privacy contact is confirmed before launch. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("Effective date", ["Effective date <span class=\"chip\">[CLIENT]</span>"]),
    ]
    return hero(local("wr05.jpg"), "A quiet Wiseman building elevation in the late afternoon.",
                "Legal", "Privacy Policy.",
                "How this website handles the information you give it, and the California rights that come with it.",
                pos="50% 50%") + doc("What this covers", "In plain English.", rows, banner=DRAFT)

# --------------------------------------------------------------------------- accessibility
def accessibility():
    rows = [
        doc_row("Our commitment", ["Wiseman Residential aims to conform to the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA, and to keep the site usable with a keyboard, a screen reader, or the browser zoomed in."]),
        doc_row("What we have done", ["<strong>Skip link and focus.</strong> A skip link to the main content, and a visible focus outline on every interactive element.",
                                      "<strong>Keyboard parity.</strong> Anything that works on hover also works on focus.",
                                      "<strong>Usable without the map.</strong> The building list stays complete and usable with the map switched off.",
                                      "<strong>Alt text.</strong> On the brand marks and on the Equal Housing Opportunity mark.",
                                      "<strong>Reduced motion.</strong> Animation collapses to a still end state when the browser asks for it."]),
        doc_row("No accessibility overlay", ["This site does not use a third-party accessibility overlay or widget. Those tools can interfere with assistive technology; we prefer to build access into the site itself."]),
        doc_row("Third-party and ongoing content", ["The resident and applicant portal is a separate system with its own accessibility. Photography is hotlinked from the leasing feed. If something on the site falls short, tell us and we will fix it."]),
        doc_row("Conformance", ["The site is partially conformant with WCAG 2.1 AA: most of it meets the standard and we are working toward full conformance. It has not yet had a formal third-party audit. <span class=\"chip\">[CLIENT]</span>"], "Partially conformant"),
        doc_row("How to reach us", ["Call +1 310-473-3000 or write to the corporate office at 1520 Federal Ave, Los Angeles, CA 90025. A dedicated accessibility contact and a response-time commitment are confirmed before launch. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("Reasonable accommodation", ["To request a reasonable accommodation, contact the building's own office or the corporate office. How Wiseman handles those requests is the company's to set out. <span class=\"chip\">[CLIENT]</span>"]),
    ]
    return hero(local("wr10.jpg"), "A sunlit stair and landing at a Wiseman building.",
                "Legal", "Accessibility.",
                "How we build this site to be usable by everyone, and how to reach a person if something falls short.",
                pos="50% 50%") + doc("Accessibility statement", "Built in, not bolted on.", rows, banner=DRAFT)

# --------------------------------------------------------------------------- your privacy choices
def privacy_choices():
    rows = [
        doc_row("Your choices", ["Under the California Consumer Privacy Act, as amended by the CPRA, you can opt out of the sale or sharing of your personal information and limit the use and disclosure of sensitive personal information."]),
        doc_row("Does Wiseman sell or share", ["Wiseman does not sell personal information for money. Whether any disclosure counts as a &ldquo;sale&rdquo; or a &ldquo;share&rdquo; as the CPRA defines those terms is being confirmed with counsel. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("How to opt out", ["The opt-out route &mdash; a form, an email address or a toll-free number &mdash; and whether the site honours Global Privacy Control (GPC) browser signals are confirmed before launch. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("Authorised agents", ["You may use an authorised agent to make a request on your behalf. We may ask the agent for proof and ask you to verify your own identity."]),
        doc_row("No discrimination", ["We will not treat you differently for exercising any of these rights."]),
        doc_row("How we verify a request", ["To protect your information we confirm your identity before acting on a request. The exact steps are set with counsel. <span class=\"chip\">[CLIENT]</span>"]),
        doc_row("The full policy", ["The complete detail sits in the privacy policy.", link("privacy.html", "Privacy Policy")]),
    ]
    return hero(local("wr15.jpg"), "A Wiseman building facade under a clear Los Angeles sky.",
                "Legal", "Your Privacy Choices.",
                "Your California rights to opt out of the sale or sharing of personal information, and to limit the use of sensitive personal information.",
                pos="50% 50%") + doc("California", "Opt out, and limit sensitive data.", rows, banner=DRAFT)

PAGES = {"company.html": company, "residents.html": residents, "contact.html": contact,
         "careers.html": careers, "privacy.html": privacy,
         "accessibility.html": accessibility, "privacy-choices.html": privacy_choices}
HEAD_LINKS = f'<link rel="stylesheet" href="../core/editorial.css?v={V}">\n<link rel="stylesheet" href="../core/map.css?v={V}">\n'
MAP_BOOT = f"""<script src="../core/map.js?v={V}" defer></script>
<script>
addEventListener('DOMContentLoaded', function () {{
  if (!window.WR || !WR.map || !document.getElementById('office-map')) return;
  WR.map({{ el: '#office-map', theme: 'light', label: 'Map of the Wiseman office at 1520 Federal Ave',
    points: [{{ no: 'HQ', lat: 34.0452, lng: -118.4541, name: 'Wiseman Residential', street: '1520 Federal Ave',
               areaLabel: 'West Los Angeles', pinLabel: 'Office', url: 'https://maps.google.com/?q=1520+Federal+Ave,+Los+Angeles,+CA+90025' }}],
    pins: 'price', breakZoom: 0 }});
  var t = setInterval(function () {{ if (WR.mapInstance) {{ clearInterval(t); WR.mapInstance.setView([34.0452, -118.4541], 15); }} }}, 150);
}});
</script>
"""

def splice(direction):
    n = 0
    for fname, build in PAGES.items():
        path = os.path.join(ROOT, direction, fname)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        m = re.search(r'(<main id="main"[^>]*>)(.*?)(</main>)', s, re.S)
        if not m:
            print("  !", direction, fname, "has no <main id=main>"); continue
        body = '\n<div class="ed">' + build() + "\n</div>\n"
        s = s[:m.start(2)] + body + s[m.end(2):]
        # every page in a direction carries ONE ?v=; read it rather than
        # hard-coding one here, so a bumped direction stays internally uniform
        mv = re.search(r'style\.css\?v=(\d+)', s)
        ver = mv.group(1) if mv else V
        if "core/editorial.css" not in s:
            s = re.sub(r'(<link rel="stylesheet" href="style\.css)',
                       HEAD_LINKS.replace("?v=" + V, "?v=" + ver) + r"\1", s, count=1)
        # The office map needs two things: core/map.js and the boot that calls
        # WR.map on #office-map. A direction whose shell already loads map.js
        # (register) still needs the boot, so test for the boot itself and add
        # the script tag only where it is missing.
        if fname == "contact.html" and "office-map" in s and "WR.map({ el: '#office-map'" not in s:
            mb = MAP_BOOT.replace("?v=" + V, "?v=" + ver)
            boot = mb if "core/map.js" not in s else mb.split("\n", 1)[1]
            s = s.replace("</body>", boot + "</body>", 1)
        # reveal hooks need the shared observers — every page already boots core.js
        open(path, "w", encoding="utf-8").write(s)
        n += 1
    print("  %-10s %d pages" % (direction, n))
    return n

if __name__ == "__main__":
    targets = sys.argv[1:] or [d for d in ("tideline", "register", "nocturne") if os.path.isdir(os.path.join(ROOT, d))]
    total = sum(splice(t) for t in targets)
    print("%d editorial pages rebuilt" % total)
