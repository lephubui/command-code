// popup.js — toggle enable/disable per-site, robust access check, auto-reload after grant, counter

const $ = (id) => document.getElementById(id);
const tbody = document.querySelector("#tbl tbody");
const thead = document.querySelector("#tbl thead");
const timelineContainer = $("#timelineContainer");

// Safe binder
function on(id, ev, fn) { const el = $(id); if (el) el.addEventListener(ev, fn); return el; }

// Safe background messaging (never returns undefined)
async function safeMessage(msg) {
  try { return (await chrome.runtime.sendMessage(msg)) || {}; }
  catch (e) { console.warn("safeMessage error:", e); return { error: String(e?.message || e) }; }
}

const chips = [$("#chip2xx"), $("#chip3xx"), $("#chip4xx"), $("#chip5xx")];
const activeClasses = new Set();

// -------- persistence (session) ----------
const SKEY = "uiState";
async function loadState() { const { [SKEY]: s } = await chrome.storage.session.get(SKEY); return s || {}; }
async function saveState(partial) { const cur = await loadState(); const next = { ...cur, ...partial }; await chrome.storage.session.set({ [SKEY]: next }); return next; }

// -------- sorting ----------
let sortKey = "t";
let sortDir = "desc";

// -------- misc helpers ----------
async function activeTabCtx() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const tab = tabs && tabs[0];
  if (!tab || !tab.url) return { tabId: -1, host: "", scheme: "" };
  try {
    const u = new URL(tab.url);
    return { tabId: tab.id ?? -1, host: u.host, scheme: u.protocol.replace(":", "") };
  } catch {
    return { tabId: tab.id ?? -1, host: "", scheme: "" }; // chrome://, edge://, etc.
  }
}
function fmt(ms) { return new Date(ms).toLocaleTimeString(); }
function statusClassOf(code) { if (!code) return ""; return String(Math.floor(code/100)); }

// Build both origin patterns for a host
function originPatternsForHost(host) {
  if (!host) return [];
  return [`https://${host}/*`, `http://${host}/*`];
}

// True if ANY scheme origin for this host is granted
async function hasAnyOriginForHost(host) {
  const all = await chrome.permissions.getAll();
  const origins = all?.origins || [];
  const patterns = new Set(originPatternsForHost(host));
  return origins.some(o => patterns.has(o));
}

function applyFilters(logs, curTabId) {
  const qHost = $("qHost")?.value.trim().toLowerCase() || "";
  const qMethod = $("qMethod")?.value || "ANY";
  const qScheme = $("qScheme")?.value || "ANY";
  const qStatusMin = parseInt($("qStatusMin")?.value || "", 10);
  const currentOnly = $("qTab")?.value === "current";
  const regexStr = $("qRegex")?.value.trim() || "";
  let regex = null; if (regexStr) { try { regex = new RegExp(regexStr); } catch {} }

  return logs.filter(r => {
    if (currentOnly && r.tabId !== curTabId) return false;
    if (qHost && !(r.host || "").toLowerCase().includes(qHost)) return false;
    if (qMethod !== "ANY" && r.method !== qMethod) return false;
    if (qScheme !== "ANY" && r.scheme !== qScheme) return false;
    if (!isNaN(qStatusMin) && (r.status || 0) < qStatusMin) return false;
    if (activeClasses.size) { const cls = statusClassOf(r.status); if (!activeClasses.has(cls)) return false; }
    if (regex && !regex.test(r.url || "")) return false;
    return (r.url || "").startsWith("http");
  });
}

function compare(a, b, key) {
  const av = a[key], bv = b[key];
  if (av == null && bv == null) return 0;
  if (av == null) return -1;
  if (bv == null) return 1;
  if (typeof av === "number" && typeof bv === "number") return av - bv;
  return String(av).localeCompare(String(bv));
}

function renderTable(rows) {
  tbody.innerHTML = "";
  rows.forEach(r => {
    const tr = document.createElement("tr");
    const len = (typeof r.contentLength === "number") ? r.contentLength : "";
    tr.innerHTML = `
      <td class="mono">${fmt(r.t)}</td>
      <td>${r.method || ""}</td>
      <td>${r.scheme || ""}</td>
      <td>${r.status ?? ""}</td>
      <td>${r.type || ""}</td>
      <td class="row">${r.host || ""}</td>
      <td class="mono row" title="${r.url}">${r.url}</td>
      <td class="mono">${len}</td>`;
    tbody.appendChild(tr);
  });
}

