# Отчёт о замерах: LAGraph vs Spla

**Текущий код:** бенчмарк Spla использует **только POCL (CPU)**

---

## 1. Соответствие требованиям (чеклист)

| Требование | Как зафиксировано в отчёте / репозитории |
|------------|------------------------------------------|
| Два стека: GraphBLAS+LAGraph и Spla | Таблицы **lagraph** / **spla**|
| Готовые реализации (демо LAGraph, примеры Spla) | `spla-bench/deps/lagraph/.../benchmark`, `spla/build/{bfs,sssp,tc,pr}` |
| Оба на CPU в бенчмарке | LAGraph — CPU; Spla — только **POCL** (OpenCL на CPU) |
| Набор данных в `graphs-theory-datasets/` |

---

## 2. Условия эксперимента

| Поле | Значение |
|------|----------|
| **ОС / ядро** | Ubuntu 24.04.3 LTS, Linux 6.17.0-20-generic |
| **CPU** | 11th Gen Intel Core i5-1135G7 @ 2.40GHz, 4 ядра, 8 потоков|
| **RAM** | 32 GB|
--

---
Полные метрики из CSV (warm_up, avg, median, stdev, мс)

Формат ячеек как в `benchmark.py --printer all`.

### BFS

| dataset | LAGraph | Spla |
|---------|---------|------|
| cit-Patents | warm_up=0.74, avg=1.50, median=1.50, stdev=0.99 | warm_up=0.00, avg=745.03, median=745.03, stdev=8.41 |
| coAuthorsCiteseer | warm_up=8.84, avg=6.54, median=6.50, stdev=0.62 | warm_up=0.00, avg=23.75, median=23.28, stdev=1.09 |
| coPapersDBLP | warm_up=24.82, avg=31.85, median=31.85, stdev=7.85 | warm_up=0.00, avg=90.79, median=90.79, stdev=1.48 |
| com-Orkut | warm_up=150.07, avg=50.60, median=50.60, stdev=1.41 | warm_up=0.00, avg=335.94, median=335.94, stdev=4.34 |
| hollywood-2009 | warm_up=93.10, avg=39.00, median=39.00, stdev=13.15 | warm_up=0.00, avg=128.87, median=128.87, stdev=2.17 |
| indochina-2004 | warm_up=1.42, avg=4.15, median=4.15, stdev=0.35 | warm_up=0.00, avg=1637.57, median=1637.57, stdev=48.85 |
| roadNet-CA | warm_up=149.62, avg=152.40, median=152.40, stdev=0.57 | warm_up=0.00, avg=291.30, median=291.30, stdev=3.51 |
| road_central | warm_up=1396.58, avg=1479.25, median=1479.25, stdev=31.61 | warm_up=0.00, avg=3075.39, median=3075.39, stdev=16.62 |
| soc-LiveJournal1 | warm_up=250.72, avg=186.70, median=186.70, stdev=40.02 | warm_up=0.00, avg=474.45, median=474.45, stdev=3.98 |

### SSSP

| dataset | LAGraph | Spla |
|---------|---------|------|
| sssp_balanced_tree_127 | warm_up=0.00, avg=0.78, median=0.60, stdev=0.71 | warm_up=0.00, avg=0.05, median=0.05, stdev=0.01 |
| sssp_grid_20_weighted | warm_up=0.00, avg=1.95, median=1.90, stdev=0.28 | warm_up=0.00, avg=1.62, median=1.57, stdev=0.14 |
| sssp_random_200_weighted | warm_up=0.00, avg=1.20, median=1.10, stdev=0.16 | warm_up=0.00, avg=0.23, median=0.23, stdev=0.02 |
| sssp_toy_weighted | warm_up=0.00, avg=0.20, median=0.10, stdev=0.54 | warm_up=0.00, avg=0.02, median=0.02, stdev=0.01 |

### TC

