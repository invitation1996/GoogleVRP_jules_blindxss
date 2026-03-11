# Explanation of Blind XSS Issues

The issues associated with `https://github.com/sho3hit/github/issues` (mirrored in this repository) relate to a comprehensive research project into **Blind Cross-Site Scripting (XSS)**. This repository acts as a Proof of Concept (PoC) for payloads that target systems where input is saved and later rendered in a different, often privileged, context (like an admin panel or a logging dashboard).

## Summary of Findings

### 1. Primary Vulnerability: Blind XSS
The core issue is the potential for **Stored Blind XSS**. These vulnerabilities are dangerous because the payload is executed in a context the attacker cannot see directly, often bypassing traditional front-end security controls.

### 2. Categorization of XSS Vectors
The research identifies and tests several categories of injection vectors:
- **Event-Based Attributes**: Utilizing handlers like `onerror` (in `<img>`), `onfocus` (in `<input>` with `autofocus`), and `onload` (in `<body>` or `<svg>`).
- **Protocol-Based Execution**: Leveraging the `javascript:` pseudo-protocol in URL-based attributes (`href`, `src`).
- **External Resource Fetching**: Using `<iframe>`, `<script>`, and `<base>` tags to load external content or hijack relative paths.
- **Template Injection**: Specific payloads for **AngularJS** that exploit expression evaluation (`{{constructor.constructor(...)()}}`).
- **Meta Redirects**: Using `<meta http-equiv="refresh" ...>` to force unauthorized navigation.

### 3. Obfuscation Techniques
A significant portion of the "issues" involve the use of **Base64 encoding** (`eval(atob(...))`). This technique is used to:
- Evade simple string-based filters and static analysis.
- Dynamically inject complex script elements that load payloads from an external server.

### 4. Callback Infrastructure
All payloads are configured to send a callback to **`1.hackeronce.com`**. These callbacks include unique identifiers (e.g., `?p=img-onerror`) that allow the researcher to pinpoint exactly which vector was successful in the backend system.

### 5. High-Value Attack Surfaces
The repository highlights that these issues are most likely to be found in:
- **Support and Feedback Forms**: Where user input is viewed by staff in internal dashboards.
- **Analytic Tracking**: UTM parameters and HTTP headers (like `User-Agent` and `Referer`) that are processed by logging engines.
- **Document Rendering**: Automated systems that generate PDFs (invoices, receipts) from user-provided data.

---
*This explanation is based on the analysis of the `test` file and the research report found in the repository.*
