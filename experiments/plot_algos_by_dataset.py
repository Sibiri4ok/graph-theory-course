#!/usr/bin/env python3
"""Per-dataset dashboards for SSSP, PageRank, TC (metrics vs MPI).

Формат такой же, как для BFS в `plot_bfs_by_dataset.py`:
одна картинка на (алгоритм, датасет), 5 панелей:
  - total_time_exec
  - sync_time
  - sync_bytes
  - replication_factor
  - graph_construct_time
"""
from pathlib import Path
import csv
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "experiments" / "report.csv"
STATS_DIR = ROOT / "experiments" / "results" / "stats"

DATASETS = [
    ("roadNet-PA", "Road network — Pennsylvania"),
    ("web-Google", "Web graph — Google"),
    ("wiki-talk-temporal", "Wikipedia talk (temporal)"),
]

ALGORITHMS = [
    ("SSSP", "SSSP", "sssp"),
    ("PageRank", "PageRank", "pr"),
    ("Triangle Counting", "Triangle Counting", "tc"),
]

# Default panel set for BFS-like push алгоритмы (SSSP, PageRank).
PANEL_METRICS_DEFAULT = [
    ("total_time_exec", "Total time", "ms", True),
    ("sync_time", "Synchronization time", "ms", False),
    ("sync_bytes", "Sync traffic", "bytes", True),
    ("replication_factor", "Replication factor", "", False),
    ("graph_construct_time", "Graph construction", "ms", False),
]

# For TC хотим видеть именно стадии построения mining-графа.
PANEL_METRICS_TC = [
    ("total_time_exec", "Total time", "ms", True),
    ("graph_construct_time", "Graph construction", "ms", False),
    ("inspect_bytes", "Inspect bytes", "bytes", True),
    ("load_bytes", "Load bytes", "bytes", True),
    ("load_vs_peak_bytes", "Load vs Peak load bytes", "bytes", True),
]

MPI_TICKS = [1, 2, 4, 6, 8]
ACCENT = {
    "roadNet-PA": "#2563eb",
    "web-Google": "#ea580c",
    "wiki-talk-temporal": "#16a34a",
}


def _apply_style() -> None:
    plt.rcParams.update(
        {
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
        }
    )


def _format_yaxis(ax, log_scale: bool) -> None:
    if log_scale:
        ax.set_yscale("log")
        ax.yaxis.set_major_formatter(mticker.LogFormatterSciNotation(base=10))
    else:
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x:,.0f}" if x >= 1000 else f"{x:g}")
        )


def _annotate_points(ax, x, y, color: str) -> None:
    for xi, yi in zip(x, y):
        if pd.isna(yi):
            continue
        label = f"{yi:,.0f}" if yi >= 1000 else (f"{yi:.2f}" if yi < 10 else f"{yi:.0f}")
        ax.annotate(
            label,
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=7,
            color=color,
            alpha=0.85,
        )


def _plot_load_vs_peak_bytes(ax, x, y_load, y_peak, accent: str) -> None:
    peak_color = "#7c3aed"
    ax.plot(
        x,
        y_load,
        color=accent,
        linewidth=2.2,
        marker="o",
        markersize=8,
        markerfacecolor="white",
        markeredgewidth=2,
        markeredgecolor=accent,
        zorder=3,
        label="Load bytes (HSUM)",
    )
    ax.plot(
        x,
        y_peak,
        color=peak_color,
        linewidth=2.0,
        linestyle="--",
        marker="s",
        markersize=7,
        markerfacecolor="white",
        markeredgewidth=1.8,
        markeredgecolor=peak_color,
        zorder=3,
        label="Peak load bytes (HMAX)",
    )
    _annotate_points(ax, x, y_load, accent)
    _annotate_points(ax, x, y_peak, peak_color)
    ax.legend(loc="upper left", fontsize=7, frameon=True, framealpha=0.9)


def _timer_min_max(algo_slug: str, dataset: str, mpi_processes: int) -> tuple[float, float]:
    path = STATS_DIR / f"{algo_slug}_{dataset}_{mpi_processes}p.stats"
    values: list[float] = []
    if not path.exists():
        return float("nan"), float("nan")

    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 6:
                continue
            category = row[3].strip()
            if category == "Timer_0":
                continue
            if not re.fullmatch(r"Timer_\d+", category):
                continue
            try:
                values.append(float(row[5]))
            except ValueError:
                pass

    if not values:
        return float("nan"), float("nan")
    return min(values), max(values)


def _add_timer_bounds(sub: pd.DataFrame, algo_slug: str) -> pd.DataFrame:
    sub = sub.copy()
    mins: list[float] = []
    maxs: list[float] = []
    for _, row in sub.iterrows():
        mn, mx = _timer_min_max(algo_slug, row["dataset"], int(row["mpi_processes"]))
        mins.append(mn)
        maxs.append(mx)
    sub["timer_min_excl_first"] = mins
    sub["timer_max_excl_first"] = maxs
    return sub


