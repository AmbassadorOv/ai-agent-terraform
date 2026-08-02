## 2026-07-08 - [EC2 Security Hardening & OpenTofu Alignment]
**Vulnerability:** EC2 instances were potentially vulnerable to SSRF via IMDSv1 and lacked data-at-rest encryption for root volumes.
**Learning:** The project uses OpenTofu (not Terraform) and expects a specific provider registry (`registry.opentofu.org`). Using standard `terraform` tools can unintentionally update lock files with `registry.terraform.io`, causing functional drift.
**Prevention:** Always check `.terraform.lock.hcl` to identify if OpenTofu or Terraform is being used. Enforce IMDSv2 and block device encryption as a standard for all `aws_instance` resources.
