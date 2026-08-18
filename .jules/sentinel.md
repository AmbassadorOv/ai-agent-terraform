# Sentinel Security Journal

## 2025-05-18 - EC2 IMDSv2 Token Enforcement and Storage Block Device Encryption

**Vulnerability:**
EC2 instance configurations in `environments/swarms-aws-agent-api/dev/us-east-1/components/machine_image/main.tf` allowed legacy IMDSv1 access (`http_tokens` omitted) and had unencrypted root block storage devices.

**Learning:**
Absence of explicit `metadata_options` leaves EC2 instances vulnerable to SSRF-based IAM credential theft via IMDSv1, and missing `root_block_device.encrypted` configuration exposes sensitive state data at rest.

**Prevention:**
Enforce mandatory IMDSv2 tokens (`http_tokens = "required"`) and explicitly set `encrypted = true` in `root_block_device` across all AWS EC2 instance definitions in Terraform templates.
