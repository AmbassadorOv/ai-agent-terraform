## 2025-05-15 - Enforce IMDSv2 and EBS Encryption

**Vulnerability:** Use of IMDSv1 and unencrypted EBS root volumes in EC2 instances. IMDSv1 is vulnerable to SSRF attacks, and unencrypted volumes risk data exposure if physical media or snapshots are compromised.

**Learning:** Although these are infrastructure-level configurations, failing to explicitly enforce them in Terraform defaults the resources to less secure states in many AWS environments.

**Prevention:** Always include `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` in all `aws_instance` and `aws_launch_template` resources.
