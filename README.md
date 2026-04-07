# Графовые алгоритмы: LAGraph (CPU) vs Spla (OpenCL)

Сравнение **BFS, SSSP, TC, PageRank** на одних и тех же матрицах: **SuiteSparse GraphBLAS + LAGraph** и **Spla** через OpenCL.

| Что | Где считается |
|-----|----------------|
| LAGraph | CPU, многопоточный GraphBLAS. Потоки: `export LAGRAPH_NUM_THREADS=8` → скрипт выставит `OMP_NUM_THREADS` для демо. |
| Spla в бенчмарке | Только **POCL** (OpenCL на **CPU**). GPU в замерах **не** используется (`opencl_pick.py`). |

**Метрика времени:** LAGraph — время вокруг вызова в демо на CPU; Spla — лапы по `gpu(ms):` в примерах (имя поля историческое: хост вокруг OpenCL на **POCL-CPU**).

Инфраструктура: [`spla-bench/`](spla-bench/). Spla собирается из [`spla/`](spla/) в корне (иначе из `spla-bench/deps/spla` — см. `spla-bench/scripts/config.py`).

**Воспроизводимость:** ОС, коммит, `CMAKE_BUILD_TYPE`, компилятор; `clinfo -l` (платформа POCL) и при желании `SPLA_OPENCL_LOG=1`.

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

## Замеры и обновление результатов (оба стека на CPU)

По умолчанию `benchmark.py` запускает **только LAGraph и Spla**. Все четыре бэкенда spla-bench:  
`--tools graphblast gunrock lagraph spla`.

**Чтобы заново снять замеры** (LAGraph на CPU, Spla на **POCL/CPU**) и обновить CSV:

1. Убедиться, что установлен **POCL** и в `clinfo -l` видна платформа *Portable Computing Language*.
2. При необходимости пересобрать бинарники (см. § «Сборка»).
3. Выполнить:

```bash
cd graph-theory-course/spla-bench/scripts
python3 benchmark.py --format csv --printer all
```

Опционально перед прогоном: `export SPLA_OPENCL_LOG=1` — в логе будет строка `spla-opencl | picked` с индексами POCL.

4. Новые таблицы появятся в **`spla-bench/benchmarks/<дата-время>/`**; симлинк **`benchmarks/recent/`** укажет на этот прогон (`bfs.csv`, `sssp.csv`, `tc.csv`, `pr.csv`).
5. Обновите текст отчёта вручную: [`docs/benchmark-report.md`](docs/benchmark-report.md) (§2 и таблицы из свежих CSV).

Без `--algo` по очереди идут **bfs → sssp → tc → pr**; комбинации, где не все драйверы подходят к графу, пропускаются.

Один алгоритм: `--algo bfs` (или `sssp`, `tc`, `pr`).

Если POCL не на стандартных индексах: задайте **`export SPLA_OPENCL_PLATFORM=…`** и **`SPLA_OPENCL_DEVICE=…`** (см. `clinfo -l`).

---

## Данные

- Папка **`graphs-theory-datasets/`** (рядом с `spla-bench`): только **Matrix Market** `имя.mtx`. Файлы **`.mat` (MATLAB)** пайплайн не подхватывает — конвертируйте в `.mtx` или положите архив Suite Sparse с матрицей. Имя набора = имя файла без `.mtx`.
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
| `SPLA_OPENCL_PLATFORM` / `DEVICE` | Индексы POCL, если авто-поиск не подходит |
| `SPLA_OPENCL_LOG` | `1` — лог выбора устройства |

---

## Частые проблемы

- Нет **`clinfo`** — авто-выбор POCL не сработает; задайте `SPLA_OPENCL_PLATFORM`/`DEVICE` или установите `clinfo`.
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

Шаблон отчёта о замерах под требования курса: [`docs/benchmark-report.md`](docs/benchmark-report.md).

Детали апстрима `spla-bench` (Gunrock и т.д.): [`spla-bench/README.md`](spla-bench/README.md).
