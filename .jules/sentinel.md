# Sentinel Security Journal

This journal records critical security learnings, vulnerability patterns specific to the codebase, and constraints/patterns to avoid regressions.

## 2025-03-05 - Enforcing Local and Cloud Secure Default States

**Vulnerability:**
EC2 resources (such as standard VM configurations or testing instances) defined in development environments may lack default-secure attributes, leaving metadata services exposed to SSRF/Credential theft via IMDSv1, or root storage unencrypted.

**Learning:**
Enforcing IMDSv2 (`http_tokens = "required"`) and root block device encryption (`encrypted = true`) in the Terraform resource configuration is necessary to maintain security hygiene, even on test instances. Additionally, variable schemas in components must strictly use the standard HCL syntax (`default` keyword instead of non-standard `value` parameter) to pass validation/syntax checks in CI/CD pipelines.

**Prevention:**
Enforce pre-commit or automated check suites running `terraform fmt` and `terraform validate` across all module directories, and review any newly added `aws_instance` configurations to ensure IMDSv2 tokens are mandatory and storage is encrypted by default.
