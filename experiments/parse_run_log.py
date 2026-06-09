#!/usr/bin/env python3
"""Extract per-run graph construction byte metrics from experiments/results/run.log."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "experiments" / "results" / "run.log"

INSPECT_RE = re.compile(
    r"Edge inspection time:.*to read (\d+) bytes", re.I
)
LOAD_RE = re.compile(r"Edge loading time:.*to read (\d+) bytes", re.I)
RUN_RE = re.compile(r"^\[[^\]]+\]\s+RUN\s+(\S+)\s*$")


def _parse_one_log(path: Path, out: dict[str, dict[str, int]]) -> None:
    if not path.exists():
        return
    current: str | None = None
    inspect: list[int] = []
    loads: list[int] = []

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

    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m_run = RUN_RE.match(line.strip())
            if m_run:
                flush()
                current = m_run.group(1)
                continue
            if current is None:
                continue
            m_i = INSPECT_RE.search(line)
            if m_i:
                inspect.append(int(m_i.group(1)))
                continue
            m_l = LOAD_RE.search(line)
            if m_l:
                loads.append(int(m_l.group(1)))

    flush()


def parse_run_log() -> dict[str, dict[str, int]]:
    """Map run_id -> {inspect_bytes, load_bytes} from all experiment logs."""
    out: dict[str, dict[str, int]] = {}
    log_dir = LOG.parent
    for name in ("run.log", "nohup.out", "nohup_mpi2.out"):
        _parse_one_log(log_dir / name, out)
    return out
