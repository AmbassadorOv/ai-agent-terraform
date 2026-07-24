## 2026-07-24 - EC2 Metadata Service v1 (IMDSv1) and Unencrypted EBS Root Volumes

**Vulnerability:** Missing enforcement of IMDSv2 and lack of root block device encryption on the test EC2 instance resource `fastapi_server_test_instance`. Additionally, invalid syntax was found in `variables.tf`.

**Learning:** Deploying EC2 instances without explicitly requiring IMDSv2 allows fallback to IMDSv1, exposing instance metadata to SSRF (Server-Side Request Forgery) attacks. Similarly, unencrypted root volumes can expose sensitive application or OS data at rest if the underlying storage media is accessed.

**Prevention:** Always include `metadata_options { http_tokens = "required" }` to enforce IMDSv2 and a `root_block_device { encrypted = true }` block on all `aws_instance` resources. Enforce this via static analysis checks or custom scan tools before deployment.
