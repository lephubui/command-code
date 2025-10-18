# Security Policy

## Overview

Command & Code: Web Firewall is a privacy-focused browser security extension designed to block malicious and unwanted web requests. Security and transparency are our top priorities.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Features

### Core Security Mechanisms

1. **Local-Only Processing**
   - All security rules evaluated locally in your browser
   - No remote servers or cloud dependencies
   - Zero network communication from the Extension

2. **Chrome's declarativeNetRequest API**
   - Uses Chrome's native, secure request blocking API
   - Rules processed at the browser level (not JavaScript)
   - High performance with minimal resource usage

3. **Three Security Modes**
   - **Off**: No blocking (all rules disabled)
   - **Balanced**: Common threats and trackers
   - **Paranoid**: Maximum protection with stricter rules

4. **Custom Rule Support**
   - User-defined blocking rules
   - Validated before application
   - Isolated from preset rules

### Privacy & Data Protection

- **No Telemetry Exfiltration**: All telemetry stored locally only
- **No Analytics**: No usage tracking or analytics services
- **No Third-Party Code**: No external libraries or dependencies
- **Minimal Permissions**: Only essential Chrome APIs used
- **Open Source**: Full code transparency for audit

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow responsible disclosure:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. **Email**: [Your contact email] or use GitHub's private vulnerability reporting
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days with assessment and timeline
- **Resolution**: Security patches prioritized and released ASAP
- **Credit**: Security researchers credited (unless anonymity requested)

### Scope

**In Scope:**
- Extension code vulnerabilities
- Permission misuse or escalation
- Data leakage or privacy issues
- Rule bypass techniques
- XSS or injection vulnerabilities
- Logic flaws in blocking mechanisms

**Out of Scope:**
- Social engineering attacks
- Physical access attacks
- Issues in Chrome itself (report to Google)
- Issues with websites being blocked
- Feature requests (use GitHub issues)

## Security Best Practices for Users

### Installation
- ✅ Install only from the official Chrome Web Store
- ✅ Verify publisher is "Command & Code" / [Your name]
- ❌ Never install from third-party sources or .crx files

### Configuration
- Start with **Balanced** mode for daily use
- Use **Paranoid** mode when extra security is needed
- Review custom rules before adding them
- Regularly check telemetry for suspicious activity

### Updates
- Enable automatic Extension updates in Chrome
- Review changelog after major updates
- Report unexpected behavior immediately

## Known Limitations

1. **Client-Side Only**: Extension cannot protect against server-side attacks
2. **Rule-Based**: Effectiveness depends on rule quality and coverage
3. **Browser-Specific**: Only protects browsing in Chrome/Chromium browsers
4. **Not a Complete Solution**: Should be used as part of layered security approach

## Security Architecture

### Request Blocking Flow

```
1. Web Request Initiated
   ↓
2. Chrome evaluates declarativeNetRequest rules
   ↓
3. Rule match? → BLOCK (telemetry recorded locally)
   ↓
4. No match? → ALLOW (request proceeds)
```

### Data Flow

```
User Preferences → Chrome Local Storage (device only)
Blocked Request → Telemetry Ring Buffer (local, max 5000 events)
Rule Match → Badge Counter (memory only)
```

**No data leaves your device**

## Threat Model

### What We Protect Against
- ✅ Known malicious domains and URLs
- ✅ Tracking scripts and beacons
- ✅ Cryptocurrency miners
- ✅ Phishing attempts (via URL patterns)
- ✅ Unwanted ad networks

### What We DON'T Protect Against
- ❌ Zero-day exploits (until rules updated)
- ❌ Social engineering on allowed sites
- ❌ Malicious browser extensions
- ❌ Operating system vulnerabilities
- ❌ Network-level attacks (use a firewall)

## Permissions Justification

Required permissions and their security implications:

| Permission | Purpose | Risk Mitigation |
|------------|---------|-----------------|
| `declarativeNetRequest` | Block malicious requests | Rules are user-controlled, no arbitrary code execution |
| `declarativeNetRequestFeedback` | Local telemetry recording | Data never transmitted, user can clear anytime |
| `storage` | Save preferences & telemetry | Chrome's local storage, never synced or uploaded |

## Compliance

### Standards & Regulations
- ✅ GDPR Compliant (no personal data processing)
- ✅ CCPA Compliant (no data sale or sharing)
- ✅ Chrome Web Store Policies
- ✅ Manifest V3 Security Requirements

### Code Quality
- Regular security audits
- Dependency scanning (none currently used)
- Manual code review for all changes
- Production builds with debug code removed

## Incident Response

In case of a confirmed security incident:

1. **Immediate**: Remove vulnerable version from Chrome Web Store
2. **1 Hour**: Begin developing and testing patch
3. **24 Hours**: Submit patched version for review
4. **48 Hours**: Publish security advisory with details
5. **Ongoing**: Monitor for exploitation attempts

## Security Updates

Security patches are released as soon as possible:
- **Critical**: Within 24-48 hours
- **High**: Within 1 week
- **Medium**: Next scheduled release
- **Low**: Bundled with feature updates

## Audit History

| Date | Auditor | Findings | Status |
|------|---------|----------|--------|
| 2025-10-17 | Internal | Pre-release security review | ✅ Passed |

## Contact

For security-related questions or to report vulnerabilities:
- **GitHub**: https://github.com/lephubui/command-code/security/advisories
- **Issues**: https://github.com/lephubui/command-code/issues (non-sensitive only)

## Acknowledgments

We thank the security research community for helping keep this Extension secure. Security researchers who responsibly disclose vulnerabilities will be credited in this section (unless anonymity is requested).

---

**Remember**: Security is a shared responsibility. Stay vigilant, keep the Extension updated, and report suspicious activity.
