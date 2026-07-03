#!/usr/bin/env bash
set -euo pipefail
CONFIG=${CONFIG:-configs/amne_config.json}
LOGDIR=${LOGDIR:-/app/outputs}
mkdir -p "$LOGDIR"
echo "Starting simulation at $(date)" > "$LOGDIR/run.log"
python orchestrator/amne_experiments_orchestrator.py --config "$CONFIG" 2>&1 | tee -a "$LOGDIR/run.log"
echo "Finished at $(date)" >> "$LOGDIR/run.log"
