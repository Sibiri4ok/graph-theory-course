#!/usr/bin/env bash
# MPI scaling: 3 datasets × 4 algorithms × 5 process counts (60 runs).
set -euo pipefail

# shellcheck source=config.sh
source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

[[ -n "${EXPERIMENT_NP_LIST:-}" ]] && NP_LIST=(${EXPERIMENT_NP_LIST})

log() { echo "[$(date -Iseconds)] $*" | tee -a "${LOG}"; }

stat_ok() {
  local f="$1"
  [[ -s "$f" ]] && grep -q 'TimerTotal' "$f" 2>/dev/null
}

build_cmd() {
  local algo=$1 graph=$2 np=$3
  local stat="${STATS}/${algo}_${graph}_${np}p.stats"
  local gr="${DATA}/${graph}.gr"
  local sgr="${DATA}/${graph}.sgr"
  local tgr="${DATA}/${graph}.tgr"
  local wgr="${DATA}/${graph}-w.gr"
  local wtgr="${DATA}/${graph}-w.tgr"

  case "${algo}" in
    bfs)
      CMD=("${MPI_BASE[@]}" -np "${np}" "${BFS}" "${sgr}" --symmetricGraph
        -t="${THREADS}" --runs="${RUNS}" -exec="${EXEC}" -startNode=0 -statFile="${stat}")
      ;;
    pr)
      CMD=("${MPI_BASE[@]}" -np "${np}" "${PR}" "${gr}" --graphTranspose="${tgr}"
        -t="${THREADS}" --runs="${RUNS}" -maxIterations=50 -tolerance=0.001
        -exec="${EXEC}" -statFile="${stat}")
      ;;
    sssp)
      if (( np > 1 )); then
        CMD=("${MPI_BASE[@]}" -np "${np}" "${SSSP}" "${wgr}" --graphTranspose="${wtgr}"
          -t="${THREADS}" --runs="${RUNS}" -startNode=0 -maxIterations=200
          -exec="${EXEC}" -statFile="${stat}")
      else
        CMD=("${MPI_BASE[@]}" -np "${np}" "${SSSP}" "${wgr}" -t="${THREADS}"
          --runs="${RUNS}" -startNode=0 -maxIterations=200 -exec="${EXEC}"
          -statFile="${stat}")
      fi
      ;;
    tc)
      local tc_sgr="${sgr}"
      [[ "${graph}" == wiki-talk-temporal ]] && tc_sgr="${DATA}/${TC_GRAPH_wiki_talk}.sgr"
      CMD=("${MPI_BASE[@]}" -np "${np}" "${TC}" "${tc_sgr}" --symmetricGraph
        -t="${THREADS}" --runs="${RUNS}" -statFile="${stat}")
      ;;
    *)
      echo "Unknown algo: ${algo}" >&2
      return 1
      ;;
  esac
}

run_one() {
  local algo=$1 graph=$2 np=$3
  local id="${algo}_${graph}_${np}p"
  local stat="${STATS}/${id}.stats"
  local cmd_file="${RES}/cmds/${id}.sh"

  build_cmd "${algo}" "${graph}" "${np}"
  local -a cmd=("${CMD[@]}")

  mkdir -p "${RES}/cmds"
  printf '%q ' "${cmd[@]}" > "${cmd_file}"
  echo >> "${cmd_file}"
  {
    echo "# ${id}"
    printf '%q ' "${cmd[@]}"
    echo
    echo
  } >> "${COMMANDS}"

  if [[ -n "${EXPERIMENT_DRY_RUN:-}" ]]; then
    return 0
  fi

  if stat_ok "${stat}"; then
    log "SKIP ${id} (valid stats exist)"
    return 0
  fi
  rm -f "${stat}"

  log "RUN ${id}"
  if "${cmd[@]}" >> "${LOG}" 2>&1; then
    log "OK ${id}"
  else
    log "FAIL ${id}"
    return 1
  fi
}

main() {
  mkdir -p "${STATS}" "${RES}/cmds"

  if [[ -n "${EXPERIMENT_DRY_RUN:-}" ]]; then
    {
      echo "#!/usr/bin/env bash"
      echo "# Generated: $(date -Iseconds) — bash experiments/generate_commands.sh"
      echo ""
    } > "${COMMANDS}"
  elif [[ -z "${EXPERIMENT_SKIP_INIT:-}" ]]; then
    : > "${COMMANDS}"
    : > "${LOG}"
  fi

  if [[ -z "${EXPERIMENT_DRY_RUN:-}" ]]; then
    log "Experiment start: NP=${NP_LIST[*]} threads=${THREADS} runs=${RUNS}"
  fi

  for graph in "${GRAPHS[@]}"; do
    for algo in "${ALGOS[@]}"; do
      for np in "${NP_LIST[@]}"; do
        run_one "${algo}" "${graph}" "${np}" || true
      done
    done
  done

  if [[ -n "${EXPERIMENT_DRY_RUN:-}" ]]; then
    chmod +x "${COMMANDS}"
    echo "Wrote ${COMMANDS}"
    return 0
  fi

  log "Experiment finished. Stats: ${STATS}"
  python3 "${ROOT}/experiments/build_report.py" 2>&1 | tee -a "${LOG}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]] || [[ -n "${EXPERIMENT_FORCE_RUN:-}" ]]; then
  main "$@"
fi
