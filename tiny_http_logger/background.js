// background.js (MV3) — observe-only HTTP/S with per-site permission
// ---------------------------------------------------------------
// - Logs request lifecycle stages (before, headers, completed, error)
// - Captures Content-Type, Content-Length, Content-Encoding, status, IP
// - Keeps logs in memory only (cleared on demand or SW unload)
// - Uses optional host permissions: users grant per-site access
// ---------------------------------------------------------------

// background.js — MV3, observe-only, dynamic listeners based on granted origins

const MAX_LOGS = 800;
const logs = []; // in-memory only

const add = (e) => { logs.push(e); if (logs.length > MAX_LOGS) logs.shift(); };
const isHttpLike = (u) => u?.startsWith("http://") || u?.startsWith("https://");

// ---- Listener fns (defined once so we can add/remove them) ----
function onBeforeRequest(d) {
  if (!isHttpLike(d.url)) return;
  const u = new URL(d.url);
  add({
    id: d.requestId, t: Date.now(), stage: "before",
    method: d.method, url: d.url, host: u.host,
    scheme: u.protocol.replace(":", ""), type: d.type,
    tabId: d.tabId, initiator: d.initiator || ""
  });
}

function onHeadersReceived(d) {
  if (!isHttpLike(d.url)) return;
  const hdr = Object.fromEntries((d.responseHeaders || []).map(h => [h.name.toLowerCase(), h.value || ""]));
  const contentType = hdr["content-type"] || "";
  const server = hdr["server"] || "";
  const contentLength = (() => {
    const v = hdr["content-length"]; if (!v) return null;
    const n = parseInt(v, 10); return Number.isFinite(n) ? n : null;
  })();
  const contentEncoding = hdr["content-encoding"] || "";
  add({
    id: d.requestId, t: Date.now(), stage: "headers",
    url: d.url, status: d.statusCode, tabId: d.tabId,
    contentType, server, contentLength, contentEncoding
  });
}

function onCompleted(d) {
  if (!isHttpLike(d.url)) return;
  const u = new URL(d.url);
  add({
    id: d.requestId, t: Date.now(), stage: "completed",
    method: d.method, url: d.url, host: u.host,
    scheme: u.protocol.replace(":", ""), type: d.type,
    tabId: d.tabId, status: d.statusCode, ip: d.ip || "",
    fromCache: !!d.fromCache
  });
}

function onErrorOccurred(d) {
  if (!isHttpLike(d.url)) return;
  add({ id: d.requestId, t: Date.now(), stage: "error", url: d.url, error: d.error, tabId: d.tabId });
}

// ---- Dynamic wiring ----
let wired = false;
let currentFilter = { urls: [] };

function detachAll() {
  if (!wired) return;
  chrome.webRequest.onBeforeRequest.removeListener(onBeforeRequest);
  chrome.webRequest.onHeadersReceived.removeListener(onHeadersReceived);
  chrome.webRequest.onCompleted.removeListener(onCompleted);
  chrome.webRequest.onErrorOccurred.removeListener(onErrorOccurred);
  wired = false;
}

function attachAll(filterUrls) {
  if (!filterUrls.length) { detachAll(); return; }
  currentFilter = { urls: filterUrls };
  chrome.webRequest.onBeforeRequest.addListener(onBeforeRequest, currentFilter);
  chrome.webRequest.onHeadersReceived.addListener(onHeadersReceived, currentFilter, ["responseHeaders"]);
  chrome.webRequest.onCompleted.addListener(onCompleted, currentFilter);
  chrome.webRequest.onErrorOccurred.addListener(onErrorOccurred, currentFilter);
  wired = true;
}

// Build a urls[] list from granted origins (e.g., ["https://example.com/*"])
async function refreshListenersFromPermissions() {
  const all = await chrome.permissions.getAll();
  // Only use origin strings; ignore permissions array
  const origins = (all.origins || []).filter(o => o.startsWith("http"));
  // If you also granted global host_permissions (dev), include them automatically
  attachAll(origins);
}

// React when user grants/revokes site access
chrome.permissions.onAdded.addListener(refreshListenersFromPermissions);
chrome.permissions.onRemoved.addListener(refreshListenersFromPermissions);

// Initial wiring on SW start
refreshListenersFromPermissions();

// ---- Messaging for popup ----
chrome.runtime.onMessage.addListener(async (msg, _sender, sendResponse) => {
  if (msg?.type === "GET_LOGS") { sendResponse({ logs }); return true; }
  if (msg?.type === "CLEAR") { logs.length = 0; sendResponse({ ok: true }); return true; }

  if (msg?.type === "REQUEST_SITE_ACCESS") {
    const origins = [`${msg.scheme}://${msg.host}/*`];
    const granted = await chrome.permissions.request({ origins });
    // listeners will refresh via onAdded, but do it here too just in case
    await refreshListenersFromPermissions();
    sendResponse({ granted });
    return true;
  }

  if (msg?.type === "CHECK_SITE_ACCESS") {
    const origins = [`${msg.scheme}://${msg.host}/*`];
    const granted = await chrome.permissions.contains({ origins });
    sendResponse({ granted });
    return true;
  }
});
// ---- end of background.js ----