# 🛡️ Web Firewall Extension

**Advanced browser security extension for Chrome that provides real-time protection against web threats, tracking, and malicious content.**

*Developed by [Command & Code Labs](https://www.cclabs.dev/)*

---

## 🌟 Features

### 🔒 **Multi-Level Security Modes**
- **Balanced Protection**: Core security without browsing interference
- **Maximum Security**: Enhanced protection for high-risk environments
- **Custom Rules**: User-configurable advanced filtering

### 🛡️ **Comprehensive Threat Protection**
- **XSS (Cross-Site Scripting) Prevention**
- **SQL Injection Blocking**
- **Malicious Script Detection**
- **Admin Path Protection**
- **Browser Storage Security**

### 📊 **Real-Time Analytics**
- **Live telemetry dashboard** with detailed blocking statistics
- **Export capabilities** (JSON/CSV) for security analysis
- **Rule effectiveness tracking**
- **Historical threat data**

### ⚙️ **Advanced Customization**
- **JSON-based custom rules** for power users
- **Declarative Net Request API** integration
- **Professional settings interface**

---

## 🚀 Quick Start

### Installation
1. Download the extension package
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the extension folder
5. Pin the extension to your toolbar for easy access

### Basic Usage
1. **Click the extension icon** in your Chrome toolbar
2. **Select your security mode**:
   - 🔓 **Disabled**: No protection (for testing)
   - ⚖️ **Balanced Protection**: Recommended for daily use
   - 🔒 **Maximum Security**: High-security environments
3. **Monitor protection** via the blocked counter badge
4. **View detailed analytics** by clicking "📊 Analytics"

---

## 🔍 Security Modes Detailed

### ⚖️ **Balanced Protection Mode**
*Recommended for daily browsing*

**Static Protection (Always Active):**

| Rule ID | Protection | What It Blocks | Example |
|---------|------------|----------------|---------|
| **10001** | 🚫 JavaScript URL Protocol | `javascript:` URLs | `javascript:alert(document.cookie)` |
| **10002** | 🚫 Data URL Protocol | Malicious `data:` URIs | `data:text/html,<script>alert(1)</script>` |
| **10010** | 🛡️ XSS Patterns | Script tags, event handlers in URLs | `?q=<script>`, `?img=x onerror=` |
| **10020** | 💉 SQL Injection | Database attack patterns | `?id=1' OR '1'='1`, `UNION SELECT` |
| **10030** | 📊 Analytics/Tracking | Google Analytics, pixels | `/analytics.js`, `/pixel.gif` |

**Dynamic Protection (Runtime Rules):**
- ✅ **Image XSS Protection**: Prevents `<img src=javascript:>` attacks
- ✅ **Base64 HTML Blocking**: Stops `data:text/html;base64,` encoded content

**Total Rules: ~7** (5 static + 2 dynamic)

### 🔒 **Maximum Security Mode**
*For high-risk environments and maximum protection*

**Includes ALL Balanced Protection PLUS Enhanced Paranoid Rules:**

| Protection Type | What It Blocks | Use Case |
|----------------|----------------|----------|
| 🍪 **Browser Storage Security** | `document.cookie`, `localStorage`, `sessionStorage` access | Prevents tracking and cookie theft |
| 🔐 **Admin Path Protection** | `/wp-admin`, `/admin/login`, `/phpmyadmin` | Blocks accidental admin access attempts |
| 🎯 **Additional XSS Vectors** | Advanced attack patterns | Enhanced malicious content detection |

**Total Rules: ~9** (5 static + 4 dynamic)

**Recommended For:**
- 🌐 Public Wi-Fi networks
- 🔍 Browsing untrusted websites
- 🏢 High-security work environments
- 🛡️ Maximum privacy protection
- 🚫 Preventing accidental admin access

---

## 🆔 Understanding Rule IDs

Every blocked request is tagged with a **Rule ID** that identifies which security rule blocked it.

### Rule ID Ranges

| ID Range | Type | Description |
|----------|------|-------------|
| **10000-10999** | Static Rules | Core security (always active when enabled) |
| **80000+** | Dynamic Rules | Mode-specific runtime rules (Balanced/Paranoid) |
| **55000-79999** | Custom Rules | Your user-defined rules |

### Quick Rule Reference

**Common Rule IDs You'll See:**
- **10001**: 🚫 Blocked JavaScript URL (XSS prevention)
- **10002**: 🚫 Blocked Data URL (XSS prevention)
- **10010**: 🛡️ Blocked XSS pattern in URL
- **10020**: 💉 Blocked SQL injection attempt
- **10030**: 📊 Blocked analytics/tracking script

**Pro Tip:** Hover over any Rule ID in the Analytics page to see a detailed description of what it blocks!

📖 **Full Reference:** See [RULE_ID_REFERENCE.md](RULE_ID_REFERENCE.md) for complete rule documentation with examples and debugging tips.

---

## 📊 Analytics & Telemetry

### Real-Time Dashboard
Access detailed security analytics through the **📊 Analytics** button:

- **📈 Total Blocked Requests**: Real-time counter of threats stopped
- **🌐 Top Blocked Domains**: Most frequently blocked malicious domains
- **📋 Rule Effectiveness**: Which security rules are most active
- **⏰ Recent Security Events**: Chronological log of blocked threats
- **📤 Export Options**: Download data in JSON or CSV format

### Key Metrics
- **Blocked request counts** by domain and rule
- **Timeline of security events** with full request details
- **Rule effectiveness statistics** - See which rules are most active
- **Rule descriptions** - Hover over Rule IDs for explanations
- **Historical threat patterns** for analysis

### Understanding Telemetry Data

**📊 Top Rules Table:**
- Shows most active security rules
- Each rule displays its ID and description
- Count indicates how many times it blocked content
- Higher counts may indicate:
  - 📊 Heavy tracking on visited sites (Rule 10030)
  - 🛡️ XSS attack attempts (Rules 10010)
  - 💉 SQL injection attempts (Rule 10020)

**🌐 Top Blocked Domains:**
- Analytics domains (google-analytics.com, doubleclick.net)
- Ad networks and trackers
- Potentially malicious domains

**📋 Recent Security Events:**
- Complete log of last 100 blocked requests
- Hover over Rule IDs to see what was blocked and why
- Timestamp, domain, rule, action, and full URL
- Export to CSV/JSON for detailed analysis

---

## ⚙️ Advanced Configuration

### Custom Rules
Create powerful custom blocking rules using Chrome's Declarative Net Request API:

```json
[
  {
    "priority": 1,
    "action": { "type": "block" },
    "condition": {
      "urlFilter": "*malicious-domain.com*",
      "resourceTypes": ["main_frame", "sub_frame"]
    }
  }
]
```

### Supported Rule Options
- **Actions**: `block`, `allow`, `allowAllRequests`
- **Resource Types**: `main_frame`, `sub_frame`, `script`, `image`, `xmlhttprequest`, `stylesheet`, `font`, `media`, `other`
- **Condition Types**: `urlFilter` (simple patterns), `regexFilter` (regex patterns), `domains` (domain lists)

---

## 🛠️ Demo Scenarios

### Testing Balanced Mode
1. **Visit analytics-heavy sites**: CNN, Forbes, TechCrunch
2. **Open Analytics**: Click "📊 Analytics" button
3. **Check telemetry**: 
   - See **Rule 10030** (Analytics/Tracking) blocking Google Analytics
   - Watch blocked counter increase on extension badge
   - View "Top Blocked Domains" showing google-analytics.com, etc.
4. **Hover over Rule IDs**: See descriptions like "📊 Analytics/Tracking - Blocks Google Analytics..."

### Testing Maximum Security
1. **Enable Maximum Security mode** in popup
2. **Try accessing admin paths**: 
   - Search for WordPress demo sites
   - Attempt to access `/wp-admin` or `/phpmyadmin`
3. **Visit storage-heavy sites**: Social media, e-commerce platforms
4. **Check telemetry**:
   - See **dynamic rules (80000+)** for storage blocking
   - More rules active than Balanced mode
   - Additional blocking for cookie/localStorage access

### Custom Rules Demo
1. **Go to Options page** (⚙️ Settings button)
2. **Add custom blocking rule**:
   ```json
   [
     {
       "priority": 1,
       "action": { "type": "block" },
       "condition": {
         "urlFilter": "*example-tracker.com*",
         "resourceTypes": ["script", "image"]
       }
     }
   ]
   ```
3. **Save and test**: Visit a site with that domain
4. **Check telemetry**:
   - See **Rule ID 55000+** (Custom rules range)
   - Verify your custom rule is working
   - Rule description shows "⚙️ Custom Rule - User-defined"

---

## 🔧 Troubleshooting

### Extension Not Blocking
- **Check security mode**: Ensure it's not set to "Disabled"
- **Reload extension**: Go to `chrome://extensions/` and reload
- **Clear cache**: Use "🗑️ Clear Data" in Analytics to reset

### Rules Not Applying
- **Check JSON syntax**: Ensure custom rules are valid JSON arrays
- **Reload after changes**: Extension automatically applies new rules
- **Use debug commands**: Check browser console for error messages

### Mode Resets to Disabled
- **Recent fix applied**: Clear button now preserves security mode
- **Manual restore**: Select your preferred mode after clearing rules

---

## 🏗️ Technical Architecture

### Core Components
- **Service Worker**: Background rule management and telemetry
- **Popup Interface**: User-friendly security mode selection
- **Options Page**: Advanced rule configuration
- **Analytics Dashboard**: Comprehensive security reporting

### APIs Used
- **Chrome Declarative Net Request**: High-performance request filtering
- **Chrome Storage**: Persistent settings and telemetry data
- **Chrome Tabs**: External navigation and analytics export

### Security Features
- **Dynamic Rule ID Allocation**: Prevents conflicts with other extensions
- **Ring Buffer Telemetry**: Efficient memory usage (5000 event limit)
- **Error Recovery**: Automatic fallback and rule conflict resolution

---

## 📈 Performance

### Efficiency
- **Zero performance impact**: Uses Chrome's native filtering engine
- **Minimal memory usage**: Optimized rule storage and telemetry
- **Fast rule updates**: Real-time security mode switching

### Scalability
- **Handles thousands of rules**: Enterprise-ready architecture
- **Efficient telemetry**: Smart data aggregation and storage
- **Background processing**: No UI blocking during rule updates

---

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Load extension in Chrome developer mode
3. Make changes and test locally
4. Submit pull requests for review

### Reporting Issues
- **GitHub Issues**: Report bugs and feature requests
- **Security Issues**: Contact security@cclabs.dev privately
- **Feature Requests**: Community discussion encouraged

---

## � Documentation

### Complete Guides
- 📖 **[RULE_ID_REFERENCE.md](RULE_ID_REFERENCE.md)**: Complete rule ID documentation with examples
- 🔧 **[DEBUG_MODE_SWITCHING.md](DEBUG_MODE_SWITCHING.md)**: Troubleshooting mode switching issues
- 🚨 **[TROUBLESHOOTING_BLOCKING.md](TROUBLESHOOTING_BLOCKING.md)**: Debugging unexpected blocking
- ⚙️ **[SERVICE_WORKER_FIX.md](SERVICE_WORKER_FIX.md)**: Technical details on service worker lifecycle
- 🔐 **[SECURITY.md](SECURITY.md)**: Security policy and vulnerability reporting
- 🔒 **[PRIVACY.md](PRIVACY.md)**: Privacy policy and data handling

### Quick Links
- **Rule explanations**: [RULE_ID_REFERENCE.md](RULE_ID_REFERENCE.md)
- **Debug commands**: [DEBUG_COMMANDS.md](DEBUG_COMMANDS.md)
- **All documentation**: See repository root for complete guides

---

## �📄 License

**MIT License** - See LICENSE file for details

---

## 🏢 About Command & Code Labs

[Command & Code Labs](https://www.cclabs.dev/) develops innovative security tools and browser extensions to protect users from emerging web threats. Our mission is to make the internet safer through accessible, powerful security technology.

### Other Products
- Visit our [product page](https://www.cclabs.dev/product/web-firewall-extention) for more information
- Explore our full security toolkit at [cclabs.dev](https://www.cclabs.dev/)

---

## 📞 Support

- **Documentation**: Full guides available at [cclabs.dev](https://www.cclabs.dev/)
- **Community**: Join our user community for tips and best practices
- **Enterprise**: Contact us for enterprise deployment and custom rules

---

**🛡️ Stay Safe, Browse Secure with Web Firewall Extension**

*Protecting your digital journey, one request at a time.*