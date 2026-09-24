/* Loci Lab service worker.
   The page is NETWORK-FIRST so a new deploy always shows; the cache is only the
   offline fallback. Icons and fonts are cache-first because they never change. */
const V = "loci-lab-v4";
const SHELL = ["./","./index.html","./manifest.webmanifest",
  "./icons/icon-180.png","./icons/icon-192.png","./icons/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const isDoc = req.mode === "navigate" || url.pathname.endsWith("/") ||
                url.pathname.endsWith("index.html");

  if (isDoc) {
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(V).then(c => c.put("./index.html", copy)).catch(()=>{});
        return res;
      }).catch(() => caches.match("./index.html").then(r => r || caches.match("./")))
    );
    return;
  }
  if (url.origin === location.origin || /fonts\.(googleapis|gstatic)\.com/.test(url.host)) {
    e.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(V).then(c => c.put(req, copy)).catch(()=>{}); }
        return res;
      }).catch(() => hit))
    );
  }
});
