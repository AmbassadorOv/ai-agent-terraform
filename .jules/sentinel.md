## 2026-07-01 - [Infrastructure Hardening for EC2 Templates]
**Vulnerability:** Default EC2 configurations often lack IMDSv2 enforcement and volume encryption, increasing risk of credential theft via SSRF and data exposure.
**Learning:** IaC templates provide a central place to enforce security best practices before resources are even created.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` in EC2 resource definitions.
