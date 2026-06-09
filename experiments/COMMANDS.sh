#!/usr/bin/env bash
# Generated: 2026-05-26T15:28:20+03:00 — bash experiments/generate_commands.sh

# bfs_web-Google_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_web-Google_1p.stats 

# bfs_web-Google_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_web-Google_2p.stats 

# bfs_web-Google_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_web-Google_4p.stats 

# bfs_web-Google_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_web-Google_6p.stats 

# bfs_web-Google_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_web-Google_8p.stats 

# pr_web-Google_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_web-Google_1p.stats 

# pr_web-Google_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_web-Google_2p.stats 

# pr_web-Google_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_web-Google_4p.stats 

# pr_web-Google_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_web-Google_6p.stats 

# pr_web-Google_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/web-Google.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_web-Google_8p.stats 

# sssp_web-Google_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/web-Google-w.gr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_web-Google_1p.stats 

# sssp_web-Google_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/web-Google-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_web-Google_2p.stats 

# sssp_web-Google_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/web-Google-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_web-Google_4p.stats 

# sssp_web-Google_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/web-Google-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_web-Google_6p.stats 

# sssp_web-Google_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/web-Google-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/web-Google-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_web-Google_8p.stats 

# tc_web-Google_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_web-Google_1p.stats 

# tc_web-Google_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_web-Google_2p.stats 

# tc_web-Google_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_web-Google_4p.stats 

# tc_web-Google_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_web-Google_6p.stats 

# tc_web-Google_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/web-Google.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_web-Google_8p.stats 

# bfs_roadNet-PA_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_roadNet-PA_1p.stats 

# bfs_roadNet-PA_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_roadNet-PA_2p.stats 

# bfs_roadNet-PA_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_roadNet-PA_4p.stats 

# bfs_roadNet-PA_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_roadNet-PA_6p.stats 

# bfs_roadNet-PA_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_roadNet-PA_8p.stats 

# pr_roadNet-PA_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_roadNet-PA_1p.stats 

# pr_roadNet-PA_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_roadNet-PA_2p.stats 

# pr_roadNet-PA_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_roadNet-PA_4p.stats 

# pr_roadNet-PA_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_roadNet-PA_6p.stats 

# pr_roadNet-PA_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_roadNet-PA_8p.stats 

# sssp_roadNet-PA_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA-w.gr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_roadNet-PA_1p.stats 

# sssp_roadNet-PA_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_roadNet-PA_2p.stats 

# sssp_roadNet-PA_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_roadNet-PA_4p.stats 

# sssp_roadNet-PA_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_roadNet-PA_6p.stats 

# sssp_roadNet-PA_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/roadNet-PA-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_roadNet-PA_8p.stats 

# tc_roadNet-PA_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_roadNet-PA_1p.stats 

# tc_roadNet-PA_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_roadNet-PA_2p.stats 

# tc_roadNet-PA_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_roadNet-PA_4p.stats 

# tc_roadNet-PA_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_roadNet-PA_6p.stats 

# tc_roadNet-PA_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/roadNet-PA.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_roadNet-PA_8p.stats 

# bfs_wiki-talk-temporal_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_wiki-talk-temporal_1p.stats 

# bfs_wiki-talk-temporal_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_wiki-talk-temporal_2p.stats 

# bfs_wiki-talk-temporal_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_wiki-talk-temporal_4p.stats 

# bfs_wiki-talk-temporal_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_wiki-talk-temporal_6p.stats 

# bfs_wiki-talk-temporal_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/bfs/bfs-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.sgr --symmetricGraph -t=2 --runs=3 -exec=Sync -startNode=0 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/bfs_wiki-talk-temporal_8p.stats 

# pr_wiki-talk-temporal_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_wiki-talk-temporal_1p.stats 

# pr_wiki-talk-temporal_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_wiki-talk-temporal_2p.stats 

# pr_wiki-talk-temporal_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_wiki-talk-temporal_4p.stats 

# pr_wiki-talk-temporal_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_wiki-talk-temporal_6p.stats 

# pr_wiki-talk-temporal_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/pagerank/pagerank-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal.tgr -t=2 --runs=3 -maxIterations=50 -tolerance=0.001 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/pr_wiki-talk-temporal_8p.stats 

# sssp_wiki-talk-temporal_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.gr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_wiki-talk-temporal_1p.stats 

# sssp_wiki-talk-temporal_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_wiki-talk-temporal_2p.stats 

# sssp_wiki-talk-temporal_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_wiki-talk-temporal_4p.stats 

# sssp_wiki-talk-temporal_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_wiki-talk-temporal_6p.stats 

# sssp_wiki-talk-temporal_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/sssp/sssp-push-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.gr --graphTranspose=/home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-w.tgr -t=2 --runs=3 -startNode=0 -maxIterations=200 -exec=Sync -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/sssp_wiki-talk-temporal_8p.stats 

# tc_wiki-talk-temporal_1p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 1 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-clean.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_wiki-talk-temporal_1p.stats 

# tc_wiki-talk-temporal_2p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 2 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-clean.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_wiki-talk-temporal_2p.stats 

# tc_wiki-talk-temporal_4p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 4 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-clean.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_wiki-talk-temporal_4p.stats 

# tc_wiki-talk-temporal_6p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 6 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-clean.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_wiki-talk-temporal_6p.stats 

# tc_wiki-talk-temporal_8p
mpirun --hostfile /home/danil/graph-theory-task-2/experiments/hostfile --oversubscribe --bind-to none -np 8 /home/danil/graph-theory-task-2/Galois/build/lonestar/analytics/distributed/triangle-counting/triangle-counting-dist /home/danil/graph-theory-task-2/datasets/wiki-talk-temporal-clean.sgr --symmetricGraph -t=2 --runs=3 -statFile=/home/danil/graph-theory-task-2/experiments/results/stats/tc_wiki-talk-temporal_8p.stats 

