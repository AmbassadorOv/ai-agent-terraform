import subprocess
import json
import os

def test_dry_run_sample():
    # Ensure we are in the root directory for the test
    cmd = ["python3", "infra/telemetry/jules_audit.py", "--input", "infra/telemetry/sample_telemetry.csv", "--dry-run"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    out = json.loads(res.stdout.strip())
    assert out['total_unique'] >= 1
