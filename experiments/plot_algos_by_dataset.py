#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
STATS_DIR = EXP / "results" / "stats"
REPORT_CSV = EXP / "results" / "report.csv"
LOG = EXP / "results" / "run.log"

ALGO_LABEL = {"bfs": "BFS", "pr": "PageRank", "sssp": "SSSP", "tc": "Triangle Counting"}
ALGO_PRIMARY = {
    "BFS": "compute_time",
    "PageRank": "compute_time",
    "SSSP": "compute_time",
    "Triangle Counting": "total_time_exec",
}
EXPECTED = [
    (algo, graph, np)
    for algo in ("bfs", "pr", "sssp", "tc")
    for graph in ("web-Google", "roadNet-PA", "wiki-talk-temporal")
    for np in (1, 2, 4, 6, 8)
]
CSV_COLUMNS = [
    "algorithm", "dataset", "mpi_processes", "threads", "runs",
    "primary_metric", "primary_metric_value", "status",
    "total_time", "total_time_exec", "compute_time", "sync_time", "barrier_time",
    "sync_bytes", "graph_construct_time", "replication_factor", "comm_mem_max",
    "comm_mem_min", "inspect_bytes", "load_bytes", "load_messages", "peak_load_bytes",
    "replication_nodes", "replication_edges", "total_node_proxies", "total_edge_proxies",
    "edge_inspection_time", "edge_loading_time",
]
METRIC_KEYS = CSV_COLUMNS[8:]

DATASETS = [
    ("roadNet-PA", "Road network — Pennsylvania"),
    ("web-Google", "Web graph — Google"),
    ("wiki-talk-temporal", "Wikipedia talk (temporal)"),
]
ALGORITHMS = [
    ("BFS", "BFS", "bfs"),
    ("SSSP", "SSSP", "sssp"),
    ("PageRank", "PageRank", "pr"),
    ("Triangle Counting", "Triangle Counting", "tc"),
]
PANEL_DEFAULT = [
    ("total_time_exec", "Total time", "ms", True),
    ("sync_time", "Synchronization time", "ms", False),
    ("sync_bytes", "Sync traffic", "bytes", True),
    ("replication_factor", "Replication factor", "", False),
]
PANEL_TC = [
    ("total_time_exec", "Total time", "ms", True),
    ("inspect_bytes", "Inspect bytes", "bytes", True),
    ("load_bytes", "Load bytes", "bytes", True),
]
MPI_TICKS = [1, 2, 4, 6, 8]
ACCENT = {"roadNet-PA": "#2563eb", "web-Google": "#ea580c", "wiki-talk-temporal": "#16a34a"}


