## 2024-07-20 - Enforcing IMDSv2 and EBS Root Encryption on EC2

**Vulnerability:**
EC2 instances running IMDSv1 are vulnerable to Server-Side Request Forgery (SSRF) attacks, allowing an attacker who exploits an SSRF flaw to retrieve IAM role credentials and sensitive metadata. Additionally, unencrypted EBS root block devices can lead to data exposure if underlying disk images or snapshots are compromised.

**Learning:**
Default cloud provider configurations in Terraform / OpenTofu templates often omit strict security parameters (such as enforcing IMDSv2 and explicitly encrypting block storage), leaving infrastructure exposed out-of-the-box. Consistent validation policies and custom linting rules are needed to catch these omissions.

**Prevention:**
Always configure `metadata_options { http_tokens = "required" }` on `aws_instance` resources to enforce IMDSv2. Additionally, explicitly configure the `root_block_device { encrypted = true }` block on all instance definitions to ensure encryption-at-rest.
