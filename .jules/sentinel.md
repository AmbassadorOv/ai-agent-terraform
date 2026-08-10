## 2025-01-26 - EC2 IMDSv2 Token Enforcement and Root Block Storage Encryption
**Vulnerability:** Default Terraform aws_instance configurations allow unauthenticated access to the Instance Metadata Service (IMDSv1) and leave the root block storage devices unencrypted. This presents serious risks:
1. SSRF (Server-Side Request Forgery) attacks can be leveraged to query the IMDS endpoint and extract sensitive IAM node instance profiles and AWS credentials.
2. Unencrypted block storage volumes pose a data exposure risk at rest if the physical storage media is compromised or improperly handled.

**Learning:** When developing Terraform/OpenTofu configurations, default settings for `aws_instance` resources prioritize backwards compatibility and ease of deployment over security. To mitigate these risks, secure defaults must be explicitly declared and enforced at the infrastructure-as-code layer.

**Prevention:** Always declare secure defaults within `aws_instance` blocks:
1. Include `metadata_options { http_endpoint = "enabled"; http_tokens = "required" }` to enforce IMDSv2 token validation.
2. Include a `root_block_device { encrypted = true }` block to ensure all data stored on the root volume is encrypted at rest.