def parse_stat_file(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 6:
                continue
            rows.append({
                "stat_type": row[0].strip(),
                "host_id": row[1].strip(),
                "region": row[2].strip(),
                "category": row[3].strip(),
                "total_type": row[4].strip(),
                "total": row[5].strip(),
            })

    def param(name):
        return next((r["total"] for r in rows if r["stat_type"] == "PARAM" and r["category"] == name), "")

    def values(category, exclude=("HostValues",)):
        out = []
        for r in rows:
            if r["category"] == category and r["total_type"] not in exclude:
                try:
                    out.append(float(r["total"]))
                except ValueError:
                    pass
        return out

    def grep(region=None, region_pat=None, category=None, category_pat=None, total_type=None):
        out = []
        for r in rows:
            if r["total_type"] == "HostValues":
                continue
            if total_type and r["total_type"] != total_type:
                continue
            if region and r["region"] != region:
                continue
            if region_pat and not re.search(region_pat, r["region"]):
                continue
            if category and r["category"] != category:
                continue
            if category_pat and not re.search(category_pat, r["category"]):
                continue
            try:
                out.append(float(r["total"]))
            except ValueError:
                pass
        return out

    def first(category, total_type=None):
        nums = grep(category=category, total_type=total_type)
        if not nums:
            return ""
        x = nums[0]
        return int(x) if x == int(x) else round(x, 2)

    benchmark_region = next(
        (r["region"] for r in rows if r["category"] == "Timer_0" and r["total_type"] != "HostValues"),
        "",
    )
    num_runs = int(values("Runs")[0]) if values("Runs") else 1
    total_time = round(values("TimerTotal")[0], 2) if values("TimerTotal") else 0
    timer_vals = grep(category_pat=r"^Timer_\d+$")
    total_time_exec = round(sum(timer_vals) / len(timer_vals), 2) if timer_vals else 0

    compute_per_run = []
    for j in range(num_runs):
        v = grep(region_pat=rf"^{re.escape(benchmark_region)}_{j}_\d+")
        if v:
            compute_per_run.append(sum(v))
    compute_vals = grep(region_pat=rf"^{re.escape(benchmark_region)}_\d+")

    if benchmark_region == "TC":
        tc_times = [
            r for r in rows
            if r["category"] == "Time"
            and re.fullmatch(rf"{re.escape(benchmark_region)}_\d+", r["region"])
            and r["total_type"] != "HostValues"
        ]
        compute_time = round(sum(float(r["total"]) for r in tc_times) / len(tc_times), 2) if tc_times else 0
    elif compute_per_run:
        compute_time = round(sum(compute_per_run) / len(compute_per_run), 2)
    elif compute_vals:
        compute_time = round(sum(compute_vals) / len(compute_vals), 2)
    else:
        compute_time = 0

    sync_per_run = []
    for j in range(num_runs):
        v = grep(category_pat=rf"^Sync_{re.escape(benchmark_region)}_{j}_\d+")
        if v:
            sync_per_run.append(sum(v))
    sync_fb = grep(category_pat=rf"^Sync_{re.escape(benchmark_region)}_\d+")
    if sync_per_run:
        sync_time = round(sum(sync_per_run) / len(sync_per_run), 2)
    elif sync_fb:
        sync_time = round(sum(sync_fb) / max(num_runs, 1), 2)
    else:
        sync_time = 0

    barrier_per_run = []
    for j in range(num_runs):
        v = grep(region="DGReducible", category_pat=rf"^ReduceDGAccum_{j}_\d+")
        if v:
            barrier_per_run.append(sum(v))
    barrier_fb = grep(region="DGReducible", category_pat=r"^ReduceDGAccum_\d+")
    if barrier_per_run:
        barrier_time = round(sum(barrier_per_run) / len(barrier_per_run), 2)
    elif barrier_fb:
        barrier_time = round(sum(barrier_fb) / max(num_runs, 1), 2)
    else:
        barrier_time = 0

    sync_bytes_rows = []
    for r in rows:
        if r["total_type"] != "HSUM":
            continue
        if re.search(rf"Reduce.*SendBytes_{re.escape(benchmark_region)}_0", r["category"]) or re.search(
            rf"Broadcast.*SendBytes_{re.escape(benchmark_region)}_0", r["category"]
        ):
            try:
                sync_bytes_rows.append(float(r["total"]))
            except ValueError:
                pass

    gct = values("GraphConstructTime")
    rf = values("ReplicationFactor")
    mem_max = grep(category="CommunicationMemUsageMax", total_type="HMAX")
    mem_min = grep(category="CommunicationMemUsageMin", total_type="HMIN")
    replication_nodes = first("ReplicationFactorNodes")
    if replication_nodes == "":
        rf_nodes = values("ReplicationFactor")
        replication_nodes = round(rf_nodes[0], 4) if rf_nodes else ""

    return {
        "num_threads": int(float(values("Threads")[0])) if values("Threads") else 0,
        "runs": num_runs,
        "total_time": total_time,
        "total_time_exec": total_time_exec,
        "compute_time": compute_time,
        "sync_time": sync_time,
        "barrier_time": barrier_time,
        "sync_bytes": int(sum(sync_bytes_rows)) if sync_bytes_rows else 0,
        "graph_construct_time": round(gct[0], 2) if gct else 0,
        "replication_factor": round(rf[0], 4) if rf else 0,
        "comm_mem_max": int(mem_max[0]) if mem_max else 0,
        "comm_mem_min": int(mem_min[0]) if mem_min else 0,
        "inspect_bytes": first("EdgeInspectionBytesSent", "HSUM"),
        "load_bytes": first("EdgeLoadingBytesSent", "HSUM"),
        "load_messages": first("EdgeLoadingMessagesSent", "HSUM"),
        "peak_load_bytes": first("EdgeLoadingMaxBytesSent", "HMAX"),
        "replication_nodes": replication_nodes,
        "replication_edges": first("ReplicatonFactorEdges"),
        "total_node_proxies": first("TotalNodeProxies"),
        "total_edge_proxies": first("TotalEdgeProxies"),
        "edge_inspection_time": first("EdgeInspection", "HMAX"),
        "edge_loading_time": first("EdgeLoading", "HMAX"),
    }


def parse_run_log():
    inspect_re = re.compile(r"Edge inspection time:.*to read (\d+) bytes", re.I)
    load_re = re.compile(r"Edge loading time:.*to read (\d+) bytes", re.I)
    run_re = re.compile(r"^\[[^\]]+\]\s+RUN\s+(\S+)\s*$")
    out = {}

    if not LOG.exists():
        return out

    current = None
    inspect = []
    loads = []

    def flush():
        nonlocal current, inspect, loads
        if current:
            out[current] = {
                "inspect_bytes": sum(inspect) if inspect else "",
                "load_bytes": sum(loads) if loads else "",
            }
        current = None
        inspect = []
        loads = []

    with open(LOG, encoding="utf-8", errors="replace") as f:
        for line in f:
            m_run = run_re.match(line.strip())
            if m_run:
                flush()
                current = m_run.group(1)
                continue
            if current is None:
                continue
            m_i = inspect_re.search(line)
            if m_i:
                inspect.append(int(m_i.group(1)))
                continue
            m_l = load_re.search(line)
            if m_l:
                loads.append(int(m_l.group(1)))
    flush()
    return out


def parse_run_id(name):
    for algo in ("bfs", "pr", "sssp", "tc"):
        prefix = f"{algo}_"
        if name.startswith(prefix):
            rest = name[len(prefix):]
            if rest.endswith("p"):
                graph, np_s = rest.rsplit("_", 1)
                return algo, graph, int(np_s[:-1])
            break
    return None, None, None


def build_report_csv():
    log_index = parse_run_log()
    rows = []
    seen = set()

    for path in sorted(STATS_DIR.glob("*.stats")):
        if path.stem.startswith("_"):
            continue
        algo, dataset, np = parse_run_id(path.stem)
        if algo is None:
            continue
        seen.add((algo, dataset, np))
        try:
            m = parse_stat_file(path)
            if path.stem in log_index:
                for key in ("inspect_bytes", "load_bytes"):
                    if m.get(key) == "" and log_index[path.stem].get(key) != "":
                        m[key] = log_index[path.stem][key]
            if m.get("replication_nodes") == "" and m.get("replication_factor") != "":
                m["replication_nodes"] = m["replication_factor"]
            status = "ok"
        except Exception as e:
            m = {}
            status = f"parse_error: {e}"
        rows.append((algo, dataset, np, m, status))

    for algo, dataset, np in EXPECTED:
        if (algo, dataset, np) not in seen:
            rows.append((algo, dataset, np, {}, "missing"))

    rows.sort(key=lambda r: (ALGO_LABEL.get(r[0], r[0]), r[1], r[2]))
    out_rows = []
    for algo_key, dataset, np, m, status in rows:
        algo_name = ALGO_LABEL[algo_key]
        pk = ALGO_PRIMARY[algo_name]
        row = {
            "algorithm": algo_name,
            "dataset": dataset,
            "mpi_processes": np,
            "threads": m.get("num_threads", ""),
            "runs": m.get("runs", ""),
            "primary_metric": pk,
            "primary_metric_value": m.get(pk, ""),
            "status": status,
        }
        for key in METRIC_KEYS:
            row[key] = m.get(key, "")
        out_rows.append(row)

    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(out_rows)
    ok = sum(1 for r in rows if r[4] == "ok")
    print(f"Wrote {REPORT_CSV} ({ok}/{len(rows)} ok)")
    return pd.read_csv(REPORT_CSV)


def plot_all(df):
    plt.rcParams.update({
        "figure.facecolor": "#fafafa",
        "axes.facecolor": "#ffffff",
        "axes.edgecolor": "#94a3b8",
        "axes.labelcolor": "#334155",
        "axes.titleweight": "bold",
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.color": "#475569",
        "ytick.color": "#475569",
        "grid.color": "#e2e8f0",
        "grid.linestyle": "-",
        "grid.alpha": 0.9,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    })

    df = df[df["status"] == "ok"].copy()

    for algo_label, algo_title, algo_slug in ALGORITHMS:
        for dataset, subtitle in DATASETS:
            sub = df[(df["algorithm"] == algo_label) & (df["dataset"] == dataset)].sort_values("mpi_processes")
            if sub.empty:
                continue

            mins = []
            maxs = []
            for _, row in sub.iterrows():
                path = STATS_DIR / f"{algo_slug}_{row['dataset']}_{int(row['mpi_processes'])}p.stats"
                values = []
                if path.exists():
                    with open(path, newline="") as f:
                        reader = csv.reader(f)
                        next(reader, None)
                        for stat_row in reader:
                            if len(stat_row) < 6 or stat_row[3].strip() == "Timer_0":
                                continue
                            if re.fullmatch(r"Timer_\d+", stat_row[3].strip()):
                                try:
                                    values.append(float(stat_row[5]))
                                except ValueError:
                                    pass
                mins.append(min(values) if values else float("nan"))
                maxs.append(max(values) if values else float("nan"))

            sub = sub.copy()
            sub["timer_min_excl_first"] = mins
            sub["timer_max_excl_first"] = maxs

            out_dir = EXP / "plots" / algo_slug / "by_dataset"
            out_dir.mkdir(parents=True, exist_ok=True)
            accent = ACCENT.get(dataset, "#334155")
            metrics = PANEL_TC if algo_slug == "tc" else PANEL_DEFAULT

            fig = plt.figure(figsize=(14, 8.5))
            fig.suptitle(f"{algo_title} scalability — {subtitle}", fontsize=15, fontweight="bold", y=0.98)
            runs_label = str(int(sub["runs"].iloc[0])) if len(sub) else "3"
            fig.text(
                0.5, 0.93,
                f"MPI processes: 1 · 2 · 4 · 6 · 8   |   threads=2, runs={runs_label}",
                ha="center", fontsize=10, color="#64748b",
            )

            gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.32, left=0.07, right=0.97, top=0.88, bottom=0.08)
            axes = [fig.add_subplot(gs[i // 2, i % 2]) for i in range(len(metrics))]
            if len(metrics) == 3:
                fig.add_subplot(gs[1, 1]).set_visible(False)

            x = sub["mpi_processes"].values
            for ax, (col, title, unit, use_log) in zip(axes, metrics):
                y = pd.to_numeric(sub[col], errors="coerce").values
                ax.plot(
                    x, y, color=accent, linewidth=2.4, marker="o", markersize=9,
                    markerfacecolor="white", markeredgewidth=2, markeredgecolor=accent, label="Mean",
                )
                scale_y = y

                if col == "total_time_exec":
                    y_min = pd.to_numeric(sub["timer_min_excl_first"], errors="coerce").values
                    y_max = pd.to_numeric(sub["timer_max_excl_first"], errors="coerce").values
                    ax.plot(x, y_min, color="#16a34a", linewidth=1.8, linestyle="--", marker="v", markersize=6, label="Min")
                    ax.plot(x, y_max, color="#dc2626", linewidth=1.8, linestyle="--", marker="^", markersize=6, label="Max")
                    scale_y = pd.concat([pd.Series(y), pd.Series(y_min), pd.Series(y_max)]).dropna().values
                    ax.legend(loc="best", fontsize=7)

                ax.set_xticks(MPI_TICKS)
                ax.set_xlabel("MPI processes", fontsize=9)
                ax.set_ylabel(f"{title} ({unit})" if unit else title, fontsize=9)
                ax.set_title(title, pad=8)
                ax.grid(True, axis="both")
                ax.set_xlim(0.2, 8.8)

                if use_log and len(scale_y) and (scale_y > 0).all():
                    ax.set_yscale("log")
                    ax.yaxis.set_major_formatter(mticker.LogFormatterSciNotation(base=10))
                else:
                    ax.yaxis.set_major_formatter(
                        mticker.FuncFormatter(lambda val, _: f"{val:,.0f}" if val >= 1000 else f"{val:g}")
                    )
                    if use_log and len(scale_y) and (scale_y <= 0).any():
                        ax.set_ylim(bottom=0)

            out = out_dir / f"{algo_slug}_{dataset}.png"
            fig.savefig(out, dpi=160, facecolor=fig.get_facecolor())
            plt.close(fig)
            print(f"Wrote {out}")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--report", action="store_true", help="only build report.csv")
    opts = args.parse_args()
    df = build_report_csv()
    if not opts.report:
        plot_all(df)


if __name__ == "__main__":
    main()
