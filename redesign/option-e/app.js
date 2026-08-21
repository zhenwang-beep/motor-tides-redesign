/* Concept E — shared behavior: damped scroll, chapter-word sweep,
   masked reveals, sliders, stepper, plans, map. */
(function(){
  'use strict';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- damped scrolling (Lenis), The Park feel ---------- */
  var lenis = null;
  if(!reduce && window.Lenis){
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 1 });
    (function raf(t){ lenis.raf(t); requestAnimationFrame(raf); })(0);
  }
  function scrollToY(y){
    if(lenis){
      var d = Math.min(2.8, Math.max(1.2, Math.abs(y - scrollY) / innerHeight * 1.1));
      lenis.scrollTo(y, { duration: d, easing: function(t){ return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2; } });
    }
    else { scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }); }
  }
  /* same-page anchors glide (handles both #id and page.html#id forms) */
  document.querySelectorAll('a[href*="#"]').forEach(function(a){
    a.addEventListener('click', function(e){
      var url = new URL(a.getAttribute('href'), location.href);
      if(url.pathname !== location.pathname || !url.hash) return;
      var el = document.querySelector(url.hash);
      if(!el) return;
      e.preventDefault();
      history.replaceState(null, '', url.hash);
      scrollToY(landY(el));
    });
  });

  /* ---------- page transitions ---------- */
  var pt = document.querySelector('.pt');
  if(pt && !reduce){
    pt.innerHTML = '<div class="pt-brand" aria-hidden="true">' +
      '<svg viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">' +
      '<polygon points="14,18 34,18 34,74 14,80"></polygon>' +
      '<polygon points="40,18 60,18 60,71 40,77"></polygon>' +
      '<polygon points="66,18 86,18 86,68 66,74"></polygon></svg>' +
      '<span class="pt-name">Motor Tides</span><span class="pt-sub">By Wiseman</span></div>';
    document.querySelectorAll('a[href]').forEach(function(a){
      var href = a.getAttribute('href');
      if(!href || href.charAt(0) === '#' || a.target === '_blank') return;
      if(/^(https?:|tel:|mailto:)/.test(href)) return;
      a.addEventListener('click', function(e){
        var url = new URL(href, location.href);
        if(url.origin !== location.origin || url.pathname === location.pathname) return;
        e.preventDefault();
        pt.classList.add('cover');
        setTimeout(function(){ location.href = url.href; }, 950);
      });
    });
    /* back/forward cache restores must never leave the panel covering */
    addEventListener('pageshow', function(e){
      if(e.persisted) pt.classList.remove('cover');
    });
  }

  /* ---------- theme variants (concept review) ---------- */
  var THEMES = ['tide','emerald','manor','champagne','olive','midnight'];
  var q = new URLSearchParams(location.search).get('theme');
  var saved = null;
  try{ saved = localStorage.getItem('mt-theme'); }catch(e){}
  var theme = THEMES.indexOf(q) > -1 ? q : (THEMES.indexOf(saved) > -1 ? saved : 'tide');
  function applyTheme(t){
    theme = t;
    if(t === 'tide') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = t;
    try{ localStorage.setItem('mt-theme', t); }catch(e){}
    document.querySelectorAll('.thsw button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.t === t));
    });
  }
  var sw = document.createElement('div');
  sw.className = 'thsw';
  sw.setAttribute('role', 'group');
  sw.setAttribute('aria-label', 'Color & type themes');
  var NAMES = { tide: 'Tide teal \u00b7 Marcellus', emerald: 'Emerald & gold \u00b7 Gloock', manor: 'Manor brass \u00b7 Cinzel', champagne: 'Champagne gold \u00b7 Cormorant', olive: 'Olive brass \u00b7 Prata', midnight: 'Midnight \u00b7 DM Serif' };
  THEMES.forEach(function(t){
    var b = document.createElement('button');
    b.className = 't-' + t;
    b.dataset.t = t;
    b.type = 'button';
    b.title = NAMES[t];
    b.setAttribute('aria-label', NAMES[t]);
    b.addEventListener('click', function(){ applyTheme(t); });
    sw.appendChild(b);
  });
  document.body.appendChild(sw);
  /* mobile: tuck the switcher while the chat teaser occupies its corner */
  var tuckTimer = setInterval(function(){
    var tz = document.querySelector('.mtc-teaser');
    if(!tz) return;
    clearInterval(tuckTimer);
    var tuckSync = function(){ sw.classList.toggle('tuck', tz.classList.contains('show')); };
    new MutationObserver(tuckSync).observe(tz, { attributes: true, attributeFilter: ['class'] });
    tuckSync();
  }, 300);
  setTimeout(function(){ clearInterval(tuckTimer); }, 12000);
  applyTheme(theme);

  /* ---------- header ---------- */
  var hdr = document.getElementById('hdr');

  /* ---------- fullscreen menu ---------- */
  var menu = document.getElementById('fsmenu'),
      btn = document.getElementById('menuBtn'),
      closeBtn = document.getElementById('menuClose');
  function setMenu(open){
    menu.classList.toggle('open', open);
    menu.setAttribute('aria-hidden', String(!open));
    btn.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('menu-open', open);
    ['main','header','footer'].forEach(function(sel){
      var el = document.querySelector(sel);
      if(el) el.toggleAttribute('inert', open && sel !== 'header' ? true : false);
    });
    if(lenis){ open ? lenis.stop() : lenis.start(); }
    if(open){ closeBtn.focus(); } else { btn.focus(); }
  }
  btn.addEventListener('click', function(){ setMenu(true); });
  closeBtn.addEventListener('click', function(){ setMenu(false); });
  menu.querySelectorAll('nav a, .fsmenu-foot a').forEach(function(a){
    a.addEventListener('click', function(){ setMenu(false); });
  });
  addEventListener('keydown', function(e){
    if(e.key === 'Escape' && menu.classList.contains('open')) setMenu(false);
  });

  /* ---------- hero titles: letters rise and turn into place ---------- */
  document.querySelectorAll('.hero-title, .curtain .w-copy.centered').forEach(function(el){
    if(reduce) return;
    var text = el.textContent.trim();
    el.setAttribute('aria-label', text);
    el.textContent = '';
    el.classList.remove('split');
    el.classList.add('lettered');
    var li = 0;
    text.trim().split(/\s+/).forEach(function(word, wi, words){
      var w = document.createElement('span');
      w.className = 'hw';
      w.setAttribute('aria-hidden', 'true');
      word.split('').forEach(function(ch){
        var o = document.createElement('span');
        o.className = 'hl';
        var t = document.createElement('span');
        t.className = 'hlt';
        t.textContent = ch;
        t.style.animationDelay = (0.5 + li * 0.05) + 's';
        li++;
        o.appendChild(t);
        w.appendChild(o);
      });
      el.appendChild(w);
      if(wi < words.length - 1) el.appendChild(document.createTextNode(' '));
      li++;
    });
  });

  /* ---------- reveals ---------- */
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){ en.target.classList.add('in', 'go'); io.unobserve(en.target); }
    });
  }, { threshold: .14, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.rv, .split').forEach(function(el){ io.observe(el); });
  var ioImg = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){ en.target.classList.add('in'); ioImg.unobserve(en.target); }
    });
  }, { threshold: 0.001 });
  document.querySelectorAll('.imgrv').forEach(function(el){ ioImg.observe(el); });

  /* ---------- chapter words: dual-layer sweep (The Park effect) ----------
     White copy sits in the pinned image layer (viewport-stable while pinned).
     Dark copy sits in an overflow-hidden mask at the top of the paper section
     and is counter-translated each frame so it occupies the same viewport
     spot; the paper edge acts as the moving seam between the two colors.  */
  var chapters = [];
  document.querySelectorAll('.curtain.chc').forEach(function(c){
    var reveal = c.querySelector('.reveal');
    var ink = c.querySelector('.cw.ink');
    if(reveal && ink) chapters.push({ c: c, reveal: reveal, ink: ink });
  });
  function sizeMasks(){
    chapters.forEach(function(s){
      /* the window starts as a band cutting mid-words, inset from the right */
      s.top0 = Math.round(innerHeight * 0.28 + s.ink.offsetHeight * 0.4);
      s.right0 = Math.round(innerWidth * 0.18);
      s.span = Math.round(innerHeight * 0.5);
    });
  }
  function runSweeps(){
    chapters.forEach(function(s){
      /* progress runs from the moment the section enters the viewport */
      var sc = innerHeight - s.c.getBoundingClientRect().top;
      var t = Math.min(1, Math.max(0, sc / (innerHeight * 1.5)));
      t = Math.pow(t, 1.7);                           /* slow entry, resolves in the pin */
      s.c.dataset.reveal = t.toFixed(2);
      s.reveal.style.clipPath = 'inset(' + Math.round(s.top0 * (1 - t)) + 'px ' + Math.round(s.right0 * (1 - t)) + 'px 0 0)';
    });
  }
  if(reduce){
    /* static: show the full image with the white words */
    chapters.forEach(function(s){ s.reveal.style.clipPath = 'none'; s.ink.style.visibility = 'hidden'; s.c.dataset.reveal = '1'; });
    chapters = [];
  } else {
    sizeMasks();
    addEventListener('resize', function(){ sizeMasks(); runSweeps(); });
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ sizeMasks(); runSweeps(); });
  }

  /* ---------- sliders: snap + arrows + counter ---------- */
  document.querySelectorAll('[data-csl]').forEach(function(root){
    var track = root.querySelector('.csl-track'),
        cur = root.querySelector('[data-cur]'),
        prev = root.querySelector('[data-prev]'),
        next = root.querySelector('[data-next]'),
        slides = track.querySelectorAll('figure').length,
        t2 = null;
    root.querySelector('[data-total]').textContent = slides;
    function step(){
      var f = track.querySelector('figure');
      var g = parseFloat(getComputedStyle(track).columnGap) || 12;
      return f ? f.offsetWidth + g : track.clientWidth;
    }
    function idx(){ return Math.min(slides, Math.max(1, Math.round(track.scrollLeft / step()) + 1)); }
    function sync(){
      var i = idx();
      cur.textContent = i;
      prev.disabled = i <= 1;
      next.disabled = i >= slides;
    }
    function go(dir){
      var i = Math.min(slides - 1, Math.max(0, idx() - 1 + dir));
      track.scrollTo({ left: i * step(), behavior: reduce ? 'auto' : 'smooth' });
    }
    prev.addEventListener('click', function(){ go(-1); });
    next.addEventListener('click', function(){ go(1); });
    track.addEventListener('scroll', function(){
      clearTimeout(t2); t2 = setTimeout(sync, 60);
    }, { passive: true });
    sync();
  });

  /* ---------- tours strip ---------- */
  var strip = document.querySelector('[data-strip]');
  if(strip){
    var sPrev = document.querySelector('[data-strip-prev]'),
        sNext = document.querySelector('[data-strip-next]');
    var stripSync = function(){
      sPrev.disabled = strip.scrollLeft <= 4;
      sNext.disabled = strip.scrollLeft >= strip.scrollWidth - strip.clientWidth - 4;
    };
    var stripGo = function(dir){
      var card = strip.querySelector('.vt-card');
      var w = card ? card.offsetWidth + 14 : 300;
      strip.scrollBy({ left: dir * w, behavior: reduce ? 'auto' : 'smooth' });
    };
    sPrev.addEventListener('click', function(){ stripGo(-1); });
    sNext.addEventListener('click', function(){ stripGo(1); });
    strip.addEventListener('scroll', function(){ requestAnimationFrame(stripSync); }, { passive: true });
    stripSync();
  }

  /* ---------- floor plan menu -> preview ---------- */
  var rows = document.querySelectorAll('.plan-row');
  if(rows.length){
    var ppImg = document.getElementById('ppImg'),
        ppName = document.getElementById('ppName'),
        ppSpec = document.getElementById('ppSpec'),
        ppAvail = document.getElementById('ppAvail');
    var pick = function(row){
      rows.forEach(function(r){ r.setAttribute('aria-pressed', String(r === row)); });
      var name = row.dataset.name;
      if(ppName.textContent === name) return;
      ppName.textContent = name;
      ppSpec.innerHTML = row.dataset.spec;
      ppAvail.textContent = row.dataset.avail;
      if(reduce){ ppImg.src = row.dataset.img; ppImg.alt = name + ' floor plan drawing'; return; }
      ppImg.classList.add('swap');
      setTimeout(function(){
        ppImg.src = row.dataset.img;
        ppImg.alt = name + ' floor plan drawing';
        ppImg.classList.remove('swap');
      }, 180);
    };
    rows.forEach(function(row){
      row.addEventListener('click', function(){ pick(row); });
      if(matchMedia('(hover:hover) and (pointer:fine)').matches){
        row.addEventListener('mouseenter', function(){ pick(row); });
      }
      row.addEventListener('focus', function(){ pick(row); });
    });
  }

  /* ---------- map interactions ---------- */
  var svg = document.querySelector('.nmap');
  if(svg){
    document.querySelectorAll('.mland').forEach(function(a){
      var pin = svg.querySelector('.mpin[data-n="' + a.dataset.n + '"]');
      if(!pin) return;
      a.addEventListener('mouseenter', function(){ pin.classList.add('hot'); pin.parentNode.appendChild(pin); });
      a.addEventListener('mouseleave', function(){ pin.classList.remove('hot'); });
    });
    document.querySelectorAll('.mpin').forEach(function(pin){
      pin.setAttribute('tabindex', '0');
      pin.setAttribute('role', 'link');
      var nm = pin.querySelector('.mname');
      if(nm) pin.setAttribute('aria-label', 'Open ' + nm.textContent + ' in Google Maps');
      function act(){
        var a = document.querySelector('.mland[data-n="' + pin.dataset.n + '"]');
        if(a) a.click();
      }
      pin.addEventListener('mouseenter', function(){ pin.parentNode.appendChild(pin); });
      pin.addEventListener('click', act);
      pin.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); act(); }
      });
    });
  }

  /* ---------- experience rail scroll-spy ---------- */
  var railLinks = document.querySelectorAll('.xp-rail nav a');
  if(railLinks.length){
    var spyIO = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(!en.isIntersecting) return;
        railLinks.forEach(function(a){
          var on = a.getAttribute('href') === '#' + en.target.id;
          a.classList.toggle('on', on);
          if(on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-30% 0px -55% 0px' });
    document.querySelectorAll('.xp-sec').forEach(function(sec){ spyIO.observe(sec); });
  }

  /* ---------- section stepper ---------- */
  var nextBtn = document.getElementById('nextBtn');
  var stops = [].slice.call(document.querySelectorAll('[data-sec]'));
  function stopTop(el){ return el.getBoundingClientRect().top + scrollY; }
  /* transform-free layout position: entrance reveals (.rv/.split) shift rects at measure time */
  function absTop(el){ var t = 0; while(el){ t += el.offsetTop; el = el.offsetParent; } return t; }
  function landY(el){
    var h = el.querySelector('h1,h2,h3,.stitle,.xp-title') || el.querySelector('.split,p,.csl,.collage');
    var top = h ? absTop(h) : absTop(el);
    /* content block = anchor down to the inner wrapper's content edge */
    var inner = el.firstElementChild || el;
    var bottom = absTop(inner) + inner.offsetHeight - (parseFloat(getComputedStyle(inner).paddingBottom) || 0);
    var secBottom = absTop(el) + el.offsetHeight;
    if(bottom > secBottom) bottom = secBottom;
    var blockH = Math.max(0, bottom - top);
    /* center the block when it fits; otherwise pin the heading 96px from the top */
    var t = blockH <= innerHeight - 144 ? top - Math.max(72, (innerHeight - blockH) / 2) : top - 96;
    var st = absTop(el);
    if(t < st) t = st;
    return Math.max(0, t);
  }
  /* clicks land on content sections; pinned image chapters are ridden through */
  var clickStops = stops.filter(function(el){ return !el.classList.contains('curtain'); });
  if(nextBtn){
    nextBtn.addEventListener('click', function(){
      if(nextBtn.classList.contains('flip')){ scrollToY(0); return; }
      var y = scrollY;
      for(var i = 0; i < clickStops.length; i++){
        if(stopTop(clickStops[i]) > y + 80){ scrollToY(landY(clickStops[i])); return; }
      }
      scrollToY(document.body.scrollHeight);
    });
  }

  /* ---------- per-frame scroll state ---------- */
  var ticking = false;
  var hdrY = scrollY;
  hdr.addEventListener('focusin', function(){
    if(hdr.classList.contains('hd')){ hdr.classList.remove('hd'); if(scrollY >= 110) hdr.classList.add('frost'); }
  });
  function onScroll(){
    ticking = false;
    /* smart header: transparent at top, slides away scrolling down, frosts scrolling up */
    var hy = scrollY;
    if(hy < 110){
      hdr.classList.remove('hd','frost');
    }else{
      if(!document.body.classList.contains('menu-open') && !hdr.matches(':focus-within')){
        if(hy > hdrY + 6) hdr.classList.add('hd');
        else if(hy < hdrY - 6) hdr.classList.remove('hd');
      }
      hdr.classList.toggle('frost', !hdr.classList.contains('hd'));
    }
    if(Math.abs(hy - hdrY) > 6) hdrY = hy;
    /* header color adapts to whatever section sits beneath it */
    if(stops.length){
      var hprobe = scrollY + 60, htype = 'dark', hel = null;
      for(var j = 0; j < stops.length; j++){
        if(stopTop(stops[j]) <= hprobe){ htype = stops[j].dataset.sec; hel = stops[j]; }
        else break;
      }
      if(hel && hel.classList.contains('chc') && +(hel.dataset.reveal || 0) < 0.8) htype = 'light';
      hdr.classList.toggle('on-light', htype === 'light');
    }
    runSweeps();
    if(nextBtn && stops.length){
      var probe = scrollY + innerHeight - 48, type = 'dark';
      for(var i = 0; i < stops.length; i++){
        if(stopTop(stops[i]) <= probe) type = stops[i].dataset.sec;
        else break;
      }
      nextBtn.classList.toggle('on-light', type === 'light');
      var last = stops[stops.length - 1];
      var atEnd = scrollY + innerHeight * 0.6 > stopTop(last);
      nextBtn.classList.toggle('flip', atEnd);
      nextBtn.setAttribute('aria-label', atEnd ? 'Back to top' : 'Scroll to the next section');
    }
  }
  if(location.hash){
    var hashDone = false;
    addEventListener('wheel', function(){ hashDone = true; }, { passive: true, once: true });
    addEventListener('touchstart', function(){ hashDone = true; }, { passive: true, once: true });
    var hashFix = function(){
      var lt = document.querySelector(location.hash);
      if(!lt || hashDone) return;
      var y = landY(lt);
      if(lenis) lenis.scrollTo(y, { immediate: true });
      else window.scrollTo(0, y);
    };
    requestAnimationFrame(hashFix);
    /* fonts and gallery images shift layout as they load; re-correct when each settles */
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ requestAnimationFrame(hashFix); });
    addEventListener('load', function(){ requestAnimationFrame(hashFix); });
  }
  addEventListener('scroll', function(){
    if(!ticking){ ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();
})();
