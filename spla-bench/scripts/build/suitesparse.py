"""
Обёртка над выбором SuiteSparse GraphBLAS для build.py.
Реализация — в build.lagraph.
"""

from pathlib import Path
from typing import List, Tuple

from build.lagraph import chosen_method_targets, suitesparse_do_chosen_method


def do_chosen_method() -> Tuple[Path, Path]:
    return suitesparse_do_chosen_method()
