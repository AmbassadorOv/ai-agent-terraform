# Sentinel Security Journal

## 2025-07-17 - Enforce IMDSv2 and Root Encryption on EC2 instances
**Vulnerability:** Insecure default EC2 configurations allowing potentially insecure metadata access (IMDSv1 instead of IMDSv2) and unencrypted root EBS volumes. Additionally, incorrect variable syntax in AWS components can break infrastructure validation.
**Learning:** Legacy configurations or scaffolding configurations in development directories can easily omit critical hardening options like IMDSv2 enforcement (`http_tokens = "required"`) and root block storage encryption (`encrypted = true`).
**Prevention:** Enforce strict terraform linting and use Sentinel policies or security checks (like Tfsec or Clustered Terraform checks) to automatically fail deployment if an EC2 instance lacks enforced IMDSv2 and encrypted root block devices. Ensure variables use the correct `default` keyword rather than `value`.
