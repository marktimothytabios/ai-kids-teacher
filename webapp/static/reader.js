// Little Whys reader: turns the page links into instant page flips. Works without JavaScript too
// (the Previous/Next links reload the page with ?page=N).
(() => {
  const root = document.getElementById("reader");
  if (!root) return;
  const slug = root.dataset.slug, variant = root.dataset.variant;
  const total = +root.dataset.total, limit = +root.dataset.limit, stories = +root.dataset.stories;
  const alts = JSON.parse(document.getElementById("alts").textContent);
  const img = document.getElementById("page-img"), locked = document.getElementById("locked");
  const status = document.getElementById("status"), prev = document.getElementById("prev"), next = document.getElementById("next");
  const stage = document.getElementById("stage");
  let page = +root.dataset.page;

  const src = (n) => `/books/${slug}/pages/${variant}/${n}.webp`;
  const open = (n) => limit === 0 || n <= limit;
  const clamp = (n) => Math.max(1, Math.min(total, n));

  function label(n) {
    const last = 3 + stories * 2;
    if (n === 1) return "Cover";
    if (n === 2) return "For the grown-up";
    if (n === 3) return "Our questions";
    if (n <= last) return `Story ${Math.floor((n - 4) / 2) + 1} of ${stories}, ${(n - 4) % 2 === 0 ? "question" : "answer"}`;
    return "End of the book";
  }

  function setLink(a, n, enabled) {
    if (enabled) { a.setAttribute("href", `?page=${n}`); a.removeAttribute("aria-disabled"); }
    else { a.removeAttribute("href"); a.setAttribute("aria-disabled", "true"); }
  }

  function show(n) {
    n = clamp(n);
    page = n;
    if (open(n)) {
      img.src = src(n);
      img.alt = alts[n - 1] || `Page ${n}`;
      img.classList.remove("hidden");
      locked.classList.add("hidden");
      [n + 1, n + 2].filter((m) => m <= total && open(m)).forEach((m) => { new Image().src = src(m); });
    } else {
      img.classList.add("hidden");
      locked.classList.remove("hidden");
    }
    status.textContent = `Page ${n} of ${total} \u2013 ${label(n)}`;
    setLink(prev, n - 1, n > 1);
    setLink(next, n + 1, n < total);
    try { history.replaceState(null, "", `?page=${n}`); } catch (e) { /* ignore */ }
  }

  prev.addEventListener("click", (e) => { e.preventDefault(); if (page > 1) show(page - 1); });
  next.addEventListener("click", (e) => { e.preventDefault(); if (page < total) show(page + 1); });
  root.querySelectorAll(".jump a").forEach((a) => a.addEventListener("click", (e) => {
    e.preventDefault(); show(+a.dataset.page); window.scrollTo({ top: 0, behavior: "smooth" });
  }));

  document.addEventListener("keydown", (e) => {
    if (e.altKey || e.ctrlKey || e.metaKey || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) return;
    if (e.key === "ArrowRight") { show(page + 1); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { show(page - 1); e.preventDefault(); }
    else if (e.key === "Home") { show(1); e.preventDefault(); }
    else if (e.key === "End") { show(total); e.preventDefault(); }
  });

  // tap the right half of the page for next, the left half for previous
  img.addEventListener("click", (e) => {
    const r = img.getBoundingClientRect();
    show(e.clientX - r.left > r.width / 2 ? page + 1 : page - 1);
  });

  // swipe
  let x0 = null, y0 = null;
  stage.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  stage.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    x0 = y0 = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) show(page + (dx < 0 ? 1 : -1));
  }, { passive: true });

  show(page); // sets labels and preloads the next pages
})();
