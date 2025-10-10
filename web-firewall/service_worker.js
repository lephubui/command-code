/*
 * Command & Code: Web Firewall — service worker
 * Uses chrome.declarativeNetRequest dynamic rules for runtime modes & custom rules.
 * Adds local-only telemetry for blocked requests (no remote exfiltration).
 */

// Rule ID space: 1-9999 reserved; 10000+ static; 20000+ balanced; 30000+ paranoid; 50000+ custom
const ID_SPACES = {
  balanced: 20000,
  paranoid: 30000,
  custom: 50000
};

// Telemetry configuration
const TELEMETRY_MAX_EVENTS = 5000; // ring buffer size

// State
let currentMode = 'off'; // 'off' | 'balanced' | 'paranoid'
let blockedCount = 0;

chrome.runtime.onInstalled.addListener(async () => {
  await chrome.storage.local.set({ mode: 'balanced', customRules: [], enabled: true });
  await ensureTelemetryInit();
  await setMode('balanced');
});

chrome.storage.onChanged.addListener((changes) => {
  if (changes.mode) {
    setMode(changes.mode.newValue);
  }
});

// Increment count and record rich telemetry details when a rule matches
chrome.declarativeNetRequest.onRuleMatchedDebug?.addListener(async (info) => {
  blockedCount += 1;
  updateBadge();
  await recordTelemetryEvent(info);
});

chrome.action.onClicked.addListener(async () => {
  // Quick toggle enable/disable
  const { enabled } = await chrome.storage.local.get({ enabled: true });
  await chrome.storage.local.set({ enabled: !enabled });
  await setEnabled(!enabled);
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.type === 'getState') {
    sendResponse({ mode: currentMode, blockedCount });
  } else if (msg.type === 'setMode') {
    setMode(msg.mode).then(() => sendResponse({ ok: true })).catch(e => sendResponse({ ok: false, error: e.message }));
    return true;
  } else if (msg.type === 'setCustomRules') {
    applyCustomRules(msg.rules).then(() => sendResponse({ ok: true })).catch(e => sendResponse({ ok: false, error: e.message }));
    return true;
  } else if (msg.type === 'telemetry:get') {
    getTelemetry().then((t) => sendResponse({ ok: true, telemetry: t })).catch(e => sendResponse({ ok: false, error: e.message }));
    return true;
  } else if (msg.type === 'telemetry:clear') {
    clearTelemetry().then(() => sendResponse({ ok: true })).catch(e => sendResponse({ ok: false, error: e.message }));
    return true;
  }
});

async function setEnabled(on) {
  if (on) {
    await setMode((await chrome.storage.local.get({ mode: 'balanced' })).mode);
    chrome.action.setBadgeText({ text: '' + blockedCount });
  } else {
    await chrome.declarativeNetRequest.updateDynamicRules({ removeRuleIds: await getAllDynamicRuleIds(), addRules: [] });
    chrome.action.setBadgeText({ text: '' });
  }
}

async function setMode(mode) {
  currentMode = mode;
  blockedCount = 0;
  updateBadge();

  const removeIds = await getAllDynamicRuleIds();
  const addRules = await buildModeRules(mode);

  await chrome.declarativeNetRequest.updateDynamicRules({ removeRuleIds: removeIds, addRules });
}

async function buildModeRules(mode) {
  const rules = [];
  const presets = await fetch(chrome.runtime.getURL('rules/presets.json')).then(r => r.json());
  const enabled = (await chrome.storage.local.get({ enabled: true })).enabled;
  if (!enabled || mode === 'off') return rules;

  const addPreset = (arr, baseId) => arr.map((r, i) => ({
    id: baseId + i + 1,
    priority: 1,
    action: { type: r.type },
    condition: { regexFilter: r.regexFilter, resourceTypes: r.resourceTypes }
  }));

  if (mode === 'balanced') rules.push(...addPreset(presets.balanced, ID_SPACES.balanced));
  if (mode === 'paranoid') {
    rules.push(...addPreset(presets.balanced, ID_SPACES.balanced));
    rules.push(...addPreset(presets.paranoid, ID_SPACES.paranoid));
  }

  // Custom user rules
  const { customRules } = await chrome.storage.local.get({ customRules: [] });
  customRules.forEach((r, idx) => {
    rules.push({
      id: ID_SPACES.custom + idx + 1,
      priority: r.priority || 1,
      action: { type: r.type || 'block' },
      condition: r.condition
    });
  });
  return rules;
}

async function applyCustomRules(rules) {
  await chrome.storage.local.set({ customRules: rules });
  await setMode(currentMode);
}

async function getAllDynamicRuleIds() {
  const { rules } = await chrome.declarativeNetRequest.getDynamicRules();
  return rules.map(r => r.id);
}

function updateBadge() {
  chrome.action.setBadgeBackgroundColor({ color: '#111' });
  chrome.action.setBadgeText({ text: blockedCount ? String(blockedCount) : '' });
}

// ---- Telemetry helpers ----
async function ensureTelemetryInit() {
  const { telemetry } = await chrome.storage.local.get({ telemetry: null });
  if (!telemetry) {
    await chrome.storage.local.set({ telemetry: { events: [], perRule: {}, perDomain: {}, lastReset: Date.now(), totalBlocked: 0 } });
  }
}

async function recordTelemetryEvent(info) {
  const t = (await chrome.storage.local.get({ telemetry: null })).telemetry || { events: [], perRule: {}, perDomain: {}, lastReset: Date.now(), totalBlocked: 0 };
  const url = info?.request?.url || '';
  const domain = tryGetDomain(url);
  const ruleId = info?.rule?.ruleId;
  const rulesetId = info?.rule?.rulesetId || 'dynamic/static';
  const resourceType = info?.request?.resourceType;
  const action = info?.rule?.action?.type || 'block';
  const event = { ts: Date.now(), url, domain, ruleId, rulesetId, resourceType, action };

  // Ring buffer
  if (t.events.length >= TELEMETRY_MAX_EVENTS) t.events.shift();
  t.events.push(event);

  // Aggregates
  t.perRule[ruleId] = (t.perRule[ruleId] || 0) + 1;
  t.perDomain[domain] = (t.perDomain[domain] || 0) + 1;
  t.totalBlocked = (t.totalBlocked || 0) + 1;

  await chrome.storage.local.set({ telemetry: t });
}

async function getTelemetry() {
  await ensureTelemetryInit();
  const { telemetry } = await chrome.storage.local.get({ telemetry: { events: [], perRule: {}, perDomain: {}, lastReset: Date.now(), totalBlocked: 0 } });
  return telemetry;
}

async function clearTelemetry() {
  await chrome.storage.local.set({ telemetry: { events: [], perRule: {}, perDomain: {}, lastReset: Date.now(), totalBlocked: 0 } });
  blockedCount = 0;
  updateBadge();
}

function tryGetDomain(url) {
  try { return new URL(url).hostname || ''; } catch { return ''; }
}