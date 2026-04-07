"""
Выбор пары (platform_id, device_id) для Spla в бенчмарке.

Используется только **POCL** (Portable Computing Language) — OpenCL на CPU,
чтобы сравнение с LAGraph было на CPU.

Переопределение: SPLA_OPENCL_PLATFORM и SPLA_OPENCL_DEVICE (если POCL не на
стандартных индексах или нет clinfo).
"""

from __future__ import annotations

import os
import re
import subprocess
from typing import List, Optional, Tuple

import lib.util as util


def _parse_clinfo_listing(text: str) -> List[Tuple[int, str, List[Tuple[int, str]]]]:
    """Разбор вывода `clinfo -l`: список (platform_id, platform_name, [(dev_id, dev_name), ...])."""
    platforms: List[Tuple[int, str, List[Tuple[int, str]]]] = []
    cur_pid: Optional[int] = None
    cur_name: Optional[str] = None
    cur_devs: List[Tuple[int, str]] = []

    plat_re = re.compile(r"^Platform\s+#(\d+):\s*(.+)\s*$")
    dev_re = re.compile(r"^\s*`--\s+Device\s+#(\d+):\s*(.+)\s*$")

    for line in text.splitlines():
        m = plat_re.match(line)
        if m:
            if cur_pid is not None:
                platforms.append((cur_pid, cur_name or "", cur_devs))
            cur_pid = int(m.group(1))
            cur_name = m.group(2).strip()
            cur_devs = []
            continue
        m = dev_re.match(line)
        if m and cur_pid is not None:
            cur_devs.append((int(m.group(1)), m.group(2).strip()))

    if cur_pid is not None:
        platforms.append((cur_pid, cur_name or "", cur_devs))

    return platforms


def _is_pocl(name: str) -> bool:
    n = name.lower()
    return "portable computing language" in n or n.strip() == "pocl"


def _pick_pocl_device(
    plats: List[Tuple[int, str, List[Tuple[int, str]]]],
) -> Optional[Tuple[int, int]]:
    for pid, pname, devs in plats:
        if not _is_pocl(pname):
            continue
        if devs:
            return pid, devs[0][0]
        return pid, 0
    return None


def _opencl_log_pick(platform_id: int, device_id: int, detail: str = "") -> None:
    if os.environ.get("SPLA_OPENCL_LOG", "").strip().lower() not in (
        "1",
        "true",
        "yes",
    ):
        return
    msg = f"platform={platform_id} device={device_id}"
    if detail:
        msg = f"{msg} ({detail})"
    util.print_status("spla-opencl", "picked", msg)


def pick_spla_opencl_platform_device() -> Tuple[int, int]:
    """Только POCL (CPU). GPU в бенчмарке не используется."""
    env_p = os.environ.get("SPLA_OPENCL_PLATFORM")
    env_d = os.environ.get("SPLA_OPENCL_DEVICE")
    if env_p is not None and env_d is not None:
        p, d = int(env_p), int(env_d)
        _opencl_log_pick(p, d, "from SPLA_OPENCL_PLATFORM/DEVICE")
        return p, d

    try:
        out = util.check_output(["clinfo", "-l"])
        text = out.decode("utf-8", errors="replace")
    except (subprocess.CalledProcessError, FileNotFoundError):
        _opencl_log_pick(0, 0, "clinfo missing or failed, fallback")
        return 0, 0

    plats = _parse_clinfo_listing(text)
    if not plats:
        _opencl_log_pick(0, 0, "empty clinfo -l")
        return 0, 0

    pocl = _pick_pocl_device(plats)
    if pocl is not None:
        _opencl_log_pick(pocl[0], pocl[1], "POCL CPU (benchmark)")
        return pocl

    _opencl_log_pick(0, 0, "no POCL in clinfo — установите POCL или задайте SPLA_OPENCL_PLATFORM/DEVICE")
    return 0, 0
