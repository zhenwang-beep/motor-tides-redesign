/* Wiseman Residential — horizontal rails.
   The scrollbar is hidden by rail.css; these arrows are the control. Trackpad and
   touch still work natively, and the buttons stay in step with whatever the user does.

   Markup:
     <div data-rail data-on="dark"?>                  <- optional dark-section flag
       <div class="rail-track" data-rail-track> …items… </div>
       <div class="rail-nav">                          <- or .rail-float for overlaid arrows
         <button class="rail-btn prev" data-rail-prev>…</button>
         <span class="rail-count" data-rail-count></span>   <- optional "03 / 12"
         <button class="rail-btn next" data-rail-next>…</button>
       </div>
       <div class="rail-bar"><i></i></div>             <- optional progress rule
     </div>

   Call WR.rails() once per page (WR.boot does not, so pages opt in).
*/
(function () {
  'use strict';
  var W = (window.WR = window.WR || {});

  var ARROW = '<svg viewBox="0 0 34 10" aria-hidden="true" focusable="false"><path d="M0 5h31M27 1l4.4 4-4.4 4"/></svg>';

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  W.rail = function (host) {
    var track = host.querySelector('[data-rail-track]');
    if (!track) return;
    var prev = host.querySelector('[data-rail-prev]');
    var next = host.querySelector('[data-rail-next]');
    var count = host.querySelector('[data-rail-count]');
    var bar = host.querySelector('.rail-bar i');
    var items = [].slice.call(track.children);
    if (!items.length) return;

    /* fill in the arrow glyph if the page did not supply one */
    [prev, next].forEach(function (b) {
      if (b && !b.querySelector('svg')) b.innerHTML = ARROW;
      if (b && !b.getAttribute('aria-label')) {
        b.setAttribute('aria-label', b === prev ? 'Previous' : 'Next');
      }
      if (b) b.type = 'button';
    });

    track.setAttribute('tabindex', '0');
    /* Never overwrite an authored role. The filter bar's track IS the page's
       <form role="search"> and a room strip's track is an <ol>; stamping "group"
       on either deletes a landmark or orphans the list items. */
    if (!track.hasAttribute('role') && !/^(FORM|OL|UL|NAV|TABLE|SECTION)$/.test(track.tagName)) {
      track.setAttribute('role', 'group');
    }
    if (!track.getAttribute('aria-label')) track.setAttribute('aria-label', host.dataset.railLabel || 'Scrollable row');

    function step() {
      /* one item plus the gap, but never more than the visible width */
      var a = items[0].getBoundingClientRect();
      var b = items[1] ? items[1].getBoundingClientRect() : null;
      var s = b ? (b.left - a.left) : a.width;
      return Math.max(120, Math.min(s || a.width, track.clientWidth));
    }

    function maxScroll() { return Math.max(0, track.scrollWidth - track.clientWidth); }

    function go(dir) {
      var to = track.scrollLeft + dir * step();
      if (W.reduce) { track.scrollLeft = to; sync(); }
      else track.scrollTo({ left: to, behavior: 'smooth' });
    }

    function nearest() {
      var x = track.scrollLeft, best = 0, bd = Infinity, l0 = items[0].offsetLeft;
      items.forEach(function (el, i) {
        var d = Math.abs((el.offsetLeft - l0) - x);
        if (d < bd) { bd = d; best = i; }
      });
      return best;
    }

    var raf = 0;
    function sync() {
      var max = maxScroll();
      var atStart = track.scrollLeft <= 1;
      var atEnd = track.scrollLeft >= max - 1;
      /* a rail with nothing to scroll hides its controls rather than showing dead ones */
      if (max <= 1) host.setAttribute('data-static', '');
      else host.removeAttribute('data-static');
      if (prev) prev.disabled = atStart;
      if (next) next.disabled = atEnd;
      if (count) {
        var i = nearest();
        count.textContent = pad(i + 1) + ' / ' + pad(items.length);
      }
      if (bar) {
        var p = max > 0 ? (track.scrollLeft / max) : 1;
        /* the rule shows how much of the row is behind you, never a zero-width sliver */
        bar.parentElement.style.setProperty('--rail-p', Math.max(items.length ? 1 / items.length : 0.08, p).toFixed(4));
      }
    }
    function queue() {
      if (raf) return;
      raf = requestAnimationFrame(function () { raf = 0; sync(); });
    }

    if (prev) prev.addEventListener('click', function () { go(-1); });
    if (next) next.addEventListener('click', function () { go(1); });
    track.addEventListener('scroll', queue, { passive: true });
    addEventListener('resize', queue);

    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
      else if (e.key === 'Home') { e.preventDefault(); track.scrollTo({ left: 0, behavior: W.reduce ? 'auto' : 'smooth' }); }
      else if (e.key === 'End') { e.preventDefault(); track.scrollTo({ left: maxScroll(), behavior: W.reduce ? 'auto' : 'smooth' }); }
    });

    /* keep the rail honest when an item is focused by Tab */
    track.addEventListener('focusin', function (e) {
      var item = e.target.closest('[data-rail-track] > *');
      if (!item) return;
      var l = item.offsetLeft - items[0].offsetLeft;
      if (l < track.scrollLeft || l + item.offsetWidth > track.scrollLeft + track.clientWidth) {
        track.scrollTo({ left: l, behavior: W.reduce ? 'auto' : 'smooth' });
      }
    });

    /* images arriving changes scrollWidth */
    [].forEach.call(track.querySelectorAll('img'), function (img) {
      if (!img.complete) img.addEventListener('load', queue, { once: true });
    });
    if (window.ResizeObserver) new ResizeObserver(queue).observe(track);

    sync();
    return { sync: sync, go: go };
  };

  W.rails = function (root) {
    [].forEach.call((root || document).querySelectorAll('[data-rail]'), W.rail);
  };
})();
