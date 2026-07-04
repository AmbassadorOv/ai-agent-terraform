## 2025-07-04 - [EC2 Security Baseline]
**Vulnerability:** EC2 instances were deployed without IMDSv2 enforcement and without root volume encryption.
**Learning:** Even when security guidelines are documented in memory, initial implementations may omit critical security configurations like `metadata_options` and `root_block_device` encryption.
**Prevention:** Use Terraform modules or provider-level overrides to enforce IMDSv2 and encryption by default. Always include a security review step for new infrastructure components.
