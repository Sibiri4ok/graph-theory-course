#!/usr/bin/env python3
"""BFS compact dashboards: Time (3×3) and Comm (3×2), datasets × metrics."""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "experiments" / "report.csv"
OUT_DIR = ROOT / "experiments" / "plots" / "bfs"

DATASETS = [
    ("roadNet-PA", "roadNet-PA"),
    ("web-Google", "web-Google"),
    ("wiki-talk-temporal", "wiki-talk"),
]

# (column, short title, unit, use_log)
TIME_METRICS = [
    ("total_time", "Total time", "ms", True),
    ("sync_time", "Sync time", "ms", False),
    ("graph_construct_time", "Graph construction", "ms", False),
]

COMM_METRICS = [
    ("sync_bytes", "Sync traffic", "bytes", True),
    ("replication_factor", "Replication factor", "", False),
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
            "axes.titlesize": 12,
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


def _annotate_points(ax, x, y, color: str, fontsize: float = 6.5) -> None:
    for xi, yi in zip(x, y):
        if pd.isna(yi):
            continue
        if yi >= 1_000_000:
            label = f"{yi / 1e6:.1f}M"
        elif yi >= 1000:
            label = f"{yi / 1e3:.1f}k" if yi >= 10_000 else f"{yi:,.0f}"
        elif yi < 10 and yi != int(yi):
            label = f"{yi:.2f}"
        else:
            label = f"{yi:.0f}"
        ax.annotate(
            label,
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=fontsize,
            color=color,
            alpha=0.9,
        )


def _plot_cell(ax, df: pd.DataFrame, dataset: str, col: str, use_log: bool) -> None:
    sub = df[(df["dataset"] == dataset)].sort_values("mpi_processes")
    accent = ACCENT[dataset]
    x = sub["mpi_processes"].values
    y = pd.to_numeric(sub[col], errors="coerce").values

    ax.plot(
        x,
        y,
        color=accent,
        linewidth=2.2,
        marker="o",
        markersize=7,
        markerfacecolor="white",
        markeredgewidth=1.8,
        markeredgecolor=accent,
        zorder=3,
    )
    _annotate_points(ax, x, y, accent)

    ax.set_xticks(MPI_TICKS)
    ax.set_xlim(0.2, 8.8)
    ax.grid(True, axis="both")
    use_log = use_log and (y > 0).all()
    _format_yaxis(ax, use_log)
    if not use_log and (y >= 0).all():
        ax.set_ylim(bottom=0)


def _build_dashboard(
    df: pd.DataFrame,
    metrics: list,
    nrows: int,
    ncols: int,
    title: str,
    outfile: Path,
    figsize: tuple[float, float],
) -> None:
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
    fig.suptitle(
        title,
        fontsize=16,
        fontweight="bold",
        color="#0f172a",
        y=0.98,
    )
    fig.text(
        0.5,
        0.94,
        "BFS  ·  MPI: 1, 2, 4, 6, 8  ·  threads=2, runs=3",
        ha="center",
        fontsize=10,
        color="#64748b",
    )

    for row, (dataset, row_label) in enumerate(DATASETS):
        for col_idx, (metric_col, metric_title, unit, use_log) in enumerate(metrics):
            ax = axes[row, col_idx]
            _plot_cell(ax, df, dataset, metric_col, use_log)

            if row == 0:
                ax.set_title(metric_title, pad=10, fontsize=12)
            if col_idx == 0:
                ax.set_ylabel(f"{row_label}\n({unit})" if unit else row_label, fontsize=9)
            elif row == 0 and unit:
                pass
            if row == nrows - 1:
                ax.set_xlabel("MPI processes", fontsize=9)
            else:
                ax.set_xlabel("")
                ax.tick_params(labelbottom=True)

    fig.subplots_adjust(left=0.1, right=0.98, top=0.9, bottom=0.07, hspace=0.38, wspace=0.28)
    fig.savefig(outfile, dpi=170, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {outfile}")


def main():
    _apply_style()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CSV)
    df = df[(df["algorithm"] == "BFS") & (df["status"] == "ok")].copy()

    _build_dashboard(
        df,
        TIME_METRICS,
        nrows=3,
        ncols=3,
        title="BFS — Time metrics (by dataset)",
        outfile=OUT_DIR / "bfs_dashboard_time.png",
        figsize=(15, 11),
    )
    _build_dashboard(
        df,
        COMM_METRICS,
        nrows=3,
        ncols=2,
        title="BFS — Communication & partitioning (by dataset)",
        outfile=OUT_DIR / "bfs_dashboard_comm.png",
        figsize=(12, 11),
    )


if __name__ == "__main__":
    main()
