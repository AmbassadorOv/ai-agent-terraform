# AI-Agent-Terraform — PR Architecture Triage

Date: 2026-09-19

## Canonical disposition

This repository is a deployment/fork workspace and historical experiment source. Current WANGA-LAB architecture is the canonical research/control-plane source.

| PR family | Disposition | Reason |
|---|---|---|
| #86 | MERGED | Canonical frontend reverse-tabnabbing fix |
| Sentinel tabnabbing / IMDS / EBS series | SUPERSEDED | Repeated fixes for the same findings; current main already contains the required infrastructure hardening |
| #17 | SUPERSEDED | Node.js 14 no longer present in main; fix already reflected |
| #82 | ARCHIVE / NOT MERGED | Forensic scanner is useful as a research idea but is too broad for this deployment fork: shell-based execution, full repository cloning, local workspace mutation, and uncalibrated High confidence output. Equivalent forensic capability belongs in WANGA-LAB evidence infrastructure. |
| #13 | SUPERSEDED | Research infrastructure is represented by current WANGA-LAB control-plane/work-manager architecture |
| #1 / #2 / #3 / #14 | HISTORICAL EXPERIMENT | Dashboard / visualization / neuromorphic UI material; retained in Git history, not part of canonical control plane |
| #4 | HISTORICAL DEPLOYMENT | Terraform FastAPI deployment experiment; retain as fork-specific infrastructure source |
| #5 / #6 / #7 / #8 / #9 / #11 | HISTORICAL ARK / LOGIC EXPERIMENTS | Preserve source material; not merged into the current canonical WANGA architecture without a separate migration specification |
| #33 / #34 / #35 | HISTORICAL EXPERIMENTS | Sandbox, P2P simulator, and protocol-bridge experiments; isolated from canonical architecture |

## Security boundary

The repository does not claim that a merged PR is a verified scientific result. Security changes are merged only after the affected main state is inspected.

## Architecture placement

- Deployment fork / infrastructure: ai-agent-terraform
- Canonical systems architecture: WANGA-LAB
- AI Drift Forensics / evidence: WANGA-LAB
- Research identity / public archive: AmbassadorOv
- Experimental ARK material: preserved as historical source

## Rule

One responsibility → one canonical owner → explicit interface → evidence status → verification gate.
