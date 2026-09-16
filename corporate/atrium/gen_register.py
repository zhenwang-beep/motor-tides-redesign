#!/usr/bin/env python3
"""Generate CLERESTORY (key: atrium) — the bright, culture-first corporate face.

    python3 atrium/gen_register.py            # run from corporate/ (or anywhere)

Writes the hand-composed pages of the direction as real, static, crawlable HTML:

  index.html            the culture-first home (the clerestory masthead + the
                        company argument, the on-site model, the featured six,
                        the portfolio map, About, and the Track Record teaser)
  live.html             a redirect stub only — LIVE AT WISEMAN is search.html,
                        the one page with filters, cards left and map right
  track.html            TRACK RECORD — Motor Tides + the sourced pipeline, cited
  buildings.html        every building, three peer views (?view=register|atlas|plates)
  neighborhoods.html    the seven areas with counts, a map, image-forward cards
  search.html           LIVE AT WISEMAN — the ILS shell with <!--SEARCH-->
                        markers for gen_search.py (cards left, map right)
  company.html          ABOUT WISEMAN  \
  careers.html          WORK AT WISEMAN  }  editorial SHELLS — gen_editorial.py
  contact.html          CONTACT          }  splices the shared image-led bodies in
  residents.html        RESIDENTS       /
  privacy.html · accessibility.html · privacy-choices.html   legal shells

Nothing here invents a number. Every count is computed from data/wiseman.json;
FACT-CHECK §2 forbids a Motor Tides rent anywhere, so 071 is suppressed in every
figure this file writes; anything the client has not confirmed renders as a
visible [CLIENT] chip, never as fiction. Corporate IA modelled on morgangroup.com,
translated to what Wiseman can truthfully say.
"""
import json, os, re, sys, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "wiseman.json")

VER = "39"
SNAPSHOT = "10 September 2026"
TOTAL = 72
FLAG_NO = "071"                    # Motor Tides — FACT-CHECK §2: never a rent
LEASING_TEL = "+1 310-473-3000"
RESIDENT = ("https://wisemanresidential.securecafe.com/residentservices/"
            "apartmentsforrent/userlogin.aspx")
APPLICANT = ("https://wisemanresidential.securecafe.com/onlineleasing/"
             "apartmentsforrent/guestlogin.aspx")
FB = "https://www.facebook.com/Officialwisemanresidential/"
IG = "https://www.instagram.com/officialwisemanresidential"
YELP = "https://www.yelp.com/biz/wiseman-residential-los-angeles-2"

AREA_ORDER = ["west-la", "beverly-grove", "brentwood", "hollywood", "venice", "palms", "glendale"]
# heading / card label (compound names keep their dot with the words either side)
NBSP = " "
CARD_LABEL = {
    "west-la": "West L.A. · Sawtelle", "brentwood": "Brentwood",
    "beverly-grove": "Beverly Grove", "hollywood": "Hollywood", "venice": "Venice",
    "palms": "Palms · Motor Ave", "glendale": "Glendale",
}
NAV_LABEL = {
    "west-la": "West Los Angeles", "brentwood": "Brentwood", "beverly-grove": "Beverly Grove",
    "hollywood": "Hollywood", "venice": "Venice", "palms": "Palms · Motor Avenue",
    "glendale": "Glendale",
}
# the featured six on the board — six areas, real buildings, data-driven figures
FEATURED = ["santa-monica-federal", "kiowa-grand", "croft-retreat",
            "wilcox-melrose", "venice-wave", "broadway-glendale"]


def esc(s):
    return _html.escape(str(s if s is not None else ""), quote=True)


def money(n):
    return None if n is None else "$" + format(int(round(n)), ",")


def cdn(u, tf):
    """Swap the Cloudinary-style transform of a RentCafe CDN URL."""
    if not u:
        return ""
    return re.sub(r"(/image/upload/)[^/]+/", r"\g<1>" + tf + "/", u, count=1)


def local(name):
    return "../assets/img/" + name


def street_line(p):
    return p["address"].split(",")[0].strip()


def beds_range(p):
    lo, hi = p.get("bedsMin"), p.get("bedsMax")
    if lo is None and hi is None:
        return ""
    lo = int(lo or 0)
    hi = int(hi if hi is not None else lo)
    one = lambda n: "Studio" if n == 0 else str(n)
    if lo == hi:
        return "Studio" if lo == 0 else ("%d bed%s" % (lo, "" if lo == 1 else "s"))
    return "%s–%d beds" % (one(lo), hi)


def plural(n, w):
    return w if n == 1 else w + "s"


# ---------------------------------------------------------------- furniture
BRAND_SVG = ('<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false" fill="currentColor">'
             '<polygon points="14,18 34,18 34,72 14,76"/><polygon points="40,18 60,18 60,72 40,76"/>'
             '<polygon points="66,18 86,18 86,72 66,76"/></svg>')
EHO_SVG = ('<svg viewBox="0 0 12 10.608" role="img" aria-label="Equal Housing Opportunity" '
           'fill="currentColor" focusable="false"><path fill-rule="evenodd" clip-rule="evenodd" '
           'd="M5.95263 1.07242L0 4.00926V5.38295H0.663158V9.51979H11.2026V5.38295H11.9921V4.00926L5.95263 '
           '1.07242ZM9.9 8.27242H1.95789V4.49874L5.95263 2.44611L9.9 4.49874V8.27242Z"/><path '
           'fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 5.82505H4.08947V4.49874H7.77632V5.82505Z"/>'
           '<path fill-rule="evenodd" clip-rule="evenodd" d="M7.77632 7.73558H4.08947V6.40926H7.77632V7.73558Z"/></svg>')

IG_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" '
          'd="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7Zm5 3.4a4.6 4.6 0 1 1 0 9.2 4.6 4.6 0 0 1 0-9.2Zm0 2a2.6 2.6 0 1 0 0 5.2 2.6 2.6 0 0 0 0-5.2ZM17.6 5.9a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2Z"/></svg>')
FB_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path '
          'd="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.51 1.49-3.9 3.78-3.9 1.09 0 2.24.2 2.24.2v2.47h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12Z"/></svg>')
YELP_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path '
            'd="m7.6885 15.1415-3.6715.8483c-.3769.0871-.755.183-1.1452.155-.2611-.0188-.5122-.0414-.7606-.213a1.179 1.179 0 0 1-.331-.3594c-.3486-.5519-.3656-1.3661-.3697-2.0004a6.2874 6.2874 0 0 1 .3314-2.0642 1.857 1.857 0 0 1 .1073-.2474 2.3426 2.3426 0 0 1 .1255-.2165 2.4572 2.4572 0 0 1 .1563-.1975 1.1736 1.1736 0 0 1 .399-.2831 1.082 1.082 0 0 1 .4592-.0837c.2355.0016.5139.052.91.1734.0555.0191.1237.0382.1856.0572.3277.1013.7048.2404 1.1499.3987.6863.2404 1.3663.487 2.0463.7397l1.2117.4423c.2217.0807.4363.18.6412.297.174.0984.3273.2298.4512.387a1.217 1.217 0 0 1 .192.4309 1.2205 1.2205 0 0 1-.872 1.4522c-.0468.0151-.0852.0239-.1085.0293l-1.105.2553-.0031-.001zM18.8208 7.565a1.8506 1.8506 0 0 0-.2042-.1754 2.4082 2.4082 0 0 0-.2077-.1394 2.3607 2.3607 0 0 0-.2269-.109 1.1705 1.1705 0 0 0-.482-.0796 1.0862 1.0862 0 0 0-.4498.1263c-.2107.1048-.4388.2732-.742.5551-.042.0417-.0947.0886-.142.133-.2502.2351-.5286.5252-.8599.863a114.6363 114.6363 0 0 0-1.5166 1.5629l-.8962.9293a4.1897 4.1897 0 0 0-.4466.5483 1.541 1.541 0 0 0-.2364.5459 1.2199 1.2199 0 0 0 .0107.4518l.0046.02a1.218 1.218 0 0 0 1.4184.923 1.162 1.162 0 0 0 .1105-.0213l4.7781-1.104c.3766-.087.7587-.1667 1.097-.3631.2269-.1316.4428-.262.5909-.5252a1.1793 1.1793 0 0 0 .1405-.4683c.0733-.6512-.2668-1.3908-.5403-1.963a6.2792 6.2792 0 0 0-1.2001-1.7103zM8.9703.0754a8.6724 8.6724 0 0 0-.83.1564c-.2754.066-.548.1383-.8146.2236-.868.2844-2.0884.8063-2.295 1.8065-.1165.5655.1595 1.1439.3737 1.66.2595.6254.614 1.1889.9373 1.7777.8543 1.5545 1.7245 3.0993 2.5922 4.6457.259.4617.5416 1.0464 1.043 1.2856a1.058 1.058 0 0 0 .1013.0383c.2248.0851.4699.1016.7041.0471a4.3015 4.3015 0 0 0 .0418-.0097 1.2136 1.2136 0 0 0 .5658-.3397 1.1033 1.1033 0 0 0 .079-.0822c.3463-.435.3454-1.0833.3764-1.6134.1042-1.771.2139-3.5423.3009-5.3142.0332-.6712.1055-1.3333.0655-2.0096-.0328-.5579-.0368-1.1984-.3891-1.6563-.6218-.8073-1.9476-.741-2.8523-.6158zm2.084 15.9505a1.1053 1.1053 0 0 0-1.2306-.4145 1.1398 1.1398 0 0 0-.1526.0633 1.4806 1.4806 0 0 0-.2171.1354c-.1992.1475-.3668.3392-.5196.5315-.0386.049-.074.1143-.12.1562l-.7686 1.0573a113.9168 113.9168 0 0 0-1.2913 1.789c-.278.3895-.5184.7184-.7083 1.0094-.036.0547-.0734.116-.1075.1647-.2277.3522-.3566.6092-.4228.8381a1.0945 1.0945 0 0 0-.046.4721c.0211.1655.0768.3246.1635.467.046.0715.0957.1406.1487.207a2.334 2.334 0 0 0 .1754.1825 1.843 1.843 0 0 0 .2108.1732c.5304.369 1.1112.6342 1.722.8391a6.0958 6.0958 0 0 0 1.5716.3004c.091.0046.1821.0025.2728-.006a2.3878 2.3878 0 0 0 .2506-.0351 2.3862 2.3862 0 0 0 .2447-.071 1.1927 1.1927 0 0 0 .4175-.2658c.1127-.113.1994-.249.2541-.3989.0889-.2214.1473-.5026.1857-.92.0034-.0593.0118-.1305.0177-.1958.0304-.3463.0443-.7531.0666-1.2315.0375-.7357.067-1.4681.0903-2.2026 0 0 .0495-1.3053.0494-1.306.0113-.3008.002-.6342-.0814-.9336a1.396 1.396 0 0 0-.1756-.4054zm8.6754 2.0439c-.1605-.176-.3878-.3514-.7462-.5682-.0518-.0288-.1124-.0674-.1684-.1009-.2985-.1795-.658-.3684-1.078-.5965a120.7615 120.7615 0 0 0-1.9427-1.042l-1.1515-.6107c-.0597-.0175-.1203-.0607-.1766-.0878-.2212-.1058-.4558-.2045-.6992-.2498a1.4915 1.4915 0 0 0-.2545-.0265 1.1527 1.1527 0 0 0-.1648.01 1.1077 1.1077 0 0 0-.9227.9133 1.4186 1.4186 0 0 0 .0159.439c.0563.3065.1932.6096.3346.875l.615 1.1526c.3422.65.6884 1.2963 1.0435 1.9406.229.4202.4196.7799.5982 1.078.0338.056.0721.1163.1011.1682.2173.3584.392.584.569.7458.1146.1107.252.195.4026.247.1583.0525.326.071.4919.0546a2.368 2.368 0 0 0 .251-.0435c.0817-.022.1622-.048.241-.0784a1.863 1.863 0 0 0 .2475-.1143 6.1018 6.1018 0 0 0 1.2818-.9597c.4596-.4522.8659-.9454 1.182-1.51.044-.08.0819-.163.1138-.2483a2.49 2.49 0 0 0 .0773-.2411c.0186-.083.033-.1669.0429-.2513a1.188 1.188 0 0 0-.0565-.491 1.0933 1.0933 0 0 0-.248-.4041z"/></svg>')

