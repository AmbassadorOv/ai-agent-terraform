## 2024-07-30 - Enforcing EC2 IMDSv2 and Volume Encryption in Terraform

**Vulnerability:**
The `aws_instance` resource in `environments/swarms-aws-agent-api/dev/us-east-1/components/machine_image/main.tf` was defined without specifying `metadata_options` (making IMDSv1 available by default) and without enabling root block device encryption. This exposes the instance to potential SSRF-based metadata leakage (where attackers can extract sensitive credentials or IAM role tokens) and physical media compromise.

**Learning:**
Infrastructure configurations created iteratively or bootstrapped via templates often overlook the security posture of low-level virtualization features (such as instance metadata service versioning and block storage encryption) in favor of functional simplicity.

**Prevention:**
Integrate static analysis (e.g., Checkov, Tfsec, or OpenTofu validate) into CI pipelines and systematically declare secure defaults (`http_tokens = "required"` and `encrypted = true` for root volumes) during initial resource scaffolding.
