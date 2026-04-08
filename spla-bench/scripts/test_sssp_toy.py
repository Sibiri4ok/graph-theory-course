#!/usr/bin/env python3
"""
Проверка Spla SSSP на маленькой цепочке с эталоном (--run-ref=true).
Те же индексы OpenCL, что и в бенчмарке: только POCL (CPU).
Запуск: python3 spla-bench/scripts/test_sssp_toy.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
SCRIPTS_DIR = SCRIPT.parent
REPO_ROOT = SCRIPTS_DIR.parent.parent
SPLA_SSSP = REPO_ROOT / "spla" / "build" / "sssp"
MTX = REPO_ROOT / "graphs-theory-datasets" / "sssp_toy_weighted.mtx"


def main() -> int:
    if not SPLA_SSSP.is_file():
        print(f"Нет бинарника {SPLA_SSSP}; соберите Spla (cmake --build … --target sssp).", file=sys.stderr)
        return 2
    if not MTX.is_file():
        print(f"Нет матрицы {MTX}.", file=sys.stderr)
        return 2

    sys.path.insert(0, str(SCRIPTS_DIR))
    from lib.opencl_pick import pick_spla_opencl_platform_device

    plat, dev = pick_spla_opencl_platform_device()

    cmd = [
        str(SPLA_SSSP),
        f"--mtxpath={MTX}",
        "--niters=1",
        "--source=0",
        f"--platform={plat}",
        f"--device={dev}",
        "--run-cpu=true",
        "--run-gpu=true",
        "--run-ref=true",
    ]
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        return proc.returncode
    out = proc.stdout
    if "VERIFY:" in out:
        print("Проверка не прошла (есть строки VERIFY:).", file=sys.stderr)
        return 1
    if "CHECK cpu" not in out:
        print("Неожиданный вывод примера.", file=sys.stderr)
        return 1
    print("OK: эталон совпал, VERIFY не выводился.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
