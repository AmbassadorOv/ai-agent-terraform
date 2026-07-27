## 2025-02-17 - EC2 IMDSv2 Enforcement and Root Block Encryption
**Vulnerability:** Insecure default EC2 instance configurations lacking IMDSv2 token requirements and unencrypted root block storage devices.
**Learning:** Cloud templates or initial configurations can revert to legacy defaults (such as IMDSv1 or unencrypted root block volumes) if not explicitly secured with explicit HCL blocks (`metadata_options` and `root_block_device`).
**Prevention:** Always define explicit `metadata_options { http_tokens = "required" }` and `root_block_device { encrypted = true }` within all `aws_instance` Terraform resources.