function renderTimeline(rows) {
  const groups = new Map();
  for (const r of rows) { if (!groups.has(r.id)) groups.set(r.id, []); groups.get(r.id).push(r); }
  const merged = Array.from(groups.values()).map(arr => arr.sort((a,b) => a.t - b.t)).sort((a,b) => b[0].t - a[0].t);
  timelineContainer.innerHTML = "";
  for (const stages of merged) {
    const head = stages[0];
    const details = document.createElement("details");
    details.className = "timeline";
    details.innerHTML = `<summary>${fmt(head.t)} ${head.method || ""} ${head.scheme || ""} ${head.host || ""} ${head.url}</summary>`;
    const ul = document.createElement("ul"); ul.style.margin = "6px 0 10px 20px";
    stages.forEach(s => {
      const len = (typeof s.contentLength === "number") ? ` len=${s.contentLength}` : "";
      const li = document.createElement("li");
      li.innerHTML = `<span class="mono">${fmt(s.t)}</span> – <b>${s.stage}</b>
        ${s.status ? ` status=${s.status}` : ""}${len}
        ${s.contentType ? ` content-type=${s.contentType}`:""}
        ${s.ip ? ` ip=${s.ip}`:""} ${s.fromCache ? " fromCache": ""}`;
      ul.appendChild(li);
    });
    details.appendChild(ul);
    timelineContainer.appendChild(details);
  }
}

async function refresh() {
  const res = await safeMessage({ type: "GET_LOGS" });
  const logs = res?.logs ?? [];
  const { tabId } = await activeTabCtx();

  let filtered = applyFilters(logs, tabId);
  filtered.sort((a, b) => (sortDir === "asc" ? compare(a,b,sortKey) : -compare(a,b,sortKey)));

  const timelineOn = $("#toggleTimeline")?.checked;
  if ($("#tbl")) $("#tbl").style.display = timelineOn ? "none" : "table";
  if (timelineContainer) timelineContainer.style.display = timelineOn ? "block" : "none";
  if (timelineOn) renderTimeline(filtered); else renderTable(filtered.slice(0, 500));

  const counter = $("#counter"); if (counter) counter.textContent = `captured: ${filtered.length}`;

  await saveState({
    qHost: $("qHost")?.value || "", qRegex: $("qRegex")?.value || "",
    qMethod: $("qMethod")?.value || "ANY", qScheme: $("qScheme")?.value || "ANY",
    qStatusMin: $("qStatusMin")?.value || "", qTab: $("qTab")?.value || "any",
    chips: Array.from(activeClasses), sortKey, sortDir, timelineOn: !!timelineOn
  });
}

function markSortHeaders() {
  if (!thead) return;
  thead.querySelectorAll("th").forEach(th => {
    th.classList.remove("sort-asc", "sort-desc");
    if (th.dataset.key === sortKey) th.classList.add(sortDir === "asc" ? "sort-asc" : "sort-desc");
  });
}
function initHeaderSorting() {
  if (!thead) return;
  thead.addEventListener("click", (e) => {
    const th = e.target.closest("th"); if (!th || !th.dataset.key) return;
    const key = th.dataset.key;
    if (sortKey === key) sortDir = (sortDir === "asc" ? "desc" : "asc");
    else { sortKey = key; sortDir = "asc"; }
    markSortHeaders(); refresh();
  });
}

function toggleChip(e) {
  const n = e.currentTarget;
  const cls = n.getAttribute("data-class");
  if (n.classList.toggle("active")) activeClasses.add(cls); else activeClasses.delete(cls);
  refresh();
}

