## 2025-05-15 - [Infrastructure Hardening: EC2 & Lambda]
**Vulnerability:** Use of IMDSv1 on EC2 (SSRF risk), unencrypted root volumes, and EOL Lambda runtimes (Node.js 14.x).
**Learning:** Legacy infrastructure code often defaults to insecure settings (IMDSv1) or remains pinned to end-of-life runtimes, increasing the attack surface for SSRF and known CVEs.
**Prevention:** Always enforce IMDSv2 (`http_tokens = "required"`) and enable `encrypted = true` on root block devices in Terraform. Regularly audit and upgrade Lambda runtimes to the latest LTS version.
