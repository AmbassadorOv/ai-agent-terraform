# Sentinel Journal

## 2025-05-22 - [Enforce IMDSv2 and Encryption on EC2]
**Vulnerability:** EC2 instances were being created with default metadata options (allowing IMDSv1) and unencrypted root volumes. IMDSv1 is vulnerable to SSRF-based credential theft. Unencrypted volumes risk data exposure if the physical media is compromised or through unauthorized snapshot access.
**Learning:** Default Terraform `aws_instance` resources do not enforce the latest security standards for metadata services or volume encryption.
**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` in EC2 resource definitions.
