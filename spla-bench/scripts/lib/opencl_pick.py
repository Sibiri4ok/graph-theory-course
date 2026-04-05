"""
Выбор пары (platform_id, device_id) для Spla (OpenCL).

Предпочтение: реальный ускоритель (встроенная/дискретная GPU), иначе POCL CPU.
Переопределение: переменные окружения SPLA_OPENCL_PLATFORM, SPLA_OPENCL_DEVICE.
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


def _is_gpu_like(platform_name: str, device_name: str) -> bool:
    blob = f"{platform_name} {device_name}".lower()
    keys = (
        "graphics",
        "nvidia",
        "amd",
        "cuda",
        "gpu",
        "radeon",
        "adreno",
        "mali",
        "iris",
        "uhd",
        "intel(r) opencl",
    )
    return any(k in blob for k in keys)


def pick_spla_opencl_platform_device() -> Tuple[int, int]:
    env_p = os.environ.get("SPLA_OPENCL_PLATFORM")
    env_d = os.environ.get("SPLA_OPENCL_DEVICE")
    if env_p is not None and env_d is not None:
        return int(env_p), int(env_d)

    try:
        out = util.check_output(["clinfo", "-l"])
        text = out.decode("utf-8", errors="replace")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0, 0

    plats = _parse_clinfo_listing(text)
    if not plats:
        return 0, 0

    candidates: List[Tuple[int, int, int]] = []
    for pid, pname, devs in plats:
        if not devs:
            candidates.append((pid, 0, 2 if _is_pocl(pname) else 1))
            continue
        for did, dname in devs:
            if _is_pocl(pname):
                pri = 2
            elif _is_gpu_like(pname, dname):
                pri = 0
            else:
                pri = 1
            candidates.append((pid, did, pri))

    candidates.sort(key=lambda t: (t[2], t[0], t[1]))
    best = candidates[0]
    return best[0], best[1]
