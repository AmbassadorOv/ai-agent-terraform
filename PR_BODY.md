Title: feat(telemetry): add Jules Telemetry Auditor and CI canary

Summary:
Add infra/telemetry/jules_audit.py with CI dry-run, sample data, k8s canary CronJob, RBAC and tests.
This enables controlled detection, dedupe and planned remediation actions for logical bugs.

What changed:
- infra/telemetry/jules_audit.py
- infra/telemetry/requirements.txt
- infra/telemetry/README.md
- infra/telemetry/sample_telemetry.csv
- infra/telemetry/config/jules-audit-configmap.yaml
- infra/telemetry/k8s/jules-audit-cronjob.yaml
- infra/telemetry/rbac/jules-audit-sa.yaml
- infra/telemetry/tests/test_jules_audit_basic.py
- .github/workflows/telemetry-audit.yml

Testing:
- CI runs dry-run on sample data
- Local test provided in infra/telemetry/tests

Deployment plan:
1. Merge to branch and run CI
2. Deploy ConfigMap and ServiceAccount to infra namespace
3. Mount repo to /opt/jules in canary nodes and run CronJob in canary mode for 48-72 hours
4. Review planned_actions artifacts and run simulation
5. Only after SRE approval enable non-dry-run and expand rollout

Safety:
- Auto-remediate is dry-run by default
- Destructive ops require manual SRE approval
- Backups created when --backup flag used
