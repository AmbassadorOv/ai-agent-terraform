## 2025-08-13 - IMDSv2 and EBS Encryption Enforcement for EC2

**Vulnerability:** EC2 instances configured without mandatory IMDSv2 (metadata options http_tokens = "required") and lacking encrypted EBS root block devices are highly vulnerable to Server-Side Request Forgery (SSRF) data extraction and data-at-rest exposure.

**Learning:** Default Terraform and Packer configurations for EC2 instances allow IMDSv1 by default, which does not require a bearer token and is prone to SSRF attacks. Additionally, unless explicitly enabled, root block storage volumes are not encrypted by default on some standard AMIs.

**Prevention:** Always explicitly define `metadata_options` requiring HTTP tokens for IMDSv2 on all `aws_instance` resources, and enforce `root_block_device` with `encrypted = true` in infrastructure configurations. Use an automated pre-commit linting or compliance tool to block the deployment of non-compliant infrastructure.
