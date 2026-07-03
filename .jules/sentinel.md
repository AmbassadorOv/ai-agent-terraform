## 2025-05-15 - Enforce IMDSv2 and EBS Encryption
**Vulnerability:** EC2 instances were configured with default metadata options, allowing IMDSv1. This could be exploited via SSRF to steal IAM role credentials. Additionally, root volumes were not encrypted by default.
**Learning:** The initial Terraform templates focused on functionality (FastAPI server setup) but lacked foundational security hardening for AWS resources.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` for EC2 instances and ensure `root_block_device { encrypted = true }` is set in Terraform configurations.
