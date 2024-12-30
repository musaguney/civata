// Settings
const SETTINGS = {
  appName: 'Kilic Civata',
  appVersion: '3.1.1', // Değişiklik sonrası bu numarayı artırın
  diagnostics: false,
  cachedFiles: [
    // Static files served via Django
    '/offline/',
    '/static/offline.html',
    '/static/app-icons/icon-32x32.png',
    '/static/app-icons/icon-180x180.png',
    '/static/app-icons/icon-144x144.png',
    '/static/app-icons/icon-192x192.png',
    '/static/app-icons/icon-512x512.png',
    '/static/js/theme-switcher.js',
    '/static/fonts/inter-variable-latin.woff2',
    '/static/css/theme.min.css',
    '/static/js/theme.min.js',
  ],
};

SETTINGS.cacheName = `${SETTINGS.appName}-${SETTINGS.appVersion}`;

/**
 * Helper function for logging messages to the console based on the message type.
 * @param {string} message - The message to log.
 * @param {string} type - The type of message ('info' or 'error').
 */
const logMessage = (message, type = 'info') => {
  if (SETTINGS.diagnostics) {
    if (type === 'error') {
      console.error(message);
    } else {
      console.log(message);
    }
  }
};

// Install Service Worker
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches
      .open(SETTINGS.cacheName)
      .then((cache) => {
        return cache.addAll(SETTINGS.cachedFiles);
      })
      .then(() => {
        logMessage('[Service Worker] All essential assets are cached');
        return self.skipWaiting();
      })
      .catch((err) => {
        logMessage(
          `[Service Worker Cache] Error: Check SETTINGS.cachedFiles array - ${err}`,
          'error'
        );
      })
  );
  logMessage('[Service Worker] Installed');
});

// Fetching data from the cache
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      if (response) {
        logMessage(`[Service Worker] Fetching ${SETTINGS.cacheName} files from Cache`);
        return response;
      }

      return fetch(e.request).catch(() => {
        logMessage('[Service Worker] Network request failed, serving offline.html');
        return caches.match('/offline/');
      });
    })
  );
});

// Activation of Service Worker
self.addEventListener('activate', (e) => {
  self.clients.claim();
  e.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName.startsWith(SETTINGS.appName + '-'))
          .filter((cacheName) => cacheName !== SETTINGS.cacheName)
          .map((cacheName) => caches.delete(cacheName))
      );
    })
  );
  logMessage('[Service Worker] Activated');
});
