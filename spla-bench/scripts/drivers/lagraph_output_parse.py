"""
Индексы токенов в строках вывода демо LAGraph (разделитель — пробелы).

Форматы заданы исходниками в deps/lagraph/src/benchmark/*.c; при смене версии LAGraph
проверьте соответствие строкам printf.
"""

# bfs_demo: строки вида "parent only ... <sec>"
BFS_TRIAL_LINE_PREFIX = "parent only"
BFS_TRIAL_TIME_TOKEN = 9
BFS_WARMUP_LINE_PREFIX = "warmup"
BFS_WARMUP_TIME_TOKEN = 4

# sssp_demo: строки вида "sssp ... <sec>"
SSSP_TRIAL_LINE_PREFIX = "sssp"
SSSP_TRIAL_TIME_TOKEN = 8

# tc_demo
TC_TRIAL_LINE_PREFIX = "trial "
TC_TRIAL_TIME_TOKEN = 2
TC_WARMUP_LINE_PREFIX = "nthreads: "
TC_WARMUP_TIME_TOKEN = 3

# gappagerank_demo: "trial: <n> time: <sec>"
PR_TRIAL_LINE_PREFIX = "trial:"
PR_TRIAL_TIME_TOKEN = 3
