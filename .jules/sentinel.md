## 2025-05-15 - [Hardening EC2 and Fixing HCL Syntax]
**Vulnerability:** EC2 instances were configured with default metadata options (allowing IMDSv1) and unencrypted root volumes. Additionally, the Terraform configuration had invalid HCL syntax in variable definitions.
**Learning:** Legacy or "test" configurations often neglect modern security standards like IMDSv2 and at-rest encryption. IMDSv1 is vulnerable to SSRF attacks that can leak IAM role credentials.
**Prevention:** Always enforce IMDSv2 (http_tokens = "required") and enable encryption for all block devices. Use 'tofu validate' to catch HCL syntax errors early in the development cycle.
