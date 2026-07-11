## 2026-07-11 - Enforce IMDSv2 and EBS Encryption for EC2

**Vulnerability:** EC2 instances were configured with default settings, potentially allowing access to sensitive metadata via IMDSv1 and lacking data-at-rest encryption for the root volume. IMDSv1 is vulnerable to SSRF attacks where an attacker can retrieve IAM role credentials.

**Learning:** Terraform/OpenTofu resources for `aws_instance` do not enforce IMDSv2 or EBS encryption by default. Explicit configuration is required to meet modern security standards.

**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` when defining EC2 instances to ensure defense-in-depth and data protection.
