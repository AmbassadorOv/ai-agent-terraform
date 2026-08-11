# Sentinel Security Journal

## 2026-08-11 - Enforce IMDSv2 and Enable EBS Root Volume Encryption
**Vulnerability:** The test EC2 instance (`fastapi_server_test_instance`) was configured without enforced Instance Metadata Service Version 2 (IMDSv2) tokens and without encryption on the root storage volume. This exposed the instance to potential SSRF (Server-Side Request Forgery) attacks where metadata could be retrieved without authentication tokens, and left the root storage block unencrypted.
**Learning:** Default EC2 configurations in Terraform do not enforce IMDSv2 or root block device encryption automatically. Without explicit resource hardening blocks (`metadata_options` and `root_block_device`), resources remain in a legacy, insecure default state.
**Prevention:** Always explicitly define `metadata_options` with `http_tokens = "required"` and configure `root_block_device` with `encrypted = true` on all EC2 instance resources.
