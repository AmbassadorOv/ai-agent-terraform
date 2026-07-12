## 2025-01-24 - EC2 Infrastructure Hardening
**Vulnerability:** EC2 instances were configured without IMDSv2 enforcement and lacked root volume encryption. IMDSv1 is vulnerable to SSRF-based credential theft.
**Learning:** Default Terraform/OpenTofu `aws_instance` resources do not enforce these security features unless explicitly configured. This is a common gap in rapid infrastructure prototyping.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` for all `aws_instance` resources. Use `tofu validate` to ensure these configurations are correctly applied and that associated variables are properly defined.
