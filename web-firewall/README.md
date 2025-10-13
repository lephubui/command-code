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
- ✅ **XSS Prevention**: Blocks `javascript:` URLs and malicious scripts
- ✅ **Data URL Protection**: Prevents malicious data URI execution
- ✅ **Script Injection Blocking**: Detects `<script>` tags and event handlers
- ✅ **SQL Injection Defense**: Blocks database attack patterns
- ✅ **Analytics Blocking**: Stops Google Analytics and tracking pixels

**Dynamic Protection:**
- ✅ **Image XSS Protection**: Prevents JavaScript in image sources
- ✅ **Base64 HTML Blocking**: Stops encoded malicious content

**Total Rules: 7**

### 🔒 **Maximum Security Mode**
*For high-risk environments and maximum protection*

**Includes ALL Balanced Protection PLUS:**
- ✅ **Browser Storage Blocking**: Prevents access to cookies, localStorage, sessionStorage
- ✅ **Admin Path Protection**: Blocks access to:
  - `/wp-admin` (WordPress admin panels)
  - `/admin/login` (Generic admin interfaces)
  - `/phpmyadmin` (Database management tools)

**Total Rules: 9**

**Use Cases:**
- Public Wi-Fi networks
- Browsing untrusted websites
- High-security work environments
- Preventing accidental admin access

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
- **Rule performance statistics** for optimization
- **Historical threat patterns** for analysis

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
1. **Visit analytics-heavy sites**: CNN, Forbes, Amazon
2. **Check telemetry**: See Google Analytics blocks in real-time
3. **Monitor counter**: Watch blocked requests increase

### Testing Maximum Security
1. **Try accessing admin paths**: Search for WordPress demo sites
2. **Visit storage-heavy sites**: Social media, e-commerce platforms
3. **Observe additional blocking**: Admin path and storage protection

### Custom Rules Demo
1. **Add blocking rule** for specific domain in Settings
2. **Test the rule** by visiting the blocked domain
3. **Verify in telemetry**: See custom rule effectiveness

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

## 📄 License

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