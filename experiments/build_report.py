#!/usr/bin/env python3
"""Build REPORT.md from experiments/results/stats/*.stats (does not overwrite report.csv)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from parse_galois_stat import parse_stat_file  # noqa: E402
from parse_run_log import parse_run_log  # noqa: E402

STATS_DIR = ROOT / "experiments" / "results" / "stats"
REPORT_MD = ROOT / "experiments" / "REPORT.md"
REPORT_CSV = ROOT / "experiments" / "report.csv"

ALGO_LABEL = {"bfs": "BFS", "pr": "PageRank", "sssp": "SSSP", "tc": "Triangle Counting"}
ALGO_PRIMARY = {
    "BFS": "compute_time",
    "PageRank": "compute_time",
    "SSSP": "compute_time",
    "Triangle Counting": "total_time_exec",
}
SUMMARY_COLS = (
    ("primary", "primary_metric_value"),
    ("total", "total_time"),
    ("t_exec", "total_time_exec"),
    ("gct", "graph_construct_time"),
    ("inspect_b", "inspect_bytes"),
    ("load_b", "load_bytes"),
    ("sync_b", "sync_bytes"),
    ("repl_n", "replication_nodes"),
)

EXPECTED = [
    (algo, graph, np)
    for algo in ("bfs", "pr", "sssp", "tc")
    for graph in ("web-Google", "roadNet-PA", "wiki-talk-temporal")
    for np in (1, 2, 4, 6, 8)
]


def parse_id(name: str):
    for algo in ("bfs", "pr", "sssp", "tc"):
        prefix = f"{algo}_"
        if name.startswith(prefix):
            rest = name[len(prefix) :]
            if rest.endswith("p"):
                graph, np_s = rest.rsplit("_", 1)
                return algo, graph, int(np_s[:-1])
            break
    return None, None, None


def merge_log_bytes(run_id: str, m: dict, log_index: dict) -> None:
    if run_id not in log_index:
        return
    for key in ("inspect_bytes", "load_bytes"):
        if m.get(key) == "" and log_index[run_id].get(key) != "":
            m[key] = log_index[run_id][key]


def enrich_replication(m: dict) -> None:
    if m.get("replication_nodes") == "" and m.get("replication_factor") != "":
        m["replication_nodes"] = m["replication_factor"]


def collect_rows():
    log_index = parse_run_log()
    rows = []
    seen = set()

    for path in sorted(STATS_DIR.glob("*.stats")):
        if path.stem.startswith("_"):
            continue
        algo, dataset, np = parse_id(path.stem)
        if algo is None:
            continue
        seen.add((algo, dataset, np))
        try:
            m = parse_stat_file(path)
            merge_log_bytes(path.stem, m, log_index)
            enrich_replication(m)
            status = "ok"
        except Exception as e:
            m = {}
            status = f"parse_error: {e}"
        rows.append((algo, dataset, np, m, status))

    for algo, dataset, np in EXPECTED:
        if (algo, dataset, np) in seen:
            continue
        rows.append((algo, dataset, np, {}, "missing"))

    rows.sort(key=lambda r: (ALGO_LABEL.get(r[0], r[0]), r[1], r[2]))
    return rows


def write_report_md(rows):
    lines = [
        "# Эксперимент: масштабирование MPI (Galois distributed)",
        "",
        "Параметры: `-t=2`, `--runs=3`, `-exec=Sync` (TC без `-exec`), MPI: 1, 2, 4, 6, 8.",
        "`mpirun --hostfile experiments/hostfile --oversubscribe --bind-to none`",
        "",
        "Полные метрики: [report.csv](report.csv), описание полей: [METRICS_GUIDE.md](METRICS_GUIDE.md).",
        "",
    ]

    for algo_key in ("bfs", "pr", "sssp", "tc"):
        algo_name = ALGO_LABEL[algo_key]
        sub = [r for r in rows if r[0] == algo_key]
        if not sub:
            continue
        pk = ALGO_PRIMARY[algo_name]
        header = "| dataset | MPI | " + " | ".join(lbl for lbl, _ in SUMMARY_COLS) + " | status |"
        sep = "|" + "|".join(["---"] * (2 + len(SUMMARY_COLS) + 1)) + "|"
        lines.extend([f"## {algo_name}", "", header, sep])
        for _algo, dataset, np, m, status in sub:
            vals = []
            for _lbl, key in SUMMARY_COLS:
                metric_key = pk if key == "primary_metric_value" else key
                vals.append(str(m.get(metric_key, "")))
            lines.append(f"| {dataset} | {np} | " + " | ".join(vals) + f" | {status} |")
        lines.append("")

    REPORT_MD.write_text("\n".join(lines))


def main():
    rows = collect_rows()
    write_report_md(rows)
    ok = sum(1 for r in rows if r[4] == "ok")
    print(f"Wrote {REPORT_MD} ({ok}/{len(rows)} runs with valid stats)")
    if REPORT_CSV.exists():
        print(f"Left unchanged: {REPORT_CSV}")


if __name__ == "__main__":
    main()
