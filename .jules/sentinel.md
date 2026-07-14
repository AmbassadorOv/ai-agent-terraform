# Sentinel Journal - Critical Security Learnings

This journal tracks critical security learnings, vulnerability patterns, and prevention strategies identified during security audits and fixes.

## 2025-05-15 - Enforced EC2 Hardening and Fixed HCL Syntax

**Vulnerability:**
1. Potential for IMDSv1 SSRF attacks on EC2 instances.
2. Unencrypted root volumes on EC2 instances.
3. Invalid HCL syntax in `variables.tf` prevented infrastructure validation and deployment.

**Learning:**
Infrastructure as Code (IaC) files in this repository were using an incorrect `value` keyword in `variable` blocks instead of `default`, and some blocks were missing types/descriptions. Security best practices for EC2 (IMDSv2 and encryption) were missing in the base templates.

**Prevention:**
Always use `http_tokens = "required"` for `metadata_options` to enforce IMDSv2. Ensure `root_block_device` has `encrypted = true`. Use `tofu validate` or `terraform validate` early to catch syntax errors like the `value`/`default` confusion.
