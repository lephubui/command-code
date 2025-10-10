/*
 * Command & Code: Web Firewall — service worker
 * Uses chrome.declarativeNetRequest dynamic rules for runtime modes & custom rules.
 * Adds local-only telemetry for blocked requests (no remote exfiltration).
 */

// Rule ID space: 1-9999 reserved; 10000+ static; 25000+ balanced; 35000+ paranoid; 55000+ custom
const ID_SPACES = {
  balanced: 25000,
  paranoid: 35000,
  custom: 55000
};

// Telemetry configuration
const TELEMETRY_MAX_EVENTS = 5000; // ring buffer size

// State
let currentMode = 'off'; // 'off' | 'balanced' | 'paranoid'
let blockedCount = 0;

chrome.runtime.onInstalled.addListener(async () => {
  await chrome.storage.local.set({ mode: 'balanced', customRules: [], enabled: true });
  await ensureTelemetryInit();
  
  // Clear any existing dynamic rules to prevent conflicts
  try {
    const existingRules = await chrome.declarativeNetRequest.getDynamicRules();
    if (existingRules.rules && existingRules.rules.length > 0) {
      await chrome.declarativeNetRequest.updateDynamicRules({ 
        removeRuleIds: existingRules.rules.map(r => r.id), 
        addRules: [] 
      });
    }
  } catch (error) {
    console.error('Error clearing existing rules:', error);
  }
  
  await setMode('balanced');
});

