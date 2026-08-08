## 2026-06-30 - EC2 Instance IMDSv2 and Root Storage Volume Block Encryption

**Vulnerability:** Default configurations of EC2 instances allow unrestricted access to Instance Metadata Service version 1 (IMDSv1), which is susceptible to credential theft via Server-Side Request Forgery (SSRF) attacks, and unencrypted root storage volumes, leaving data vulnerable to unauthorized offline reading and snapshot tampering.

**Learning:** Legacy and template Terraform configurations often prioritize backward compatibility or initial deployment simplicity over modern, zero-trust cloud security practices, leading to unhardened default instances.

**Prevention:** Enforce IMDSv2 (http_tokens = "required") and enable root_block_device encryption (encrypted = true) as mandatory security compliance controls for all EC2 resources in our Terraform codebase.
