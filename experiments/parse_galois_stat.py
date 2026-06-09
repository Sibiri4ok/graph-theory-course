#!/usr/bin/env python3
"""Parse Galois distributed -statFile output (replaces galois_log_parser.R core logic)."""
import csv
import re
import sys
from pathlib import Path


def load_stat(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 6:
                continue
            rows.append(
                {
                    "stat_type": row[0].strip(),
                    "host_id": row[1].strip(),
                    "region": row[2].strip(),
                    "category": row[3].strip(),
                    "total_type": row[4].strip(),
                    "total": row[5].strip(),
                }
            )
    return rows


def val(rows, category, total_type_exclude=("HostValues",)):
    out = []
    for r in rows:
        if r["category"] == category and r["total_type"] not in total_type_exclude:
            try:
                out.append(float(r["total"]))
            except ValueError:
                pass
    return out


def first_val(rows, category, total_type=None):
    v = grep_total(rows, category=category, total_type=total_type)
    if not v:
        return ""
    x = v[0]
    return int(x) if x == int(x) else round(x, 2)


def grep_total(
    rows,
    region_pat=None,
    category_pat=None,
    region=None,
    category=None,
    total_type=None,
    exclude_host_values=True,
):
    out = []
    for r in rows:
        if exclude_host_values and r["total_type"] == "HostValues":
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


def parse_stat_file(path):
    rows = load_stat(path)
    param = lambda c: next(
        (r["total"] for r in rows if r["stat_type"] == "PARAM" and r["category"] == c),
        "",
    )

    benchmark_region = next(
        (r["region"] for r in rows if r["category"] == "Timer_0" and r["total_type"] != "HostValues"),
        "",
    )
    num_runs = int(val(rows, "Runs")[0]) if val(rows, "Runs") else 1

    total_time = val(rows, "TimerTotal")
    total_time = round(total_time[0], 2) if total_time else 0

    timer_vals = grep_total(rows, category_pat=r"^Timer_\d+$")
    total_time_exec = round(sum(timer_vals) / len(timer_vals), 2) if timer_vals else 0

    compute_per_run = []
    for j in range(num_runs):
        v = grep_total(rows, region_pat=rf"^{re.escape(benchmark_region)}_{j}_\d+")
        if v:
            compute_per_run.append(sum(v))
    compute_vals = grep_total(rows, region_pat=rf"^{re.escape(benchmark_region)}_\d+")
    if benchmark_region == "TC":
        tc_times = [
            r
            for r in rows
            if r["category"] == "Time"
            and re.fullmatch(rf"{re.escape(benchmark_region)}_\d+", r["region"])
            and r["total_type"] != "HostValues"
        ]
        compute_time = (
            round(sum(float(r["total"]) for r in tc_times) / len(tc_times), 2)
            if tc_times
            else 0
        )
    elif compute_per_run:
        compute_time = round(sum(compute_per_run) / len(compute_per_run), 2)
    elif compute_vals:
        compute_time = round(
            sum(compute_vals) / len(compute_vals) if compute_vals else 0, 2
        )
    else:
        compute_time = 0

    sync_per_run = []
    for j in range(num_runs):
        v = grep_total(
            rows, category_pat=rf"^Sync_{re.escape(benchmark_region)}_{j}_\d+"
        )
        if v:
            sync_per_run.append(sum(v))
    sync_fallback = grep_total(
        rows, category_pat=rf"^Sync_{re.escape(benchmark_region)}_\d+"
    )
    if sync_per_run:
        sync_time = round(sum(sync_per_run) / len(sync_per_run), 2)
    elif sync_fallback:
        sync_time = round(sum(sync_fallback) / max(num_runs, 1), 2)
    else:
        sync_time = 0

    barrier_per_run = []
    for j in range(num_runs):
        v = grep_total(
            rows,
            region="DGReducible",
            category_pat=rf"^ReduceDGAccum_{j}_\d+",
        )
        if v:
            barrier_per_run.append(sum(v))
    barrier_fb = grep_total(
        rows, region="DGReducible", category_pat=r"^ReduceDGAccum_\d+"
    )
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
    sync_bytes = int(sum(sync_bytes_rows)) if sync_bytes_rows else 0

    gct = val(rows, "GraphConstructTime")
    graph_construct_time = round(gct[0], 2) if gct else 0

    rf = val(rows, "ReplicationFactor")
    replication_factor = round(rf[0], 4) if rf else 0

    mem_max = grep_total(rows, category="CommunicationMemUsageMax", total_type="HMAX")
    mem_min = grep_total(rows, category="CommunicationMemUsageMin", total_type="HMIN")
    comm_mem_max = int(mem_max[0]) if mem_max else 0
    comm_mem_min = int(mem_min[0]) if mem_min else 0

    input_path = param("Input")
    input_name = Path(input_path).name if input_path else ""
    if "." in input_name:
        input_name = input_name.rsplit(".", 1)[0]

    inspect_bytes = first_val(rows, "EdgeInspectionBytesSent", "HSUM")
    load_bytes = first_val(rows, "EdgeLoadingBytesSent", "HSUM")
    load_messages = first_val(rows, "EdgeLoadingMessagesSent", "HSUM")
    peak_load_bytes = first_val(rows, "EdgeLoadingMaxBytesSent", "HMAX")
    replication_nodes = first_val(rows, "ReplicationFactorNodes")
    if replication_nodes == "":
        rf_nodes = val(rows, "ReplicationFactor")
        replication_nodes = round(rf_nodes[0], 4) if rf_nodes else ""
    edge_inspection_time = first_val(rows, "EdgeInspection", "HMAX")
    edge_loading_time = first_val(rows, "EdgeLoading", "HMAX")
    replication_edges = first_val(rows, "ReplicatonFactorEdges")
    total_node_proxies = first_val(rows, "TotalNodeProxies")
    total_edge_proxies = first_val(rows, "TotalEdgeProxies")

    return {
        "benchmark": (
            Path(param("CommandLine").split()[0]).name if param("CommandLine") else ""
        ),
        "benchmark_region": benchmark_region,
        "input": input_name,
        "hosts": int(val(rows, "Hosts")[0]) if val(rows, "Hosts") else 0,
        "num_threads": int(float(val(rows, "Threads")[0])) if val(rows, "Threads") else 0,
        "partition_scheme": param("PartitionScheme"),
        "runs": num_runs,
        "total_time": total_time,
        "total_time_exec": total_time_exec,
        "compute_time": compute_time,
        "sync_time": sync_time,
        "barrier_time": barrier_time,
        "sync_bytes": sync_bytes,
        "graph_construct_time": graph_construct_time,
        "replication_factor": replication_factor,
        "comm_mem_max": comm_mem_max,
        "comm_mem_min": comm_mem_min,
        "inspect_bytes": inspect_bytes,
        "load_bytes": load_bytes,
        "load_messages": load_messages,
        "peak_load_bytes": peak_load_bytes,
        "replication_nodes": replication_nodes,
        "replication_edges": replication_edges,
        "total_node_proxies": total_node_proxies,
        "total_edge_proxies": total_edge_proxies,
        "edge_inspection_time": edge_inspection_time,
        "edge_loading_time": edge_loading_time,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file.stats [file2.stats ...]")
        sys.exit(1)
    import json

    for p in sys.argv[1:]:
        print(json.dumps(parse_stat_file(p)))