chrome.runtime.onStartup.addListener(async () => {
  // Restore state from storage on browser startup
  const { mode, enabled } = await chrome.storage.local.get({ mode: 'balanced', enabled: true });
  currentMode = mode;
  
  if (enabled) {
    await setMode(mode);
  } else {
    await setEnabled(false);
  }
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
  } else if (msg.type === 'debug:clearRules') {
    // Debug function to manually clear all dynamic rules
    clearAllDynamicRules().then(() => sendResponse({ ok: true })).catch(e => sendResponse({ ok: false, error: e.message }));
    return true;
  } else if (msg.type === 'debug:listRules') {
    // Debug function to list all rules
    listAllRules().then((rules) => sendResponse({ ok: true, rules })).catch(e => sendResponse({ ok: false, error: e.message }));
    return true;
  } else if (msg.type === 'debug:forceReset') {
    // Nuclear option: clear everything and restart fresh
    forceCompleteReset().then(() => sendResponse({ ok: true })).catch(e => sendResponse({ ok: false, error: e.message }));
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

async function validateAndApplyRules(rules) {
  if (rules.length === 0) return;
  
  console.log(`Attempting to validate and apply ${rules.length} rules with IDs:`, rules.map(r => r.id));
  
  // Test approach: try to add one rule at a time to identify conflicts
  const successfulRules = [];
  
  for (const rule of rules) {
    try {
      // Test if this single rule can be added
      await chrome.declarativeNetRequest.updateDynamicRules({ 
        removeRuleIds: [], 
        addRules: [rule] 
      });
      
      successfulRules.push(rule);
      console.log(`✓ Successfully added rule with ID ${rule.id}`);
      
    } catch (error) {
      console.error(`✗ Failed to add rule with ID ${rule.id}:`, error.message);
      
      // Try with a different ID
      let attempts = 0;
      let newId = rule.id;
      
      while (attempts < 100) {
        newId = Math.floor(Math.random() * 900000) + 100000; // Random ID
        
        try {
          const retryRule = { ...rule, id: newId };
          await chrome.declarativeNetRequest.updateDynamicRules({ 
            removeRuleIds: [], 
            addRules: [retryRule] 
          });
          
          successfulRules.push(retryRule);
          console.log(`✓ Successfully added rule with fallback ID ${newId} (was ${rule.id})`);
          break;
          
        } catch (retryError) {
          attempts++;
          console.log(`Retry ${attempts}: ID ${newId} also conflicts`);
        }
      }
      
      if (attempts >= 100) {
        console.error(`Failed to find working ID for rule after 100 attempts`);
      }
    }
  }
  
  console.log(`Successfully applied ${successfulRules.length}/${rules.length} rules`);
  return successfulRules;
}

async function setMode(mode) {
  currentMode = mode;
  blockedCount = 0;
  updateBadge();

  try {
    // Step 1: Clear all our dynamic rules first
    const removeIds = await getAllDynamicRuleIds();
    if (removeIds.length > 0) {
      console.log(`Removing ${removeIds.length} existing dynamic rules`);
      await chrome.declarativeNetRequest.updateDynamicRules({ 
        removeRuleIds: removeIds, 
        addRules: [] 
      });
      
      // Delay to ensure rules are cleared
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    // Step 2: Build new rules
    const proposedRules = await buildModeRules(mode);
    
    if (proposedRules.length > 0) {
      console.log(`Built ${proposedRules.length} rules for mode: ${mode}`);
      
      // Step 3: Use the new validation approach
      const appliedRules = await validateAndApplyRules(proposedRules);
      
      if (appliedRules.length > 0) {
        console.log(`✓ Successfully set mode to ${mode} with ${appliedRules.length} rules`);
      } else {
        console.error(`Failed to apply any rules for mode ${mode}`);
        currentMode = 'off';
      }
    } else {
      console.log(`No rules needed for mode: ${mode}`);
    }
    
  } catch (error) {
    console.error('Error setting mode:', error);
    
    // Fallback: Clear everything and disable
    try {
      console.log('Attempting fallback recovery...');
      await clearAllDynamicRules();
      currentMode = 'off';
      console.log('Fallback: Extension disabled due to persistent conflicts');
    } catch (fallbackError) {
      console.error('Fallback recovery failed:', fallbackError);
    }
  }
}

async function findAvailableIdRange(startId, count) {
  // Get all existing rules (both static and dynamic)
  const [staticRules, dynamicRules] = await Promise.all([
    chrome.declarativeNetRequest.getSessionRules().catch(() => ({ rules: [] })),
    chrome.declarativeNetRequest.getDynamicRules().catch(() => ({ rules: [] }))
  ]);
  
  const existingIds = new Set([
    ...(staticRules.rules || []).map(r => r.id),
    ...(dynamicRules.rules || []).map(r => r.id)
  ]);
  
  console.log('Existing rule IDs:', Array.from(existingIds).sort((a,b) => a-b));
  
  // Use random ID generation approach to avoid conflicts
  const maxAttempts = 1000;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    // Generate random starting ID in a high range
    const randomStart = Math.floor(Math.random() * 900000) + 100000; // 100k to 1M range
    
    let rangeAvailable = true;
    // Check if this entire range is available
    for (let i = 0; i < count; i++) {
      if (existingIds.has(randomStart + i)) {
        rangeAvailable = false;
        break;
      }
    }
    
    if (rangeAvailable) {
      console.log(`Found available random ID range: ${randomStart} to ${randomStart + count - 1} (${count} rules) after ${attempt + 1} attempts`);
      return randomStart;
    }
  }
  
  throw new Error(`Could not find available ID range after ${maxAttempts} attempts`);
}

async function buildModeRules(mode) {
  const rules = [];
  try {
    const presets = await fetch(chrome.runtime.getURL('rules/presets.json')).then(r => r.json());
    const enabled = (await chrome.storage.local.get({ enabled: true })).enabled;
    if (!enabled || mode === 'off') return rules;

    let ruleCount = 0;
    
    // Count total rules needed
    if (mode === 'balanced') {
      ruleCount += (presets.balanced || []).length;
    }
    if (mode === 'paranoid') {
      ruleCount += (presets.balanced || []).length;
      ruleCount += (presets.paranoid || []).length;
    }
    
    const { customRules } = await chrome.storage.local.get({ customRules: [] });
    ruleCount += (customRules || []).length;

    // Find available ID range for all rules - start much higher to avoid conflicts
    const startId = await findAvailableIdRange(80000, ruleCount); // Start at 80000
    let currentId = startId;

    const addPreset = (arr, label) => {
      const presetRules = (arr || []).map((r) => {
        const rule = {
          id: currentId++,
          priority: 1,
          action: { type: r.type },
          condition: { regexFilter: r.regexFilter, resourceTypes: r.resourceTypes }
        };
        console.log(`Adding ${label} rule with ID ${rule.id}`);
        return rule;
      });
      return presetRules;
    };

    if (mode === 'balanced') {
      rules.push(...addPreset(presets.balanced, 'balanced'));
    }
    if (mode === 'paranoid') {
      rules.push(...addPreset(presets.balanced, 'balanced'));
      rules.push(...addPreset(presets.paranoid, 'paranoid'));
    }

    // Custom user rules
    (customRules || []).forEach((r, idx) => {
      const rule = {
        id: currentId++,
        priority: r.priority || 1,
        action: { type: r.type || 'block' },
        condition: r.condition
      };
      console.log(`Adding custom rule with ID ${rule.id}`);
      rules.push(rule);
    });
    
    console.log(`Built ${rules.length} rules with IDs from ${startId} to ${currentId - 1}`);
  } catch (error) {
    console.error('Error building mode rules:', error);
  }
  return rules;
}

async function applyCustomRules(rules) {
  await chrome.storage.local.set({ customRules: rules });
  await setMode(currentMode);
}

async function getAllDynamicRuleIds() {
  const { rules } = await chrome.declarativeNetRequest.getDynamicRules();
  const ruleIds = (rules || []).map(r => r.id);
  console.log('Current dynamic rule IDs:', ruleIds);
  return ruleIds;
}

async function listAllRules() {
  const [staticRules, dynamicRules, sessionRules] = await Promise.all([
    chrome.declarativeNetRequest.getDynamicRules().catch(() => ({ rules: [] })),
    chrome.declarativeNetRequest.getSessionRules().catch(() => ({ rules: [] })),
    fetch(chrome.runtime.getURL('rules/static_rules.json')).then(r => r.json()).catch(() => [])
  ]);
  
  return {
    static: staticRules.rules || [],
    session: sessionRules.rules || [],
    manifest: staticRules || []
  };
}

async function forceCompleteReset() {
  console.log('FORCE RESET: Clearing all rules and resetting state...');
  
  try {
    // Clear all dynamic rules
    await clearAllDynamicRules();
    
    // Reset storage state
    await chrome.storage.local.set({ 
      mode: 'off', 
      customRules: [], 
      enabled: false 
    });
    
    // Reset internal state
    currentMode = 'off';
    blockedCount = 0;
    updateBadge();
    
    console.log('FORCE RESET: Complete');
    
    // Wait a moment then try to enable balanced mode
    setTimeout(async () => {
      try {
        await chrome.storage.local.set({ enabled: true });
        await setMode('balanced');
      } catch (error) {
        console.error('Failed to re-enable after reset:', error);
      }
    }, 1000);
    
  } catch (error) {
    console.error('Force reset failed:', error);
    throw error;
  }
}

async function clearAllDynamicRules() {
  try {
    const allRules = await chrome.declarativeNetRequest.getDynamicRules();
    if (allRules.rules && allRules.rules.length > 0) {
      const ruleIds = allRules.rules.map(r => r.id);
      console.log('Clearing dynamic rules with IDs:', ruleIds);
      await chrome.declarativeNetRequest.updateDynamicRules({ 
        removeRuleIds: ruleIds, 
        addRules: [] 
      });
      console.log('All dynamic rules cleared successfully');
    } else {
      console.log('No dynamic rules to clear');
    }
  } catch (error) {
    console.error('Error clearing dynamic rules:', error);
    throw error;
  }
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