# "Live at Wiseman" IS the property-search page: one destination, cards left,
# map right, filters live. live.html survives only as a redirect stub for old
# links (see build_live_stub) — there is no second, search-less "Live" page.
NAV = [("company.html", "About Wiseman", "about"),
       ("search.html", "Live at Wiseman", "live"),
       ("careers.html", "Work at Wiseman", "work"),
       ("track.html", "Track Record", "track"),
       ("contact.html", "Contact", "contact")]


def header(base, current=None, home=False, exact=True):
    # `exact=False` marks the SECTION, not the page: buildings.html and
    # neighborhoods.html sit under Live at Wiseman but are not search.html,
    # so they get aria-current="true" rather than the untrue "page".
    items = []
    for href, label, key in NAV:
        cur = (' aria-current="%s"' % ("page" if exact else "true")) if key == current else ""
        items.append('      <a href="%s%s"%s>%s</a>' % (base, href, cur, label))
    brand_cur = ' aria-current="page"' if home else ""
    # The band is FULL PAGE WIDTH (no wrap/wrap-n on <header>); the inner
    # .hd-in carries the same wrap + wrap-n the footer and every section use,
    # so the header content sits on exactly the page gutter at every width.
    return """<header class="hd" id="hd">
  <div class="hd-in wrap wrap-n">
  <a class="brand" href="{base}index.html" aria-label="Wiseman Residential, home"{brand_cur}>
    {mark}
    <b>Wiseman Residential</b>
  </a>
  <nav class="hnav" aria-label="Primary">
{items}
  </nav>
  <div class="hd-cta">
    <a class="btn btn-teal" href="{base}search.html">Find a home <span class="ar" aria-hidden="true">&rarr;</span></a>
    <button class="mbtn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
  </div>
</header>""".format(base=base, brand_cur=brand_cur, mark=BRAND_SVG, items="\n".join(items))


def footer(base, groups):
    n = {k: len(v) for k, v in groups.items()}
    areas = "\n".join(
        '        <li><a href="%sneighborhoods/%s.html">%s <span class="ct tnum">%d</span></a></li>'
        % (base, k, NAV_LABEL[k], n[k]) for k in AREA_ORDER)
    return """<footer class="ft" id="site-map" data-menu-inert>
  <div class="wrap wrap-n">
    <div class="ft-top">
      <div class="ft-brand">
        {mark}
        <div class="wm">Wiseman Residential</div>
        <div class="tag">Los Angeles living, managed wisely.</div>
        <div class="addr">1520 Federal Ave, Los Angeles, CA 90025<br><a href="tel:+13104733000">+1 310-473-3000</a></div>
      </div>
      <div class="ft-col">
        <h2>Company</h2>
        <ul>
          <li><a href="{base}company.html">About Wiseman</a></li>
          <li><a href="{base}search.html">Live at Wiseman</a></li>
          <li><a href="{base}careers.html">Work at Wiseman</a></li>
          <li><a href="{base}track.html">Track Record</a></li>
          <li><a href="{base}contact.html">Contact</a></li>
          <li><a href="{base}residents.html">Residents</a></li>
        </ul>
      </div>
      <div class="ft-col">
        <h2>Neighbourhoods</h2>
        <ul>
{areas}
        </ul>
      </div>
      <div class="ft-col">
        <h2>Find a home</h2>
        <ul>
          <li><a href="{base}buildings.html">All {total} buildings</a></li>
          <li><a href="{base}neighborhoods.html">The seven areas</a></li>
          <li><a href="{resident}" rel="noopener">Resident login</a></li>
          <li><a href="{applicant}" rel="noopener">Applicant login</a></li>
        </ul>
      </div>
    </div>
    <div class="ft-base">
      <div class="lg">
        <p class="eho">{eho}<span>Equal Housing Opportunity</span></p>
        <span class="social"><a href="{ig}" rel="noopener" aria-label="Instagram">{ig_svg}</a><a href="{fb}" rel="noopener" aria-label="Facebook">{fb_svg}</a><a href="{yelp}" rel="noopener" aria-label="Yelp">{yelp_svg}</a></span>
      </div>
      <p class="cp">&copy; 2026 Wiseman Residential</p>
    </div>
    <p class="ft-note"><a href="{base}privacy.html">Privacy Policy</a> &middot; <a href="{base}accessibility.html">Accessibility</a> &middot; <a href="{base}privacy-choices.html">Your Privacy Choices</a> &middot; <a href="{base}sitemap.html">Site Map</a> &middot; Every figure here is a point-in-time snapshot of the live leasing system. No DRE number is published pending the client&rsquo;s confirmation of the responsible broker entity.</p>
  </div>
</footer>""".format(base=base, mark=BRAND_SVG, areas=areas, total=TOTAL, eho=EHO_SVG,
                    resident=RESIDENT, applicant=APPLICANT, fb=FB, ig=IG, yelp=YELP,
                    ig_svg=IG_SVG, fb_svg=FB_SVG, yelp_svg=YELP_SVG)


def mnav(base):
    # "Live at Wiseman" already IS search.html, so the old duplicate
    # "Find a home" row is gone; the two hub pages take its place.
    items = ([(h, l) for h, l, k in NAV]
             + [("buildings.html", "Every building"), ("residents.html", "Residents")])
    lis = "\n".join(
        '      <li><a href="%s%s"><span class="mn-no tnum">%02d</span><span>%s</span></a></li>'
        % (base, h, i + 1, l) for i, (h, l) in enumerate(items))
    return """<nav class="mnav" id="mnav" aria-label="Menu">
  <div class="mnav-in">
    <ul class="mnav-list">
{lis}
    </ul>
    <div class="mfoot">
      <p>1520 Federal Ave, Los Angeles, CA 90025</p>
      <p><a href="tel:+13104733000">+1 310-473-3000</a> &middot; Leasing</p>
      <p><a href="{resident}" rel="noopener">Resident login</a> &middot; <a href="{applicant}" rel="noopener">Apply</a></p>
    </div>
  </div>
</nav>""".format(lis=lis, resident=RESIDENT, applicant=APPLICANT)


# The curtain carries a centred brand lockup on the deep ground, the way the
# Motor Tides concept does: mark, name, and a letterspaced sub beneath it.
CURTAIN = """<div class="pt" aria-hidden="true">
  <div class="ptmark">
    %s
    <span class="pt-name">Wiseman Residential</span>
    <span class="pt-sub">Los Angeles</span>
  </div>
</div>""" % BRAND_SVG


