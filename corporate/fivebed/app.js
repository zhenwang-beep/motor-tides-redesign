/* Wiseman Residential — direction: FIVE BEDROOMS.
   One app.js for all nine pages. Everything is guarded on element presence,
   so the same file is safe on the home page, the register, a building page,
   availability, residents, company and contact.

   Rules this file obeys (see ../CONVENTIONS.md):
   - core.js owns the single rAF loop. We subscribe with WR.onScroll and never
     call requestAnimationFrame ourselves.
   - Every mechanic reads WR.reduce once and branches to a STATIC END STATE,
     rather than simply not animating.
   - We never drive the scroll position. We only read it.

   Data: pages declare <html data-index="../data/index.json"> (root pages) or
   "../../data/index.json" (pages inside buildings/ or neighborhoods/). */
(function () {
  'use strict';
  var W = window.WR;
  if (!W) return;

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------------ boot */
  W.boot({ header: { heroEnd: 140 }, transition: true });

  var INDEX_URL = document.documentElement.dataset.index || '../data/index.json';

  /* =====================================================================
     THE COUNT — the signature mechanic. Home page only.

     Markup:
       <section class="count">
         <div class="stage" data-stage style="--img:url('…')">
           <div class="stage-in wrap wrap-n">
             <span class="digit" data-digit aria-hidden="true">4</span>
             <p class="digit-line">…</p>
           </div>
         </div>  ×5

     Each stage is 1.7 viewports tall with one sticky full-height panel.
     WR.pinned(stage) is 0 when the stage top reaches the viewport top and 1
     when its bottom does. From that one number we write three custom
     properties on the numeral:
       --s   0.96 → 1.10   scale. FORWARD ONLY — it never runs backwards
                           within a stage, and each stage owns its own element.
       --bx  34% → 64%     the clipped photograph drifts across the glyph
       --by  64% → 34%
     ===================================================================== */
  (function theCount() {
    var stages = $$('[data-stage]');
    if (!stages.length) return;

    var items = stages.map(function (st) {
      return { el: st, d: $('[data-digit]', st), s: -1, b: -1 };
    }).filter(function (it) { return !!it.d; });
    if (!items.length) return;

    /* Reduced motion: the photographs stay in the numerals as a static piece
       of art. Only the drift and the bloom are deleted. */
    if (W.reduce) {
      items.forEach(function (it) {
        it.d.style.setProperty('--s', '1');
        it.d.style.setProperty('--bx', '50%');
        it.d.style.setProperty('--by', '50%');
      });
      return;
    }

    items.forEach(function (it) {
      it.d.style.setProperty('--s', '0.96');
      it.d.style.setProperty('--bx', '34%');
      it.d.style.setProperty('--by', '64%');
    });

    W.onScroll(function (y, vh) {
      for (var i = 0; i < items.length; i++) {
        var it = items[i], r = it.el.getBoundingClientRect();
        if (r.bottom < -vh * 0.25 || r.top > vh * 1.25) continue;  /* off-stage: skip */

        var e = W.smooth(W.pinned(it.el));
        var s = 0.96 + 0.14 * e;
        var b = 34 + 30 * e;

        /* forward only: a bloom that contracts undoes the reveal it paid for */
        if (s <= it.s + 0.0004 && Math.abs(b - it.b) < 0.15) continue;
        if (s > it.s) { it.s = s; it.d.style.setProperty('--s', s.toFixed(4)); }
        it.b = b;
        it.d.style.setProperty('--bx', b.toFixed(2) + '%');
        it.d.style.setProperty('--by', (98 - b).toFixed(2) + '%');
      }
    });
  })();

  /* =====================================================================
     THE REGISTER — sort, never filter. core.js owns the sorting; we only
     choose the default. On the home page the rows are authored in bedroom
     order inside one group, so asking core for 'beds' on load is a no-op
     visually: it just claims the right sort button and the flat label.
     ===================================================================== */
  (function theRegister() {
    var list = $('[data-register]');
    if (!list) return;
    var flat = list.dataset.flatlabel || 'All 72 buildings · largest homes first';
    var hadSort = false;
    try { hadSort = new URLSearchParams(location.search).has('sort'); } catch (e) {}

    W.register({ list: '[data-register]', flatLabel: flat });

    var def = list.dataset.defaultsort;
    if (!hadSort && def && W.sortRegister) {
      W.sortRegister(def);
      /* core writes ?sort= into the URL; a default does not deserve a query
         string, so put the clean address back. */
      try { history.replaceState(null, '', location.pathname + location.hash); } catch (e) {}
    }
  })();

  /* =====================================================================
     TYPEAHEAD — street, building name or number. Progressive: the field is
     a real <form> that lands on the register, and this only adds suggestions.
     ===================================================================== */
  (function theSearch() {
    /* NAME CLASH. This direction's typeahead field has been [data-search] since
       the first build; core/search.js later took the same attribute for the ILS
       root on search.html, where it sits on a <div>. Without the tag test
       this module adopted that div as its "input", wrote a .value on to it and
       fetched index.json for a typeahead that has no [data-ta] list to render
       into. Ask for the element type we actually need. */
    var input = $('input[data-search]');
    if (!input) return;
    var base = (document.documentElement.dataset.index || '').indexOf('../../') === 0 ? '../' : '';

    W.load(INDEX_URL).then(function (ix) {
      var areas = ix.areas || {};
      var items = (ix.p || []).map(function (p) {
        var area = (areas[p.a] && areas[p.a].name) || '';
        return {
          hay: (p.no + ' ' + p.n + ' ' + p.s + ' ' + area).toLowerCase(),
          no: p.no,
          name: p.n,
          sub: p.s + ' · ' + area,
          url: base + 'buildings/' + p.u + '.html'
        };
      });
      W.typeahead({ input: 'input[data-search]', out: '[data-ta]', items: items });

      /* Both search fields are real <form>s that GET buildings.html?q=…, so
         Enter always goes somewhere. Carry the term across: prefill the
         register's own field and open its suggestions, rather than landing on
         the full list with the query silently dropped. */
      var q = '';
      try { q = new URLSearchParams(location.search).get('q') || ''; } catch (e) {}
      if (q && !input.value) {
        input.value = q;
        input.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }).catch(function () { /* the form still submits to the register */ });
  })();

  /* =====================================================================
     THE HERO — the photograph drifts 1.00 -> 1.04 across one viewport of
     scroll. Transform only, one subscriber on the shared rAF loop, and
     nothing at all under reduced motion.
     ===================================================================== */
  (function heroDrift() {
    var fig = $('.hero-fig');
    if (!fig || W.reduce) return;
    var last = -1;
    W.onScroll(function (y, vh) {
      var hero = fig.parentNode, r = hero.getBoundingClientRect();
      if (r.bottom < 0) return;
      var t = W.clamp01(-r.top / vh);
      var z = 1 + 0.04 * t;
      if (Math.abs(z - last) < 0.0015) return;
      last = z;
      fig.style.setProperty('--z', z.toFixed(4));
    });
  })();

  /* =====================================================================
     THE MAP — a real embedded map, four placements:

       neighborhoods.html          all 72 + area bubbles
       neighborhoods/<key>.html    that area only, coordinates inline
       buildings.html?view=atlas   all 72 + bubbles, beside the register rows
       buildings/<no>-<slug>.html  one building, zoom 15, no bubbles

     core/map.js loads Leaflet on demand and falls back to the drawn SVG
     (WR.atlas) by itself if the CDN is unreachable, so the drawn atlas lives
     only inside map.js now and never in a page body.

     FACT-CHECK §2: no rent is ever handed to a popup. A Motor Tides figure
     may not appear anywhere on the site, and a popup is anywhere — so the
     whole site's popups carry bedrooms and never a price.
     ===================================================================== */
  (function theMap() {
    var host = $('[data-map]');
    if (!host) return;

    var theme = host.dataset.theme === 'dark' ? 'dark' : 'light';
    var base = (document.documentElement.dataset.index || '').indexOf('../../') === 0 ? '../' : '';

    var waited = false;
    function draw(points, areas, single) {
      if (!points || !points.length) return;
      if (!W.map) {
        /* map.js is a deferred sibling of this file. Give the rest of the
           deferred queue a turn before deciding it never arrived. */
        if (!waited) { waited = true; setTimeout(function () { draw(points, areas, single); }, 0); return; }
        if (W.atlas) W.atlas({ el: '[data-map]', points: points });
        return;
      }
      W.map({
        el: '[data-map]',
        points: points,
        areas: areas || null,
        theme: theme,
        label: host.dataset.label || undefined,
        /* A single building has no bounds to fit: fitBounds on one point runs
           to maxZoom. Put it back on the street at zoom 15. */
        onReady: single ? function (map) {
          map.setView([points[0].lat, points[0].lng], 15);
        } : null
      });
    }

    /* one building — its coordinates ship on the element itself */
    if (host.hasAttribute('data-one')) {
      var d = host.dataset;
      draw([{
        no: d.no, lat: +d.lat, lng: +d.lng, name: d.name,
        street: d.street, areaLabel: d.arealabel, url: d.url
      }], null, true);
      return;
    }

    /* one neighbourhood — the generator ships that area's points inline, so
       the page needs no fetch at all */
    var inline = host.getAttribute('data-points');
    if (inline) {
      try { draw(JSON.parse(inline), null, false); } catch (e) {}
      return;
    }

    /* the whole portfolio, with the seven counted bubbles */
    W.load(INDEX_URL).then(function (ix) {
      var areas = ix.areas || {};
      var pts = (ix.p || []).map(function (p) {
        var lo = p.bmin, hi = p.bmax, beds = '';
        if (lo != null) {
          hi = hi == null ? lo : hi;
          beds = (lo === hi ? (lo === 0 ? 'Studio' : lo + ' bed')
                            : (lo === 0 ? 'Studio–' + hi + ' bed' : lo + '–' + hi + ' bed'));
        }
        return {
          no: p.no, lat: p.lat, lng: p.lng, name: p.n, street: p.s,
          area: p.a, areaLabel: (areas[p.a] && areas[p.a].name) || '',
          beds: beds, img: p.img, url: base + 'buildings/' + p.u + '.html'
        };
      });
      var bub = {};
      Object.keys(areas).forEach(function (k) { bub[k] = { name: areas[k].name, count: areas[k].count }; });
      draw(pts, bub, false);
    }).catch(function () {});
  })();

  /* =====================================================================
     AVAILABILITY FILTERS — the only filters on the site, on the only page
     that has them. Rows are authored as real HTML; this hides and counts.
     ===================================================================== */
  (function theFilters() {
    if (!$('[data-filters]')) return;
    W.filters({
      form: '[data-filters]',
      rows: '[data-frow]',
      count: '[data-fcount]',
      empty: '[data-fempty]'
    });
  })();

  /* =====================================================================
     ROOM STRIPS — the second device, on building pages. The rail is now
     core/rail.js: no visible scrollbar, arrows over the photograph, a tabular
     count and a hairline that fills as you go. Each building page boots it
     with WR.rails() inline, so this file has nothing left to do here — the
     progress rule that used to be scrubbed from the rail's scroll event is
     .rail-bar now, and rail.js keeps it in step.
     ===================================================================== */

  /* =====================================================================
     SEARCH DROPDOWNS — un-clipping the filter popovers.

     core/search.css scrolls the filter bar sideways (.sbar-in), which makes
     it a scroll container; `overflow-x: auto` forces `overflow-y` to auto
     too, so every dropdown opened inside it was clipped to a 12px sliver.
     core/search.css is shared by all three directions and is not edited, so
     the fix lives here: when a menu is shown, it is lifted onto fixed
     coordinates taken from its own button, which puts it outside the
     scroller; when it closes, every inline style is handed back. One
     subscriber on the shared rAF loop keeps it under the button while the
     bar is still travelling up to its sticky position.

     .sbar must not carry a backdrop-filter for this to work — a filter makes
     the element the containing block for fixed descendants. See style.css.
     ===================================================================== */
  (function searchPopovers() {
    var bar = $('.sbar');
    if (!bar || !window.MutationObserver) return;
    var pops = $$('[data-fpop]', bar).map(function (pop) {
      return { btn: $('[data-fbtn]', pop), menu: $('[data-fmenu]', pop) };
    }).filter(function (p) { return p.btn && p.menu; });
    if (!pops.length) return;

    var open = null;

    function place(p) {
      var r = p.btn.getBoundingClientRect();
      var w = p.menu.offsetWidth;
      var left = r.left;
      if (left + w > innerWidth - 12) left = Math.max(12, r.right - w);
      p.menu.style.position = 'fixed';
      p.menu.style.top = Math.round(r.bottom + 7) + 'px';
      p.menu.style.left = Math.round(left) + 'px';
      p.menu.style.right = 'auto';
    }

    function clear(p) {
      p.menu.style.position = '';
      p.menu.style.top = '';
      p.menu.style.left = '';
      p.menu.style.right = '';
    }

    pops.forEach(function (p) {
      new MutationObserver(function () {
        if (!p.menu.hidden) { open = p; place(p); }
        else { clear(p); if (open === p) open = null; }
      }).observe(p.menu, { attributes: true, attributeFilter: ['hidden'] });
    });

    W.onScroll(function () { if (open) place(open); });
    addEventListener('resize', function () { if (open) place(open); });
  })();

  /* =====================================================================
     SEARCH CHROME — two repairs to the shared ILS that have to live here,
     because core/search.js and scripts/gen_search.py are shared with the
     other two directions and are not edited from inside one of them.

     1. "Clear all" never appeared.
        core/search.js ends paintChips() with

            var all = root.querySelector('[data-clearall]');
            if (all) all.hidden = out.length === 0;

        — querySelector, singular. gen_search.py writes TWO [data-clearall]
        buttons and the modal's "Clear all filters" is first in document
        order, so it is the one that gets toggled and the one beside the
        chips — the primary affordance, authored hidden — stayed hidden at
        every filter state. Measured: 1 chip set, .sresults button still
        display:none. Both buttons are painted here instead, off the same
        condition, on the wr:filtered event the module already fires after
        paintChips().

     2. The filter popovers skipped a heading level.
        The four dropdown bodies open with <h4> (Neighbourhood, Bedrooms,
        Bathrooms, Monthly rent) and the page's only heading above them is
        the <h1>, so the outline read h1 -> h4. The <h4> is a group label,
        not a document heading — .fmenu already carries role="group" with
        the same name — so it keeps its size and takes aria-level="2",
        which fixes the outline without touching the shared markup or the
        .fmenu h4 rules in either stylesheet.
     ===================================================================== */
  (function searchChrome() {
    var root = $('[data-search]');
    if (!root || !root.querySelector('[data-cards]')) return;

    var clears = $$('[data-clearall]', root);
    if (clears.length > 1) {
      root.addEventListener('wr:filtered', function () {
        var any = !!root.querySelector('[data-chips] .chip-f');
        clears.forEach(function (b) { b.hidden = !any; });
      });
    }

    $$('[data-fmenu] > h4', root).forEach(function (h) { h.setAttribute('aria-level', '2'); });
  })();

  /* =====================================================================
     RAIL SEMANTICS — core/rail.js adopts a track with

         track.setAttribute('role', 'group');

     unconditionally. That is right for the plain <div> it was written for,
     but two of this direction's three rails are not plain divs:

       · search.html's filter bar is the <form role="search"> the
         generator authors — the search landmark was being overwritten;
       · every building page's room strip is an <ol> of <li> frames —
         role="group" drops the list role and orphans four listitems.

     The authored role is read here at defer time, before the inline
     WR.rails() call on DOMContentLoaded, and put back afterwards. A track
     that authored no role keeps rail.js's group unless it is an element
     whose own role is worth more than "group".
     ===================================================================== */
  (function railSemantics() {
    var tracks = $$('[data-rail-track]');
    if (!tracks.length) return;
    var was = tracks.map(function (t) { return t.getAttribute('role'); });
    var OWN = /^(UL|OL|FORM|TABLE|DL|NAV|MAIN|ASIDE)$/;
    document.addEventListener('DOMContentLoaded', function () {
      tracks.forEach(function (t, i) {
        if (was[i] !== null) t.setAttribute('role', was[i]);
        else if (OWN.test(t.tagName)) t.removeAttribute('role');
      });
    });
  })();

  /* =====================================================================
     Small courtesies. Nothing here moves the page on its own.
     ===================================================================== */

  /* The current page gets aria-current in the header and the footer map. */
  (function markCurrent() {
    var here = location.pathname.split('/').pop() || 'index.html';
    $$('.hnav a, .mnav-list a').forEach(function (a) {
      var href = (a.getAttribute('href') || '').split('#')[0].split('?')[0];
      if (href && href === here) a.setAttribute('aria-current', 'page');
    });
  })();
})();
