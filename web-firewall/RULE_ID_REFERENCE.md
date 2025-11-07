# Web Firewall - Rule ID Reference Guide

## Understanding Rule IDs

Every security rule in Web Firewall has a unique ID number. This guide explains what each rule ID means and what it blocks.

---

## 📋 Rule ID Ranges

| Range | Type | Description |
|-------|------|-------------|
| **1-9999** | Reserved | Future use |
| **10000-10999** | Static Rules | Always loaded from `static_rules.json` |
| **25000-34999** | Balanced Mode | Dynamic rules for balanced protection |
| **35000-54999** | Paranoid Mode | Dynamic rules for maximum security |
| **55000-79999** | Custom Rules | User-defined rules |
| **80000+** | Runtime | Dynamically assigned at startup |

---

## 🛡️ Static Rules (10000-10999)

These rules are always available and defined in `static_rules.json`:

### **10001** - 🚫 JavaScript URL Protocol
- **Blocks:** `javascript:` URLs
- **Prevents:** XSS attacks using javascript: protocol
- **Example:** `javascript:alert(document.cookie)`
- **Severity:** High

### **10002** - 🚫 Data URL Protocol
- **Blocks:** `data:` URLs in scripts, frames, and images
- **Prevents:** XSS attacks using data URLs
- **Example:** `data:text/html,<script>alert('xss')</script>`
- **Severity:** High

### **10010** - 🛡️ XSS Patterns in URLs
- **Blocks:** Common XSS patterns in request URLs
  - `<script>` tags (encoded or plain)
  - `onerror=` event handlers
  - `onload=` event handlers
- **Prevents:** Reflected XSS attacks
- **Example:** `http://site.com?q=<script>alert(1)</script>`
- **Severity:** Critical

### **10020** - 💉 SQL Injection Patterns
- **Blocks:** Common SQL injection patterns
  - `UNION SELECT` statements
  - `OR 1=1` conditions
  - `information_schema` queries
  - `sleep()` and `load_file()` functions
  - SQL comment syntax (`--`, `'--`)
- **Prevents:** SQL injection attacks
- **Example:** `http://site.com?id=1' OR '1'='1`
- **Severity:** Critical

### **10030** - 📊 Analytics & Tracking
- **Blocks:** Common analytics and tracking requests
  - Google Analytics (`/analytics.js`, `/gtag/js`)
  - Tracking pixels (`/pixel.gif`)
  - Data collection endpoints (`/collect?`)
- **Prevents:** User tracking and privacy invasion
- **Example:** `https://www.google-analytics.com/analytics.js`
- **Severity:** Low (Privacy)

---

## ⚖️ Balanced Mode Rules (Dynamic IDs)

When you select **Balanced Protection** mode, additional dynamic rules are loaded from `presets.json`:

### Common Balanced Rules:
- **🖼️ JavaScript in Image Tags** - Blocks `<img src=javascript:>` patterns
- **📄 Base64 HTML Data URLs** - Blocks `data:text/html;base64,` encoded content
- **And more...** (See `rules/presets.json` for full list)

**Note:** These rules get **random IDs starting around 80000+** to avoid conflicts.

---

## 🔒 Paranoid Mode Rules (Dynamic IDs)

When you select **Maximum Security** mode, you get:
- ✅ All Balanced mode rules
- ✅ Plus additional paranoid rules:

### Additional Paranoid Rules:
- **🍪 Cookie/Storage Access** - Blocks suspicious access to:
  - `document.cookie`
  - `localStorage`
  - `sessionStorage`
- **🔐 Admin Panel Access** - Blocks common admin paths:
  - `/wp-admin`
  - `/admin/login`
  - `/phpmyadmin`
- **And more...** (See `rules/presets.json` for full list)

**Note:** These also get **random IDs starting around 80000+**.

---

## ⚙️ Custom Rules (55000-79999)

Users can add custom blocking rules through the **Options** page. These are assigned IDs in the 55000 range.

