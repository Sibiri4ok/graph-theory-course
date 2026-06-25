#!/usr/bin/env bash
# 3 datasets × 4 algorithms × 5 MPI counts = 60 runs
set -euo pipefail

EXP="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${EXP}/.." && pwd)"
BUILD="${ROOT}/Galois/build"
DATA="${ROOT}/datasets"
RES="${EXP}/results"
STATS="${RES}/stats"
LOG="${RES}/run.log"
HOSTFILE="${RES}/hostfile"

NP_LIST=(1 2 4 6 8)
THREADS=2
RUNS=3
EXEC=Sync
GRAPHS=(web-Google roadNet-PA wiki-talk-temporal)
ALGOS=(bfs pr sssp tc)
TC_GRAPH_wiki_talk=wiki-talk-temporal-clean

MPI_BASE=(mpirun --hostfile "${HOSTFILE}" --oversubscribe --bind-to none)
BFS="${BUILD}/lonestar/analytics/distributed/bfs/bfs-push-dist"
PR="${BUILD}/lonestar/analytics/distributed/pagerank/pagerank-push-dist"
SSSP="${BUILD}/lonestar/analytics/distributed/sssp/sssp-push-dist"
TC="${BUILD}/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist"

if [[ -x "${ROOT}/.venv/bin/python3" ]]; then
  PYTHON="${ROOT}/.venv/bin/python3"
else
  PYTHON=python3
fi

[[ -n "${EXPERIMENT_NP_LIST:-}" ]] && NP_LIST=(${EXPERIMENT_NP_LIST})

log() { echo "[$(date -Iseconds)] $*" | tee -a "${LOG}"; }

build_galois() {
  mkdir -p "${BUILD}"
  [[ -f "${BUILD}/CMakeCache.txt" ]] || \
    cmake -S "${ROOT}/Galois" -B "${BUILD}" -DCMAKE_BUILD_TYPE=Release -DGALOIS_ENABLE_DIST=1
  cmake --build "${BUILD}" --target bfs-push-dist pagerank-push-dist sssp-push-dist triangle-counting-dist -j "$(nproc)"
}

stat_ok() { [[ -s "$1" ]] && grep -q TimerTotal "$1" 2>/dev/null; }

build_cmd() {
  local algo=$1 graph=$2 np=$3
  local stat="${STATS}/${algo}_${graph}_${np}p.stats"
  local gr="${DATA}/${graph}.gr" sgr="${DATA}/${graph}.sgr" tgr="${DATA}/${graph}.tgr"
  local wgr="${DATA}/${graph}-w.gr" wtgr="${DATA}/${graph}-w.tgr"
  local -a sssp_extra=()
  (( np > 1 )) && sssp_extra=(--graphTranspose="${wtgr}")

  case "${algo}" in
    bfs) CMD=("${MPI_BASE[@]}" -np "${np}" "${BFS}" "${sgr}" --symmetricGraph
      -t="${THREADS}" --runs="${RUNS}" -exec="${EXEC}" -startNode=0 -statFile="${stat}") ;;
    pr) CMD=("${MPI_BASE[@]}" -np "${np}" "${PR}" "${gr}" --graphTranspose="${tgr}"
      -t="${THREADS}" --runs="${RUNS}" -maxIterations=50 -tolerance=0.001
      -exec="${EXEC}" -statFile="${stat}") ;;
    sssp) CMD=("${MPI_BASE[@]}" -np "${np}" "${SSSP}" "${wgr}" "${sssp_extra[@]}"
      -t="${THREADS}" --runs="${RUNS}" -startNode=0 -maxIterations=200
      -exec="${EXEC}" -statFile="${stat}") ;;
    tc)
      [[ "${graph}" == wiki-talk-temporal ]] && sgr="${DATA}/${TC_GRAPH_wiki_talk}.sgr"
      CMD=("${MPI_BASE[@]}" -np "${np}" "${TC}" "${sgr}" --symmetricGraph
        -t="${THREADS}" --runs="${RUNS}" -statFile="${stat}") ;;
  esac
}

run_one() {
  local algo=$1 graph=$2 np=$3
  local stat="${STATS}/${algo}_${graph}_${np}p.stats"
  local id="${algo}_${graph}_${np}p"

  stat_ok "${stat}" && { log "SKIP ${id}"; return 0; }

  build_cmd "${algo}" "${graph}" "${np}"
  rm -f "${stat}"
  log "RUN ${id}"
  "${CMD[@]}" >> "${LOG}" 2>&1 && log "OK ${id}" || { log "FAIL ${id}"; return 1; }
}

mkdir -p "${STATS}"
[[ -f "${HOSTFILE}" ]] || echo "$(hostname) slots=8" > "${HOSTFILE}"
build_galois
: > "${LOG}"
log "start NP=${NP_LIST[*]} threads=${THREADS} runs=${RUNS}"

for algo in "${ALGOS[@]}"; do
  for graph in "${GRAPHS[@]}"; do
    for np in "${NP_LIST[@]}"; do
      run_one "${algo}" "${graph}" "${np}" || true
    done
  done
done

log "done"
"${PYTHON}" "${EXP}/plot_algos_by_dataset.py" --report 2>&1 | tee -a "${LOG}"
