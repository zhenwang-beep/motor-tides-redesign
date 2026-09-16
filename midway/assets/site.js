/* Motor Midway — shared behaviour for all three concepts.
   No dependencies. Everything degrades to a working page without it. */
(function () {
  'use strict';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Header: frost after scroll, invert over dark sections ─────────────── */
  var hd = document.querySelector('.hd');
  if (hd) {
    var invZones = [].slice.call(document.querySelectorAll('[data-hd="inv"]'));
    var onScroll = function () {
      var y = window.scrollY;
      hd.classList.toggle('frost', y > 24);
      var probe = y + 28, inv = false;
      for (var i = 0; i < invZones.length; i++) {
        var r = invZones[i].getBoundingClientRect(), top = r.top + y;
        if (probe >= top && probe < top + r.height) { inv = true; break; }
      }
      hd.classList.toggle('inv', inv);
    };
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll);
    onScroll();
  }

  /* ── Mobile menu ───────────────────────────────────────────────────────── */
  var mbtn = document.querySelector('.mbtn'), mnav = document.querySelector('.mnav');
  if (mbtn && mnav) {
    var setMenu = function (open) {
      mnav.classList.toggle('open', open);
      mbtn.setAttribute('aria-expanded', String(open));
      if (open) { var f = mnav.querySelector('a,button'); if (f) f.focus(); }
    };
    mbtn.addEventListener('click', function () {
      setMenu(!mnav.classList.contains('open'));
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mnav.classList.contains('open')) { setMenu(false); mbtn.focus(); }
    });
  }

  /* ── Scroll reveal ─────────────────────────────────────────────────────── */
  var rv = [].slice.call(document.querySelectorAll('.rv'));
  if (!rv.length) { /* nothing */ }
  else if (reduce || !('IntersectionObserver' in window)) {
    rv.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  }

  /* ── Gallery filter + lightbox ─────────────────────────────────────────── */
  var gal = document.querySelector('.gal');
  if (gal) {
    var figs = [].slice.call(gal.querySelectorAll('figure'));

    var filterBar = document.querySelector('.gal-filter');
    if (filterBar) {
      filterBar.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        var g = b.dataset.group;
        [].forEach.call(filterBar.querySelectorAll('button'), function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        figs.forEach(function (f) {
          f.hidden = !(g === 'all' || f.dataset.group === g);
        });
      });
    }

    var dlg = document.querySelector('dialog.lb');
    if (dlg && typeof dlg.showModal === 'function') {
      var img = dlg.querySelector('img'), cap = dlg.querySelector('.lb-cap'), idx = 0;
      var visible = function () { return figs.filter(function (f) { return !f.hidden; }); };
      var show = function (i) {
        var list = visible(); if (!list.length) return;
        idx = (i + list.length) % list.length;
        var f = list[idx], src = f.querySelector('img');
        img.src = src.dataset.full || src.src;
        img.alt = src.alt;
        cap.textContent = src.alt;
      };
      gal.addEventListener('click', function (e) {
        var f = e.target.closest('figure'); if (!f) return;
        show(visible().indexOf(f)); dlg.showModal();
      });
      dlg.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
      dlg.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
      dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
      dlg.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
        if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    }
  }

  /* ── Floor-plan sort + filter ──────────────────────────────────────────── */
  var planWrap = document.querySelector('[data-plans]');
  if (planWrap) {
    var plans = [].slice.call(planWrap.querySelectorAll('[data-plan]'));
    var bar = document.querySelector('[data-plan-filter]');
    if (bar) {
      bar.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        var beds = b.dataset.beds;
        [].forEach.call(bar.querySelectorAll('button'), function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        var shown = 0;
        plans.forEach(function (p) {
          var hit = beds === 'all' || p.dataset.beds === beds;
          p.hidden = !hit; if (hit) shown++;
        });
        var count = document.querySelector('[data-plan-count]');
        if (count) count.textContent = shown + (shown === 1 ? ' plan' : ' plans');
      });
    }
  }

  /* ── Contact form: client-side only, this is a design concept ──────────── */
  var form = document.querySelector('form[data-demo]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('[data-demo-note]');
      if (note) {
        note.hidden = false;
        note.textContent = 'This is a design concept — the form is not wired to a mailbox. '
          + 'On the live site this posts to the leasing office.';
        note.focus();
      }
    });
  }

  /* ── Concept A: chapter palette + hour rail ────────────────────────────
     Sections declare which hour of the evening they belong to via
     data-chapter. Whichever one owns the middle of the viewport sets the
     page palette. Without JS the page keeps the daylight palette and every
     section still reads — the chapters carry their own backgrounds.        */
  var chapters = [].slice.call(document.querySelectorAll('[data-chapter]'));
  if (chapters.length && document.body.classList.contains('gh')) {
    var railItems = [].slice.call(document.querySelectorAll('.hour-rail li'));
    var current = -1;
    var setHour = function (h) {
      if (h === current) return;
      current = h;
      document.body.dataset.hour = String(h);
      railItems.forEach(function (li) {
        li.classList.toggle('on', Number(li.dataset.hour) === h);
      });
    };
    var pick = function () {
      var mid = innerHeight / 2, best = 0;
      for (var i = 0; i < chapters.length; i++) {
        var r = chapters[i].getBoundingClientRect();
        if (r.top <= mid && r.bottom > mid) { best = Number(chapters[i].dataset.chapter); break; }
        if (r.top > mid) break;
        best = Number(chapters[i].dataset.chapter);
      }
      setHour(best);
    };
    var ticking = false;
    addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { pick(); ticking = false; });
    }, { passive: true });
    addEventListener('resize', pick);
    pick();
  }

  /* ── Tours: load Matterport only on request (they are heavy) ───────────── */
  [].forEach.call(document.querySelectorAll('[data-tour]'), function (btn) {
    btn.addEventListener('click', function () {
      var frame = btn.closest('.tour').querySelector('.frame');
      var id = btn.dataset.tour;
      frame.innerHTML = '<iframe title="Matterport 360 tour" allowfullscreen '
        + 'allow="xr-spatial-tracking" loading="lazy" '
        + 'src="https://my.matterport.com/show/?m=' + id + '"></iframe>';
      btn.closest('.tour').querySelector('.meta .btn').remove();
    });
  });
})();
