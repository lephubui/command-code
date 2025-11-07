# Service Worker Auto-Disable Fix

## The Problem: Extension Resets to "Disable" After a Few Minutes

### Root Cause: Chrome Service Worker Lifecycle

Chrome Manifest V3 service workers are **event-driven** and don't stay alive forever:

1. **Service worker starts** when an event occurs (extension click, message, alarm, etc.)
2. **Stays alive for ~30 seconds** of inactivity
3. **Terminates automatically** to save memory/resources
4. **Restarts on next event** with **fresh variables**

### What Was Happening:

```javascript
// OLD CODE
let currentMode = 'off'; // Initial value

chrome.runtime.onStartup.addListener(async () => {
  // Only fires when BROWSER starts, not when service worker restarts!
  const { mode } = await chrome.storage.local.get({ mode: 'balanced' });
  currentMode = mode;
});
```

**Timeline:**
```
00:00 - User sets mode to "paranoid" → currentMode = 'paranoid' ✅
00:30 - Service worker terminates (no activity)
05:00 - User opens popup → Service worker restarts
05:00 - currentMode = 'off' (default value) ❌
05:00 - Popup shows "Disabled" even though storage has 'paranoid'
```

### Why `onStartup` Wasn't Enough:

| Event | When It Fires | Restores State? |
|-------|---------------|-----------------|
| `chrome.runtime.onStartup` | Browser launch only | ✅ Yes (but only once) |
| Service worker restart | After 30s inactivity | ❌ No - variables reset! |
| Extension reload | Developer reload | ❌ No - goes to onInstalled |
| Extension update | Auto-update | ❌ No - goes to onInstalled |

## The Solution: State Restoration on Every Activation

### What We Changed:

#### 1. Added State Initialization Tracking
```javascript
let stateInitialized = false; // Track if state has been restored
```

#### 2. Created `restoreState()` Function
```javascript
async function restoreState() {
  if (stateInitialized) {
    return; // Already restored
  }
  
  console.log('[restoreState] Restoring extension state from storage');
  const { mode, enabled } = await chrome.storage.local.get({ 
    mode: 'balanced', 
    enabled: true 
  });
  
  currentMode = mode;
  stateInitialized = true;
  
  if (enabled) {
    await setMode(mode);
  } else {
    await setEnabled(false);
  }
}
```

#### 3. Call `restoreState()` on Every Entry Point

**On Browser Startup:**
```javascript
chrome.runtime.onStartup.addListener(async () => {
  await restoreState();
});
```

**On Extension Icon Click:**
```javascript
chrome.action.onClicked.addListener(async () => {
  if (!stateInitialized) {
    await restoreState();
  }
  // ... toggle logic
});
```

**On Every Message (Popup, Options, etc.):**
```javascript
chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  (async () => {
    if (!stateInitialized) {
      await restoreState(); // Restore before handling message
    }
    await handleMessage(msg, sendResponse);
  })();
  return true;
});
```

### How It Works Now:

**Timeline:**
```
00:00 - User sets mode to "paranoid"
      → currentMode = 'paranoid' ✅
      → storage.mode = 'paranoid' ✅
      → stateInitialized = true ✅

00:30 - Service worker terminates (inactive)
      → All variables cleared from memory

05:00 - User opens popup
      → Service worker restarts
      → currentMode = 'off' (default)
      → stateInitialized = false (default)
      
05:00 - Popup sends 'getState' message
      → onMessage listener fires
      → Checks stateInitialized === false
      → Calls restoreState()
      → Reads storage.mode = 'paranoid'
      → Sets currentMode = 'paranoid' ✅
      → Sets stateInitialized = true ✅
      → Returns correct state to popup ✅
```

## Testing the Fix

### Test 1: Service Worker Termination
1. Set mode to "Maximum Security"
2. Wait 2 minutes (let service worker terminate)
3. Open popup
4. **Expected:** Still shows "Maximum Security" ✅