function downloadBlob(filename, text) {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function exportCSV() {
  const res = await safeMessage({ type: "GET_LOGS" });
  const logs = res?.logs ?? [];
  const { tabId } = await activeTabCtx();
  const rows = applyFilters(logs, tabId).sort((a,b)=>a.t-b.t);

  const header = ["t","stage","method","scheme","status","type","host","url","ip","fromCache","tabId","contentLength","contentType","contentEncoding"].join(",");
  const csvRows = rows.map(r => [
    new Date(r.t).toISOString(), r.stage || "", r.method || "", r.scheme || "", r.status ?? "",
    r.type || "", r.host || "", (r.url || "").replaceAll('"','""'), r.ip || "", r.fromCache ? "true":"false", r.tabId,
    (typeof r.contentLength === "number" ? r.contentLength : ""), r.contentType || "", r.contentEncoding || ""
  ].map(v => (typeof v === "string" ? `"${v}"` : v)).join(","));
  downloadBlob(`http-logger-${Date.now()}.csv`, [header, ...csvRows].join("\n"));
}
async function exportNDJSON() {
  const res = await safeMessage({ type: "GET_LOGS" });
  const logs = res?.logs ?? [];
  const { tabId } = await activeTabCtx();
  const rows = applyFilters(logs, tabId).sort((a,b)=>a.t-b.t);
  downloadBlob(`http-logger-${Date.now()}.ndjson`, rows.map(r => JSON.stringify(r)).join("\n"));
}

// ---- About modal ----
function openAbout() { const m = $("#aboutModal"); if (m) m.style.display = "block"; }
function closeAbout() { const m = $("#aboutModal"); if (m) m.style.display = "none"; }

// ---- UI sync (now toggles Enable/Disable) ----
async function setSiteLabel() {
  const { host } = await activeTabCtx();
  const el = $("siteLabel");
  if (el) el.textContent = host ? `Site: ${host}` : "Site: (unavailable)";
}

// Returns true if any origin for current host is granted; updates button+badge text
async function syncAccessUI() {
  const { host, scheme } = await activeTabCtx();
  const btn = $("btnEnable");
  const badge = $("permStatus");

  if (!host || (scheme !== "http" && scheme !== "https")) {
    if (btn) { btn.textContent = "Enable on this site"; btn.disabled = true; }
    if (badge) { badge.textContent = "not an http(s) page"; badge.className = "badge warn"; }
    return false;
  }

  const granted = await hasAnyOriginForHost(host);

  if (btn) { // toggle wording instead of disabling the button
    btn.textContent = granted ? "Disable on this site" : "Enable on this site";
    btn.disabled = false;
  }
  if (badge) {
    badge.textContent = granted ? "access granted" : "no access";
    badge.className = `badge ${granted ? "ok" : "warn"}`;
  }
  return granted;
}

function restoreChips(arr) {
  activeClasses.clear();
  chips.forEach(c => {
    if (!c) return;
    const cls = c.getAttribute("data-class");
    if (arr && arr.includes(cls)) { c.classList.add("active"); activeClasses.add(cls); }
    else c.classList.remove("active");
  });
}

// ---- boot + handlers ----
async function boot() {
  // restore UI state
  const s = await loadState();
  if (s.qHost && $("qHost")) $("qHost").value = s.qHost;
  if (s.qRegex && $("qRegex")) $("qRegex").value = s.qRegex;
  if (s.qMethod && $("qMethod")) $("qMethod").value = s.qMethod;
  if (s.qScheme && $("qScheme")) $("qScheme").value = s.qScheme;
  if (s.qStatusMin && $("qStatusMin")) $("qStatusMin").value = s.qStatusMin;
  if (s.qTab && $("qTab")) $("qTab").value = s.qTab;
  if (s.chips) restoreChips(s.chips);
  if (s.sortKey) sortKey = s.sortKey;
  if (s.sortDir) sortDir = s.sortDir;
  if (s.timelineOn != null && $("#toggleTimeline")) $("#toggleTimeline").checked = !!s.timelineOn;

  markSortHeaders();
  initHeaderSorting();

  // Toggle handler (enable OR disable based on current state)
  on("btnEnable", "click", async () => {
    const { host, scheme, tabId } = await activeTabCtx();
    if (!host || (scheme !== "http" && scheme !== "https")) return;

    const granted = await hasAnyOriginForHost(host);
    if (granted) {
      // Disable: remove both http and https origins for the host
      await chrome.permissions.remove({ origins: originPatternsForHost(host) });
      await syncAccessUI();
      await refresh();
    } else {
      // Enable: request only the current scheme for least privilege
      const req = await safeMessage({ type: "REQUEST_SITE_ACCESS", host, scheme });
      await syncAccessUI();
      if (req.granted && tabId > 0) {
        chrome.tabs.reload(tabId);         // generate fresh traffic
        setTimeout(refresh, 1200);
      }
    }
  });

  on("btnRefresh", "click", refresh);
  on("btnClear", "click", async () => { await safeMessage({ type: "CLEAR" }); refresh(); });

  ["qHost","qRegex","qStatusMin"].forEach(id => on(id, "input", refresh));
  ["qMethod","qScheme","qTab","toggleTimeline"].forEach(id => on(id, "change", refresh));
  chips.forEach(c => c && c.addEventListener("click", toggleChip));
  on("btnExportCSV", "click", exportCSV);
  on("btnExportNDJSON", "click", exportNDJSON);
  on("btnAbout", "click", openAbout);
  on("aboutClose", "click", closeAbout);
  const modal = $("#aboutModal");
  if (modal) modal.addEventListener("click", (e) => { if (e.target.id === "aboutModal") closeAbout(); });

  await setSiteLabel();
  await syncAccessUI();
  await refresh();
}

boot();
// ---- end of popup.js ----