| dataset | LAGraph | Spla |
|---------|---------|------|
| cit-Patents | warm_up=629.05, avg=618.86, median=621.92, stdev=64.73 | warm_up=0.00, avg=1878.63, median=1878.63, stdev=88.49 |
| coAuthorsCiteseer | warm_up=18.85, avg=17.45, median=15.77, stdev=3.76 | warm_up=0.00, avg=61.18, median=62.13, stdev=8.47 |
| coPapersDBLP | warm_up=414.13, avg=486.29, median=469.82, stdev=40.27 | warm_up=0.00, avg=2365.57, median=2365.57, stdev=144.57 |
| com-Orkut | warm_up=17451.52, avg=19021.76, median=18963.37, stdev=144.61 | warm_up=0.00, avg=69331.05, median=69331.05, stdev=392.66 |
| hollywood-2009 | warm_up=12360.31, avg=12399.13, median=12370.96, stdev=50.42 | warm_up=0.00, avg=75926.95, median=75926.95, stdev=592.77 |
| indochina-2004 | warm_up=37304.38, avg=28713.91, median=28828.04, stdev=433.36 | warm_up=0.00, avg=325158.50, median=325158.50, stdev=3066.72 |
| roadNet-CA | warm_up=49.48, avg=43.98, median=42.43, stdev=3.07 | warm_up=0.00, avg=63.02, median=63.02, stdev=14.52 |
| road_central | warm_up=418.35, avg=413.87, median=421.88, stdev=14.41 | warm_up=0.00, avg=697.24, median=697.24, stdev=48.59 |
| soc-LiveJournal1 | warm_up=2404.06, avg=2877.44, median=2961.78, stdev=212.46 | warm_up=0.00, avg=10768.65, median=10768.65, stdev=323.78 |
| sssp_toy_weighted | warm_up=0.02, avg=0.01, median=0.01, stdev=0.00 | warm_up=0.00, avg=0.00, median=0.00, stdev=0.00 |

### PageRank

| dataset | LAGraph | Spla |
|---------|---------|------|
| cit-Patents | warm_up=0.00, avg=327.09, median=324.40, stdev=65.39 | warm_up=0.00, avg=543.70, median=524.09, stdev=47.30 |
| coAuthorsCiteseer | warm_up=0.00, avg=70.60, median=67.55, stdev=32.82 | warm_up=0.00, avg=10.14, median=9.99, stdev=0.56 |
| coPapersDBLP | warm_up=0.00, avg=276.96, median=277.05, stdev=3.14 | warm_up=0.00, avg=127.83, median=126.45, stdev=4.41 |
| com-Orkut | warm_up=0.00, avg=4505.99, median=4318.25, stdev=374.50 | warm_up=0.00, avg=1889.12, median=1863.34, stdev=71.02 |
| hollywood-2009 | warm_up=0.00, avg=976.84, median=944.65, stdev=80.40 | warm_up=0.00, avg=979.92, median=979.62, stdev=5.12 |
| indochina-2004 | warm_up=0.00, avg=2610.93, median=2601.60, stdev=63.87 | warm_up=0.00, avg=2571.21, median=2559.86, stdev=43.60 |
| roadNet-CA | warm_up=0.00, avg=214.26, median=211.00, stdev=12.42 | warm_up=0.00, avg=99.15, median=98.16, stdev=3.35 |
| road_central | warm_up=0.00, avg=2550.67, median=2455.05, stdev=195.69 | warm_up=0.00, avg=534.76, median=529.65, stdev=17.56 |
| soc-LiveJournal1 | warm_up=0.00, avg=1876.21, median=1871.10, stdev=17.08 | warm_up=0.00, avg=1436.25, median=1429.61, stdev=18.74 |

---

## Где лежат сырые данные

- `spla-bench/benchmarks/recent/*.csv`

---

## Как провести замер

1. `python3 benchmark.py` из `spla-bench/scripts`.
