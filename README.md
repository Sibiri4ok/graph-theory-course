# Графовые алгоритмы: LAGraph (CPU) vs Spla (OpenCL)

Сравнение **BFS, SSSP, TC, PageRank** на одних и тех же матрицах: **SuiteSparse GraphBLAS + LAGraph** против **Spla** с OpenCL (GPU или POCL на CPU).

| Что | Где считается |
|-----|----------------|
| LAGraph | CPU, многопоточный GraphBLAS. Потоки: `export LAGRAPH_NUM_THREADS=8` → скрипт выставит `OMP_NUM_THREADS` для демо. |
| Spla | OpenCL: устройство подбирается в `opencl_pick.py` (`clinfo -l`). Вручную: `SPLA_OPENCL_PLATFORM`, `SPLA_OPENCL_DEVICE`. Лог выбора: `SPLA_OPENCL_LOG=1`. |

**Метрика времени:** LAGraph — оболочка демо вокруг вызова API; Spla в бенчмарке — лапы по `gpu(ms):` (хост вокруг OpenCL), не «чистое» время ядра. Сравнение — на одной машине, с оговоркой про разное железо.

Инфраструктура: [`spla-bench/`](spla-bench/). Spla собирается из [`spla/`](spla/) в корне (иначе из `spla-bench/deps/spla` — см. `spla-bench/scripts/config.py`).

---

## Зависимости (Linux)

`cmake`, `g++` (C++17), `git`, **Python 3**, OpenCL (заголовки + ICD; для CPU без GPU — **POCL**). По желанию **`clinfo`**.

---

## Сборка

```bash
cd graph-theory-course/spla-bench
./scripts/build_tool.py lagraph   # GraphBLAS — см. SUITESPARSE в config.py
./scripts/build_tool.py spla
```

Вручную Spla: `cmake -S spla -B spla/build -DCMAKE_BUILD_TYPE=Release && cmake --build spla/build -j$(nproc)`.

---

## Замеры

```bash
cd graph-theory-course/spla-bench/scripts
python3 benchmark.py --tools lagraph spla --format csv --printer all
```

- Без `--algo` идут по очереди **bfs → sssp → tc → pr**; сочетание «граф + алгоритм» пропускается, если не все драйверы умеют (например SSSP без весов).
- Результаты: **`spla-bench/benchmarks/<дата>/`**, последний прогон — симлинк **`benchmarks/recent/`** (`bfs.csv`, `sssp.csv`, …).

Один алгоритм: `--algo bfs` (или `sssp`, `tc`, `pr`).

---

## Данные

- Папка **`graphs-theory-datasets/`** (рядом с `spla-bench`): матрицы **Matrix Market** `имя.mtx`. Имя набора = имя файла без `.mtx`.
- **Автосписок:** все подходящие `*.mtx` в этой папке (алфавит), минус вспомогательные файлы из архивов Suite Sparse (`*_nodename`, `*_nodeid`, `*_coord`, `*Communities*` — см. `_is_auxiliary_mtx_name` в `config.py`). Минус тяжёлый **`rgg_n_2_23_s0`**, пока не задано **`SPLA_BENCH_INCLUDE_HEAVY=1`**.
- **Явный список:** `SPLA_BENCH_DATASETS_JSON='["a","b"]'`.
- Нет локального `.mtx` — скрипт может скачать по **`DATASET_URL`** в `config.py`. Свойства графа кэшируются в **`properties.json`**.

| Алгоритм | Нужен тип значений в `.mtx` |
|----------|------------------------------|
| BFS, PR | pattern (void) |
| SSSP | float или int |
| TC | по правилам драйвера (обычно ваши pattern-графы ок) |

Проверка Spla SSSP на цепочке: `python3 spla-bench/scripts/test_sssp_toy.py` (нужен `spla/build/sssp`). Число повторов на граф — от размера (`DatasetSize` в `config.py`). Старт BFS/SSSP: **`DEFAULT_SOURCE`** в `config.py`.

PageRank: в LAGraph зашито **16** trial; драйвер Spla для PR передаёт столько же `--niters`.

---

## Переменные окружения (кратко)

| Переменная | Назначение |
|------------|------------|
| `LAGRAPH_NUM_THREADS` | Потоки для демо LAGraph |
| `SPLA_BENCH_DATASETS_JSON` | Список датасетов вместо авто |
| `SPLA_BENCH_INCLUDE_HEAVY` | `1` — включить `rgg_n_2_23_s0` в авто-режиме |
| `SPLA_OPENCL_PLATFORM` / `DEVICE` | Жёстко выбрать OpenCL |
| `SPLA_OPENCL_LOG` | `1` — лог выбора устройства |

---

## Частые проблемы

- Нет **`clinfo`** — выбор OpenCL может остаться `0,0`.
- **Dataset not found** — имя как у `.mtx`, файл в `graphs-theory-datasets/` или URL в `config.py`.
- **SSSP пустой** — нужны веса в MTX, не только pattern.
- Кэш **`properties.json`** устарел после замены файла с тем же именем — удалить строку или файл.

---

## Структура

```
graph-theory-course/
├── spla/                     # Spla + build/
├── graphs-theory-datasets/   # *.mtx
└── spla-bench/
    ├── scripts/config.py, benchmark.py, drivers/
    └── benchmarks/           # CSV по запускам
```

Детали апстрима `spla-bench` (Gunrock и т.д.): [`spla-bench/README.md`](spla-bench/README.md).
