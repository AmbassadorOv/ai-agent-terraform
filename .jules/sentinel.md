# Sentinel's Journal - Critical Security Learnings

## 2025-01-24 - Infrastructure Hardening for EC2 Instances
**Vulnerability:** EC2 instances were configured without IMDSv2 enforcement and without root volume encryption. IMDSv1 is vulnerable to SSRF attacks that can leak IAM role credentials. Unencrypted volumes pose a data-at-rest security risk.
**Learning:** The project uses OpenTofu for infrastructure. Some components (like `machine_image`) lacked standard security hardening in their Terraform configurations.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` in `aws_instance` and `aws_launch_template` resources.
