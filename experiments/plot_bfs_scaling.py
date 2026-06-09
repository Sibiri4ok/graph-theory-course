#!/usr/bin/env python3
"""BFS scalability plots: MPI processes (X) vs metric (Y), all datasets."""
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import LogFormatterSciNotation

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "experiments" / "report.csv"
OUT_DIR = ROOT / "experiments" / "plots" / "bfs"

DATASETS = ["roadNet-PA", "web-Google", "wiki-talk-temporal"]
DATASET_LABELS = {
    "roadNet-PA": "roadNet-PA",
    "web-Google": "web-Google",
    "wiki-talk-temporal": "wiki-talk",
}
COLORS = {
    "roadNet-PA": "#1f77b4",
    "web-Google": "#ff7f0e",
    "wiki-talk-temporal": "#2ca02c",
}
MARKERS = {
    "roadNet-PA": "o",
    "web-Google": "s",
    "wiki-talk-temporal": "^",
}

METRICS = [
    ("total_time", "total_time (ms)"),
    ("sync_time", "sync_time (ms)"),
    ("sync_bytes", "sync_bytes (bytes)"),
    ("replication_factor", "replication_factor"),
    ("graph_construct_time", "graph_construct_time (ms)"),
    ("edge_inspection_time", "edge_inspection_time (ms)"),
    ("edge_loading_time", "edge_loading_time (ms)"),
]

LOG_Y_METRICS = {"total_time", "sync_time", "sync_bytes"}
MPI_TICKS = [1, 2, 4, 6, 8]
Y_MARGIN_LINEAR = 0.12
# Extra log-space above max point (in decades). Larger when the max is
# closer to the lower decade tick — so the top grid line stays farther
# from the data than the lower neighbor tick.
LOG_HEADROOM_DECADES = 0.5


def _style_axes(ax) -> None:
    for spine in ax.spines.values():
        spine.set_visible(True)
    ax.set_xlim(0.5, 8.5)
    ax.margins(x=0.02)


def _set_log_ylim(ax, ymin: float, ymax: float) -> None:
    log_lo = math.log10(ymin)
    log_hi = math.log10(ymax)
    kmin = int(math.floor(log_lo))
    k_floor = int(math.floor(log_hi))
    frac = log_hi - k_floor  # 0..1 position within [10^k_floor, 10^(k_floor+1))

    bottom = 10**kmin
    # Top limit: extend above max; more headroom when value is low in its decade.
    top = 10 ** (log_hi + LOG_HEADROOM_DECADES * (1.0 - frac))

    # Decade ticks only (10^k). Do not add the next decade label unless the
    # maximum is already high inside the current decade.
    k_tick_max = k_floor + 1 if frac >= 0.65 else k_floor
    ticks = [10**k for k in range(kmin, k_tick_max + 1)]

    ax.set_ylim(bottom=bottom, top=top)
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(LogFormatterSciNotation(base=10))
    ax.grid(True, axis="y", which="major", alpha=0.4, linestyle="--", linewidth=0.7)


def _set_y_limits(ax, series: pd.Series, column: str) -> None:
    vals = series.dropna()
    positive = vals[vals > 0]
    if positive.empty:
        return
    ymin, ymax = positive.min(), positive.max()
    if column in LOG_Y_METRICS:
        _set_log_ylim(ax, ymin, ymax)
    else:
        pad = (ymax - ymin) * Y_MARGIN_LINEAR if ymax > ymin else ymax * Y_MARGIN_LINEAR
        bottom = max(0, ymin - pad * 0.3) if ymin >= 0 else ymin - pad
        ax.set_ylim(bottom=bottom, top=ymax + pad)


def load_bfs() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    df = df[(df["algorithm"] == "BFS") & (df["status"] == "ok")].copy()
    for col, _ in METRICS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values(["dataset", "mpi_processes"])


def plot_metric(df: pd.DataFrame, column: str, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    for dataset in DATASETS:
        sub = df[df["dataset"] == dataset]
        ax.plot(
            sub["mpi_processes"],
            sub[column],
            marker=MARKERS[dataset],
            color=COLORS[dataset],
            label=DATASET_LABELS[dataset],
            linewidth=2,
            markersize=8,
        )

    ax.set_xlabel("MPI processes")
    ax.set_ylabel(ylabel)
    ax.set_xticks(MPI_TICKS)
    ax.grid(True, axis="x", alpha=0.3, linestyle="--", linewidth=0.6)
    ax.legend(loc="best", framealpha=0.95)

    if column in LOG_Y_METRICS:
        ax.set_yscale("log")
    _set_y_limits(ax, df[column], column)
    if column not in LOG_Y_METRICS:
        ax.grid(True, axis="y", alpha=0.3, linestyle="--", linewidth=0.6)
    _style_axes(ax)

    ax.set_title(f"BFS scalability — {column}")
    fig.tight_layout()

    out = OUT_DIR / f"bfs_{column}.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Wrote {out}")


def plot_combined(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(16, 9))
    axes = axes.flatten()

    for ax, (column, ylabel) in zip(axes, METRICS):
        for dataset in DATASETS:
            sub = df[df["dataset"] == dataset]
            ax.plot(
                sub["mpi_processes"],
                sub[column],
                marker=MARKERS[dataset],
                color=COLORS[dataset],
                label=DATASET_LABELS[dataset],
                linewidth=1.8,
                markersize=6,
            )
        ax.set_xlabel("MPI", fontsize=9)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.set_xticks(MPI_TICKS)
        ax.grid(True, axis="x", alpha=0.3, linestyle="--", linewidth=0.6)
        ax.set_title(column, fontsize=10)
        if column in LOG_Y_METRICS:
            ax.set_yscale("log")
        _set_y_limits(ax, df[column], column)
        if column not in LOG_Y_METRICS:
            ax.grid(True, axis="y", alpha=0.3, linestyle="--", linewidth=0.6)
        _style_axes(ax)

    axes[-1].axis("off")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower right", bbox_to_anchor=(0.98, 0.02))
    fig.suptitle("BFS: metrics vs MPI processes (all datasets)", fontsize=12, y=1.01)
    fig.tight_layout()

    out = OUT_DIR / "bfs_all_metrics.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_bfs()
    if df.empty:
        raise SystemExit("No BFS rows with status=ok in report.csv")

    for column, ylabel in METRICS:
        plot_metric(df, column, ylabel)
    plot_combined(df)


if __name__ == "__main__":
    main()
