/* Language Corner — shared behaviour: deck (swipe, progress), speech, quiz, hide-translation, theme. No dependencies. */
(function () {
  var root = document.documentElement;
  var LS = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var B = function (n) { return String(n).replace(/\d/g, function (d) { return '০১২৩৪৫৬৭৮৯'[d]; }); };

  // ---- theme ----
  var savedTheme = LS.get('lang:theme');
  if (savedTheme) root.setAttribute('data-theme', savedTheme);
  function toggleTheme() {
    var cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    LS.set('lang:theme', next);
  }

  // ---- toast ----
  var toastEl = null;
  function toast(html, ms) {
    if (toastEl) toastEl.remove();
    toastEl = document.createElement('div');
    toastEl.className = 'toast';
    toastEl.innerHTML = html;
    document.body.appendChild(toastEl);
    if (ms) setTimeout(function () { if (toastEl) { toastEl.remove(); toastEl = null; } }, ms);
    return toastEl;
  }

  // ---- speech (browser's own voices: no audio files) ----
  var voices = [];
  var warned = {};
  var slow = LS.get('lang:slow') === '1';
  function loadVoices() { if ('speechSynthesis' in window) voices = speechSynthesis.getVoices(); }
  if ('speechSynthesis' in window) { loadVoices(); speechSynthesis.onvoiceschanged = loadVoices; }
  function pickVoice(lang) {
    var l = lang.toLowerCase();
    var exact = voices.filter(function (v) { return v.lang.toLowerCase().replace('_', '-') === l; });
    var any = voices.filter(function (v) { return v.lang.toLowerCase().indexOf(l.slice(0, 2)) === 0; });
    return exact[0] || any[0] || null;
  }
  function speak(text, lang, done) {
    if (!('speechSynthesis' in window)) { toast('এই browser-এ উচ্চারণ শোনা যায় না। Chrome বা Safari ব্যবহার করো।', 3500); if (done) done(); return; }
    speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = lang;
    var v = pickVoice(lang);
    if (v) u.voice = v;
    else if (lang.indexOf('en') !== 0 && !warned[lang] && voices.length) {
      warned[lang] = true;
      var nm = lang.indexOf('ja') === 0 ? ['জাপানি', 'Japanese'] : ['জার্মান', 'German'];
      toast('তোমার ফোনে ' + nm[0] + ' voice পাওয়া যায়নি। Settings → Text-to-speech-এ ' + nm[1] + ' যোগ করো।', 5000);
    }
    u.rate = slow ? 0.6 : (lang.indexOf('en') === 0 ? 0.9 : 0.8);
    u.onend = u.onerror = function () { if (done) done(); };
    speechSynthesis.speak(u);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-say]');
    if (!b) return;
    e.stopPropagation();
    b.classList.add('on');
    speak(b.getAttribute('data-say'), b.getAttribute('data-lang') || 'en-US', function () { b.classList.remove('on'); });
  });
  // ---- hide translation (tap a blurred line to peek) ----
  document.addEventListener('click', function (e) {
    var t = e.target.closest('.bn, .pr'), b = document.body.classList;
    if (t && b.contains(t.classList.contains('pr') ? 'hide-pr' : 'hide-bn')) t.classList.toggle('peek');
  });
  // ---- sentence builder: tap a step to open it (one open at a time; the data-say handler speaks it) ----
  document.addEventListener('click', function (e) {
    var st = e.target.closest('.bstep');
    if (!st) return;
    var was = st.classList.contains('open');
    [].forEach.call(st.parentNode.querySelectorAll('.bstep.open'), function (x) { x.classList.remove('open'); });
    if (!was) st.classList.add('open');
  });
  // ---- reveal cards ----
  document.addEventListener('click', function (e) {
    var c = e.target.closest('.rcard');
    if (c && !e.target.closest('[data-say]')) c.classList.toggle('open');
  });

  // ---- quiz ----
  function initQuiz(el, deckKey, goNext) {
    var qs = JSON.parse(el.getAttribute('data-quiz'));
    var i = 0, score = 0, wrong = [];
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function show() {
      if (i >= qs.length) return done();
      var q = qs[i];
      var h = '<div class="qhead"><span>প্রশ্ন ' + B(i + 1) + ' / ' + B(qs.length) + '</span><span>✓ ' + B(score) + '</span></div>';
      h += '<div class="qq">' + esc(q.q) + '</div>';
      if (q.big) h += '<div class="qbig">' + esc(q.big) + '</div>';
      if (q.say) h += '<div style="text-align:center"><button class="say big" data-say="' + esc(q.say) + '" data-lang="' + (q.lang || 'en-US') + '">🔊</button></div>';
      h += '<div class="opts' + (q.ko ? ' kopts' : '') + '">';
      q.o.forEach(function (o, k) { h += '<button class="opt" data-k="' + k + '">' + esc(o) + '</button>'; });
      h += '</div><div class="why"></div>';
      el.innerHTML = h;
      el.classList.toggle('sm', Math.max.apply(null, q.o.map(function (x) { return String(x).length; }).concat([String(q.q).length - 30])) > 58);
      if (q.say && q.auto) { var sb = el.querySelector('[data-say]'); setTimeout(function () { sb.click(); }, 150); }
      [].forEach.call(el.querySelectorAll('.opt'), function (b) {
        b.addEventListener('click', function () {
          var k = +b.getAttribute('data-k');
          [].forEach.call(el.querySelectorAll('.opt'), function (x) { x.disabled = true; });
          var right = k === q.a;
          b.classList.add(right ? 'ok' : 'bad');
          if (!right) el.querySelectorAll('.opt')[q.a].classList.add('ok');
          [].forEach.call(el.querySelectorAll('.opt'), function (x) { if (!x.classList.contains('ok') && !x.classList.contains('bad')) x.classList.add('gone'); });
          if (right) score++; else wrong.push(q);
          var why = el.querySelector('.why');
          why.innerHTML = (right ? '🎉 ঠিক!' : '❌ ভুল।') + (q.why ? ' ' + esc(q.why) : '') + '<div style="margin-top:10px"><button class="btn">' + (i + 1 < qs.length ? 'পরের প্রশ্ন →' : 'ফলাফল দেখো') + '</button></div>';
          why.querySelector('.btn').addEventListener('click', function () { i++; show(); });
        });
      });
    }
    function done() {
      var pct = Math.round(100 * score / qs.length);
      var best = +(LS.get('lang:q:' + deckKey) || 0);
      if (score > best) LS.set('lang:q:' + deckKey, score);
      el.innerHTML = '<div class="score"><div class="big">' + B(score) + ' / ' + B(qs.length) + '</div><div class="qq">' +
        (pct >= 90 ? '🌟 দারুণ! প্রায় নিখুঁত।' : pct >= 60 ? '👍 ভালো হয়েছে! আরেকবার চেষ্টা করলে আরও ভালো।' : '💪 আবার পড়ে এসে চেষ্টা করো — শেখা হচ্ছে।') +
        '</div><div class="row-actions" style="justify-content:center"><button class="btn ghost" id="again">আবার</button><button class="btn" id="goon">পরের স্লাইড →</button></div></div>';
      el.querySelector('#again').addEventListener('click', function () { i = 0; score = 0; wrong = []; show(); });
      el.querySelector('#goon').addEventListener('click', goNext);
    }
    show();
  }

  // ---- fit: spread [data-split] lists over extra slides so no slide needs vertical scrolling ----
  function overflows(s) { return s.scrollHeight > s.clientHeight + 1; }
  function fitSlides(deck) {
    [].slice.call(deck.children).forEach(function (s) {
      var box = s.querySelector('[data-split]');
      if (!box || !overflows(s)) return;
      var step = +(box.getAttribute('data-step') || 1);
      var items = [].slice.call(box.children);
      items.forEach(function (it) { box.removeChild(it); });
      var after = [];
      while (box.nextSibling) after.push(box.parentNode.removeChild(box.nextSibling));
      var template = s.cloneNode(true);          // whatever comes before the list, plus the empty list
      var cur = s, curBox = box, count = 0;
      function newPart() {
        var next = template.cloneNode(true);
        cur.parentNode.insertBefore(next, cur.nextSibling);
        cur = next; curBox = next.querySelector('[data-split]'); count = 0;
      }
      for (var k = 0; k < items.length; k += step) {
        var chunk = items.slice(k, k + step);
        chunk.forEach(function (it) { curBox.appendChild(it); });
        if (count > 0 && overflows(cur)) {
          chunk.forEach(function (it) { curBox.removeChild(it); });
          newPart();
          chunk.forEach(function (it) { curBox.appendChild(it); });
        }
        count += chunk.length;
      }
      if (after.length) {
        after.forEach(function (a) { curBox.parentNode.appendChild(a); });
        if (overflows(cur) && count > 0) {
          after.forEach(function (a) { a.parentNode.removeChild(a); });
          newPart();
          curBox.parentNode.removeChild(curBox);
          after.forEach(function (a) { cur.querySelector('.inner').appendChild(a); });
        }
      }
    });
  }

  // ---- deck ----
  var deck = document.getElementById('deck');
  if (deck) {
    var ORIGINAL = deck.innerHTML;
    var slides = [], n = 0, i = 0, started = false;
    var key = document.body.getAttribute('data-deck');
    var bar = document.getElementById('bar'), count = document.getElementById('count');

    function layout() {
      deck.innerHTML = ORIGINAL;
      fitSlides(deck);
      slides = [].slice.call(deck.children);
      n = slides.length;
      [].forEach.call(document.querySelectorAll('.quiz'), function (q) {
        initQuiz(q, key, function () { go(i + 1); });
      });
    }
    function go(k) {
      if (!started) return;
      i = Math.max(0, Math.min(n - 1, k));
      deck.style.transform = 'translateX(-' + (i * 100) + '%)';
      bar.style.width = ((i + 1) / n * 100) + '%';
      count.textContent = B(i + 1) + ' / ' + B(n);
      slides[i].scrollTop = 0;
      LS.set('lang:p:' + key, String(i));
      if (i > 0) { var days = []; try { days = JSON.parse(LS.get('lang:days') || '[]'); } catch (e) {} var td = new Date().toDateString(); if (days.indexOf(td) < 0) { days.push(td); LS.set('lang:days', JSON.stringify(days.slice(-400))); } }
      if (i === n - 1) LS.set('lang:done:' + key, '1');
      try { history.replaceState(null, '', '#' + (i + 1)); } catch (e) {}
      if ('speechSynthesis' in window) speechSynthesis.cancel();
    }
    function start() {
      if (started) return;
      layout();
      started = true;
      document.body.setAttribute('data-ready', '1');
      var h = parseInt((location.hash || '').slice(1), 10);
      if (!isNaN(h)) { go(h - 1); return; }
      var last = parseInt(LS.get('lang:p:' + key) || '0', 10);
      go(0);
      if (last > 0 && last < n - 1) {
        var t = toast('আগেরবার ' + B(last + 1) + ' নম্বর স্লাইড পর্যন্ত পড়েছিলে। <button id="rgo">চালিয়ে যাও</button><button class="alt" id="rno">শুরু থেকে</button>');
        t.querySelector('#rgo').onclick = function () { go(last); t.remove(); };
        t.querySelector('#rno').onclick = function () { t.remove(); };
      }
    }
    function relayout() {   // fonts arrived late or the window changed size: measure again, stay near the same place
      if (!started) return;
      var frac = n > 1 ? i / (n - 1) : 0;
      layout();
      go(Math.round(frac * (n - 1)));
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (started) relayout(); else start(); });
    setTimeout(start, 1500);
    var lastW = innerWidth, lastH = innerHeight, rt = null;
    window.addEventListener('resize', function () {
      if (Math.abs(innerWidth - lastW) < 30 && Math.abs(innerHeight - lastH) < 120) return;   // ignore the phone URL bar
      lastW = innerWidth; lastH = innerHeight;
      clearTimeout(rt); rt = setTimeout(relayout, 250);
    });

    document.getElementById('prev').onclick = function () { go(i - 1); };
    document.getElementById('next').onclick = function () { go(i + 1); };
    document.getElementById('theme').onclick = toggleTheme;
    var slowBtn = document.getElementById('slow');
    if (slowBtn) {
      function paintSlow() { slowBtn.classList.toggle('active', slow); }
      slowBtn.onclick = function () { slow = !slow; LS.set('lang:slow', slow ? '1' : '0'); paintSlow(); toast(slow ? '🐢 ধীরে বলবে' : '🐇 স্বাভাবিক গতি', 1200); };
      paintSlow();
    }
    var bnBtn = document.getElementById('bnBtn');
    if (bnBtn) {
      var hidden = LS.get('lang:hidebn') === '1';
      var paintBn = function () { document.body.classList.toggle('hide-bn', hidden); bnBtn.classList.toggle('active', hidden); };
      bnBtn.onclick = function () { hidden = !hidden; LS.set('lang:hidebn', hidden ? '1' : '0'); paintBn(); toast(hidden ? '👁 বাংলা লুকানো — ট্যাপ করলে দেখা যাবে' : '👁 বাংলা দেখানো হচ্ছে', 1500); };
      paintBn();
    }
    var prBtn = document.getElementById('prBtn');
    if (prBtn) {
      var hidePr = LS.get('lang:hidepr') === '1';
      var paintPr = function () { document.body.classList.toggle('hide-pr', hidePr); prBtn.classList.toggle('active', hidePr); };
      prBtn.onclick = function () { hidePr = !hidePr; LS.set('lang:hidepr', hidePr ? '1' : '0'); paintPr(); toast(hidePr ? '🔤 উচ্চারণ লুকানো — ট্যাপ করলে দেখা যাবে' : '🔤 উচ্চারণ দেখানো হচ্ছে', 1500); };
      paintPr();
    }
    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(i + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(i - 1); }
    });
    // swipe left/right = change slide
    var x0 = null, y0 = null;
    document.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    document.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(i + (dx < 0 ? 1 : -1));
      x0 = null;
    });
    window.addEventListener('hashchange', function () {
      var t = parseInt((location.hash || '').slice(1), 10) - 1;
      if (!isNaN(t) && t !== i) go(t);
    });
  }

  // ---- photo lightbox ----
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-zoom]');
    if (!a) return;
    e.preventDefault();
    var lb = document.createElement('div');
    lb.id = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', a.getAttribute('aria-label') || 'ছবি');
    lb.innerHTML = '<img alt=""><button aria-label="বন্ধ">×</button>';
    lb.firstChild.src = a.getAttribute('href');
    lb.firstChild.alt = a.querySelector('img').alt;
    var close = function () { lb.remove(); document.removeEventListener('keydown', onKey); a.focus(); };
    var onKey = function (ev) { if (ev.key === 'Escape') close(); };
    lb.addEventListener('click', close);
    document.addEventListener('keydown', onKey);
    document.body.appendChild(lb);
    lb.lastChild.focus();
  });

  // ---- greeting by time of day ----
  [].forEach.call(document.querySelectorAll('[data-greet]'), function (el) {
    var h = new Date().getHours();
    var g = h < 4 ? 'শুভ রাত্রি' : h < 12 ? 'শুভ সকাল' : h < 16 ? 'শুভ দুপুর' : h < 18 ? 'শুভ বিকেল' : h < 20 ? 'শুভ সন্ধ্যা' : 'শুভ রাত্রি';
    var name = el.getAttribute('data-greet');
    el.textContent = g + (name ? ', ' + name : '') + '! 👋';
  });

  // ---- progress per course on language pages ----
  [].forEach.call(document.querySelectorAll('[data-coursekeys]'), function (c) {
    var ks = c.getAttribute('data-coursekeys').split(' ');
    var d = ks.filter(function (k) { return LS.get('lang:done:' + k) === '1'; }).length;
    var out = c.querySelector('.cprog');
    if (out && d) out.textContent = '✅ ' + B(d) + ' / ' + B(ks.length) + ' অধ্যায় শেষ';
  });

  // ---- progress marks on course pages ----
  var decks = document.querySelectorAll('[data-deckkey]');
  if (decks.length) {
    var done = 0, total = decks.length, firstOpen = null;
    [].forEach.call(decks, function (d) {
      var k = d.getAttribute('data-deckkey');
      if (LS.get('lang:done:' + k) === '1') { d.classList.add('done'); done++; }
      else if (!firstOpen) firstOpen = d;
    });
    var p = document.getElementById('progress');
    if (p) p.style.width = (100 * done / total) + '%';
    var st = document.getElementById('streak');
    if (st) {
      var ds = []; try { ds = JSON.parse(LS.get('lang:days') || '[]'); } catch (e) {}
      var n = 0, d = new Date();
      if (ds.indexOf(d.toDateString()) < 0) d.setDate(d.getDate() - 1);
      while (ds.indexOf(d.toDateString()) >= 0) { n++; d.setDate(d.getDate() - 1); }
      var bd = '০১২৩৪৫৬৭৮৯';
      var nb = String(n).replace(/\d/g, function (c) { return bd[c]; });
      st.textContent = n ? '🔥 ' + nb + ' দিন টানা পড়েছ — আজকেও ১০ মিনিট!' : '😴 আজ শুধু ১০ মিনিট — একটা স্লাইড দেখলেই শুরু হয়ে যায়!';
    }
    var pt = document.getElementById('progress-text');
    if (pt) pt.textContent = B(done) + ' / ' + B(total) + ' অধ্যায় শেষ';
    var cont = document.getElementById('continue');
    if (cont && firstOpen) {
      cont.setAttribute('href', firstOpen.getAttribute('href'));
      var t = firstOpen.querySelector('.t b');
      var label = t ? t.textContent.replace(/\s+/g, ' ').trim() : firstOpen.querySelector('.n').textContent.replace(/\s+/g, ' ').trim();
      cont.textContent = done ? '▶ চালিয়ে যাও — ' + label : '▶ শুরু করো — ' + label;
    } else if (cont) { cont.textContent = '🎉 সব শেষ! আবার পড়ো'; }
  }
})();
