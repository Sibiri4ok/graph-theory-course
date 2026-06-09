#!/usr/bin/env bash
# Regenerate experiments/COMMANDS.sh without running benchmarks.
set -euo pipefail
export EXPERIMENT_DRY_RUN=1
exec bash "$(dirname "${BASH_SOURCE[0]}")/run_all.sh"