# ---------------------------------------------------------------- live.html stub
# The old portfolio door is retired: "Live at Wiseman" IS search.html, the one
# page with the filter bar, the cards on the left and the map on the right.
# This file stays behind purely so an old link still lands somewhere real —
# meta refresh first (works with JS off), canonical for crawlers, a
# location.replace for speed, and a visible link if all three are blocked.
LIVE_STUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Live at Wiseman &mdash; find a home in Los Angeles</title>
<link rel="canonical" href="search.html">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url=search.html">
<meta name="theme-color" content="#F3F0E7">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E%3Crect%20width='100'%20height='100'%20fill='%23F3F0E7'/%3E%3Cg%20fill='%23169BAC'%3E%3Cpolygon%20points='14,18%2034,18%2034,72%2014,76'/%3E%3Cpolygon%20points='40,18%2060,18%2060,72%2040,76'/%3E%3Cpolygon%20points='66,18%2086,18%2086,72%2066,76'/%3E%3C/g%3E%3C/svg%3E">
<style>
  html,body{margin:0;height:100%;background:#F3F0E7;color:#0E1520}
  body{display:grid;place-items:center;font:400 1rem/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-align:center;padding:24px}
  a{color:#0B5E68}
</style>
<script>location.replace('search.html' + location.search + location.hash);</script>
</head>
<body>
<p>Live at Wiseman has moved to the property search.<br><a href="search.html">Find a home &rarr;</a></p>
</body>
</html>
"""


# ---------------------------------------------------------------- page head/tail
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Prata'
         '&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;'
         '1,6..72,500&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">')


def head(title, desc, img, extra="", ld="", base=""):
    return """<!doctype html>
<html lang="en" data-base="{base}" data-data="../data/wiseman.json" data-index="../data/index.json">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F3F0E7">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E%3Crect%20width='100'%20height='100'%20fill='%23F3F0E7'/%3E%3Cg%20fill='%23169BAC'%3E%3Cpolygon%20points='14,18%2034,18%2034,72%2014,76'/%3E%3Cpolygon%20points='40,18%2060,18%2060,72%2040,76'/%3E%3Cpolygon%20points='66,18%2086,18%2086,72%2066,76'/%3E%3C/g%3E%3C/svg%3E">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wiseman Residential">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://resource.rentcafe.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<link rel="stylesheet" href="../core/base.css?v={ver}">
<link rel="stylesheet" href="../core/map.css?v={ver}">{extra}
<link rel="stylesheet" href="style.css?v={ver}">
<script>(function(d){{var r=d.documentElement;r.classList.add('js');if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{r.classList.add('js-pt');setTimeout(function(){{r.classList.remove('js-pt');}},1500);}}}})(document);</script>{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""".format(base=base, title=title, desc=esc(desc), img=esc(img), fonts=FONTS, ver=VER, extra=extra, ld=ld)


def tail(groups, extra_js="", boot=""):
    return """
{footer}

{mnav}

{curtain}

<script src="../core/core.js?v={ver}" defer></script>
<script src="../core/map.js?v={ver}" defer></script>{extra}
<script src="app.js?v={ver}" defer></script>{boot}
</body>
</html>
""".format(footer=footer("", groups), mnav=mnav(""), curtain=CURTAIN, ver=VER, extra=extra_js, boot=boot)


HOME_BOOT = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  /* The history rail is the only rail on the home page. rail.js is what makes
     it reachable without a mouse — it gives the <ol> tabindex="0" and binds
     ArrowLeft/Right, Home and End, labels and disables the arrows at each end,
     and scrolls a Tab-focused chapter into view. Without this call the row is
     a plain overflow box that a keyboard cannot move. */
  if (window.WR && WR.rails) WR.rails();
});
</script>"""


ORG_LD = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Wiseman Residential",
  "slogan": "Los Angeles Living, Managed Wisely.",
  "telephone": "+1-310-473-3000",
  "address": {"@type": "PostalAddress", "streetAddress": "1520 Federal Ave",
    "addressLocality": "Los Angeles", "addressRegion": "CA", "postalCode": "90025", "addressCountry": "US"},
  "areaServed": ["West Los Angeles", "Brentwood", "Beverly Grove", "Hollywood", "Venice",
    "Palms \\u00b7 Motor Avenue", "Glendale"],
  "sameAs": ["%s", "%s", "%s"]
}
</script>""" % (FB, IG, YELP)


# ---------------------------------------------------------------- featured cell
def featured_card(p, delay):
    beds = beds_range(p)
    if p["no"] == FLAG_NO:
        fig = '<span class="flag">Now leasing</span>'
    elif p.get("priceMin") is not None:
        fig = '<span class="p"><span class="from">from</span>%s</span>' % money(p["priceMin"])
    else:
        fig = '<span class="p">Call for rents</span>'
    # The card paints ~400 CSS px, so a 2x screen wants ~800 real pixels. The
    # RentCafe originals measure 2048px, so the larger ask never upscales —
    # we were simply requesting too few pixels and letting the browser stretch.
    img = cdn(p["image"], "q_auto,f_auto,w_760")
    img2x = cdn(p["image"], "q_auto,f_auto,w_1400")
    return """    <a class="card rv" data-d="{d}" href="buildings/{path}.html">
      <span class="ph rvi"><img src="{img}" srcset="{img} 760w, {img2x} 1400w" sizes="(min-width:1000px) 32vw, (min-width:640px) 46vw, 90vw" alt="{name}, {area}." loading="lazy" decoding="async"></span>
      <span class="info">
        <span class="area">{label}</span>
        <span class="nm">{name}</span>
        <span class="facts"><span class="b">{beds}</span>{fig}</span>
      </span>
    </a>""".format(d=delay, path=p["path"], img=esc(img), img2x=esc(img2x), name=esc(p["short"]),
                   area=esc(p["area"]), label=esc(CARD_LABEL[p["areaKey"]]), beds=esc(beds), fig=fig)


def featured_grid(props_by_slug):
    cards = []
    for i, slug in enumerate(FEATURED):
        p = props_by_slug.get(slug)
        if not p:
            continue
        cards.append(featured_card(p, (i % 3) + 1))
    return "\n".join(cards)


# ---------------------------------------------------------------- build
def main():
    data = json.load(open(DATA, encoding="utf-8"))
    props = data["properties"]
    areas = data["areas"]
    by_slug = {p["slug"]: p for p in props}
    by_no = {p["no"]: p for p in props}
    groups = {k: [p for p in props if p["areaKey"] == k] for k in AREA_ORDER}
    area_counts = {k: len(v) for k, v in groups.items()}
    streets_total = len({p["street"] for p in props})
    four_plus = sum(1 for p in props if (p.get("bedsMax") or 0) >= 4)
    hero = by_no["001"]

    # ============================================================== index.html
    feat = featured_grid(by_slug)
    page = head(
        title="Wiseman Residential &mdash; Los Angeles living, managed wisely",
        desc=("Wiseman owns, develops and manages all 72 of its apartment buildings across seven "
              "parts of Los Angeles, each with its own on-site office, leasing line and maintenance "
              "team. Los Angeles living, managed wisely."),
        img="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1200/s3/2/9707/rsz_2motor_jpeg_1.jpg",
        extra='<link rel="stylesheet" href="../core/rail.css?v=%s">' % VER,
        ld=ORG_LD)
    page += header("", home=True)
    page += """
<main id="main">

  <!-- 1. the living monogram — WISEMAN cut from a Los Angeles building.
       A full-bleed exterior photograph shows through the letterforms; the warm
       cream ground fills everything around them. The word IS the h1; the SVG
       carries no text a screen reader needs, so the accessible name lives in
       the .vh span.

       THE THREE BEATS (style.css "HERO — LIVING MONOGRAM", app.js "monogram").
         1  load    the photograph fills the whole viewport, unmasked, for ~1s,
                    breathing on a very slow alternating scale.
         2  clip-in the cream veil + teal tone fade up while the letterforms
                    scale down into place, so the image survives only inside
                    WISEMAN. ~1.05s on the one Motor Tides ease.
         3  scroll  .hero-runway gives the sticky stage a viewport of runway;
                    scrolling re-opens the frame (letters scale out, veil and
                    tone fade off) before the stats ribbon arrives.
       Beats 1-2 are pure CSS keyframes with `both` fill, so they run on load
       without a scroll observer and settle even in a headless render. Nothing
       is gated on JS: with no .js class, or under prefers-reduced-motion, the
       hero paints its settled end state and the runway collapses.

       VIDEO HOOK — the hero is already video-ready and ships as a still.
       To swap in motion: drop a file at  assets/video/hero-la.mp4  and put its
       path in the video's data-src below (one line, nothing else changes):
           data-src="../assets/video/hero-la.mp4"
       app.js only assigns .src when data-src is non-empty, fades the clip in on
       `playing`, and hides it again on `error` — so the wr03 still underneath
       stays the fallback at every step. Left empty, preload="none" + no src
       means the element costs nothing. -->
  <div class="hero-runway">
  <section class="hero-mono" aria-label="Wiseman Residential — Los Angeles living, managed wisely">
    <div class="mono-stage" aria-hidden="true">
      <img class="mono-photo" src="../assets/img/wr03.jpg" alt="" width="1800" height="1200" fetchpriority="high" decoding="async">
      <video class="mono-video" muted loop playsinline preload="none" poster="../assets/img/wr03.jpg" data-src=""></video>
      <span class="mono-duo"></span>
      <span class="mono-haze"></span>
      <span class="mono-tone"></span>
    </div>
    <h1 class="mono-word">
      <span class="vh">Wiseman Residential</span>
      <svg class="mono-veil" width="100%" height="100%" preserveAspectRatio="none" aria-hidden="true" focusable="false">
        <defs>
          <mask id="mono-mask" maskUnits="userSpaceOnUse">
            <rect width="100%" height="100%" fill="#fff"></rect>
            <g class="mono-type"><text class="mono-letters" x="50%" y="40%" text-anchor="middle" dominant-baseline="middle" fill="#000">WISEMAN</text></g>
          </mask>
        </defs>
        <rect width="100%" height="100%" fill="#F3F0E7" mask="url(#mono-mask)"></rect>
      </svg>
    </h1>
    <div class="mono-content">
      <p class="mono-tag">Los&nbsp;Angeles&nbsp;living, managed&nbsp;wisely.</p>
      <p class="mono-lead">Owner, developer and manager of {total} apartment buildings across seven parts of Los&nbsp;Angeles.</p>
      <div class="mono-cta">
        <a class="btn btn-solid" href="search.html">Find a home <span class="ar" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn-line" href="company.html">Inside Wiseman</a>
      </div>
    </div>
    <p class="mono-loc" aria-hidden="true"><span>Los Angeles</span></p>
    <span class="mono-scroll" aria-hidden="true"></span>
  </section>
  </div>

  <!-- 2. stats ribbon — calm scroll reveal only (no count-up); four figures
       read as one consistent set: 72 · 7 · 52 · 5. -->
  <div class="stats">
    <div class="wrap wrap-n">
      <div class="row">
        <div class="stat rv" data-d="1"><div class="n tnum">{total}</div><div class="k">Apartment buildings, owned and&nbsp;managed</div></div>
        <div class="stat rv" data-d="2"><div class="n tnum">7</div><div class="k">Parts of Los Angeles, from Sawtelle to&nbsp;Glendale</div></div>
        <div class="stat rv" data-d="3"><div class="n tnum">{streets}</div><div class="k">Named streets across the Westside and the&nbsp;Valley</div></div>
        <div class="stat rv" data-d="4"><div class="n tnum">5</div><div class="k">Bedrooms at the largest homes &mdash; {four} buildings go to four or more</div></div>
      </div>
    </div>
  </div>

  <!-- 3. what Wiseman does -->
  <section class="band wrap wrap-n" id="what">
    <div class="band-head">
      <p class="eyebrow rv">What Wiseman does</p>
      <h2 class="rv" data-d="1">One company, from the drawing to the&nbsp;door.</h2>
      <p class="rv" data-d="2">The industry splits the work; Wiseman does all of it, and keeps what it builds. The person who answers about a repair works for the company that poured the&nbsp;foundation.</p>
    </div>
    <div class="dolayout">
      <div class="pillars">
        <div class="pillar rv" data-d="1"><div class="idx tnum">01</div><div><h3>Develop</h3><p>New apartments where the city needs housing &mdash; most recently the Motor Avenue corridor in&nbsp;Palms.</p></div></div>
        <div class="pillar rv" data-d="2"><div class="idx tnum">02</div><div><h3>Build</h3><p>Built in-house, through the family&rsquo;s licensed California construction&nbsp;arm.</p></div></div>
        <div class="pillar rv" data-d="3"><div class="idx tnum">03</div><div><h3>Own</h3><p>Held, not flipped &mdash; seventy-two buildings on our own&nbsp;books.</p></div></div>
        <div class="pillar rv" data-d="4"><div class="idx tnum">04</div><div><h3>Manage, on site</h3><p>Each building keeps its own office, leasing line and maintenance&nbsp;team.</p></div></div>
      </div>
      <figure class="dofig rvi">
        <img src="{do_src}" alt="A blue-glass Wiseman apartment elevation against a clean sky." loading="lazy" decoding="async">
      </figure>
    </div>
  </section>

  <!-- 4. the on-site model -->
  <section class="promise" data-hd="light">
    <div class="band wrap wrap-n">
      <div class="grid">
        <div>
          <p class="eyebrow rv" style="display:block;margin-bottom:1.4rem">The on-site model</p>
          <p class="statement rv" data-d="1">Repairs and questions go to the building&rsquo;s <em>own office</em> &mdash; not a call centre in another&nbsp;city.</p>
          <p class="trust rv" data-d="2">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
            <span>The name on the door is a person you can find &mdash; the one thing residents tell us they value&nbsp;most.</span>
          </p>
        </div>
        <figure class="promise-fig rvi">
          <img src="{onsite_src}" alt="A planted Wiseman courtyard in morning light." loading="lazy" decoding="async">
        </figure>
      </div>
    </div>
  </section>

  <!-- 5. live at Wiseman -->
  <section class="band wrap wrap-n" id="live">
    <div class="live-top">
      <div>
        <p class="eyebrow rv">Live at Wiseman</p>
        <h2 class="rv" data-d="1">Six of seventy-two, across the&nbsp;city.</h2>
      </div>
      <p class="aside rv" data-d="2">From a Sawtelle studio to a Beverly Grove four-bedroom &mdash; each links straight to today&rsquo;s plans and&nbsp;rents.</p>
    </div>
    <div class="communities">
{feat}
    </div>
    <div class="live-foot">
      <a class="btn btn-teal" href="search.html">Find a home <span class="ar" aria-hidden="true">&rarr;</span></a>
      <a class="btn btn-line" href="buildings.html">All {total} buildings</a>
      <span class="note">Rents are a point-in-time snapshot from the live leasing feed, not a quote.</span>
    </div>
  </section>

  <!-- 6. portfolio map -->
  <section class="band wrap wrap-n" id="map" style="padding-top:0">
    <div class="band-head" style="margin-bottom:clamp(24px,3vh,40px)">
      <p class="eyebrow rv">The portfolio</p>
      <h2 class="rv" data-d="1">Every building, on one&nbsp;map.</h2>
    </div>
    <div class="homemap">
      <div class="mapbox" id="portfolio-map" data-map='{{"scope":"all","bubbles":true,"theme":"light","label":"Map of all {total} Wiseman buildings across Los Angeles"}}'></div>
      <p class="map-foot"><span><span class="tnum">{total}</span> buildings &middot; one dot per building, gathered into area counts as you zoom&nbsp;out</span><span>The list stays complete with the map switched&nbsp;off</span></p>
    </div>
  </section>

  <!-- 7. about + values -->
  <section class="promise" id="about">
    <div class="band wrap wrap-n">
      <div class="band-head">
        <p class="eyebrow rv">About Wiseman</p>
        <h2 class="rv" data-d="1">A family-run Los Angeles apartment&nbsp;company.</h2>
        <p class="rv" data-d="2">Founded by Isaac Cohanzad; building, owning and managing apartments across the Westside and into the&nbsp;Valley.</p>
      </div>
      <div class="values">
        <div class="value rv" data-d="1"><h3>Our story <span class="chip">[CLIENT]</span></h3><p>Founding year and milestones are the client&rsquo;s to confirm &mdash; no date shown until they&nbsp;do.</p></div>
        <div class="value rv" data-d="2"><h3>Leadership <span class="chip">[CLIENT]</span></h3><p>Isaac Cohanzad, founder; any further team or biography from the&nbsp;company.</p></div>
        <div class="value rv" data-d="3"><h3>Core values <span class="chip">[CLIENT]</span></h3><p>The principles the company puts its name to &mdash; written by&nbsp;Wiseman.</p></div>
      </div>

      <!-- 8. track record teaser -->
      <div class="track" id="track">
        <figure class="track-fig rvi">
          <img src="{track_src}" alt="Motor Tides, the seven-storey Wiseman flagship on Motor Avenue in Palms." loading="lazy" decoding="async">
        </figure>
        <div>
          <p class="eyebrow rv">Track Record</p>
          <h2 class="rv" data-d="1">What we&rsquo;re building&nbsp;next.</h2>
          <p class="rv" data-d="2">Motor Tides brings 107 homes to Motor Avenue in Palms &mdash; seven storeys, one to four bedrooms, a rooftop deck, now&nbsp;leasing.</p>
          <p class="cite rv" data-d="3">Pipeline figures reported by Urbanize LA and The Real Deal; totals beyond the public record appear only as <span class="chip">[CLIENT]</span>. <a href="track.html" style="color:var(--accent-ink)">The full track record &rarr;</a></p>
        </div>
      </div>
    </div>
  </section>

  <!-- 9. history ------------------------------------------------------------
       Morgan's "Explore Our History" is the model the client pointed at. Two
       things it does are worth taking and one is not.

       TAKE: the year rail on its own line. Morgan renders each slide's year as
       its pagination control, sitting on a dashed rule that the labels knock
       out — one cheap graphic that says "continuous span" and "discrete stops"
       at once, and it gives direct access to any chapter instead of stepping
       through with arrows. Here the years are real anchors (href="#h-..."), so
       they deep-link and still work with JavaScript off; app.js upgrades them
       to scroll the rail instead of the page.

       TAKE: an image per entry. Twelve photographs are most of why Morgan's
       page feels substantiated.

       DO NOT TAKE: its even-spaced rail as a measure of time — that device is
       powered by a left end reading 1925, and over a shorter record it invites
       counting the gaps. Chapters carrying date RANGES absorb what bare years
       expose. Nor its stock photography: two of Morgan's twelve cards are
       Pexels, inside the one section whose whole job is to be documentary.

       So every photograph here is a real Wiseman building, captioned as what
       it actually is. Two chapters have no honest photograph — a dispute
       between four records, and a 2010 magazine profile — and rather than
       reach for stock they carry a typographic plate holding the best piece
       of text on the page. The gap is the point. -->
  <section class="band wrap wrap-n" id="history" aria-labelledby="history-h">
    <div class="band-head">
      <p class="eyebrow rv">Our History</p>
      <h2 class="rv" data-d="1" id="history-h">The record, as it&nbsp;stands.</h2>
      <p class="rv" data-d="2">Five chapters, each resting on a document anyone can&nbsp;check.</p>
    </div>

    <div class="tl-rail rv" data-rail data-rail-label="Company history, five chapters from 1980 to today">
      <div class="tl-index">
        <nav class="tl-years" aria-label="Jump to a chapter">
          <a class="tl-yr" href="#h-origins" aria-current="true"><span class="tnum">1980&ndash;87</span></a>
          <a class="tl-yr" href="#h-2010"><span class="tnum">2010</span></a>
          <a class="tl-yr" href="#h-floorplans"><span class="tnum">2013&ndash;23</span></a>
          <a class="tl-yr" href="#h-palms"><span class="tnum">2018&ndash;24</span></a>
          <a class="tl-yr" href="#h-now"><span class="tnum">2025&ndash;now</span></a>
        </nav>
        <div class="rail-nav">
          <button class="rail-btn prev" data-rail-prev aria-label="Previous chapter"></button>
          <button class="rail-btn next" data-rail-next aria-label="Next chapter"></button>
        </div>
      </div>
      <ol class="tl rail-track" data-rail-track>
      <li class="tl-e" id="h-origins">
        <div class="tl-plate" aria-hidden="true">
          <span class="tnum">1980</span><span class="tnum">1982</span>
          <span class="tnum">1985</span><span class="tnum">1987</span>
        </div>
        <div class="tl-c">
          <h3>Four records, four founding&nbsp;years <span class="chip">[CLIENT]</span></h3>
          <p>LinkedIn says 1980. Contractor licence <span class="tnum">417744</span> carries an issue date of February&nbsp;1982. Wiseman&rsquo;s own Archinect profile says 1985. The Better Business Bureau has June&nbsp;1987. No year is printed here until Wiseman confirms&nbsp;one.</p>
          <p class="tl-s">LinkedIn &middot; CSLB &middot; Archinect &middot; BBB</p>
        </div>
      </li>

      <li class="tl-e" id="h-2010">
        <div class="tl-plate quote" aria-hidden="true">
          <p>&ldquo;My father built apartment buildings throughout my&nbsp;childhood.&rdquo;</p>
        </div>
        <div class="tl-c">
          <h3>A Westside builder, in his own&nbsp;words</h3>
          <p>The <em>Los Angeles Business Journal</em> profiled Isaac Cohanzad, then president of Wiseman Development Co., with 63 homes rising on Santa Monica Boulevard and 34 in&nbsp;Glendale.</p>
          <p class="tl-s">Los Angeles Business Journal, 29&nbsp;August&nbsp;2010</p>
        </div>
      </li>

      <li class="tl-e" id="h-floorplans">
        <figure class="tl-fig">
          <img src="{selby}" srcset="{selby} 760w, {selby2x} 1400w" sizes="(min-width:861px) 30vw, 90vw"
               alt="Selby Venti, a Wiseman building on Selby Avenue in West Los Angeles with four- and five-bedroom homes."
               loading="lazy" decoding="async" width="760" height="570">
        </figure>
        <div class="tl-c">
          <h3>One claim held for eleven&nbsp;years</h3>
          <p>Wiseman put its portfolio online in 2013. Through two rebuilds of the site one sentence survived verbatim &mdash; that its three- and four-bedroom plans are rare. The feed still bears it out: <span class="tnum">17</span> buildings offer four bedrooms, <span class="tnum">5</span> go to&nbsp;five.</p>
          <p class="tl-s">Internet Archive captures 2014&ndash;2025 &middot; live leasing feed</p>
        </div>
      </li>

      <li class="tl-e" id="h-palms">
        <figure class="tl-fig">
          <img src="{midway}" srcset="{midway} 760w, {midway2x} 1400w" sizes="(min-width:861px) 30vw, 90vw"
               alt="Motor Midway, the 68-apartment Wiseman building at 3659 South Motor Avenue in Palms."
               loading="lazy" decoding="async" width="760" height="570">
        </figure>
        <div class="tl-c">
          <h3>Ground-up, and mostly in&nbsp;Palms</h3>
          <p>Filings on Lincoln Boulevard, then East Venice. Motor Avenue broke ground in 2021 and again in 2022. Over the same stretch the trade press put the portfolio at around thirty buildings, then nearly&nbsp;seventy.</p>
          <p class="tl-s">Urbanize LA &middot; The Real Deal, 2022 and&nbsp;2024</p>
        </div>
      </li>

      <li class="tl-e" id="h-now">
        <figure class="tl-fig">
          <img src="{tides}" srcset="{tides} 760w, {tides2x} 1400w" sizes="(min-width:861px) 30vw, 90vw"
               alt="Motor Tides, the seven-storey Wiseman building at 3557 Motor Avenue in Palms."
               loading="lazy" decoding="async" width="760" height="570">
        </figure>
        <div class="tl-c">
          <h3>Seven storeys on Motor&nbsp;Avenue</h3>
          <p>Motor Tides finished in 2026 &mdash; <span class="tnum">104</span> apartments with three accessory dwellings, <span class="tnum">107</span> homes in all. In March, Wiseman filed for <span class="tnum">490</span> more on Venice&nbsp;Boulevard.</p>
          <p class="tl-s">Urbanize LA, May and March&nbsp;2026</p>
        </div>
      </li>
      </ol>
    </div>

    <p class="cite rv">Dates are sourced to public records and to reporting, not to marketing copy. The founding year, the number of homes built to date and anything about the family behind the firm are the company&rsquo;s to confirm. <span class="chip">[CLIENT]</span></p>
  </section>

</main>
""".format(total=TOTAL, streets=streets_total, four=four_plus,
           hero_src=esc(cdn(hero["image"], "q_auto,f_auto,w_1200")),
           do_src=esc(local("wr19.jpg")), onsite_src=esc(local("wr06.jpg")),
           track_src=esc(local("wr13.jpg")), feat=feat,
           selby=esc(cdn(by_slug["selby-venti"]["image"], "q_auto,f_auto,w_760,h_570,c_fill,g_auto")),
           selby2x=esc(cdn(by_slug["selby-venti"]["image"], "q_auto,f_auto,w_1400,h_1050,c_fill,g_auto")),
           midway=esc(cdn(by_slug["motor-midway"]["image"], "q_auto,f_auto,w_760,h_570,c_fill,g_auto")),
           midway2x=esc(cdn(by_slug["motor-midway"]["image"], "q_auto,f_auto,w_1400,h_1050,c_fill,g_auto")),
           tides=esc(cdn(by_slug["motor-tides"]["image"], "q_auto,f_auto,w_760,h_570,c_fill,g_auto")),
           tides2x=esc(cdn(by_slug["motor-tides"]["image"], "q_auto,f_auto,w_1400,h_1050,c_fill,g_auto")))
    page += tail(groups,
                 extra_js='\n<script src="../core/rail.js?v=%s" defer></script>' % VER,
                 boot=HOME_BOOT)
    write("index.html", page)

    # ======================================================= live.html (stub)
    # "Live at Wiseman" is now the property-search page itself. Nothing on the
    # site links here any more; the file stays as a redirect so old bookmarks,
    # shared links and any cached search result still land on the real page.
    write("live.html", LIVE_STUB)


    # ============================================================== track.html
    tp = head(
        title="Track Record &mdash; what Wiseman is building",
        desc=("Wiseman's development pipeline along the Motor Avenue corridor and across the "
              "Westside: Motor Tides (107 homes, now leasing) and the filed and proposed projects, "
              "each cited to Urbanize LA and The Real Deal."),
        img=esc(local("wr13.jpg")),
        extra='\n<link rel="stylesheet" href="../core/editorial.css?v=%s">' % VER)
    tp += header("", current="track")
    PIPE = [
        ("3659 South Motor Avenue", "Sixty-eight apartments, a block north on the same street.", "Built", "Urbanize LA"),
        ("3418&ndash;3554 South Motor Avenue", "Two hundred apartments proposed, twenty-two set aside for extremely-low-income households.", "Proposed", "Urbanize LA"),
        ("9000&ndash;9020 Venice Boulevard", "Four hundred and ninety apartments filed, sixty-four of them set aside.", "Filed", "Urbanize LA / The Real Deal"),
        ("11261 Santa Monica Boulevard", "One hundred and nineteen apartments. Current status to confirm. <span class=\"chip\">[CLIENT]</span>", "Reported", "Urbanize LA / The Real Deal"),
        ("1600 East Venice Boulevard", "Seventy-seven apartments. Current status to confirm. <span class=\"chip\">[CLIENT]</span>", "Reported", "Urbanize LA / The Real Deal"),
        ("1808 Lincoln Boulevard", "Fifty apartments. Current status to confirm. <span class=\"chip\">[CLIENT]</span>", "Reported", "Urbanize LA / The Real Deal"),
    ]
    rows = "\n".join(
        '      <li class="ed-row"><h3>%s</h3><div><p>%s</p></div><span class="ed-state">%s</span><span class="ed-cite">%s</span></li>'
        % (a, d, s, c) for a, d, s, c in PIPE)
    tp += """
<main id="main">
<div class="ed">

  <section class="fbhero" data-hd="dark" style="--pos:50% 44%">
    <div class="fbimg"><img src="{hero}" alt="Motor Tides, the seven-storey Wiseman building on Motor Avenue in Palms." width="2000" height="1333" fetchpriority="high" decoding="async"></div>
    <div class="fb-in wrap wrap-n">
      <p class="tagline">Track Record</p>
      <h1>What we&rsquo;re building on <em>Motor&nbsp;Avenue</em>.</h1>
      <p class="sub">A corridor of new apartments in Palms, minutes from Culver City &mdash; and more filed across the&nbsp;Westside.</p>
    </div>
    <p class="fb-cred">Palms &middot; Motor Avenue</p>
  </section>

  <section class="ed-sec wrap wrap-n">
    <div class="ed-band">
      <figure class="ed-fig rvi" style="--pos:50% 44%"><img src="{mt}" alt="Motor Tides on Motor Avenue in Palms." width="1400" height="1750" loading="lazy" decoding="async"><figcaption>Motor Tides &middot; Palms</figcaption></figure>
      <div class="ed-copy rv">
        <p class="ed-eyebrow">Now leasing</p>
        <h2 class="ed-h2">Motor Tides.</h2>
        <p>Seven storeys and 107 homes &mdash; 104 apartments plus three accessory dwelling units &mdash; at 3557 Motor Avenue, 90034, in the City of Los Angeles, minutes from Culver City. One to four bedrooms, a rooftop deck and a fitness centre. Architect: Uriu &amp; Associates.</p>
        <p>The building&rsquo;s own page carries today&rsquo;s plans and its leasing line. <span class="chip">[CLIENT]</span> confirms move-in dates and rents.</p>
      </div>
    </div>
  </section>

  <section class="ed-sec wrap wrap-n" style="padding-top:0">
    <p class="ed-eyebrow">Still building here</p>
    <h2 class="ed-h2">What is under way, and who reported&nbsp;it.</h2>
    <p class="ed-lede" style="margin-top:16px">Every line is as the trade press reported it; the citation stays on the line. Any total not in the public record &mdash; dollars invested, jobs, unit counts beyond the cited filings &mdash; is a <span class="chip">[CLIENT]</span> until confirmed.</p>
    <ul class="ed-rows rv" style="margin-top:32px">
{rows}
    </ul>
  </section>

  <section class="ed-sec wrap wrap-n" style="padding-top:0">
    <p class="ed-note">Wiseman&rsquo;s development model is teardown-and-rebuild; the site reports what is filed and built, and does not make preservation or displacement claims. Nothing about active litigation appears here.</p>
    <p style="margin-top:22px"><a class="ed-link" href="search.html">Find a home today <svg viewBox="0 0 26 8" aria-hidden="true"><path d="M0 4h24M20 1l4 3-4 3"/></svg></a></p>
  </section>

</div>
</main>
""".format(hero=esc(local("wr13.jpg")), mt=esc(local("wr13.jpg")), rows=rows)
    tp += tail(groups)
    write("track.html", tp)

    # ============================================================== buildings.html
    build_buildings(groups, areas, area_counts, streets_total, props)

    # ============================================================== neighborhoods.html
    build_neighborhoods(groups, areas, area_counts)

    # ============================================================== search.html
    build_search(groups, props)

    # ============================================================== sitemap.html
    build_sitemap(groups, areas, props)

    # ============================================================== editorial shells
    for fn, title, desc, cur in [
        ("company.html", "About Wiseman &mdash; owner, developer, manager",
         "What Wiseman does: one Los Angeles company owns, develops and manages all 72 buildings, each with its own on-site office and leasing line.", "about"),
        ("careers.html", "Work at Wiseman &mdash; careers",
         "Careers at Wiseman: on-site management, maintenance, leasing and the corporate office at 1520 Federal Ave.", "work"),
        ("contact.html", "Contact Wiseman Residential",
         "Reach Wiseman by intent: leasing, current residents, maintenance, development, careers and press. One number, the corporate office, and a routed form.", "contact"),
        ("residents.html", "Residents &mdash; Wiseman Residential",
         "For Wiseman residents: report a repair without a login, pay rent, security deposits, moving in, and where the rules live.", None),
        ("privacy.html", "Privacy Policy &mdash; Wiseman Residential",
         "How this website handles the information you give it, and the California privacy rights that come with it.", None),
        ("accessibility.html", "Accessibility &mdash; Wiseman Residential",
         "How Wiseman builds this website to be usable by everyone, and how to reach a person if something falls short.", None),
        ("privacy-choices.html", "Your Privacy Choices &mdash; Wiseman Residential",
         "Your California rights to opt out of the sale or sharing of personal information and to limit the use of sensitive personal information.", None),
    ]:
        shell = head(title=title, desc=desc,
                     img="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1200/s3/2/9707/rsz_2motor_jpeg_1.jpg",
                     extra='\n<link rel="stylesheet" href="../core/editorial.css?v=%s">' % VER)
        shell += header("", current=cur)
        shell += "\n\n<main id=\"main\"></main>\n"
        shell += tail(groups)
        write(fn, shell)

    print("atrium: wrote index, live, track, buildings, neighborhoods, search, sitemap + 7 editorial shells")
    print("areas   " + "  ".join("%s %d" % (k, area_counts[k]) for k in AREA_ORDER))
    print("streets %d · four+ beds %d · featured %d" % (streets_total, four_plus, len(FEATURED)))
    return 0


# ---------------------------------------------------------------- buildings.html
def register_row(p, area_label):
    bmax = "" if p.get("bedsMax") is None else str(int(p["bedsMax"]))
    suppress = p["no"] == FLAG_NO
    rent_sort = "" if suppress or p.get("priceMin") is None else str(int(p["priceMin"]))
    beds = beds_range(p) or "&mdash;"
    if suppress:
        fig = '<span class="row-flag">Now leasing</span>'
    elif p.get("priceMin") is not None:
        fig = '<span class="row-rent tnum">%s</span>' % money(p["priceMin"])
    else:
        fig = '<span class="row-rent tnum is-none">&mdash;</span>'
    return """          <div class="reg-row" data-row data-no="{no}" data-name="{name}" data-street="{street}"
               data-area="{area}" data-arealabel="{arealabel}" data-bedsmax="{bmax}" data-rent="{rent}"
               data-img="{img}">
            <a class="row-link" href="buildings/{path}.html">
              <img class="row-thumb" src="{thumb}" alt="" width="56" height="56" loading="lazy" decoding="async">
              <span class="row-body">
                <span class="row-name">{name}</span>
                <span class="row-street">{street}</span>
              </span>
              <span class="row-figs">
                <span class="row-beds tnum">{beds}</span>
                {fig}
              </span>
            </a>
          </div>""".format(no=p["no"], name=esc(p["short"]), street=esc(p["street"]),
                           area=p["areaKey"], arealabel=esc(area_label), bmax=bmax, rent=rent_sort,
                           img=esc(p["image"]), path=p["path"],
                           thumb=esc((p.get("thumb") or "").replace("w_600,h_400", "w_160,h_160")),
                           beds=beds, fig=fig)


def register_block(key, rows, areas):
    a = areas[key]
    body = "\n".join(register_row(p, a["name"]) for p in rows)
    return """        <section class="reg-block" id="{key}" data-group="{key}" aria-labelledby="h-{key}">
          <h2 class="reg-head" id="h-{key}"><span class="reg-head-label" data-grouplabel>{label}</span> <span class="reg-head-count tnum">{n}</span></h2>
          <p class="reg-head-sub">{sub}</p>
          <div class="reg-rows" data-rows>
{body}
          </div>
        </section>""".format(key=key, n=len(rows), label=esc(a["name"]), sub=esc(a["sub"]), body=body)


def plate_item(p, opener=False):
    beds = beds_range(p)
    if p["no"] == FLAG_NO:
        fig = '<span class="pl-flag">Now leasing</span>'
    elif p.get("priceMin") is not None:
        fig = '<span class="tnum">%s &middot; from %s</span>' % (esc(beds), money(p["priceMin"]))
    else:
        fig = '<span class="tnum">%s</span>' % esc(beds)
    tf = "q_auto,f_auto,w_1600,h_685,c_fill,g_auto" if opener else "q_auto,f_auto,w_900,h_600,c_fill,g_auto"
    src = cdn(p["image"], tf)
    return """          <a class="pl{oc}" href="buildings/{path}.html">
            <span class="pl-frame rvi"><img src="{src}" alt="{name}, {street}" loading="lazy" decoding="async"></span>
            <span class="pl-cap"><span class="pl-nm">{name}</span><span class="pl-st">{street}</span><span class="pl-fg">{fig}</span></span>
          </a>""".format(oc=" pl--open" if opener else "", path=p["path"], src=esc(src),
                         name=esc(p["short"]), street=esc(street_line(p)), fig=fig)


def run_block(key, rows, areas, ordinal):
    a = areas[key]
    body = "\n".join(plate_item(p, opener=(i == 0)) for i, p in enumerate(rows))
    return """      <section class="run" id="p-{key}" data-group="{key}" aria-labelledby="ph-{key}">
        <header class="run-head">
          <p class="run-eyebrow"><span class="tnum">{ord:02d}</span><span>of seven</span></p>
          <h2 class="run-h" id="ph-{key}">{label}</h2>
          <p class="run-meta"><span><b class="tnum">{n}</b> {word}</span><a href="neighborhoods/{key}.html">The area &rarr;</a></p>
        </header>
        <div class="pgrid">
{body}
        </div>
      </section>""".format(key=key, ord=ordinal, label=esc(areas[key]["name"]),
                           n=len(rows), word=plural(len(rows), "building"), body=body)


def build_buildings(groups, areas, area_counts, streets_total, props):
    blocks = "\n".join(register_block(k, groups[k], areas) for k in AREA_ORDER)
    runs = "\n\n".join(run_block(k, groups[k], areas, i) for i, k in enumerate(AREA_ORDER, 1))
    page = head(
        title="Every building &mdash; all 72 Wiseman buildings in Los Angeles",
        desc=("All 72 Wiseman apartment buildings, grouped by neighbourhood. Sort by street, "
              "bedrooms or rent, read the same list against a map, or see one photograph for each."),
        img="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1200/s3/2/9707/rsz_2motor_jpeg_1.jpg",
        extra='\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % VER)
    page += header("", current="live", exact=False)
    page += """
<main id="main">

  <section class="pagehead pagehead-split wrap wrap-n">
    <div class="pagehead-l">
      <p class="pagehead-no"><span>Live at Wiseman</span><span class="tnum">{total} buildings &middot; 7 areas</span></p>
      <h1 class="pagehead-h">Every building Wiseman&nbsp;owns.</h1>
      <p class="pagehead-sub">Listed in full, west to east &mdash; nothing hidden behind a filter.</p>
    </div>
    <form class="search" action="search.html" method="get" role="search">
      <label class="vh" for="q">Search by building, street or area</label>
      <div class="search-row">
        <input class="search-field" id="q" name="q" type="search" autocomplete="off" placeholder="Building, street or area"
               data-typeahead role="combobox" aria-expanded="false" aria-controls="ta" aria-autocomplete="list">
        <button class="search-btn" type="submit">Search</button>
      </div>
      <ul class="ta" id="ta" role="listbox" aria-label="Matching buildings" data-typeahead-out hidden></ul>
    </form>
  </section>

  <div class="toolbar wrap wrap-n">
    <div class="sortbar">
      <span class="sortbar-label" id="views-label">View</span>
      <div class="views" role="tablist" aria-labelledby="views-label">
        <a class="view-btn" role="tab" href="?view=register" data-viewbtn="register" aria-selected="true">Index</a>
        <a class="view-btn" role="tab" href="?view=atlas" data-viewbtn="atlas" aria-selected="false">Map</a>
        <a class="view-btn" role="tab" href="?view=plates" data-viewbtn="plates" aria-selected="false">Photographs</a>
      </div>
    </div>
    <div class="sortbar" role="group" aria-label="Sort" data-showin="register atlas">
      <span class="sortbar-label">Sort</span>
      <button class="sort-btn" type="button" data-sort="area" aria-pressed="true">Neighbourhood</button>
      <button class="sort-btn" type="button" data-sort="no" aria-pressed="false">Recommended</button>
      <button class="sort-btn" type="button" data-sort="street" aria-pressed="false">Street A&ndash;Z</button>
      <button class="sort-btn" type="button" data-sort="beds" aria-pressed="false">Bedrooms</button>
      <button class="sort-btn" type="button" data-sort="rent" aria-pressed="false">Rent</button>
    </div>
  </div>

  <div class="mapbleed wrap wrap-n" data-showin="atlas" hidden>
    <div class="mapbox" id="all-map" data-map='{{"scope":"all","bubbles":true,"theme":"light","label":"Map of all {total} Wiseman buildings"}}'></div>
    <p class="map-key"><span><span class="tnum">{total}</span> buildings</span><span>Hover a row to light its pin &middot; the list is complete with the map off</span></p>
  </div>

  <section class="reg wrap wrap-n view-pane" data-viewpane="register atlas">
    <div data-register data-mode="grouped">
{blocks}
    </div>
    <p class="reg-legend">
      <span>Seventy-two buildings in seven areas, set out west to east. Bedrooms and rent are the leasing feed&rsquo;s own figures, read on {snap}; rent is the lowest a building lists, an em dash where the feed lists none&nbsp;today.</span>
      <span>Motor Tides completes in 2026 and leases through the live system &mdash; no rent is published for it.</span>
    </p>
  </section>

  <section class="book wrap wrap-n view-pane" data-viewpane="plates" hidden>
    <h2 class="vh">The photographs</h2>
    <p class="reg-note"><span>One photograph per building, grouped by neighbourhood, west to east.</span><span>Photographs are Wiseman&rsquo;s own, as published in the leasing feed.</span></p>
{runs}
  </section>

  <p class="avail-line wrap wrap-n">
    For what is available this week, see <a href="search.html">Find a home</a>.
    <span class="avail-sub">The live leasing system is the authority on availability and price.</span>
  </p>

</main>
""".format(total=TOTAL, snap=SNAPSHOT, blocks=blocks, runs=runs)
    page += tail(groups, extra_js='\n<script src="../core/rail.js?v=%s" defer></script>' % VER)
    write("buildings.html", page)


# ---------------------------------------------------------------- neighborhoods.html
def area_card(key, rows, areas, delay):
    a = areas[key]
    p = rows[0]
    img = cdn(a.get("image") or p["image"], "q_auto,f_auto,w_900,h_1125,c_fill,g_auto")
    return """    <a class="card rv" data-d="{d}" href="neighborhoods/{key}.html">
      <span class="ph rvi"><img src="{img}" alt="{label}." loading="lazy" decoding="async"></span>
      <span class="info">
        <span class="area">{n} {word}</span>
        <span class="nm">{label}</span>
        <span class="facts"><span class="b">{sub}</span><span class="go" aria-hidden="true">&rarr;</span></span>
      </span>
    </a>""".format(d=delay, key=key, img=esc(img), label=esc(a["name"]),
                   n=len(rows), word=plural(len(rows), "building"), sub=esc(a["sub"]))


def build_neighborhoods(groups, areas, area_counts):
    cards = "\n".join(area_card(k, groups[k], areas, (i % 3) + 1) for i, k in enumerate(AREA_ORDER))
    page = head(
        title="Neighbourhoods &mdash; seven parts of Los Angeles",
        desc=("The seven parts of Los Angeles where Wiseman owns and manages apartments: West Los "
              "Angeles and Sawtelle, Beverly Grove, Brentwood, Hollywood, Venice, Palms and Glendale."),
        img="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1200/s3/2/9707/rsz_2motor_jpeg_1.jpg")
    page += header("", current="live", exact=False)
    page += """
<main id="main">

  <section class="pagehead pagehead-split wrap wrap-n">
    <div class="pagehead-l">
      <p class="pagehead-no"><span>Live at Wiseman</span><span class="tnum">7 areas &middot; {total} buildings</span></p>
      <h1 class="pagehead-h">Seven parts of Los&nbsp;Angeles.</h1>
    </div>
    <p class="pagehead-sub">{wla} buildings stand in West Los Angeles alone &mdash; the rest reach from Brentwood to Glendale. <a href="buildings.html">All {total} buildings</a></p>
  </section>

  <section class="band wrap wrap-n" style="padding-top:clamp(20px,3vh,34px)">
    <div class="homemap">
      <div class="mapbox" id="portfolio-map" data-map='{{"scope":"all","bubbles":true,"theme":"light","label":"Map of all {total} Wiseman buildings across Los Angeles"}}'></div>
      <p class="map-foot"><span><span class="tnum">{total}</span> buildings &middot; gathered into area counts as you zoom&nbsp;out</span><span>The list below stays complete with the map switched&nbsp;off</span></p>
    </div>
  </section>

  <section class="band wrap wrap-n" style="padding-top:0">
    <div class="band-head" style="margin-bottom:clamp(24px,3vh,40px)"><p class="eyebrow rv">The seven</p><h2 class="rv" data-d="1">Every area, with its&nbsp;count.</h2></div>
    <div class="communities">
{cards}
    </div>
  </section>

  <p class="avail-line wrap wrap-n">
    For what is available across the city this week, see <a href="search.html">Find a home</a>.
    <span class="avail-sub">The live leasing system is the authority on availability and price.</span>
  </p>

</main>
""".format(total=TOTAL, wla=area_counts["west-la"], cards=cards)
    page += tail(groups)
    write("neighborhoods.html", page)


# ---------------------------------------------------------------- search.html
AV_BOOT = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  WR.rails();
  var bar = document.querySelector('.sbar [data-rail-track]');
  if (bar && bar.tagName === 'FORM') bar.setAttribute('role', 'search');
  [].forEach.call(document.querySelectorAll('[data-card]'), function (c) {
    if (c.dataset.bedsmin === '') c.dataset.bedsmin = 'na';
    if (c.dataset.bedsmax === '') c.dataset.bedsmax = 'na';
  });
  [].forEach.call(document.querySelectorAll('[data-fmenu] h4'), function (h) { h.setAttribute('role', 'presentation'); });
  WR.searchPage({});
  (function clearAll() {
    var chips = document.querySelector('[data-chips]'), btn = document.querySelector('.sresults [data-clearall]');
    if (!chips || !btn) return;
    function sync() { btn.hidden = chips.children.length === 0; }
    new MutationObserver(sync).observe(chips, { childList: true }); sync();
  })();
  fetch('../data/wiseman.json').then(function (r) { return r.json(); }).then(function (d) {
    WR.map({ el: '#search-map', pins: 'price', theme: 'light',
      points: d.properties.map(function (p) {
        return { no: p.no, lat: p.lat, lng: p.lng, name: p.short, street: p.street, area: p.areaKey,
                 areaLabel: p.area, beds: p.beds, img: p.thumb, url: 'buildings/' + p.path + '.html',
                 pinLabel: p.no === '071' ? 'New' : '' };
      }),
      areas: Object.fromEntries(Object.entries(d.areas).map(function (e) { return [e[0], { name: e[1].name, count: e[1].count }]; }))
    });
    if (WR.searchApply) WR.searchApply(false);
  });
});
</script>"""


def build_search(groups, props):
    page = head(
        title="Live at Wiseman &mdash; find a home in Los Angeles",
        desc=("Search 72 Wiseman apartment buildings in Los Angeles. Filter by neighbourhood, "
              "bedrooms, baths, rent, size and amenities, then open the live leasing listing. "
              "Figures are a snapshot of the leasing feed on %s." % SNAPSHOT),
        img="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1200/s3/2/9707/rsz_2motor_jpeg_1.jpg",
        extra=('\n<link rel="stylesheet" href="../core/search.css?v=%s">'
               '\n<link rel="stylesheet" href="../core/rail.css?v=%s">' % (VER, VER)))
    page += header("", current="live")
    page += """
<main id="main">

  <!-- LIVE AT WISEMAN — the one property-search destination. Two marks on one
       baseline row: the title, and a qualifier that says what the count row
       below does not. The kicker restated the nav item that is already
       aria-current; the standing-figures line opened on "72 buildings", the
       same number the count row repeats. Both removed. -->
  <section class="shead wrap wrap-n">
    <h1 class="shead-h">Find a home in Los&nbsp;Angeles.</h1>
    <p class="shead-sub">Seven areas, studios to five&nbsp;bedrooms.</p>
  </section>

  <h2 class="vh">Filters and results</h2>
<!--SEARCH-->
<!--/SEARCH-->

  <p class="avail-line wrap wrap-n">
    Apply, pay and renew in the <a href="{applicant}" rel="noopener">live leasing system</a>.
    <span class="avail-sub">Or call the leasing office on {tel}. Wiseman Residential is an equal housing opportunity&nbsp;provider.</span>
  </p>

</main>
""".format(tel=LEASING_TEL, applicant=esc(APPLICANT))
    page += tail(groups,
                 extra_js=('\n<script src="../core/rail.js?v=%s" defer></script>'
                           '\n<script src="../core/search.js?v=%s" defer></script>' % (VER, VER)),
                 boot=AV_BOOT)
    write("search.html", page)


# ---------------------------------------------------------------- sitemap.html
# The footer has always carried a "Site Map" link and it has always pointed at
# `#site-map` — the id on the <footer> the link itself sits inside. Clicking it
# from the footer did nothing at all. This builds the page it should have been
# pointing at: every URL Clerestory publishes, in one flat list, grouped the way
# the site is actually organised. Nothing here is hand-typed — the seven areas
# and all 72 buildings are read from data/wiseman.json, so the page cannot drift
# out of date behind the register.
SM_SECTIONS = [
    ("About Wiseman", "about", [
        ("company.html", "About Wiseman",
         "One Los Angeles company owns, develops and manages every building on this site."),
    ]),
    ("Live at Wiseman", "live", [
        ("search.html", "Find a home",
         "The property search: filters, cards and the map, on one page."),
        ("buildings.html", "Every building",
         "All %d buildings as an index, a map or a photograph each." % TOTAL),
        ("neighborhoods.html", "The seven areas",
         "Where in Los Angeles Wiseman owns, with a count for each area."),
    ]),
    ("Work at Wiseman", "work", [
        ("careers.html", "Work at Wiseman",
         "On-site management, maintenance, leasing, and the corporate office."),
    ]),
    ("Track Record", "track", [
        ("track.html", "Track Record",
         "Motor Tides and the filed pipeline, each figure cited to its source."),
    ]),
    ("Residents", "residents", [
        ("residents.html", "Resident services",
         "Report a repair without a login, pay rent, deposits, moving in."),
    ]),
    ("Contact", "contact", [
        ("contact.html", "Contact Wiseman",
         "Six ways in, routed by what you need. 1520 Federal Ave, +1 310-473-3000."),
    ]),
    ("This site", "legal", [
        ("privacy.html", "Privacy Policy",
         "What this website does with the information you give it."),
        ("accessibility.html", "Accessibility",
         "How the site is built to be usable by everyone, and who to tell if it is not."),
        ("privacy-choices.html", "Your Privacy Choices",
         "Your California rights to opt out, and to limit the use of sensitive information."),
        ("sitemap.html", "Site Map",
         "This page."),
    ]),
]


def sm_group(title, key, rows, extra=""):
    lis = "\n".join(
        '        <li><a href="%s">%s</a><span class="sm-d">%s</span></li>' % (h, esc(l), esc(d))
        for h, l, d in rows)
    return """      <section class="sm-grp" aria-labelledby="sm-{key}">
        <h2 class="sm-h" id="sm-{key}">{title}</h2>
        <ul class="sm-list">
{lis}
        </ul>{extra}
      </section>""".format(key=key, title=esc(title), lis=lis, extra=extra)


def build_sitemap(groups, areas, props):
    # the leasing system is a different system, not a page of this site — it is
    # listed, and it says so, rather than being quietly mixed in with the rest
    offsite = """
        <ul class="sm-list sm-off">
          <li><a href="{resident}" rel="noopener">Resident login</a><span class="sm-d">The live leasing system &mdash; a separate site.</span></li>
          <li><a href="{applicant}" rel="noopener">Applicant login</a><span class="sm-d">Apply and pay in the live leasing system &mdash; a separate site.</span></li>
        </ul>""".format(resident=esc(RESIDENT), applicant=esc(APPLICANT))

    grps = []
    for title, key, rows in SM_SECTIONS:
        extra = offsite if key == "residents" else ""
        grps.append(sm_group(title, key, rows, extra))
        if key == "live":
            area_rows = "\n".join(
                '        <li><a href="neighborhoods/%s.html">%s</a>'
                '<span class="sm-ct tnum">%d</span></li>' % (k, esc(areas[k]["name"]), len(groups[k]))
                for k in AREA_ORDER)
            grps.append("""      <section class="sm-grp" aria-labelledby="sm-areas">
        <h2 class="sm-h" id="sm-areas">The seven areas</h2>
        <ul class="sm-list sm-areas">
{rows}
        </ul>
      </section>""".format(rows=area_rows))

    blocks = []
    for k in AREA_ORDER:
        rows = sorted(groups[k], key=lambda p: p["short"].lower())
        items = "\n".join(
            '            <li><a href="buildings/%s.html">%s</a></li>' % (p["path"], esc(p["short"]))
            for p in rows)
        blocks.append("""        <section class="sm-area" aria-labelledby="sma-{k}">
          <h3 class="sm-area-h" id="sma-{k}">{label} <span class="sm-ct tnum">{n}</span></h3>
          <ul class="sm-cols">
{items}
          </ul>
        </section>""".format(k=k, label=esc(areas[k]["name"]), n=len(rows), items=items))

    pages = sum(len(r) for _, _, r in SM_SECTIONS) + 1 + len(AREA_ORDER) + len(props)  # +1 home

    page = head(
        title="Site Map &mdash; every page on wisemanresidential.com",
        desc=("Every page on this site in one list: About Wiseman, the property search, all %d "
              "buildings across seven Los Angeles neighbourhoods, careers, track record, resident "
              "services, contact and the legal pages." % TOTAL),
        img="https://resource.rentcafe.com/image/upload/q_auto,f_auto,w_1200/s3/2/9707/rsz_2motor_jpeg_1.jpg")
    page += header("")
    page += """
<main id="main">

  <section class="pagehead pagehead-split wrap wrap-n">
    <div class="pagehead-l">
      <p class="pagehead-no"><span>Site map</span><span class="tnum">{pages} pages</span></p>
      <h1 class="pagehead-h">Every page on this&nbsp;site.</h1>
    </div>
    <p class="pagehead-sub">Seven sections, seven areas and all {total} buildings &mdash; each one a real, linkable page. <a href="search.html">Find a home</a></p>
  </section>

  <nav class="sitemap wrap wrap-n" aria-label="Site map">
      <section class="sm-grp" aria-labelledby="sm-home">
        <h2 class="sm-h" id="sm-home">Home</h2>
        <ul class="sm-list">
          <li><a href="index.html">Wiseman Residential</a><span class="sm-d">Los Angeles living, managed wisely.</span></li>
        </ul>
      </section>
{grps}
  </nav>

  <section class="sitemap-b wrap wrap-n" aria-labelledby="sm-all">
    <div class="sm-bhead">
      <h2 class="sm-h" id="sm-all">All {total} buildings</h2>
      <p class="sm-note">Grouped by area, west to east, then A&ndash;Z. Every building has its own page, its own leasing line and its own map.</p>
    </div>
    <div class="sm-areas-grid">
{blocks}
    </div>
  </section>

  <p class="avail-line wrap wrap-n">
    For what is available this week, see <a href="search.html">Find a home</a>.
    <span class="avail-sub">The live leasing system is the authority on availability and price.</span>
  </p>

</main>
""".format(pages=pages, total=TOTAL, grps="\n".join(grps), blocks="\n".join(blocks))
    page += tail(groups)
    write("sitemap.html", page)


def write(name, content):
    open(os.path.join(HERE, name), "w", encoding="utf-8").write(content)


if __name__ == "__main__":
    sys.exit(main())
