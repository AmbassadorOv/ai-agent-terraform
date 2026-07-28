## 2025-07-28 - Enforce IMDSv2 and Root EBS Encryption for EC2 Instances
**Vulnerability:** The EC2 instances configured in the Terraform codebase were deployed with default metadata options, enabling IMDSv1 by default and leaving instance credentials vulnerable to Server-Side Request Forgery (SSRF). Additionally, root storage volumes were unencrypted, violating secure defaults.
**Learning:** Legacy configurations and standard Terraform code templates often lack explicit secure metadata and encryption blocks, failing to implement "Defense in Depth" by default.
**Prevention:** Enforce mandatory IMDSv2 (`http_tokens = "required"`) and enable root block device encryption (`encrypted = true`) for all EC2 resources.
