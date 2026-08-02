## 2026-07-29 - Divergent Active Branches Reverting Infrastructure Hardening

**Vulnerability:** Key security configurations—including IMDSv2 token enforcement (`metadata_options { http_tokens = "required" }`), root EBS volume encryption (`root_block_device { encrypted = true }`), and secure AWS Lambda runtimes (updating `nodejs14.x` to `nodejs20.x`)—were silently reverted on the active branch due to divergent branch merges and legacy templates, leaving instances and APIs exposed to SSRF and outdated execution environments.

**Learning:** When developing multiple experimental/autonomous branches (such as the WGI Multi-Branch Edge Network and AMNE Codex-Jules), critical security baselines can easily be rolled back if changes are merged back to main or branched from outdated states. Static configuration templates also masked invalid HCL variables (e.g., using `value` instead of `default`).

**Prevention:** Implement programmatic branch-protection rules and mandatory pre-commit / CI checks that automatically run security validators (such as static analysis on `.tf` files) before merging. Ensure that all infrastructure templates explicitly override default AWS behaviors to enforce IMDSv2 and block encryption globally.
