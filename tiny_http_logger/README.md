# 🔍 Tiny HTTP/S Logger

**Lightweight Chrome extension for viewing and analyzing HTTP/HTTPS requests made by websites in real-time.**

*Developed by [Command & Code Labs](https://www.cclabs.dev/)*

---

## 🌟 Overview

Tiny HTTP/S Logger is a developer-focused Chrome extension that captures and displays HTTP/HTTPS network activity with detailed metadata. Perfect for debugging, security analysis, and understanding how websites communicate with servers.

### Key Features

✅ **Real-Time Request Logging**  
✅ **Per-Site Permission Control** (privacy-first)  
✅ **Advanced Filtering & Sorting**  
✅ **Request Timeline Visualization**  
✅ **Zero Data Transmission** (100% local)  
✅ **Lightweight & Fast** (MV3 architecture)

---

## 🚀 Quick Start

### Installation

1. **Download** the extension package
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable **"Developer mode"** (top-right toggle)
4. Click **"Load unpacked"** and select the `tiny_http_logger` folder
5. Pin the extension to your toolbar for easy access

### Basic Usage

1. **Navigate to any website** you want to monitor
2. **Click the extension icon** in your toolbar
3. **Click "Enable on this site"** to grant permission
4. **Browse the site** normally—requests appear in real-time
5. **Use filters** to find specific requests (status codes, methods, hosts, etc.)

---

## 📊 Features Detailed

### 🎯 Request Capture

The extension logs comprehensive metadata for each HTTP/HTTPS request:

| Field | Description | Example |
|-------|-------------|---------|
| **Time** | Request timestamp | `3:45:23 PM` |
| **Method** | HTTP method | `GET`, `POST`, `PUT`, `DELETE` |
| **Scheme** | Protocol | `https`, `http` |
| **Status** | HTTP status code | `200`, `404`, `500` |
| **Type** | Resource type | `script`, `image`, `xhr`, `document` |
| **Host** | Target domain | `api.example.com` |
| **URL** | Full request URL | `https://api.example.com/data` |
| **Size** | Content length (bytes) | `1024` |
| **IP** | Server IP address | `192.0.2.1` |

### 🔍 Advanced Filtering

Filter requests using multiple criteria:

**Filter Options:**
- **Host Filter**: Search for specific domains or subdomains
- **Method Filter**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`
- **Scheme Filter**: `http`, `https`
- **Status Filter**: Minimum status code (e.g., `≥ 400` for errors)
- **Tab Filter**: "All tabs" or "Current tab only"
- **Regex Filter**: Advanced pattern matching on URLs
- **Status Code Chips**: Quick filters for 2xx, 3xx, 4xx, 5xx responses

**Examples:**
```
Host: "api"          → Shows all requests to hosts containing "api"
Method: POST         → Only POST requests
Status: ≥ 400        → Only errors (4xx/5xx)
Regex: \.json$       → Only URLs ending in .json
Chip: 4xx           → Only 4xx client errors
```

### 📈 Request Timeline

Visual representation of request timing:
- **Color-coded bars** show request duration
- **Length indicates** relative time spent
- **Hover tooltips** display exact timing
- **Chronological view** of network activity

### 🔄 Sorting

Click any column header to sort:
- **Time**: Chronological order (newest/oldest first)
- **Status**: By HTTP status code
- **Method**: Alphabetically by HTTP method
- **Host**: By domain name
- **Size**: By content length

Click again to reverse sort direction.

### 💾 Data Management

- **Clear Logs**: Remove all captured requests (🗑️ Clear button)
- **Auto-Limit**: Automatically keeps last 800 requests
- **Session Persistence**: UI state persists across popup opens/closes
- **In-Memory Storage**: Data cleared when browser restarts (privacy-focused)

---

## 🔒 Privacy & Security

### Privacy-First Design

✅ **No Data Transmission**  
All request data stays on your device. Nothing is sent to external servers.

✅ **Per-Site Permissions**  
You explicitly grant access per website. No blanket monitoring.

✅ **In-Memory Storage**  
Logs are temporary and cleared when the browser restarts.

✅ **No Tracking**  
No analytics, no telemetry, no user profiling.

### Security Features

🔐 **Manifest V3** (modern security architecture)  
🔐 **No Remote Code** (all code packaged locally)  
🔐 **Content Security Policy** (prevents injection attacks)  
🔐 **Optional Host Permissions** (user controls access)

📖 **Full Security Policy**: See [SECURITY.md](SECURITY.md) for details

---

## 🛠️ Use Cases

### 🧑‍💻 Web Development

**Debug API Calls:**
```
Filter: Method = POST, Host = "api"
→ See all POST requests to your API endpoint
```

**Check Resource Loading:**
```
Filter: Type = script, Status ≥ 400
→ Find failed script loads breaking your site
```

**Monitor Third-Party Services:**
```
Filter: Host = "analytics", Regex: tracking
→ Identify which analytics scripts are running
```

### 🔍 Security Analysis

**Detect Tracking:**
```
Filter: Type = image, Host = "pixel"
→ Find tracking pixels and beacons
```

**Identify API Endpoints:**
```
Filter: Type = xhr, Method = GET
→ Map AJAX/fetch requests
```

**Check HTTPS Usage:**
```
Filter: Scheme = http
→ Find insecure HTTP requests
```

### 📊 Performance Monitoring

**Find Large Requests:**
```
Sort by: Size (descending)
→ Identify bandwidth-heavy resources
```

**Check Caching:**
```
Filter: Status = 304
→ See which resources are cached
```

**Monitor API Response Times:**
```
Timeline view → Visual duration analysis
```

---

## 🎨 User Interface

### Dark Theme Design

Built with Command & Code Labs' signature dark theme:
- **High contrast** for easy readability
- **Purple-blue accent** colors
- **Monospace fonts** for URLs and timestamps
- **Smooth animations** and transitions
- **Responsive table** with horizontal scrolling

### Keyboard-Friendly

- ✅ Full tab navigation
- ✅ Accessible form controls
- ✅ Clear focus indicators

---

## ⚙️ Technical Architecture

### Core Components

**Background Service Worker** (`background.js`)
- Listens to `webRequest` API events
- Captures request lifecycle stages: `before`, `headers`, `completed`, `error`
- Manages dynamic listener attachment based on granted permissions
- Stores logs in memory (max 800 entries)

**Popup Interface** (`popup.html` / `popup.js`)
- Displays request table with filters and sorting
- Renders timeline visualization
- Manages permission grants per site
- Persists UI state in session storage

**Permissions System**
- Uses **optional host permissions** for privacy
- Users grant access per domain when needed
- Dynamic listener registration based on active permissions

### Chrome APIs Used

| API | Purpose |
|-----|---------|
| `webRequest` | Capture network requests |
| `tabs` | Identify current active tab/site |
| `storage.session` | Persist UI state (filters, sort) |
| `permissions` | Manage optional host permissions |

### Data Flow

```
Website Request
    ↓
webRequest API Events (onBeforeRequest, onHeadersReceived, onCompleted)
    ↓
background.js Listeners
    ↓
In-Memory Log Array (max 800)
    ↓
popup.js Queries via chrome.runtime.sendMessage()
    ↓
Filtered & Sorted Display in popup.html Table
```

---

## 🔧 Advanced Features

### Request Lifecycle Tracking

The extension tracks 4 stages of each request:

1. **before**: Initial request sent (captures method, URL, type)
2. **headers**: Response headers received (captures status, content-type, server)
3. **completed**: Request finished successfully (captures IP, cache status)
4. **error**: Request failed (captures error message)

### Content Analysis

Extracts from response headers:
- `Content-Type`: MIME type (e.g., `application/json`)
- `Content-Length`: Response size in bytes
- `Content-Encoding`: Compression method (`gzip`, `br`)
- `Server`: Server software (e.g., `nginx/1.21.0`)

### Automatic Memory Management

- **Ring Buffer**: Keeps last 800 requests, auto-removes oldest
- **Service Worker Lifecycle**: Logs cleared when SW unloads (privacy)
- **No Persistent Storage**: Data never written to disk

---

## 📖 Filter Reference

### Status Code Chips

| Chip | Range | Meaning |
|------|-------|---------|
| **2xx** | 200-299 | Success (OK, Created, Accepted) |
| **3xx** | 300-399 | Redirection (Moved, Not Modified) |
| **4xx** | 400-499 | Client Errors (Not Found, Forbidden) |
| **5xx** | 500-599 | Server Errors (Internal Error, Bad Gateway) |

### Common HTTP Methods

| Method | Typical Use |
|--------|-------------|
| `GET` | Retrieve data (pages, images, API responses) |
| `POST` | Submit data (forms, file uploads, API writes) |
| `PUT` | Update existing resource |
| `DELETE` | Remove resource |
| `PATCH` | Partial update |
| `HEAD` | Get headers only (no body) |
| `OPTIONS` | CORS preflight checks |

### Resource Types

| Type | Description |
|------|-------------|
| `main_frame` | HTML document (page navigation) |
| `sub_frame` | Iframe content |
| `script` | JavaScript files |
| `stylesheet` | CSS files |
| `image` | Images (PNG, JPG, SVG, etc.) |
| `xmlhttprequest` | AJAX/fetch requests |
| `font` | Web fonts |
| `media` | Audio/video |

---

## 🔄 Workflow Examples

### Example 1: Debug Failed API Call

**Scenario**: Your web app shows "Failed to load data"

**Steps**:
1. Enable logger on the site
2. Filter: `Method = GET`, `Host = "api"`
3. Sort by: `Status` (descending)
4. Look for **4xx/5xx** responses
5. Hover URL to see full endpoint
6. Check timeline for timing issues

**Result**: Identify which API endpoint is failing and why (404? 500? timeout?)

---

### Example 2: Find Tracking Scripts

**Scenario**: You want to see what analytics/tracking runs on a site

**Steps**:
1. Enable logger on the site
2. Filter: `Type = script`
3. Filter: `Regex = analytics|tracking|pixel|beacon`
4. Or use Host filter: `google|facebook|doubleclick`

**Result**: See all tracking scripts loaded by the page

---

### Example 3: Monitor API Performance

**Scenario**: Check how fast your backend API responds

**Steps**:
1. Enable logger on your app
2. Filter: `Host = "api.yoursite.com"`
3. View **Timeline** to see request durations
4. Sort by **Time** to see chronological order

**Result**: Visual performance analysis of API calls

---

## 🚧 Troubleshooting

### Extension Not Showing Requests

✅ **Check permission**: Click "Enable on this site" in popup  
✅ **Verify site uses HTTP/HTTPS**: chrome:// and file:// URLs aren't captured  
✅ **Reload page**: Some requests happen before enabling  
✅ **Check filters**: Disable all filters to see everything

### "Needs Access" Message Won't Go Away

✅ **Click the button**: Extension needs explicit user permission  
✅ **Reload popup**: Close and reopen the extension popup  
✅ **Check site URL**: Some special pages can't grant permissions

### Logs Not Persisting

✅ **This is by design**: Logs are cleared on browser restart for privacy  
✅ **Max 800 requests**: Older logs auto-delete when limit reached  
✅ **Service worker lifecycle**: Background worker unloading clears logs

### Timeline Not Showing

✅ **Requires size data**: Timeline needs Content-Length headers  
✅ **Some requests don't report size**: Normal for certain resource types

---

## 🤝 Contributing

### Development Setup

1. Clone the repository
2. Load extension in Chrome (Developer mode → Load unpacked)
3. Make changes to source files
4. Reload extension in `chrome://extensions/`
5. Test functionality

### Reporting Issues

- **Bug Reports**: Describe steps to reproduce, expected vs actual behavior
- **Feature Requests**: Explain use case and expected benefit
- **Security Issues**: Report privately to lebui2892@gmail.com

---

## 📄 Documentation

### Related Files

- 📖 **[SECURITY.md](SECURITY.md)**: Security practices and vulnerability reporting
- 🔒 **[PRIVATE.md](PRIVATE.md)**: Privacy policy and data handling (if exists)

### External Resources

- 📚 [Chrome WebRequest API Documentation](https://developer.chrome.com/docs/extensions/reference/webRequest/)
- 📚 [Manifest V3 Migration Guide](https://developer.chrome.com/docs/extensions/mv3/intro/)
- 📚 [HTTP Status Codes Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## 📜 License

**MIT License** - See LICENSE file for details

---

## 🏢 About Command & Code Labs

[Command & Code Labs](https://www.cclabs.dev/) develops innovative developer tools and browser extensions to improve web development workflows and security analysis.

### Our Philosophy

- **Privacy-First**: Your data stays on your device
- **Developer-Focused**: Tools built by developers, for developers
- **Open & Transparent**: Clear documentation and honest practices
- **Minimal & Fast**: Lightweight tools that don't slow you down

### Other Products

- 🛡️ **Web Firewall Extension**: Browser security for blocking XSS, SQLi, and trackers
- 📦 Explore our full toolkit at [cclabs.dev](https://www.cclabs.dev/)

---

## 📞 Support

- **Website**: [https://www.cclabs.dev/](https://www.cclabs.dev/)
- **Email**: lebui2892@gmail.com
- **Documentation**: See repository files for detailed guides

---

**🔍 Analyze Smarter, Debug Faster with Tiny HTTP/S Logger**

*Understanding network traffic, one request at a time.*
