# Privacy Policy

**Last Updated:** October 17, 2025

## Overview

Command & Code: Web Firewall ("the Extension") is committed to protecting your privacy. This privacy policy explains how the Extension handles data.

## Data Collection

### What We DON'T Collect

- **No Remote Data Collection**: The Extension does NOT transmit any data to external servers
- **No Personal Information**: We do not collect, store, or transmit any personally identifiable information
- **No Browsing History**: Your browsing history is never collected or shared
- **No Analytics**: We do not use any analytics services or tracking
- **No Third-Party Services**: No data is shared with third parties

### What We Store Locally

The Extension stores the following data **locally on your device only**:

1. **Security Telemetry** (optional, local-only):
   - Timestamps of blocked requests
   - Blocked URLs and domains
   - Rule IDs that triggered blocks
   - Action types (block/allow)
   - **Storage Location**: Chrome's local storage API
   - **Retention**: Ring buffer of up to 5,000 most recent events
   - **User Control**: Can be cleared anytime via the Telemetry page

2. **User Preferences**:
   - Selected security mode (off/balanced/paranoid)
   - Extension enabled/disabled state
   - Custom blocking rules (if configured)
   - **Storage Location**: Chrome's local storage API

3. **Block Count**:
   - Number of requests blocked in current session
   - **Storage Location**: Memory and extension badge
   - **Reset**: Cleared when telemetry is cleared

## Data Access

- **You Have Full Control**: All data is stored locally on your device
- **No Cloud Sync**: Data is NOT synchronized across devices
- **Export Capability**: You can export telemetry data as JSON or CSV for your own analysis
- **Easy Deletion**: All telemetry can be cleared with one click

## Permissions Usage

The Extension requires the following permissions:

### `declarativeNetRequest`
**Purpose**: Block malicious or unwanted web requests based on user-selected security rules
**Data Access**: Reviews request URLs to apply blocking rules
**Data Transmission**: None - all processing is local

### `declarativeNetRequestFeedback`
**Purpose**: Record telemetry about blocked requests (local-only)
**Data Access**: Captures metadata about blocked requests (URL, timestamp, rule ID)
**Data Transmission**: None - stored locally only

### `storage`
**Purpose**: Save user preferences and local telemetry
**Data Access**: Stores settings and telemetry in Chrome's local storage
**Data Transmission**: None - remains on your device

### `activeTab` (if added in future)
**Purpose**: Would allow manual blocking/allowing of specific tabs
**Current Status**: Not currently implemented

## Security

- **Local Processing Only**: All security rules are evaluated locally in your browser
- **No Network Communication**: The Extension does not make any network requests
- **Open Source**: Code is available for review and audit
- **Minimal Permissions**: Only requests permissions necessary for core functionality

## Changes to Privacy Policy

We may update this privacy policy from time to time. Changes will be reflected in the "Last Updated" date above. Continued use of the Extension after changes constitutes acceptance of the updated policy.

## Data Retention

- **Telemetry Events**: Automatically limited to 5,000 most recent events (ring buffer)
- **User Preferences**: Retained until Extension is uninstalled or manually reset
- **Session Data**: Block counts reset when telemetry is cleared

## Your Rights

You have the right to:
- **Access Your Data**: View all telemetry via the Telemetry page
- **Export Your Data**: Download telemetry as JSON or CSV
- **Delete Your Data**: Clear all telemetry with one click
- **Control Collection**: Disable telemetry collection by turning off the Extension

## Children's Privacy

The Extension does not knowingly collect any information from anyone, including children under 13.

## Contact

For privacy concerns or questions about this policy, please open an issue on our GitHub repository:
https://github.com/lephubui/command-code

## Compliance

This Extension complies with:
- Chrome Web Store Developer Program Policies
- General Data Protection Regulation (GDPR) principles
- California Consumer Privacy Act (CCPA) principles

**Key Compliance Points**:
- ✅ No data collection or transmission to remote servers
- ✅ All data processing is local
- ✅ Users have full control over their data
- ✅ Clear disclosure of permissions and data usage
- ✅ No third-party data sharing
