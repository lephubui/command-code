Security Notes for Tiny HTTP/S Logger

Effective Date: 09/27/2025

Tiny HTTP/S Logger is built with security in mind.

Security Practices

No remote code execution: All scripts are packaged inside the extension. The extension never loads or executes code from external servers.

Minimal permissions: Only webRequest, tabs, and storage are requested. Site access is granted per-site, only when the user explicitly clicks Enable on this site.

Data stays local: Network request metadata is only logged and displayed inside the user’s browser. Logs are temporary and can be cleared at any time. No data is transmitted outside the device.

MV3 compliance: Built on Chrome Extension Manifest V3, ensuring a service worker–based architecture with improved isolation and security.

Reporting Issues

If you discover a potential security issue in this extension, please report it responsibly to: Le Bui - lebui2892@gmail.com.

We will investigate promptly and address confirmed issues with updates.