!function(){"use strict";const e=["client/index.e64a1fc6.js","client/index.d2811cfc.js","client/index.0979fff8.js","client/_commonjsHelpers.e0f9ccb2.js","client/dashboard.4bccfd22.js","client/client.00b9d082.js","client/index.0dac54ce.js","client/[slug].5f7cc921.js","client/sub.f270715a.js","client/screen.fdab7e10.js","client/bundle.esm.6028de20.js"].concat(["service-worker-index.html","favicon.ico","favicon.png","global.css","great-success.png","logo-192.png","logo-512.png","manifest.json"]),t=new Set(e);self.addEventListener("install",t=>{t.waitUntil(caches.open("cache1576097873786").then(t=>t.addAll(e)).then(()=>{self.skipWaiting()}))}),self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(async e=>{for(const t of e)"cache1576097873786"!==t&&await caches.delete(t);self.clients.claim()}))}),self.addEventListener("fetch",e=>{if("GET"!==e.request.method||e.request.headers.has("range"))return;const c=new URL(e.request.url);c.protocol.startsWith("http")&&(c.hostname===self.location.hostname&&c.port!==self.location.port||(c.host===self.location.host&&t.has(c.pathname)?e.respondWith(caches.match(e.request)):"only-if-cached"!==e.request.cache&&e.respondWith(caches.open("offline1576097873786").then(async t=>{try{const c=await fetch(e.request);return t.put(e.request,c.clone()),c}catch(c){const s=await t.match(e.request);if(s)return s;throw c}}))))})}();
