## 2025-07-25 - Secure AWS EC2 Instance Enforcements
**Vulnerability:** Legacy or untagged AWS EC2 instance definitions (like `fastapi_server_test_instance`) lacked IMDSv2 requirements (`metadata_options { http_tokens = "required" }`) and lacked root block device encryption blocks (`root_block_device { encrypted = true }`), exposing the metadata service to SSRF exploits and storage to data leaks.
**Learning:** Development test instances are often omitted from security validation rules, but they form a high-exposure vector in local development sandboxes.
**Prevention:** Enforce mandatory OpenTofu/Terraform infrastructure security checks to verify all `aws_instance` blocks explicitly declare IMDSv2 token enforcement and root volume block device encryption.
