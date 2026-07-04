## 2026-07-04 - [Security Hardening] Infrastructure as Code (Terraform)
**Vulnerability:** Weak default security posture for EC2 instances (IMDSv1 enabled, unencrypted root volumes).
**Learning:** Default Terraform `aws_instance` resources do not enforce IMDSv2 or root volume encryption, leaving instances vulnerable to SSRF-based credential theft and data-at-rest exposure.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` in EC2 resource definitions.
