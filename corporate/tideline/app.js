/* =====================================================================
   WISEMAN RESIDENTIAL — direction: TIDELINE
   Direction JS. Loads AFTER ../core/core.js.

   Everything shared lives in core.js: WR.onScroll (the ONE rAF-gated
   dispatcher), WR.through, WR.pinned, WR.smooth, WR.clamp01, WR.lerp,
   WR.reveals, WR.header, WR.menu, WR.transition, WR.typeahead.

   This file adds exactly two mechanics, both HOME PAGE ONLY:
     A. the masked lockup — background-clip:text over one photograph,
        scroll-scrubbed across a 340vh runway, blooming to full-bleed.
     B. the tideline — ONE custom property (--tide) per section drives
        the travelling gap on the 1px rule and the bottom-fill mask on
        every photograph inside that section.

   Horizontal rails are NOT here: core/rail.js owns every one of them.

   Never add a second requestAnimationFrame loop. Every mechanic branches
   on WR.reduce to a static END state, not to a frozen mid-animation.
   ===================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;

  /* If core.js failed to load, drop the curtain class so the page is not
     left behind a permanent cover, and stop. */
  if (!window.WR) { root.classList.remove('js-pt'); return; }
  var W = window.WR;

  W.boot({ header: { heroEnd: 130 }, transition: true });

  var R2 = function (v) { return Math.round(v * 1000) / 1000; };

  /* ------------------------------------------------------------------
     SEARCH FIRST. The typeahead is wired before either cinematic
     mechanic. The form has a real action= and name="q", so it already
     works with no JS; this only makes it answer sooner.
     data/index.json is 22KB — the compact index — so the first keystroke
     is answered without pulling the 200KB portfolio file. WR.load is
     reserved for data/wiseman.json on pages that need the full record.
  ------------------------------------------------------------------ */
  (function search() {
    var input = document.querySelector('[data-ta-input]');
    if (!input) return;
    fetch('../data/index.json')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var areas = d.areas || {};
        var items = (d.p || []).map(function (p) {
          var area = (areas[p.a] && areas[p.a].name) || '';
          return {
            /* no register number in the haystack or the result: the client
               does not want the properties numbered anywhere visible. core.js
               still writes the .ta-no cell, so it is handed an empty string
               and style.css hides it. */
            hay: (p.n + ' ' + p.s + ' ' + area).toLowerCase(),
            no: '',
            name: p.n,
            sub: p.s + ' · ' + area,
            url: 'buildings/' + p.u + '.html'
          };
        });
        W.typeahead({ input: '[data-ta-input]', out: '[data-ta-out]', items: items });
        input.removeAttribute('aria-busy');
      })
      .catch(function () { input.removeAttribute('aria-busy'); });
  })();

  /* ------------------------------------------------------------------
     A. THE MASKED LOCKUP
     One element carries the photograph; its two block spans clip it, so
     the image paints once across the whole lockup and the two lines read
     as windows onto one continuous scene.

       p < 0.30   scale 0.94 → 1.02, background drifts 38% → 58%
       0.30–0.66  smoothstep the scale to peak (7.2, or 4.8 under 700px)
                  while the identical photograph fades up full-bleed
                  behind at a staggered offset — there is never a gap
       p >= 0.66  hold peak; push the full frame 1.00 → 1.06

     Scale never decreases on either element.
  ------------------------------------------------------------------ */
  (function lockup() {
    var sec = document.querySelector('[data-bloom]');
    if (!sec) return;
    var lock = sec.querySelector('[data-lockup]');
    var full = sec.querySelector('[data-bloomfull]');
    if (!lock) return;

    if (W.reduce) {
      /* static end state: the photograph stays in the letters as a piece
         of art. Only the bloom is deleted. */
      lock.style.setProperty('--lock-k', '1');
      lock.style.setProperty('--lock-x', '48%');
      lock.style.setProperty('--lock-o', '1');
      return;
    }

    var pk = -1, px = -1, po = -1, fo = -1, fk = -1;

    W.onScroll(function () {
      var p = W.pinned(sec);
      var peak = window.innerWidth < 700 ? 4.8 : 7.2;
      var k, x, o, bo, bk;

      if (p < 0.30) {
        var t = W.smooth(p / 0.30);
        k = W.lerp(0.94, 1.02, t);
        x = W.lerp(38, 58, t);
      } else {
        k = W.lerp(1.02, peak, W.smooth(W.clamp01((p - 0.30) / 0.36)));
        x = 58;
      }
      if (p >= 0.66) { k = peak; }

      /* the full frame is fully up (0.58) before the glyph edges leave */
      bo = W.smooth(W.clamp01((p - 0.34) / 0.24));
      bk = 1 + 0.06 * W.smooth(W.clamp01((p - 0.66) / 0.34));
      o = 1 - W.smooth(W.clamp01((p - 0.56) / 0.14));

      k = R2(k); x = Math.round(x * 10) / 10; o = R2(o); bo = R2(bo); bk = R2(bk);

      if (k !== pk) { pk = k; lock.style.setProperty('--lock-k', k); }
      if (x !== px) { px = x; lock.style.setProperty('--lock-x', x + '%'); }
      if (o !== po) { po = o; lock.style.setProperty('--lock-o', o); }
      if (full) {
        if (bo !== fo) { fo = bo; full.style.setProperty('--bloom-o', bo); }
        if (bk !== fk) { fk = bk; full.style.setProperty('--bloom-k', bk); }
      }
    });
  })();

  /* ------------------------------------------------------------------
     B. THE TIDELINE
     One property write per section per frame. --tide (0–100%) drives:
       · .tide-fill  clip-path: rect(0 calc(--tide - 14px) 100% 0)
       · .tide-track clip-path: rect(0 100% 100% calc(--tide + 14px))
         → a 28px gap travels left to right along a shared 1px rule
       · .tidefig img mask-image bottom fill → the photograph fills from
         the bottom like water rising

     CSS defaults --tide to 100%, so with no JS every rule is whole and
     every photograph is visible. This only animates it.
  ------------------------------------------------------------------ */
  (function tide() {
    var secs = [].slice.call(document.querySelectorAll('[data-tide]'));
    if (!secs.length) return;

    /* a full-bleed band starts part-filled: a 78svh photograph that begins
       at 0% would open as an empty frame. data-tide-min is that floor. */
    var floors = secs.map(function (el) { return +el.dataset.tideMin || 0; });

    if (W.reduce) {
      secs.forEach(function (el) {
        el.style.setProperty('--tide', '100%');
        el.style.setProperty('--tidek', '1');
      });
      return;
    }

    var last = secs.map(function () { return -1; });

    W.onScroll(function () {
      for (var i = 0; i < secs.length; i++) {
        var el = secs[i], lo = floors[i];
        /* remap: start filling once the section is properly in frame,
           finish before it leaves, so the gap travels while you read it */
        var t = W.smooth(W.clamp01((W.through(el) - 0.16) / 0.5));
        var v = Math.round((lo + (100 - lo) * t) * 10) / 10;
        if (v !== last[i]) {
          last[i] = v;
          el.style.setProperty('--tide', v + '%');
          /* the unitless twin: one extra write, no extra loop. It carries
             the settle on any full-bleed photograph inside this section. */
          el.style.setProperty('--tidek', Math.round(t * 1000) / 1000);
        }
      }
    });
  })();

  /* ------------------------------------------------------------------
     The Selected rail used to be wired here. It is now core/rail.js —
     one shared module for every horizontal scroller on the site, with the
     overflow scrollbar hidden and the arrow buttons as the control, exactly
     as the client asked. Pages that have a rail load ../core/rail.js and
     call WR.rails() once; app.js does not, so a page can never bind it twice.
  ------------------------------------------------------------------ */

  /* ------------------------------------------------------------------
     C. THE BUILDING'S INQUIRE ROUTE — contact.html?building=<slug>.
     The building page's Inquire button lands here. contact.html is built by
     the shared gen_editorial.py and we do NOT edit it: this reads the form it
     renders and drives it. The building field, the topic and a starter line
     are pre-set, and a small "About <building>" line is placed above the form.
     Guarded by the query param AND the form's own fields, so it is inert on
     the contact page with no building and on every other page.
  ------------------------------------------------------------------ */
  (function contactPrefill() {
    var params;
    try { params = new URLSearchParams(location.search); } catch (e) { return; }
    var slug = params.get('building');
    if (!slug) return;
    var form = document.querySelector('.ed-form');
    if (!form) return;
    var buildingField = form.querySelector('[name="building"]');
    var messageField = form.querySelector('[name="message"]');
    var topicField = form.querySelector('[name="topic"]');

    fetch('../data/index.json')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var areas = d.areas || {};
        var rec = (d.p || []).filter(function (p) { return p.u === slug; })[0];
        if (!rec) return;
        var area = (areas[rec.a] && areas[rec.a].name) || '';
        var where = rec.s + (area ? ', ' + area : '');

        if (buildingField && !buildingField.value) {
          buildingField.value = rec.n + (rec.s ? ' — ' + where : '');
        }
        if (topicField) {
          for (var i = 0; i < topicField.options.length; i++) {
            if (/leasing/i.test(topicField.options[i].text)) { topicField.selectedIndex = i; break; }
          }
        }
        if (messageField && !messageField.value) {
          messageField.value = 'I would like to enquire about ' + rec.n +
            ' (' + where + '). Please tell me what is available and how to apply.';
        }
        if (!document.querySelector('.ed-about')) {
          var line = document.createElement('p');
          line.className = 'ed-about';
          line.appendChild(document.createTextNode('About '));
          var b = document.createElement('b');
          b.textContent = rec.n;
          line.appendChild(b);
          if (where) { line.appendChild(document.createTextNode(' · ' + where)); }
          form.parentNode.insertBefore(line, form);
        }
      })
      .catch(function () {});
  })();

  /* ------------------------------------------------------------------
     D. THE PHONE ACTION BAR — a fixed Apply + Call bar under 640px.
     It must never sit over the footer, so it slides away (transform only)
     while the footer is on screen. Guarded by [data-botbar], so it only runs
     on a building page. Below 640 CSS shows it; above, it is display:none and
     the observer is harmless.
  ------------------------------------------------------------------ */
  (function botbar() {
    var bar = document.querySelector('[data-botbar]');
    if (!bar) return;
    var footer = document.querySelector('.ft');
    var footerIn = false;
    function update() {
      /* down while the hero still fills the screen (so it never sits over the
         hero's own trio) and while the footer is in view */
      var y = window.scrollY || window.pageYOffset || 0;
      bar.classList.toggle('botbar--down', y < 300 || footerIn);
    }
    if (footer && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { footerIn = en.isIntersecting; });
        update();
      }, { threshold: 0 }).observe(footer);
    }
    if (window.WR && WR.onScroll) WR.onScroll(update);
    else addEventListener('scroll', update, { passive: true });
    update();
  })();

  /* ------------------------------------------------------------------
     E. NO SINGLE-WORD LAST LINES — a widont for the editorial pages.
     The client does not want one word alone on a heading/lede/caption's
     last line. company/contact/residents are set by the shared
     gen_editorial.py, which we do not edit; the client's own remedy is to
     join the last two words with a non-breaking space, so we do exactly
     that in the DOM here (the same drive-the-rendered-page pattern used for
     the contact form). We revert a join that would overflow its box, so a
     two-word heading in a narrow cell is left rather than made to spill.
     Scoped to .ed, so the register/list pages (already clean) are untouched.
  ------------------------------------------------------------------ */
  (function widont() {
    var scope = document.querySelector('.ed');
    if (!scope) return;
    var SEL = 'h1,h2,h3,.ed-lede,.ed-row p,.ed-copy p,.ed-note,.ed-about,.measure,figcaption';
    var store = [];

    function lastLineWordCount(el) {
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), node, tops = [];
      while ((node = walker.nextNode())) {
        if (!/\S/.test(node.nodeValue)) continue;
        if (node.parentElement && node.parentElement.closest('.vh,.chip')) continue;
        var s = node.nodeValue, re = /\S+/g, m;
        while ((m = re.exec(s))) {
          var r = document.createRange();
          r.setStart(node, m.index); r.setEnd(node, m.index + m[0].length);
          var rc = r.getClientRects();
          if (rc.length) tops.push(rc[rc.length - 1].top);
        }
      }
      if (tops.length < 2) return 99;
      var sorted = tops.slice().sort(function (a, b) { return a - b; });
      var lines = 1;
      for (var i = 1; i < sorted.length; i++) if (sorted[i] - sorted[i - 1] > 3) lines++;
      if (lines < 2) return 99;
      var max = sorted[sorted.length - 1];
      return tops.filter(function (t) { return Math.abs(t - max) < 3; }).length;
    }

    function lastTextNode(el) {
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), node, last = null;
      while ((node = walker.nextNode())) {
        if (/\S/.test(node.nodeValue) && !(node.parentElement && node.parentElement.closest('.vh,.chip'))) last = node;
      }
      return last;
    }

    function process() {
      store.forEach(function (s) { s.node.nodeValue = s.original; });
      store = [];
      [].forEach.call(scope.querySelectorAll(SEL), function (el) {
        if (el.classList.contains('vh')) return;
        if (lastLineWordCount(el) !== 1) return;
        var tn = lastTextNode(el);
        if (!tn) return;
        var m = tn.nodeValue.match(/^([\s\S]*\S)(\s+)(\S[\s\S]*)$/);
        if (!m) return;
        var original = tn.nodeValue;
        var docBefore = document.documentElement.scrollWidth;
        tn.nodeValue = m[1] + ' ' + m[3];
        /* revert if the forced pair overflows the element's box OR widens the
           page — a grid cell with min-width:auto grows to its content rather
           than clipping, so the element check alone misses it. */
        if (el.scrollWidth > el.clientWidth + 1 ||
            document.documentElement.scrollWidth > docBefore) {
          tn.nodeValue = original; return;
        }
        store.push({ node: tn, original: original });
      });
    }

    if (document.fonts && document.fonts.ready) document.fonts.ready.then(process);
    else process();
    var t;
    addEventListener('resize', function () { clearTimeout(t); t = setTimeout(process, 200); });
  })();
})();