### Test 2: Extension Reload
1. Set mode to "Maximum Security"
2. Go to chrome://extensions/
3. Click "Reload" button
4. Open popup
5. **Expected:** Still shows "Maximum Security" ✅

### Test 3: Multiple Interactions
1. Set mode to "Maximum Security"
2. Close popup
3. Wait 1 minute
4. Open popup again
5. Change to "Balanced"
6. Wait 1 minute
7. Open popup again
8. **Expected:** Shows "Balanced" ✅

## Debugging Service Worker Lifecycle

### Check If Service Worker Is Active:
1. Go to `chrome://extensions/`
2. Find "Web Firewall"
3. Look for **"service worker"** link:
   - If it says **(inactive)** → terminated
   - If it's a blue link → currently running

### Monitor Termination/Restart:
Open service worker console and you'll see:
```
[restoreState] Restoring extension state from storage
[restoreState] Found in storage - mode: paranoid, enabled: true
[setMode] Mode set to: paranoid, saved to storage
```

If you see this message repeatedly, it means the service worker is restarting.

### Force Service Worker Termination (Testing):
```javascript
// In service worker console:
chrome.runtime.reload(); // Restart service worker
```

## Related Chrome Bugs & Limitations

### Service Worker Lifetime:
- **Idle timeout:** ~30 seconds of inactivity
- **Max execution time:** 5 minutes (even if active)
- **Cannot be kept alive:** No way to prevent termination

### Best Practices:
✅ **Always store state in `chrome.storage`**, not just memory
✅ **Restore state lazily** on first use after restart
✅ **Track initialization** to avoid repeated restoration
❌ **Don't rely on global variables** persisting across restarts
❌ **Don't assume `onStartup` restores everything**

## Additional Fixes Applied

### Fix 1: Storage Sync After Mode Changes
```javascript
// Now saves to storage after successful mode change
await chrome.storage.local.set({ mode: currentMode });
```

### Fix 2: Prevent Accidental Icon Click Disable
```javascript
// Added logging to track icon clicks
console.log(`[Extension Icon Click] Toggling: ${enabled} → ${newState}`);
```

### Fix 3: Don't Auto-Disable on Errors
```javascript
// Old: currentMode = 'off' on any error
// New: Keep current mode, log error, let user decide
console.error('[setMode] Failed to apply rules, but keeping mode');
```

## What Was NOT the Problem

❌ **Not a timeout** - No setTimeout/setInterval causing auto-disable
❌ **Not a Chrome bug** - Expected service worker behavior
❌ **Not storage corruption** - Storage was fine, just not being read
❌ **Not rule conflicts** - Rules were applying correctly
❌ **Not error recovery** - We fixed that separately but wasn't the cause

## Monitoring Your Extension

### Check Current State (Run in service worker console):
```javascript
chrome.storage.local.get(['mode', 'enabled'], (result) => {
  console.log('Storage:', result);
  console.log('Memory:', { currentMode, stateInitialized });
});
```

### Expected Output:
```
Storage: { mode: 'paranoid', enabled: true }
Memory: { currentMode: 'paranoid', stateInitialized: true }
```

If `stateInitialized` is `false`, the service worker just restarted and hasn't restored state yet.

## Impact

**Before Fix:**
- ❌ Extension appeared "disabled" after 30 seconds
- ❌ User settings lost on service worker restart
- ❌ Had to manually re-enable after idle periods
- ❌ Confusing user experience

**After Fix:**
- ✅ Extension stays in selected mode indefinitely
- ✅ Settings persist across service worker restarts
- ✅ Seamless experience for users
- ✅ No manual re-enabling needed

## References

- [Chrome Service Worker Lifecycle](https://developer.chrome.com/docs/extensions/mv3/service_workers/)
- [chrome.storage API](https://developer.chrome.com/docs/extensions/reference/storage/)
- [Manifest V3 Migration Guide](https://developer.chrome.com/docs/extensions/mv3/intro/)
