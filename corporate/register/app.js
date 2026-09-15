/* ============================================================================
   WISEMAN RESIDENTIAL — DIRECTION "THE PLATES"
   One file for all nine pages. Everything is guarded by element presence, so
   a page with no strip / plate / map / filters simply skips that block.

   Depends on core/core.js, and on core/map.js wherever a page carries a map.
   Adds NO second requestAnimationFrame loop: every scroll-bound mechanic
   subscribes to the single WR.onScroll dispatcher. Every mechanic branches on
   WR.reduce.

   Root attributes each page must set on <html>:
     data-base="" | "../"                prefix for links built in JS
     data-data="../data/wiseman.json"    WR.load()
     data-index="../data/index.json"     map + typeahead source
   ========================================================================== */
(function () {
  'use strict';

  var W = window.WR;
  if (!W) return;
  var doc = document;
  var root = doc.documentElement;
  var BASE = root.dataset.base || '';
  var MQ_PLATE = matchMedia('(min-width: 1280px)');  /* where .rail-fig is the sticky right column */

  /* the shared spine first: reveals, header, menu, favourites, curtain */
  W.boot({ header: { heroEnd: 120 }, transition: true });

  /* --------------------------------------------------------------- helpers */
  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return [].slice.call((ctx || doc).querySelectorAll(sel)); }
  function inList(attr, name) { return (attr || '').split(/\s+/).indexOf(name) >= 0; }

  var idxPromise = null;
  function loadIndex() {
    if (!idxPromise) {
      idxPromise = fetch(root.dataset.index || '../data/index.json')
        .then(function (r) { return r.json(); })
        .catch(function () { return null; });
    }
    return idxPromise;
  }

  /* ------------------------------------------------------------------------
     1. THE INDEX + THE SPECIMEN PLATE
     WR.register does the sorting and the plate's hover/focus wiring. This
     block owns everything else the plate does:
       - it shows a building from the first paint: the first row of the
         current sort, and again after every sort (client note, round 7 —
         the column was empty until a row was hovered);
       - when View Transitions are available it pre-empts WR.register's swap:
         claim() writes plate.dataset.cur synchronously, which makes
         WR.register's internal show() early-return, and performs the same
         mutation inside document.startViewTransition. Capture-phase listeners
         on the list run before WR's target-phase listeners on the row, so the
         claim always wins. Without View Transitions, or under reduced motion,
         hover and focus stay with WR.register's own crossfade;
       - while the pointer is off the list, the plate follows the scroll: it
         names the row under the reading line once that row has been there
         for a beat, so a fast scroll does not fire seventy swaps.
  --------------------------------------------------------------------------*/
  var list = $('[data-register]');
  var plate = $('[data-plate]');
  var plateTo = null;

  if (list && ($('[data-sort]') || plate)) {
    W.register({ list: '[data-register]', flatLabel: 'All ' + $$('[data-row]', list).length + ' buildings' });
    plateTo = wirePlate(list, plate);
  }

  function wirePlate(list, plate) {
    if (!plate) return null;
    var img = $('img', plate), no = $('[data-plateno]', plate),
        nm = $('[data-platename]', plate), st = $('[data-platestreet]', plate);
    if (!img) return null;
    var vt = !W.reduce && !!doc.startViewTransition;
    var token = 0;

    function apply(row, ok) {
      if (ok) { img.src = row.dataset.img; img.alt = row.dataset.name; }
      if (no) no.textContent = row.dataset.no;
      if (nm) nm.textContent = row.dataset.name;
      if (st) st.textContent = row.dataset.street + ' · ' + row.dataset.arealabel;
      var link = $('[data-platelink]', plate);
      if (link) link.href = row.querySelector('a') ? row.querySelector('a').getAttribute('href') : link.href;
    }

    function claim(row) {
      if (!row || plate.dataset.cur === row.dataset.no) return;
      plate.dataset.cur = row.dataset.no;           /* pre-empts WR.register */
      var t = ++token, src = row.dataset.img, ok = true;

      function run() {
        if (t !== token) return;                    /* a newer row won */
        /* no transitions: WR.register's own crossfade class. A hidden document
           skips the transition too, and rejects its promises. */
        if (!vt || doc.hidden) {
          apply(row, ok);
          if (ok) { plate.classList.remove('swap'); void plate.offsetWidth; plate.classList.add('swap'); }
          return;
        }
        var v = doc.startViewTransition(function () { apply(row, ok); });
        ['ready', 'finished', 'updateCallbackDone'].forEach(function (k) {
          if (v && v[k] && v[k].catch) v[k].catch(function () {});
        });
      }

      var pre = new Image();
      pre.decoding = 'async';
      pre.onload = run;
      /* a photograph that will not load must not blank the plate: swap the
         caption, keep the last good image */
      pre.onerror = function () { ok = false; run(); };
      pre.src = src;
      if (pre.complete) run();
    }

    if (vt) {
      var from = function (e) { return e.target.closest ? e.target.closest('[data-row]') : null; };
      list.addEventListener('mouseenter', function (e) { claim(from(e)); }, true);
      list.addEventListener('mouseover', function (e) { claim(from(e)); }, true);
      list.addEventListener('focusin', function (e) { claim(from(e)); }, true);
    }
    return claim;
  }

  (function plateDefault() {
    if (!list || !plateTo) return;
    function first() { return list.querySelector('[data-group]:not([hidden]) [data-row]'); }
    function settle() { plateTo(first()); }
    settle();
    /* WR.register re-parents the rows on the same click; the first row of
       the new order is read on the next turn */
    $$('[data-sort]').forEach(function (b) { b.addEventListener('click', function () { setTimeout(settle, 0); }); });

    var want = null, timer = 0;
    W.onScroll(function () {
      if (!plate.getClientRects().length) return;                 /* ≤640: no plate */
      if (list.matches(':hover') || list.contains(doc.activeElement)) return;   /* hover and focus rule */
      var pr = plate.getBoundingClientRect();
      /* the reading line: 40px under the plate's top where it is the sticky
         column beside the rows (≥1280), 40px under its foot where it is the
         sticky strip above them */
      var y = (MQ_PLATE.matches ? pr.top : pr.bottom) + 40;
      var lr = list.getBoundingClientRect();
      if (y < lr.top || y > lr.bottom || y > innerHeight - 1) return;
      var el = doc.elementFromPoint(Math.min(lr.left + 24, innerWidth - 1), y);
      var row = el && el.closest ? el.closest('[data-row]') : null;
      if (!row || row === want) return;
      want = row;
      clearTimeout(timer);
      timer = setTimeout(function () { plateTo(want); }, 160);
    });
  })();

  /* ------------------------------------------------------------------------
     2. THE NEIGHBOURHOOD STRIP — buildings.html, all three views (client
     note, round 7, in place of the ruler). A sticky row of seven links with
     counts under the header. As the page scrolls the link for the area under
     the reading line is lit (aria-current); what it reads is whichever
     [data-pool] collection is on screen — the register rows under Index and
     Map, the photographs under ?view=plates. In a flat sort (Street, Rent…)
     the one visible block holds every area, so the row under the line names
     the area; a click in that state restores the neighbourhood grouping
     first, so the link has somewhere to land. A click travels smoothly to
     the group (instantly under reduced motion) and moves focus to its
     heading. Below the width at which the seven names fit the row is a rail
     — hidden scrollbar, arrows (core/rail.js) — and the lit link is kept in
     view. Every link is a real anchor, so the strip works with none of this.
  --------------------------------------------------------------------------*/
  (function strip() {
    var el = $('[data-nstrip]');
    if (!el) return;
    var links = $$('[data-nmark]', el);
    var pools = $$('[data-pool]');
    if (!links.length || !pools.length) return;
    var track = $('[data-rail-track]', el);
    if (W.rail) W.rail(el);

    function visible(n) { return !!(n.offsetParent || n.getClientRects().length); }
    function pool() {
      for (var i = 0; i < pools.length; i++) if (visible(pools[i])) return pools[i];
      return pools[0];
    }

    var reg = null, groups = [], gtops = [], rows = [], rtops = [], regH = 0, dirty = true, cur = '';

    function measure() {
      var y = window.pageYOffset;
      reg = pool();
      regH = reg.getBoundingClientRect().height;
      groups = $$('[data-group]', reg).filter(visible);
      gtops = groups.map(function (g) { return g.getBoundingClientRect().top + y; });
      rows = reg.dataset.mode === 'flat' ? $$('[data-row]', reg) : [];
      rtops = rows.map(function (r) { return r.getBoundingClientRect().top + y; });
      dirty = false;
    }
    /* the last top at or above the line; the first before the list begins */
    function at(tops, lineY) {
      var lo = 0, hi = tops.length - 1, best = 0;
      while (lo <= hi) {
        var mid = (lo + hi) >> 1;
        if (tops[mid] <= lineY) { best = mid; lo = mid + 1; } else { hi = mid - 1; }
      }
      return best;
    }
    function light(key) {
      if (key === cur) return;
      cur = key;
      var lit = null;
      links.forEach(function (a) {
        if (a.dataset.nmark === key) { a.setAttribute('aria-current', 'location'); lit = a; }
        else a.removeAttribute('aria-current');
      });
      /* on a narrow screen the row scrolls: keep the lit link in view */
      if (lit && track && track.scrollWidth > track.clientWidth + 1) {
        var r = lit.getBoundingClientRect(), t = track.getBoundingClientRect();
        if (r.left < t.left + 36 || r.right > t.right - 36) {
          var to = track.scrollLeft + (r.left - t.left) - 36;
          try { track.scrollTo({ left: to, behavior: W.reduce ? 'instant' : 'smooth' }); }
          catch (e) { track.scrollLeft = to; }
        }
      }
    }

    W.onScroll(function (y) {
      /* images arriving, a sort, a view switch: any of them moves the tops */
      if (dirty || Math.abs(reg.getBoundingClientRect().height - regH) > 2) measure();
      /* the reading line sits just below the strip's foot — but it must clear
         where a clicked group lands. A group's scroll-margin-top is
         hd-h + band-h + 14, and the strip's foot is hd-h + band-h, so a link's
         own target settles ~14–18px under the foot (round 7 follow-up: at +12
         the line fell a hair short of the landed group and lit the PREVIOUS
         area after every strip click). +22 clears the landing at every width. */
      var line = y + el.getBoundingClientRect().bottom + 22;
      var key = rows.length ? rows[at(rtops, line)].dataset.area
              : groups.length ? groups[at(gtops, line)].dataset.group : '';
      if (key) light(key);
    });

    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        var key = a.dataset.nmark, r = pool();
        if (r.dataset.mode === 'flat' && W.sortRegister) W.sortRegister('area');
        var g = r.querySelector('[data-group="' + key + '"]');
        if (!g) return;                              /* the href works on its own */
        e.preventDefault();
        soil();
        /* scrollIntoView honours the group's scroll-margin-top, which is the
           header plus this strip; `instant` is spelled out because base.css
           sets scroll-behavior:smooth on <html> */
        try { g.scrollIntoView({ block: 'start', behavior: W.reduce ? 'instant' : 'smooth' }); }
        catch (err) { g.scrollIntoView(true); }
        try { history.replaceState(null, '', '#' + g.id); } catch (err) {}
        var h = g.querySelector('h2');
        if (h) {
          if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1');
          try { h.focus({ preventScroll: true }); } catch (err) {}
        }
      });
    });

    function soil() { dirty = true; W.pump(); }
    W.soilStrip = soil;
    addEventListener('resize', soil);
    addEventListener('load', soil);
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(soil);
    $$('[data-sort]').forEach(function (b) { b.addEventListener('click', function () { setTimeout(soil, 0); }); });
    if (MQ_PLATE.addEventListener) MQ_PLATE.addEventListener('change', soil);
  })();

  /* ------------------------------------------------------------------------
     3. THE MAP — the real one. core/map.js loads Leaflet on demand and draws
     CARTO raster tiles over OpenStreetMap data, with WR.atlas (the drawn SVG)
     as its own automatic fallback if the CDN is unreachable. Nothing on this
     site draws the SVG atlas into a page body any more.

     A container declares itself with data-map='{...}':
       scope:  "all" for the whole portfolio
       area:   an area key for one neighbourhood
       points: [{no,lat,lng}] straight from the template context
       one:    {no,lat,lng} for a single building, with zoom
     Everything a popup needs — name, street, photograph, bedrooms — is read
     from data/index.json, which already suppresses the figures FACT-CHECK §2
     forbids publishing.
  --------------------------------------------------------------------------*/
  (function maps() {
    var hosts = $$('[data-map]');
    if (!hosts.length || !W.map) return;
    var pending = [];

    function cfgOf(el) {
      try { return JSON.parse(el.getAttribute('data-map') || '{}'); }
      catch (e) { return {}; }
    }

    function build(el, cfg, ix) {
      var areas = (ix && ix.areas) || {};
      var byNo = {};
      if (ix && ix.p) ix.p.forEach(function (p) { byNo[p.no] = p; });

      var wanted;
      if (cfg.one) wanted = [cfg.one];
      else if (cfg.points && cfg.points.length) wanted = cfg.points;
      else if (cfg.area) wanted = (ix && ix.p ? ix.p : []).filter(function (p) { return p.a === cfg.area; });
      else wanted = (ix && ix.p) ? ix.p : [];

      var pts = wanted.map(function (w) {
        /* the template's own points array wins where it has an answer; index.json
           fills the rest, so a page still draws a usable map if the fetch fails */
        var p = byNo[w.no] || {};
        var area = areas[p.a] || {};
        var img = w.img || p.img || '';
        return {
          no: w.no,
          lat: w.lat != null ? w.lat : p.lat,
          lng: w.lng != null ? w.lng : p.lng,
          name: w.name || p.n || ('Building ' + w.no),
          street: w.street || p.s || '',
          area: p.a || cfg.area || '',
          areaLabel: w.areaLabel || area.name || '',
          beds: w.beds || bedLabel(p),
          rent: p.pmin == null ? '' : 'From $' + Math.round(p.pmin).toLocaleString('en-US'),
          img: img.replace('w_600,h_400', 'w_420,h_280').replace('w_700,h_500', 'w_420,h_300'),
          url: w.url || (p.u ? BASE + 'buildings/' + p.u + '.html' : '#')
        };
      }).filter(function (p) { return p.lat != null && p.lng != null; });

      if (!pts.length) return;

      var opts = {
        el: '#' + el.id,
        points: pts,
        theme: cfg.theme || 'light',
        label: cfg.label || null
      };
      if (cfg.bubbles && ix && ix.areas) {
        opts.areas = {};
        Object.keys(ix.areas).forEach(function (k) {
          opts.areas[k] = { name: ix.areas[k].name, count: ix.areas[k].count };
        });
      }
      /* map.js fits the bounds of whatever it is given. A single building has no
         bounds worth fitting, and a two-building neighbourhood fits at zoom 18 —
         close enough to read the parking stripes and useless for placing the
         building in its city. Settle both cases after the fit. */
      var CEIL = cfg.maxZoom || 15;
      opts.onReady = function (m) {
        if (cfg.zoom) m.setView([pts[0].lat, pts[0].lng], cfg.zoom, { animate: false });
        else if (m.getZoom() > CEIL) m.setZoom(CEIL, { animate: false });
        setTimeout(function () { m.invalidateSize(); }, 40);
      };
      W.map(opts);
    }

    function bedLabel(p) {
      if (p.bmin == null && p.bmax == null) return '';
      var lo = p.bmin == null ? p.bmax : p.bmin, hi = p.bmax == null ? p.bmin : p.bmax;
      if (lo === 0 && hi === 0) return 'Studio';
      if (lo === hi) return lo + ' bed';
      return (lo === 0 ? 'Studio' : lo) + '–' + hi + ' bed';
    }

    function visible(el) {
      return !!(el.offsetParent || el.getClientRects().length);
    }

    function start(el) {
      if (el.dataset.mapped) return;
      if (!visible(el)) { if (pending.indexOf(el) < 0) pending.push(el); return; }
      el.dataset.mapped = '1';
      var cfg = cfgOf(el);
      loadIndex().then(function (ix) { build(el, cfg, ix); });
    }

    hosts.forEach(start);
    /* a map inside a hidden view has no width; Leaflet would size it to zero.
       The view switch wakes it the moment its pane is shown. */
    W.wakeMaps = function () {
      pending.slice().forEach(function (el) {
        if (visible(el)) {
          pending.splice(pending.indexOf(el), 1);
          start(el);
        }
      });
      if (W.mapInstance) setTimeout(function () { W.mapInstance.invalidateSize(); }, 60);
    };
  })();

  /* ------------------------------------------------------------------------
     4. THE OPENERS — the one column-wide plate that opens a run scales 1.00 to
     1.04 across one viewport of scroll. Transform only, no second rAF loop,
     and only for the frames currently near the viewport: an
     IntersectionObserver keeps the measured set small.
  --------------------------------------------------------------------------*/
  (function openers() {
    var frames = $$('.pl--open .pl-frame');
    if (!frames.length || W.reduce) return;
    var live = [];
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var i = live.indexOf(e.target);
        if (e.isIntersecting) { if (i < 0) live.push(e.target); }
        else if (i >= 0) { live.splice(i, 1); }
      });
    }, { rootMargin: '200px 0px' });
    frames.forEach(function (f) { io.observe(f); });

    W.onScroll(function () {
      var vh = innerHeight;
      for (var i = 0; i < live.length; i++) {
        var r = live[i].getBoundingClientRect();
        var t = W.clamp01((vh - r.top) / (vh + r.height));
        live[i].style.setProperty('--z', (1 + t * 0.04).toFixed(4));
      }
    });
  })();

  /* ------------------------------------------------------------------------
     5. TYPEAHEAD — the search field. The form is a real GET form, so it still
     goes somewhere with JS off.
  --------------------------------------------------------------------------*/
  (function search() {
    var input = $('[data-typeahead]');
    if (!input) return;
    loadIndex().then(function (ix) {
      if (!ix || !ix.p) return;
      var areas = ix.areas || {};
      var items = ix.p.map(function (p) {
        var area = (areas[p.a] && (areas[p.a].name || areas[p.a])) || p.a;
        /* no register number in the results (or in the haystack): the client
           does not want the properties numbered anywhere a reader can see */
        return {
          hay: (p.n + ' ' + p.s + ' ' + area).toLowerCase(),
          no: '',
          name: p.n,
          sub: p.s + ' · ' + area,
          url: BASE + 'buildings/' + p.u + '.html'
        };
      });
      W.typeahead({ input: '[data-typeahead]', out: '[data-typeahead-out]', items: items });
    });
  })();

  /* ------------------------------------------------------------------------
     6. AVAILABILITY FILTERS — search.html only.
  --------------------------------------------------------------------------*/
  if ($('[data-filters]')) {
    W.filters({
      form: '[data-filters]',
      rows: '[data-avrow]',
      count: '[data-avcount]',
      empty: '[data-avempty]'
    });
  }

  /* ------------------------------------------------------------------------
     7. VIEW SWITCH
     buildings.html  ?view=register | atlas | plates
     A pane may belong to several views (the index rows stay on screen under
     ?view=atlas so the row/pin highlight has something to highlight), and a
     [data-showin] element swaps the specimen plate for the map in the rail,
     and hides the sort group under Photographs. The strip is re-measured on
     every switch, because the collection it reads changes with the view.
  --------------------------------------------------------------------------*/
  (function views() {
    var btns = $$('[data-viewbtn]');
    if (!btns.length) return;
    var panes = $$('[data-viewpane]');
    var shows = $$('[data-showin]');

    function show(name, push) {
      btns.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.viewbtn === name)); });
      panes.forEach(function (p) { p.hidden = !inList(p.dataset.viewpane, name); });
      shows.forEach(function (e) { e.hidden = !inList(e.dataset.showin, name); });
      if (push !== false) {
        try {
          var u = new URL(location.href);
          u.searchParams.set('view', name);
          history.replaceState(null, '', u);
        } catch (e) {}
      }
      if (W.wakeMaps) W.wakeMaps();
      if (W.soilStrip) W.soilStrip();
      W.pump();
    }
    btns.forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); show(b.dataset.viewbtn); }); });
    var q = new URLSearchParams(location.search).get('view');
    show(btns.some(function (b) { return b.dataset.viewbtn === q; }) ? q : btns[0].dataset.viewbtn, false);
  })();

  /* ------------------------------------------------------------------------
     8. MENU HOUSEKEEPING — core.js makes <main> inert while the overlay is
     open; anything else that is focusable outside <main> opts in with
     data-menu-inert.
  --------------------------------------------------------------------------*/
  (function menuInert() {
    var btn = $('.mbtn');
    var targets = $$('[data-menu-inert]');
    if (!btn || !targets.length || !window.MutationObserver) return;
    new MutationObserver(function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      targets.forEach(function (el) { el.inert = open; });
    }).observe(btn, { attributes: true, attributeFilter: ['aria-expanded'] });
  })();

  /* ------------------------------------------------------------------------
     9. ANCHOR LANDINGS — the fixed header and the strip would otherwise cover
     the heading a same-page link lands on. scroll-margin-top does the work in
     CSS; this only re-pumps the scroll subscribers after the jump.
  --------------------------------------------------------------------------*/
  addEventListener('hashchange', function () { W.pump(); });

  /* ------------------------------------------------------------------------
     10. INQUIRE — contact.html, arrived at from a building page's Inquire
     button (?building=<slug>). The form is written by the shared generator
     and carries a "Building or street" field: it is filled with the
     building's name and street, the topic is set to Leasing, one line above
     the form names the building (with a way back to its page), and the page
     opens on the form. An unknown slug fills nothing rather than a guess.
  --------------------------------------------------------------------------*/
  (function inquire() {
    var form = $('form.ed-form');
    if (!form) return;
    var slug = new URLSearchParams(location.search).get('building');
    if (!slug || !/^[a-z0-9-]+$/.test(slug)) return;
    var field = form.querySelector('[name="building"]'), topic = form.querySelector('[name="topic"]');
    loadIndex().then(function (ix) {
      var p = null;
      if (ix && ix.p) ix.p.forEach(function (q) { if (q.u === slug) p = q; });
      if (!p) return;
      if (field && !field.value) field.value = p.n + ' — ' + p.s;
      if (topic) topic.selectedIndex = 0;
      var line = doc.createElement('p');
      line.className = 'ed-about';
      line.id = 'inquire';
      line.appendChild(doc.createTextNode('About '));
      var b = doc.createElement('b'); b.textContent = p.n; line.appendChild(b);
      line.appendChild(doc.createTextNode(' · '));
      var a = doc.createElement('a'); a.href = BASE + 'buildings/' + p.u + '.html'; a.textContent = p.s; line.appendChild(a);
      form.parentNode.insertBefore(line, form);
      try { line.scrollIntoView({ block: 'start', behavior: 'instant' }); } catch (e) { line.scrollIntoView(true); }
      W.pump();
    });
  })();

  /* ------------------------------------------------------------------------
     11. THE ACTION BARS — the pinned action row (.acts, fixed under the
     header) and, on a phone, the fixed bottom bar (.mbar). Both carry the
     building's Apply / Call and both slide in only once the hero trio (.cta,
     in the facts strip) has scrolled up past the header: while the trio is on
     screen the pinned row would duplicate it a hairline below and the phone
     bar would sit over the facts. The bars gain `.in` when the trio's foot
     clears the header band and lose it when it returns. The phone bar also
     steps aside (`.off`) while the footer is on screen, so it never covers
     the footer's links or the Equal Housing mark. Transform and opacity only;
     the single WR.onScroll loop, no second rAF.
  --------------------------------------------------------------------------*/
  (function actionBars() {
    var cta = $('[data-cta]');
    var bars = $$('[data-acts],[data-mbar]');
    if (cta && bars.length) {
      var on = null;
      var check = function () {
        var hd = parseInt(getComputedStyle(root).getPropertyValue('--hd-h'), 10);
        if (isNaN(hd)) hd = 64;
        var past = cta.getBoundingClientRect().bottom <= hd + 1;
        if (past === on) return;
        on = past;
        bars.forEach(function (b) { b.classList.toggle('in', past); });
      };
      W.onScroll(check);
      check();
    }
    /* the phone bar steps aside while the footer is on screen */
    var bar = $('[data-mbar]'), foot = $('footer.colophon');
    if (bar && foot && window.IntersectionObserver) {
      new IntersectionObserver(function (es) {
        bar.classList.toggle('off', es[es.length - 1].isIntersecting);
      }).observe(foot);
    }
  })();

  /* ------------------------------------------------------------------------
     12. THE WIDOW GUARD — no heading, lede or caption ends on a word alone on
     its line (client note, round 7). The generator ties the last two words of
     everything it writes with a no-break space; this does the same for copy
     the shared generator writes (company, residents, contact) and for every
     building name, so the rule holds at every width without a per-heading
     exception. The last run of whitespace before the last word becomes one
     no-break space, wherever in the element's text nodes it falls (it may be
     the space before a [CLIENT] chip). Flex and grid containers are left
     alone — a no-break space between two flex items would be a third — and a
     <br> the shared generator wrote into a display heading becomes a space,
     so the heading can balance its own lines. text-wrap:balance / pretty in
     style.css do the rest.
  --------------------------------------------------------------------------*/
  (function widows() {
    var SEL = 'h1,h2,h3,.hero-sub,.hsec-sub,.hsec-p,.pagehead-sub,.shead-sub,.lead,.ed-lede,' +
              '.reg-head-sub,figcaption,.cite,.plans-none,.reg-note span,.reg-legend span,.avail-line,' +
              '.ed-note,.ed-row p,.ed-copy p,.hsec-eyebrow span,.run-eyebrow span,.pagehead-no span,' +
              '.essay-kicker,.prose p,.card-nm';
    var NBSP = ' ';
    $$(SEL).forEach(function (el) {
      if (el.classList.contains('vh') || el.closest('.colophon,.mnav')) return;
      var d = getComputedStyle(el).display;
      if (d.indexOf('flex') >= 0 || d.indexOf('grid') >= 0) return;
      if (el.matches('.ed-h1')) {
        $$('br', el).forEach(function (br) { br.parentNode.replaceChild(doc.createTextNode(' '), br); });
      }
      var nodes = [], full = '', n;
      var walker = doc.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      while ((n = walker.nextNode())) {
        if (n.parentElement && n.parentElement.closest('.vh')) continue;
        nodes.push({ n: n, start: full.length });
        full += n.nodeValue;
      }
      var m = /(\s+)(\S+)(\s*)$/.exec(full);
      if (!m || !/\S/.test(full.slice(0, m.index))) return;          /* one word: nothing to tie */
      var runStart = m.index, runEnd = m.index + m[1].length, placed = false;
      nodes.forEach(function (o) {
        var len = o.n.nodeValue.length;
        var a = Math.max(runStart, o.start), b = Math.min(runEnd, o.start + len);
        if (a >= b) return;
        var v = o.n.nodeValue, i = a - o.start, j = b - o.start;
        o.n.nodeValue = v.slice(0, i) + (placed ? '' : NBSP) + v.slice(j);
        placed = true;
      });
    });
  })();

})();
