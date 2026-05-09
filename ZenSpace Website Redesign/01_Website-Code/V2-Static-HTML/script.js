document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('entering');
  setTimeout(() => document.body.classList.remove('entering'), 600);

  // Nav
  const nav = document.querySelector('nav');
  window.addEventListener('scroll', () => nav && nav.classList.toggle('scrolled', scrollY > 40), { passive: true });
  const ham = document.querySelector('.hamburger'), links = document.querySelector('.nav-links');
  if (ham) ham.addEventListener('click', () => links.classList.toggle('open'));
  const pg = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a:not(.nav-cta)').forEach(a => { if (a.getAttribute('href') === pg) a.classList.add('active'); });

  // Page transitions
  document.querySelectorAll('a[href]').forEach(a => {
    const h = a.getAttribute('href');
    if (!h || h.startsWith('#') || h.startsWith('mailto') || h.startsWith('tel') || h.startsWith('http') || a.getAttribute('target')) return;
    a.addEventListener('click', e => { e.preventDefault(); document.body.classList.add('leaving'); setTimeout(() => location.href = h, 500); });
  });

  // Scroll reveal
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -50px 0px', threshold: 0.1 });
  document.querySelectorAll('.reveal, .stagger').forEach(el => obs.observe(el));

  // Parallax
  const pEls = document.querySelectorAll('[data-speed]');
  if (pEls.length) window.addEventListener('scroll', () => {
    pEls.forEach(el => { const s = parseFloat(el.dataset.speed); el.style.transform = `translateY(${-(el.getBoundingClientRect().top + scrollY - innerHeight / 2) * s * 0.12}px)`; });
  }, { passive: true });

  // Cursor glow
  const glow = document.querySelector('.cursor-glow');
  if (glow && innerWidth > 768) {
    let mx = 0, my = 0, gx = 0, gy = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    (function loop() { gx += (mx - gx) * 0.07; gy += (my - gy) * 0.07; glow.style.left = gx + 'px'; glow.style.top = gy + 'px'; requestAnimationFrame(loop); })();
  }

  // Particles
  const c = document.getElementById('particles');
  if (c) {
    const ctx = c.getContext('2d'); let w, h, pts = [];
    const colors = ['#FF9933', '#C0C0C0', '#138808', '#000080'];
    function resize() { w = c.width = innerWidth; h = c.height = innerHeight; } resize(); addEventListener('resize', resize);
    for (let i = 0; i < 45; i++) pts.push({ x: Math.random()*w, y: Math.random()*h, r: Math.random()*2.2+0.8, dx: (Math.random()-0.5)*0.35, dy: (Math.random()-0.5)*0.25, color: colors[i%4], a: Math.random()*0.18+0.04 });
    (function draw() {
      ctx.clearRect(0, 0, w, h);
      pts.forEach(p => { p.x += p.dx; p.y += p.dy; if (p.x<0) p.x=w; if (p.x>w) p.x=0; if (p.y<0) p.y=h; if (p.y>h) p.y=0;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fillStyle = p.color; ctx.globalAlpha = p.a; ctx.fill(); });
      ctx.globalAlpha = 0.02; ctx.strokeStyle = '#C0C0C0'; ctx.lineWidth = 0.5;
      for (let i=0; i<pts.length; i++) for (let j=i+1; j<pts.length; j++) {
        const d = Math.hypot(pts[i].x-pts[j].x, pts[i].y-pts[j].y);
        if (d < 130) { ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y); ctx.stroke(); }
      } ctx.globalAlpha = 1; requestAnimationFrame(draw);
    })();
  }

  // Expandable tiles
  document.querySelectorAll('.exp-tile-header').forEach(header => {
    header.addEventListener('click', () => {
      const tile = header.parentElement;
      const wasOpen = tile.classList.contains('open');
      // Close all
      document.querySelectorAll('.exp-tile').forEach(t => t.classList.remove('open'));
      // Toggle clicked
      if (!wasOpen) tile.classList.add('open');
    });
  });

  // Why-choose dropdowns
  document.querySelectorAll('.why-dropdown-header').forEach(h => {
    h.addEventListener('click', () => h.parentElement.classList.toggle('open'));
  });

  // Smooth scroll for anchor links (Read More buttons)
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = 100; // account for fixed nav
        const top = target.getBoundingClientRect().top + scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // Counters
  document.querySelectorAll('[data-count]').forEach(el => {
    const cObs = new IntersectionObserver(entries => { entries.forEach(e => { if (e.isIntersecting) {
      const target = +el.dataset.count, suf = el.dataset.suffix || '', dur = 2000, start = performance.now();
      (function anim(now) { const p = Math.min((now-start)/dur, 1); el.textContent = Math.floor((1-Math.pow(1-p,3))*target) + suf; if (p<1) requestAnimationFrame(anim); })(start);
      cObs.unobserve(el);
    }}); }, { threshold: 0.5 });
    cObs.observe(el);
  });

  // Form
  const form = document.getElementById('contactForm');
  if (form) form.addEventListener('submit', e => { e.preventDefault(); const btn = form.querySelector('button[type="submit"]'); btn.textContent = '✓ Sent!'; btn.style.background = '#138808'; setTimeout(() => { btn.textContent = 'Send Message →'; btn.style.background = ''; form.reset(); }, 3000); });

  const yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
});