**Example custom rule:**
```json
{
  "id": 55001,
  "priority": 1,
  "action": { "type": "block" },
  "condition": {
    "urlFilter": "evil-tracker.com",
    "resourceTypes": ["script", "image"]
  }
}
```

---

## 🔧 Runtime Dynamic Rules (80000+)

When you switch modes, the extension:
1. Calculates how many rules are needed
2. Finds an available ID range starting around 80000
3. Assigns sequential IDs to avoid conflicts

**Example flow:**
```
Mode: Balanced
- Rule 1 → ID 82341
- Rule 2 → ID 82342
- Rule 3 → ID 82343
...
```

---

## 📊 Interpreting Telemetry Rule IDs

### In the Telemetry Page:

When you see rule IDs in telemetry:

**Rule ID 10030** → Look up in Static Rules section
- 📊 Analytics & Tracking
- Likely blocked Google Analytics or tracking pixel

**Rule ID 82451** → Dynamic runtime rule
- 🔧 Check your current mode (Balanced or Paranoid)
- Rule was loaded from presets.json
- Hover over the ID for description

**Rule ID 55123** → Custom user rule
- ⚙️ Check Options page for your custom rules
- You defined this rule manually

---

## 🎯 Quick Reference Cheat Sheet

| If Rule ID is... | It's Blocking... | Threat Level |
|-----------------|------------------|--------------|
| **10001** | `javascript:` URLs | 🔴 High |
| **10002** | `data:` URLs | 🔴 High |
| **10010** | XSS patterns in URLs | 🔴 Critical |
| **10020** | SQL injection | 🔴 Critical |
| **10030** | Analytics/tracking | 🟡 Low (Privacy) |
| **80000+** | Dynamic security rules | 🟠 Medium-High |
| **55000-79999** | Your custom rules | ⚪ User-defined |

---

## 💡 Pro Tips

### 1. **Check Rule Performance**
In the telemetry page, the **"📊 Top Rules"** table shows which rules are blocking the most:
- High count for **10030** → Lots of tracking blocked ✅
- High count for **10010** → Suspicious XSS attempts ⚠️
- High count for **10020** → Possible SQL injection attacks 🚨

### 2. **Identify False Positives**
If a legitimate site is blocked:
1. Check telemetry to see which rule blocked it
2. If it's a static rule (10000-10999), might be a false positive
3. If it's a dynamic rule (80000+), try switching to Balanced mode
4. Report issues to help improve rules

### 3. **Custom Rules**
You can add rules to whitelist or block specific domains:
- Go to **Options** page
- Add custom rules in JSON format
- IDs will be assigned in the 55000 range

### 4. **Understanding Blocked Counts**
- **Badge shows total blocks** (all time, until telemetry cleared)
- **Telemetry shows detailed logs** (last 5000 events)
- **Per-rule stats** show which rules are most effective

---

## 🔍 Debugging Rule IDs

### To see what a specific rule ID does:

**Option 1: Hover in Telemetry UI**
- Open Telemetry page
- Hover over any rule ID
- Tooltip shows description

**Option 2: Console Command**
Open browser console on telemetry page:
```javascript
chrome.runtime.sendMessage({ 
  type: 'getRuleDescription', 
  ruleId: 10030 
}, (response) => {
  console.log(response.description);
});
```

**Option 3: Check Source Files**
- Static rules: `rules/static_rules.json`
- Dynamic rules: `rules/presets.json`
- Custom rules: Options page or storage

---

## 📚 Additional Resources

- **Static Rules Source:** `rules/static_rules.json`
- **Dynamic Rules Source:** `rules/presets.json`
- **Service Worker:** `service_worker.js` (see `getRuleDescription()` function)
- **Telemetry:** `telemetry.html` (live blocking data)

---

## 🆘 Need Help?

If you see a rule ID you don't understand:
1. Check this guide for the ID range
2. Open telemetry and hover over the ID
3. Check the source JSON files
4. Report unclear rules for documentation updates

---

**Last Updated:** October 19, 2025  
**Extension Version:** 0.1.0
