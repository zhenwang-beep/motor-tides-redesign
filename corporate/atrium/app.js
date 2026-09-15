/* ============================================================================
   WISEMAN RESIDENTIAL — DIRECTION "CLERESTORY" (key: atrium)
   One file for every page. Everything is guarded by element presence, so a page
   with no map / register / filters / contact form simply skips that block.

   Depends on core/core.js, and core/map.js / rail.js wherever a page carries a
   map or a rail. Adds NO second requestAnimationFrame loop: every scroll-bound
   mechanic subscribes to the single WR.onScroll dispatcher, and every mechanic
   branches on WR.reduce. Motion is transform/opacity/clip-path only.

   Root attributes each page sets on <html>:
     data-base="" | "../"                 prefix for links built in JS
     data-data="../data/wiseman.json"     WR.load()
     data-index="../data/index.json"      map + typeahead source
   ========================================================================== */
(function () {
  'use strict';
  var W = window.WR;
  if (!W) return;
  var doc = document, root = doc.documentElement;
  var BASE = root.dataset.base || '';

  function $(s, c) { return (c || doc).querySelector(s); }
  function $$(s, c) { return [].slice.call((c || doc).querySelectorAll(s)); }
  function inList(a, n) { return (a || '').split(/\s+/).indexOf(n) >= 0; }

  /* -------------------------------------------------- expanded-nav open state
     core.js owns the menu (open/close, <main> inert, Escape, focus return to
     the button). This only mirrors its state onto <body> and relabels the
     control, so the header can present a proper open-state: the burger becomes
     a ringed white cross on the deep-teal panel and announces itself as
     "Close". Watching aria-expanded rather than wrapping the click keeps every
     path in sync — button, link click, Escape. */
  (function menuState() {
    var btn = $('.mbtn'), nav = $('.mnav');
    if (!btn || !nav || !window.MutationObserver) return;
    function sync() {
      var on = btn.getAttribute('aria-expanded') === 'true';
      doc.body.classList.toggle('menu-open', on);
      btn.setAttribute('aria-label', on ? 'Close' : 'Menu');
    }
    new MutationObserver(sync).observe(btn, { attributes: true, attributeFilter: ['aria-expanded'] });
    sync();
  })();

  /* -------------------------------------------------- reveals (rv / rvi / rvl)
     Motor Tides observes at `threshold:0.12` with NO root margin
     (ref/home.html). This used to add `rootMargin:'0px 0px -6% 0px'`, which
     holds a reveal back until the element is 6% of the viewport past the fold
     — so a block that is already fully on screen is still waiting, and then
     pops as you keep scrolling. Dropping the inset lets each block begin the
     moment it enters, which is both earlier and calmer: the travel is spent
     while you are still scrolling toward it rather than after you arrive. */
  (function reveals() {
    var els = $$('.rv, .rvi, .rvl');
    if (!els.length) return;
    if (W.reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    var kick = function () { els.forEach(function (e) { io.observe(e); }); };
    if (doc.fonts && doc.fonts.ready) {
      doc.fonts.ready.then(function () { requestAnimationFrame(kick); });
      setTimeout(kick, 600);
    } else kick();
  })();

  /* -------------------------------------------------- living monogram
     Owns two jobs on the home hero, and nothing anywhere else.

     1. OVERFLOW GUARD. The CSS clamp sizes WISEMAN to its natural width at
        ~72-85% of the viewport, so it fits by construction; textLength is gone
        (stretching over-tracked it on desktop, and `spacingAndGlyphs` squashed
        Prata's glyphs below 1024). This only ever COMPRESSES, and only if some
        odd aspect ratio or a fallback font would push the caps into the gutter.

     2. BEAT 3. The CSS keyframes play beats 1 and 2 on their own. Once they are
        spent we add .mono-settled — which switches those keyframes off, since a
        `both`-filled animation outranks an inline style — and drive the reveal
        from the single WR.onScroll dispatcher: the letters scale back out while
        the veil and tone fade off, re-opening the full frame over the runway.
        Transform and opacity only.

     Plus the video hook: .src is assigned only when data-src is non-empty, the
     clip fades in on `playing`, and any error hides it for good. The wr03 still
     underneath is the fallback at every step. */
  (function monogram() {
    var word = $('.mono-letters');
    if (!word) return;
    var hero = word.closest('.hero-mono');
    var runway = hero && hero.closest('.hero-runway');
    var veil = $('.mono-veil', hero);
    var tone = $('.mono-tone', hero);
    var duo = $('.mono-duo', hero);
    var type = $('.mono-type', hero);
    var content = $('.mono-content', hero);
    var scroll = $('.mono-scroll', hero);
    var video = $('.mono-video', hero);

    /* ---- 1. overflow guard (compress only, never stretch) ---- */
    function fit() {
      if (!word.getComputedTextLength) return;
      word.removeAttribute('textLength');
      word.removeAttribute('lengthAdjust');
      var pad = parseInt(getComputedStyle(root).getPropertyValue('--pad'), 10);
      if (isNaN(pad)) pad = 24;
      var room = (hero ? hero.clientWidth : root.clientWidth) - pad * 2;
      var natural = word.getComputedTextLength();
      if (natural > room && room > 0) {
        word.setAttribute('lengthAdjust', 'spacingAndGlyphs');
        word.setAttribute('textLength', Math.round(room));
      }
    }

    /* ---- 2. beat 3 ---- */
    var settled = false, top = 0, span = 1, queued = false;
    function measure() {
      if (!runway || !hero) return;
      top = runway.getBoundingClientRect().top + scrollY;
      span = Math.max(1, runway.offsetHeight - hero.offsetHeight);
    }
    function render() {
      queued = false;
      if (!settled || !runway) return;
      var p = Math.max(0, Math.min(1, (scrollY - top) / span));
      /* hold for the first tenth, then a smoothstep out to the open frame */
      var r = Math.max(0, Math.min(1, (p - 0.1) / 0.7));
      r = r * r * (3 - 2 * r);
      if (type) type.style.transform = 'scale(' + (1 + r * 0.55) + ')';
      if (veil) veil.style.opacity = String(1 - r);
      if (tone) tone.style.opacity = String(1 - r);
      if (duo) duo.style.opacity = String(1 - r);
      var c = 1 - Math.max(0, Math.min(1, (p - 0.04) / 0.26));
      if (content) { content.style.opacity = String(c); content.inert = c === 0; }
      if (scroll) scroll.style.opacity = String(c * 0.7);
    }
    function settle() {
      if (settled) return;
      settled = true;
      if (hero) hero.classList.add('mono-settled');
      measure();
      render();
    }

    if (W.reduce || !runway) {
      /* static end state: no beats to wait for, nothing to drive */
      if (hero) hero.classList.add('mono-settled');
    } else {
      /* settle when the last beat finishes, and on any of the usual escapes */
      if (scroll) scroll.addEventListener('animationend', settle);
      setTimeout(settle, 3800);   /* the last beat now ends at 2.48s + 1.2s */
      addEventListener('pointerdown', settle, { once: true, passive: true });
      addEventListener('keydown', settle, { once: true });
      W.onScroll(function (y) {
        if (!settled && y > 24) settle();
        if (!queued) { queued = true; requestAnimationFrame(render); }
      });

      /* park the ambient breathe (and the clip) whenever the hero is off screen */
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) {
          var seen = es[0].isIntersecting;
          hero.classList.toggle('mono-still', !seen);
          if (video && video.src) { seen ? video.play().catch(function () {}) : video.pause(); }
        }).observe(hero);
      }

      /* ---- video hook — see the comment above the markup in gen_register.py */
      if (video && video.dataset.src) {
        video.addEventListener('playing', function () { video.classList.add('on'); });
        video.addEventListener('error', function () { video.classList.remove('on'); video.hidden = true; });
        video.src = video.dataset.src;
        var go = video.play();
        if (go && go.catch) go.catch(function () { video.classList.remove('on'); });
      }
    }

    if (doc.fonts && doc.fonts.ready) {
      doc.fonts.ready.then(function () { fit(); measure(); render(); });
      setTimeout(function () { fit(); measure(); render(); }, 400);
    } else { fit(); measure(); render(); }

    var tid;
    addEventListener('resize', function () {
      clearTimeout(tid);
      tid = setTimeout(function () { fit(); measure(); render(); }, 120);
    }, { passive: true });
  })();

  /* -------------------------------------------------- header: frost + invert
     Never retracts (style.css neutralises .up). Transparent over the bright
     masthead; frosts once the page scrolls; inverts to light while any
     [data-hd="dark"] hero sits under the header band. */
  (function header() {
    var hd = $('.hd');
    if (!hd) return;
    W.onScroll(function (y) { hd.classList.toggle('frost', y > 18); });
    var dark = $$('[data-hd="dark"]');
    if (dark.length && 'IntersectionObserver' in window) {
      var lit = [];
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var i = lit.indexOf(e.target);
          if (e.isIntersecting) { if (i < 0) lit.push(e.target); }
          else if (i >= 0) lit.splice(i, 1);
        });
        hd.classList.toggle('inv', lit.length > 0);
      }, { rootMargin: '0px 0px -90% 0px' });
      dark.forEach(function (e) { io.observe(e); });
    }
    W.pump();
  })();

  /* the shared spine: menu. W.favourites() is deliberately NOT booted here —
     the client does not want a favourites function on this site, so Clerestory
     ships no Save control on a card or a building page and nothing listens for
     one. The shared helper stays intact for the other directions. */
  W.menu();

  /* ------------------------------------------------------------- transition
     The Motor Tides page transition, to the millisecond — the concept the
     client picked. This DELIBERATELY replaces core's W.transition() rather
     than running beside it: core navigates 620ms after the cover starts,
     which is 20ms after its own .6s panel lands, so the curtain arrives and
     the page swaps in the same frame and the whole move reads as a snap.
     Motor Tides holds 950ms — .6s of travel on cubic-bezier(.65,0,.35,1)
     plus ~350ms of settled cover — and that pause is most of the smoothness.
     The retract is pure CSS (`.js-pt .pt` keyframes in style.css), so there
     is no `reveal` class here and nothing to schedule on load.

     Everything else matches core: same link filter (skip hashes, new tabs,
     downloads, cross-origin and non-http schemes, modified clicks), same
     bfcache handling, and a hard bail under prefers-reduced-motion, where
     the curtain never paints and links behave natively. */
  (function transition() {
    var pt = $('.pt');
    if (!pt) return;
    addEventListener('pageshow', function (e) { if (e.persisted) pt.classList.remove('cover'); });
    if (W.reduce) return;
    doc.addEventListener('click', function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a') : null;
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      if (a.target === '_blank' || a.hasAttribute('download')) return;
      var href = a.getAttribute('href') || '';
      if (!href || href.charAt(0) === '#' || /^(https?|tel|mailto):/i.test(href)) return;
      if (a.origin && a.origin !== location.origin) return;
      e.preventDefault();
      pt.classList.add('cover');
      var url = a.href;
      setTimeout(function () { location.href = url; }, 950);
    });
  })();

  /* -------------------------------------------------- data index (map/typeahead) */
  var idxPromise = null;
  function loadIndex() {
    if (!idxPromise) {
      idxPromise = fetch(root.dataset.index || '../data/index.json')
        .then(function (r) { return r.json(); }).catch(function () { return null; });
    }
    return idxPromise;
  }

  /* -------------------------------------------------- register (sortable index) */
  if ($('[data-register]') && $('[data-sort]')) {
    W.register({ list: '[data-register]',
      flatLabel: 'All ' + $$('[data-row]').length + ' buildings' });
  }

  /* -------------------------------------------------- the real map (core/map.js) */
  (function maps() {
    var hosts = $$('[data-map]');
    if (!hosts.length || !W.map) return;
    var pending = [];
    function cfgOf(el) { try { return JSON.parse(el.getAttribute('data-map') || '{}'); } catch (e) { return {}; } }
    function bedLabel(p) {
      if (p.bmin == null && p.bmax == null) return '';
      var lo = p.bmin == null ? p.bmax : p.bmin, hi = p.bmax == null ? p.bmin : p.bmax;
      if (lo === 0 && hi === 0) return 'Studio';
      if (lo === hi) return lo + ' bed';
      return (lo === 0 ? 'Studio' : lo) + '–' + hi + ' bed';
    }
    function build(el, cfg, ix) {
      var areas = (ix && ix.areas) || {}, byNo = {};
      if (ix && ix.p) ix.p.forEach(function (p) { byNo[p.no] = p; });
      var wanted;
      if (cfg.one) wanted = [cfg.one];
      else if (cfg.points && cfg.points.length) wanted = cfg.points;
      else if (cfg.area) wanted = (ix && ix.p ? ix.p : []).filter(function (p) { return p.a === cfg.area; });
      else wanted = (ix && ix.p) ? ix.p : [];
      var pts = wanted.map(function (w) {
        var p = byNo[w.no] || {}, area = areas[p.a] || {}, img = w.img || p.img || '';
        return {
          no: w.no, lat: w.lat != null ? w.lat : p.lat, lng: w.lng != null ? w.lng : p.lng,
          name: w.name || p.n || ('Building ' + w.no), street: w.street || p.s || '',
          area: p.a || cfg.area || '', areaLabel: w.areaLabel || area.name || '',
          beds: w.beds || bedLabel(p),
          rent: p.pmin == null ? '' : 'From $' + Math.round(p.pmin).toLocaleString('en-US'),
          img: img.replace('w_600,h_400', 'w_420,h_280').replace('w_700,h_500', 'w_420,h_300'),
          url: w.url || (p.u ? BASE + 'buildings/' + p.u + '.html' : '#')
        };
      }).filter(function (p) { return p.lat != null && p.lng != null; });
      if (!pts.length) return;
      var opts = { el: '#' + el.id, points: pts, theme: cfg.theme || 'light', label: cfg.label || null };
      if (cfg.bubbles && ix && ix.areas) {
        opts.areas = {};
        Object.keys(ix.areas).forEach(function (k) { opts.areas[k] = { name: ix.areas[k].name, count: ix.areas[k].count }; });
      }
      var CEIL = cfg.maxZoom || 15;
      opts.onReady = function (m) {
        if (cfg.zoom) m.setView([pts[0].lat, pts[0].lng], cfg.zoom, { animate: false });
        else if (m.getZoom() > CEIL) m.setZoom(CEIL, { animate: false });
        setTimeout(function () { m.invalidateSize(); }, 40);
      };
      W.map(opts);
    }
    function visible(el) { return !!(el.offsetParent || el.getClientRects().length); }
    function start(el) {
      if (el.dataset.mapped) return;
      if (!visible(el)) { if (pending.indexOf(el) < 0) pending.push(el); return; }
      el.dataset.mapped = '1';
      var cfg = cfgOf(el);
      loadIndex().then(function (ix) { build(el, cfg, ix); });
    }
    hosts.forEach(start);
    W.wakeMaps = function () {
      pending.slice().forEach(function (el) {
        if (visible(el)) { pending.splice(pending.indexOf(el), 1); start(el); }
      });
      if (W.mapInstance) setTimeout(function () { W.mapInstance.invalidateSize(); }, 60);
    };
  })();

  /* -------------------------------------------------- typeahead */
  (function search() {
    var input = $('[data-typeahead]');
    if (!input) return;
    loadIndex().then(function (ix) {
      if (!ix || !ix.p) return;
      var areas = ix.areas || {};
      var items = ix.p.map(function (p) {
        var area = (areas[p.a] && (areas[p.a].name || areas[p.a])) || p.a;
        return { hay: (p.n + ' ' + p.s + ' ' + area).toLowerCase(), no: '', name: p.n,
          sub: p.s + ' · ' + area, url: BASE + 'buildings/' + p.u + '.html' };
      });
      W.typeahead({ input: '[data-typeahead]', out: '[data-typeahead-out]', items: items });
    });
  })();

  /* -------------------------------------------------- view switch (buildings.html) */
  (function views() {
    var btns = $$('[data-viewbtn]');
    if (!btns.length) return;
    var panes = $$('[data-viewpane]'), shows = $$('[data-showin]');
    function show(name, push) {
      btns.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.viewbtn === name)); });
      panes.forEach(function (p) { p.hidden = !inList(p.dataset.viewpane, name); });
      shows.forEach(function (e) { e.hidden = !inList(e.dataset.showin, name); });
      if (push !== false) {
        try { var u = new URL(location.href); u.searchParams.set('view', name); history.replaceState(null, '', u); } catch (e) {}
      }
      if (W.wakeMaps) W.wakeMaps();
      W.pump();
    }
    btns.forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); show(b.dataset.viewbtn); }); });
    var q = new URLSearchParams(location.search).get('view');
    show(btns.some(function (b) { return b.dataset.viewbtn === q; }) ? q : btns[0].dataset.viewbtn, false);
  })();

  /* -------------------------------------------------- opener frames (photographs view)
     the column-wide plate that opens a run scales 1.00 -> 1.04 across one
     viewport of scroll; only the frames near the viewport are measured. */
  (function openers() {
    var frames = $$('.pl--open .pl-frame');
    if (!frames.length || W.reduce) return;
    var live = [];
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var i = live.indexOf(e.target);
        if (e.isIntersecting) { if (i < 0) live.push(e.target); }
        else if (i >= 0) live.splice(i, 1);
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

  /* -------------------------------------------------- building action bars */
  (function actionBars() {
    var cta = $('[data-cta]'), bars = $$('[data-acts],[data-mbar]');
    if (cta && bars.length) {
      var on = null;
      var check = function () {
        var hd = parseInt(getComputedStyle(root).getPropertyValue('--hd-h'), 10);
        if (isNaN(hd)) hd = 70;
        var past = cta.getBoundingClientRect().bottom <= hd + 1;
        if (past === on) return;
        on = past;
        bars.forEach(function (b) { b.classList.toggle('in', past); });
      };
      W.onScroll(check); check();
    }
    var bar = $('[data-mbar]'), foot = $('footer.ft');
    if (bar && foot && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        bar.classList.toggle('off', es[es.length - 1].isIntersecting);
      }).observe(foot);
    }
  })();

  /* -------------------------------------------------- contact prefill (?building=slug) */
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
      line.className = 'ed-note'; line.id = 'inquire';
      line.style.marginBottom = '20px';
      line.appendChild(doc.createTextNode('About '));
      var b = doc.createElement('b'); b.textContent = p.n; line.appendChild(b);
      line.appendChild(doc.createTextNode(' · '));
      var a = doc.createElement('a'); a.href = BASE + 'buildings/' + p.u + '.html'; a.textContent = p.s;
      a.style.color = 'var(--teal-ink)'; line.appendChild(a);
      form.parentNode.insertBefore(line, form);
      try { line.scrollIntoView({ block: 'start', behavior: 'instant' }); } catch (e) { line.scrollIntoView(true); }
      W.pump();
    });
  })();

  /* -------------------------------------------------- menu housekeeping */
  (function menuInert() {
    var btn = $('.mbtn'), targets = $$('[data-menu-inert]');
    if (!btn || !targets.length || !window.MutationObserver) return;
    new MutationObserver(function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      targets.forEach(function (el) { el.inert = open; });
    }).observe(btn, { attributes: true, attributeFilter: ['aria-expanded'] });
  })();

  addEventListener('hashchange', function () { W.pump(); });

  /* -------------------------------------------------- widow guard
     No heading, lede or caption ends on a word alone on its line. The last run
     of whitespace before the last word becomes one no-break space. Flex/grid
     containers are skipped (a nbsp between two items would be a third).

     TWO THINGS IT MUST NOT DO, both of which it was doing. A no-break space is
     not free: it DELETES a break opportunity. Where the surviving run is wider
     than the box it sits in, `overflow-wrap:break-word` then cuts that run
     wherever the edge falls, and the reader gets a word sawn in half with no
     hyphen — "Reasonable accommodatio / n" on accessibility.html at 1440, and
     "Venice Bouleva / rd", "Our commitme / nt", "Maintenance e / mergency" in
     the 144px editorial label track at 768. Nineteen of them across seven
     pages, every one of them a heading this guard had just glued. */
  (function widows() {
    var SEL = 'h1,h2,h3,.hero .sub,.band-head p,.pagehead-sub,.shead-sub,.lead,.ed-lede,' +
      '.reg-head-sub,figcaption,.cite,.plans-none,.reg-legend span,.avail-line,.ed-note,' +
      '.ed-row p,.ed-copy p,.card .nm,.fnl p,.pillar p,.promise .trust span,.track p,.fbhero .sub';
    var NBSP = ' ';
    $$(SEL).forEach(function (el) {
      if (el.classList.contains('vh') || el.closest('.ft,.mnav')) return;
      /* 2. The editorial row label sits in a FIXED track — core/editorial.css
         gives it clamp(9rem,18vw,16rem), so 144px from 760px up to about 890px
         — and holds short address and topic phrases. There is no width for a
         glued tail to fall back into; "9000-9020 Venice Boulevard" glued is one
         166px run in a 144px box. The label wraps on its own spaces instead. */
      if (el.matches('.ed-row > h3')) return;
      var d = getComputedStyle(el).display;
      if (d.indexOf('flex') >= 0 || d.indexOf('grid') >= 0) return;
      var nodes = [], full = '', n;
      var walker = doc.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      while ((n = walker.nextNode())) {
        if (n.parentElement && n.parentElement.closest('.vh')) continue;
        nodes.push({ n: n, start: full.length }); full += n.nodeValue;
      }
      var m = /(\s+)(\S+)(\s*)$/.exec(full);
      if (!m || !/\S/.test(full.slice(0, m.index))) return;
      /* 1. Two words cannot widow. There is no line the second could be alone
         on that the first is not already on, so gluing them prevents nothing
         and removes the only break point the phrase has. Where the pair fits,
         glued and unglued render identically; where it does not, the glue is
         the whole defect. Three words is the first case with a widow to fix. */
      if (full.trim().split(/\s+/).length < 3) return;
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

  /* ----------------------------------------------- search field placeholder
     scripts/gen_search.py is shared by every direction and ships a 33-character
     placeholder, "Building, street or neighbourhood". It renders 266px wide at
     the desktop size and 288px at the 16px mobile size — wider than the field
     can be at 360-390px without pushing the first filter button off the rail,
     so it was being sliced mid-word ("...neighbourhoo"). A placeholder is a
     hint, not a sentence: this is the same promise in 24 characters, and the
     full wording still reaches assistive tech through the field's own
     <label class="vh">, which is untouched. Atrium-scoped; the shared markup
     and every sibling direction are left exactly as they are. */
  (function searchChrome() {
    var q = $('.sbar .sfield input#q');
    if (q) q.placeholder = 'Building, street or area';
    /* The snapshot note carries a middot separator with an ordinary space on
       both sides, so on a phone-width column the break landed in front of it
       and line two opened on a floating "·". Binding the middot to the word it
       follows leaves it no way to start a line. */
    var note = $('.sresults .snote');
    if (note) note.innerHTML = note.innerHTML.replace(/\s+\u00B7\s/g, '\u00A0\u00B7 ');
  })();

  /* --------------------------------------------------- map pin: keep the name on the map
     The price pill now carries the building's NAME as well as the figure
     (core/map.js writes it, atrium/style.css reveals it). A named pill is
     ~200px wide against the ~46px it used to be, and Leaflet centres a marker
     icon on its address — so a pin sitting within 100px of the panel edge
     expanded straight into the map's own overflow clip and lost the first half
     of the name it had just been asked for.

     This nudges the expanded pill back inside. It measures the pill against the
     map's box and translates it the minimum distance that brings it fully in,
     clamped so the figure never walks further than half a pill from the address
     it belongs to. The translate lands on the INNER span; the 72x28
     .leaflet-marker-icon the pointer is actually over never moves, so the hover
     cannot chase itself off the element. Transform only, on the one brand ease
     core already transitions, and it is undone the moment the pointer leaves.

     Atrium-scoped by construction: --pin-dx is only read by this direction's
     stylesheet, and the shared map keeps its own behaviour untouched. */
  (function pinNudge() {
    var PAD = 6;
    /* How far the pill is translated AT THIS INSTANT. The nudge rides on a
       transitioned transform, so the moment a second pointerover arrives — and
       one always does, because the name the pill just revealed becomes a new
       element under the pointer — a naive re-measure reads the rect the nudge
       has already moved, decides the pill is safely inside, and cancels the
       very translate that put it there. The pill then slides back out and stays
       out. Measuring is only safe against the pill's UNNUDGED position. */
    function shift(pin) {
      var m = getComputedStyle(pin).transform;
      if (!m || m === 'none') return 0;
      var mm = m.match(/^matrix\(([^)]+)\)/);
      if (mm) return parseFloat(mm[1].split(',')[4]) || 0;
      var m3 = m.match(/^matrix3d\(([^)]+)\)/);
      if (m3) return parseFloat(m3[1].split(',')[12]) || 0;
      return 0;
    }
    function box(pin) {
      var host = pin.closest('.wr-map');
      if (!host) return null;
      var r = pin.getBoundingClientRect(), h = host.getBoundingClientRect();
      if (!r.width) return null;
      var tx = shift(pin), left = r.left - tx, right = r.right - tx, dx = 0;
      if (left < h.left + PAD) dx = (h.left + PAD) - left;
      else if (right > h.right - PAD) dx = (h.right - PAD) - right;
      /* never further than half a pill: the figure stays over its own address */
      var cap = Math.max(0, r.width / 2 - 10);
      dx = Math.max(-cap, Math.min(cap, dx));
      /* round AWAY from the edge, so the rounding can never put the tail back
         over it — a 0.2px shortfall is still a clipped letter */
      return dx < 0 ? Math.floor(dx) : Math.ceil(dx);
    }
    function place(pin) {
      if (!pin) return;
      var dx = box(pin);
      if (dx === null) return;
      pin.style.setProperty('--pin-dx', dx + 'px');
    }
    function clear(pin) { if (pin) pin.style.removeProperty('--pin-dx'); }
    function pinFor(el) {
      if (!el || !el.closest) return null;
      var direct = el.closest('.wr-pin.price');
      if (direct) return direct;
      /* keyboard focus lands on the .leaflet-marker-icon WRAPPER, not on the
         pill inside it, so the pointer path alone would have left a tabbed-to
         pin expanding straight off the edge of the map */
      if (el.querySelector) {
        var inner = el.classList && el.classList.contains('leaflet-marker-icon')
          ? el.querySelector('.wr-pin.price') : null;
        if (inner) return inner;
      }
      /* a register row lights its pin without the pointer ever going near it */
      var row = el.closest('[data-row][data-no]');
      return row ? document.querySelector('.wr-pin.price[data-no="' + row.dataset.no + '"]') : null;
    }
    ['pointerover', 'focusin'].forEach(function (t) {
      document.addEventListener(t, function (e) {
        var pin = pinFor(e.target);
        if (pin) requestAnimationFrame(function () { place(pin); });
      }, true);
    });
    ['pointerout', 'focusout'].forEach(function (t) {
      document.addEventListener(t, function (e) { clear(pinFor(e.target)); }, true);
    });
  })();

  W.pump();
})();


/* ---------------------------------------------------------------------------
   MORE-FILTERS DIALOG — let the close animation actually play.
   A <dialog> closes synchronously, so the out-keyframes never render: the panel
   just vanishes. Defer the real close until the animation ends. Escape does not
   route through .close(), it fires `cancel` and closes natively, so that is
   intercepted too. core/search.js's own open/close logic is untouched — this
   only delays the final native close.
--------------------------------------------------------------------------- */
(function fmodalMotion () {
  var d = document.querySelector('dialog.fmodal');
  if (!d || !d.close) return;
  var native = d.close.bind(d);
  var closing = false;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion:reduce)').matches;

  d.close = function (val) {
    if (closing || reduce || !d.open) { closing = false; return native(val); }
    closing = true;
    d.classList.add('is-closing');
    var done = function () {
      d.removeEventListener('animationend', onEnd);
      clearTimeout(t);
      d.classList.remove('is-closing');
      closing = false;
      native(val);
    };
    var onEnd = function (e) { if (e.target === d) done(); };
    d.addEventListener('animationend', onEnd);
    var t = setTimeout(done, 320);          /* never strand the dialog open */
  };

  d.addEventListener('cancel', function (e) { e.preventDefault(); d.close(); });
})();
