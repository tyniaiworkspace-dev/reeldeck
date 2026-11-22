/* ReelDeck service worker.
   - handles the Android share sheet (POST ./share) by redirecting to ?share=<url>
   - caches the shell so the app opens instantly / offline
   Registered only on https (GitHub Pages), so the plain-LAN copy is unaffected. */
const CACHE = 'reeldeck-v2';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'channels.json', 'family.json',
               'icons/icon-192.png', 'icons/icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Share target: the page is static, so turn the POST into a GET the app understands.
  if (e.request.method === 'POST' && url.pathname.endsWith('/share')) {
    e.respondWith((async () => {
      let shared = '';
      try {
        const form = await e.request.formData();
        shared = form.get('url') || form.get('text') || form.get('title') || '';
      } catch (err) {
        try { shared = await e.request.text(); } catch (err2) { shared = ''; }
      }
      const target = new URL('./?share=' + encodeURIComponent(shared), self.registration.scope);
      return Response.redirect(target.toString(), 303);
    })());
    return;
  }

  if (url.hostname === 'api.dailymotion.com') return; // always live
  if (e.request.method !== 'GET') return;

  e.respondWith(
    fetch(e.request)
      .then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
        return r;
      })
      .catch(() => caches.match(e.request).then((m) => m || caches.match('index.html')))
  );
});
