# Sentinel Security Journal

## 2026-03-29 - EC2 IMDSv2 Token Enforcement and Root EBS Encryption
**Vulnerability:** EC2 instances configured without mandatory IMDSv2 tokens (`http_tokens = "required"`) allow legacy IMDSv1 access, increasing SSRF risk and credential exfiltration vulnerability via IMDS endpoints. Additionally, missing root block device encryption leaves data unencrypted at rest.
**Learning:** Default Terraform `aws_instance` resource definitions do not enforce IMDSv2 or encrypted root volumes unless explicitly specified in `metadata_options` and `root_block_device`.
**Prevention:** Always declare `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` for all EC2 instances across infrastructure code.
