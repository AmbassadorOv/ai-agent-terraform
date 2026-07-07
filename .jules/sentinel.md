## 2025-05-14 - [EC2 Infrastructure Hardening]
**Vulnerability:** EC2 instances were configured with default settings, allowing IMDSv1 (susceptible to SSRF) and lacking root volume encryption.
**Learning:** Default Terraform `aws_instance` resources do not enforce IMDSv2 or root volume encryption, which can lead to insecure-by-default infrastructure if not explicitly hardened.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` in EC2 resource definitions to ensure defense-in-depth and data-at-rest protection.
