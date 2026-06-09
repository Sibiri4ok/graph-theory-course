#!/usr/bin/env bash
# Re-run only MPI=2 jobs (e.g. after fixing hostfile or deleting bad *.stats).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export EXPERIMENT_SKIP_INIT=1
export EXPERIMENT_NP_LIST="2"
export EXPERIMENT_FORCE_RUN=1

for g in web-Google roadNet-PA wiki-talk-temporal; do
  for a in bfs pr sssp tc; do
    rm -f "${ROOT}/experiments/results/stats/${a}_${g}_2p.stats"
  done
done

# shellcheck source=run_all.sh
source "${ROOT}/experiments/run_all.sh"
