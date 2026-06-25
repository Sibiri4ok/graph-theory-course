
# Оценка масштабируемости распределенной обработки графов с помощью Galois

```bash
pip install -r requirements.txt
```

## Запуск

```bash
./run_bench.sh
```

Скрипт прогоняет все комбинации алгоритмов, графов и числа MPI-процессов (по умолчанию 1, 2, 4, 6, 8). Уже успешно выполненные прогоны пропускаются (проверка по файлам в `results/stats/`).


## Графы (`datasets/`)

| Граф | Файлы | Вершин | Рёбер |
|------|-------|--------|-------|
| web-Google | `web-Google.*` | 916 428 | 5 105 039 |
| roadNet-PA | `roadNet-PA.*` | 1 090 920 | 3 083 796 |
| wiki-talk-temporal | `wiki-talk-temporal.*` | 1 140 149 | 7 833 140 |


## Результаты (`results/`)

- `results/stats/` — файлы статистики (`<algo>_<graph>_<np>p.stats`)
- `results/run.log` — лог прогонов
- `results/hostfile` — конфигурация MPI-хостов (по умолчанию localhost, 8 слотов)
