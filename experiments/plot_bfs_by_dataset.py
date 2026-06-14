#!/usr/bin/env python3
"""BFS dashboard: one presentation figure per dataset (metrics vs MPI)."""
from pathlib import Path
import csv
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "experiments" / "report.csv"
STATS_DIR = ROOT / "experiments" / "results" / "stats"
OUT_DIR = ROOT / "experiments" / "plots" / "bfs" / "by_dataset"

DATASETS = [
    ("roadNet-PA", "Road network — Pennsylvania"),
    ("web-Google", "Web graph — Google"),
    ("wiki-talk-temporal", "Wikipedia talk (temporal)"),
]

PANEL_METRICS = [
    ("total_time_exec", "Total time", "ms", True),
    ("sync_time", "Synchronization time", "ms", False),
    ("sync_bytes", "Sync traffic", "bytes", True),
    ("replication_factor", "Replication factor", "", False),
    ("graph_construct_time", "Graph construction", "ms", False),
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


def plot_dataset(df: pd.DataFrame, dataset: str, subtitle: str) -> None:
    sub = df[df["dataset"] == dataset].sort_values("mpi_processes")
    if sub.empty:
        return
    sub = _add_timer_bounds(sub, "bfs")

    accent = ACCENT.get(dataset, "#334155")
    fig = plt.figure(figsize=(14, 8.5))
    fig.suptitle(
        f"BFS scalability — {subtitle}",
        fontsize=15,
        fontweight="bold",
        color="#0f172a",
        y=0.98,
    )
    runs = int(sub["runs"].iloc[0]) if "runs" in sub.columns and len(sub) else 3
    fig.text(
        0.5,
        0.93,
        f"MPI processes: 1 · 2 · 4 · 6 · 8   |   threads=2, runs={runs}",
        ha="center",
        fontsize=10,
        color="#64748b",
    )

    gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.32, left=0.07, right=0.97, top=0.88, bottom=0.08)

    axes = [fig.add_subplot(gs[i // 3, i % 3]) for i in range(5)]
    # hide unused sixth cell
    fig.add_subplot(gs[1, 2]).set_visible(False)

    x = sub["mpi_processes"].values

    for ax, (col, title, unit, use_log) in zip(axes, PANEL_METRICS):
        y = pd.to_numeric(sub[col], errors="coerce").values
        ylabel = f"{title} ({unit})" if unit else title

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

    out = OUT_DIR / f"bfs_{dataset}.png"
    fig.savefig(out, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def main():
    _apply_style()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CSV)
    df = df[(df["algorithm"] == "BFS") & (df["status"] == "ok")].copy()

    for dataset, subtitle in DATASETS:
        plot_dataset(df, dataset, subtitle)


if __name__ == "__main__":
    main()
