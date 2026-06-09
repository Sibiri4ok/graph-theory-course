# Shared experiment settings (sourced by run_all.sh).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="${ROOT}/Galois/build"
DATA="${ROOT}/datasets"
RES="${ROOT}/experiments/results"
STATS="${RES}/stats"
LOG="${RES}/run.log"
COMMANDS="${ROOT}/experiments/COMMANDS.sh"
HOSTFILE="${ROOT}/experiments/hostfile"

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
