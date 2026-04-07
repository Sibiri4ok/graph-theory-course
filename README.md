# Графовые алгоритмы: LAGraph (CPU) vs Spla (OpenCL)

Сравнение **BFS, SSSP, TC, PageRank** на одних и тех же матрицах: **SuiteSparse GraphBLAS + LAGraph** и **Spla** через OpenCL.

| Что | Где считается |
|-----|----------------|
| LAGraph | CPU, многопоточный GraphBLAS |
| Spla в бенчмарке | **POCL** (OpenCL на **CPU**)|

**Метрика времени:** LAGraph — время вокруг вызова в демо на CPU; Spla — лапы по `gpu(ms):` в примерах (имя поля историческое: хост вокруг OpenCL на **POCL-CPU**).

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
---

## Замеры и обновление результатов

benchmark.py` запускает **LAGraph и Spla**

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

---

## Данные

- Папка **`graphs-theory-datasets/`**).

## Переменные окружения (кратко)

| Переменная | Назначение |
|------------|------------|
| `LAGRAPH_NUM_THREADS` | Потоки для демо LAGraph |
| `SPLA_BENCH_DATASETS_JSON` | Список датасетов вместо авто |
---