def plot_dataset_for_algo(
    df: pd.DataFrame,
    algo_label: str,
    algo_title: str,
    algo_slug: str,
    dataset: str,
    subtitle: str,
    *,
    runs_label: str = "3",
    out_path: Path | None = None,
) -> None:
    sub = df[(df["algorithm"] == algo_label) & (df["dataset"] == dataset)].sort_values(
        "mpi_processes"
    )
    if sub.empty:
        return
    sub = _add_timer_bounds(sub, algo_slug)

    out_dir = ROOT / "experiments" / "plots" / algo_slug / "by_dataset"
    out_dir.mkdir(parents=True, exist_ok=True)

    accent = ACCENT.get(dataset, "#334155")
    fig = plt.figure(figsize=(14, 8.5))
    fig.suptitle(
        f"{algo_title} scalability — {subtitle}",
        fontsize=15,
        fontweight="bold",
        color="#0f172a",
        y=0.98,
    )
    runs_label = str(int(sub["runs"].iloc[0])) if "runs" in sub.columns and len(sub) else "3"
    fig.text(
        0.5,
        0.93,
        f"MPI processes: 1 · 2 · 4 · 6 · 8   |   threads=2, runs={runs_label}",
        ha="center",
        fontsize=10,
        color="#64748b",
    )

    gs = fig.add_gridspec(
        2, 3, hspace=0.42, wspace=0.32, left=0.07, right=0.97, top=0.88, bottom=0.08
    )

    axes = [fig.add_subplot(gs[i // 3, i % 3]) for i in range(5)]
    fig.add_subplot(gs[1, 2]).set_visible(False)

    x = sub["mpi_processes"].values

    metrics = PANEL_METRICS_TC if algo_slug == "tc" else PANEL_METRICS_DEFAULT

    for ax, (col, title, unit, use_log) in zip(axes, metrics):
        if col == "load_vs_peak_bytes":
            y_load = pd.to_numeric(sub["load_bytes"], errors="coerce").values
            y_peak = pd.to_numeric(sub["peak_load_bytes"], errors="coerce").values
            y = y_load
            scale_y = pd.concat(
                [
                    pd.Series(y_load, dtype="float64"),
                    pd.Series(y_peak, dtype="float64"),
                ],
                ignore_index=True,
            ).dropna().values
            _plot_load_vs_peak_bytes(ax, x, y_load, y_peak, accent)
        else:
            y = pd.to_numeric(sub[col], errors="coerce").values
            ax.plot(
                x,
                y,
                color=accent,
                linewidth=2.4,
                marker="o",
                markersize=9,
                markerfacecolor="white",
                markeredgewidth=2,
                markeredgecolor=accent,
                zorder=3,
                label="Mean",
            )
            _annotate_points(ax, x, y, accent)
            scale_y = y

            if col == "total_time_exec":
                y_min = pd.to_numeric(sub["timer_min_excl_first"], errors="coerce").values
                y_max = pd.to_numeric(sub["timer_max_excl_first"], errors="coerce").values
                ax.plot(
                    x,
                    y_min,
                    color="#16a34a",
                    linewidth=1.8,
                    linestyle="--",
                    marker="v",
                    markersize=6,
                    zorder=2,
                    label="Min (runs 1-19)",
                )
                ax.plot(
                    x,
                    y_max,
                    color="#dc2626",
                    linewidth=1.8,
                    linestyle="--",
                    marker="^",
                    markersize=6,
                    zorder=2,
                    label="Max (runs 1-19)",
                )
                scale_y = pd.concat(
                    [
                        pd.Series(y, dtype="float64"),
                        pd.Series(y_min, dtype="float64"),
                        pd.Series(y_max, dtype="float64"),
                    ],
                    ignore_index=True,
                ).dropna().values
                ax.legend(loc="best", fontsize=7, frameon=True, framealpha=0.9)

        ylabel = f"{title} ({unit})" if unit else title

        ax.set_xticks(MPI_TICKS)
        ax.set_xlabel("MPI processes", fontsize=9)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.set_title(title, pad=8)
        ax.grid(True, axis="both")
        ax.set_xlim(0.2, 8.8)
        _format_yaxis(ax, use_log and (scale_y > 0).all())

        if use_log and (scale_y <= 0).any():
            _format_yaxis(ax, False)
            ax.set_ylim(bottom=0)

    out = out_path or (out_dir / f"{algo_slug}_{dataset}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    _apply_style()
    df = pd.read_csv(CSV)
    df = df[df["status"] == "ok"].copy()

    for algo_label, algo_title, algo_slug in ALGORITHMS:
        for dataset, subtitle in DATASETS:
            plot_dataset_for_algo(df, algo_label, algo_title, algo_slug, dataset, subtitle)


if __name__ == "__main__":
    main()

