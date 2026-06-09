# Воспроизведение эксперимента

## Что нужно заранее

1. Собранный Galois: `Galois/build/lonestar/analytics/distributed/{bfs,pagerank,sssp,triangle-counting}/*-dist`
2. Графы в `datasets/` (для TC на wiki-talk — `wiki-talk-temporal-clean.sgr`)
3. Open MPI, в `experiments/hostfile` — `hostname slots=8` (или ваш хост)
4. Python 3

## Порядок запуска

### 1. (Опционально) Список команд без прогона

```bash
cd /home/danil/graph-theory-task-2
bash experiments/generate_commands.sh
```

Создаёт `experiments/COMMANDS.sh` (60 команд). Бенчмарки не запускаются.

### 2. Полный прогон

```bash
cd /home/danil/graph-theory-task-2
bash experiments/run_all.sh
```

- Пропускает прогоны, для которых уже есть валидный `experiments/results/stats/*.stats`
- Лог: `experiments/results/run.log`
- После завершения обновляет `experiments/REPORT.md`
- **`experiments/report.csv` не перезаписывается** (финальная таблица метрик)

Долгий прогон в фоне:

```bash
nohup bash experiments/run_all.sh > experiments/results/nohup.out 2>&1 &
```

### 3. (Опционально) Только MPI = 2

Если нужно перезапустить только 12 прогонов с `-np 2`:

```bash
bash experiments/run_mpi2.sh
```

### 4. Отчёт по уже собранным `.stats`

```bash
python3 experiments/build_report.py
```

Проверка одного файла статистики:

```bash
python3 experiments/parse_galois_stat.py experiments/results/stats/bfs_web-Google_4p.stats
```

## Параметры эксперимента

| Параметр | Значение |
|----------|----------|
| MPI processes | 1, 2, 4, 6, 8 |
| Потоки (`-t`) | 2 |
| Повторы (`--runs`) | 3 |
| Датасеты | web-Google, roadNet-PA, wiki-talk-temporal |
| Алгоритмы | BFS, PageRank, SSSP, Triangle Counting |

## Графы по алгоритму

| Алгоритм | Файл | Доп. флаги |
|----------|------|------------|
| BFS | `*.sgr` | `--symmetricGraph` |
| PageRank | `*.gr` | `--graphTranspose=*.tgr` |
| SSSP | `*-w.gr` | при np>1: `--graphTranspose=*.tgr` |
| TC | `*.sgr` (wiki-talk: `*-clean.sgr`) | `--symmetricGraph` |

## Важно для MPI

- В командах: `--oversubscribe --bind-to none` (без `--bind-to none` при np=2 Open MPI может развести ранги по разным CPU и Galois падает в ThreadPool).
- Для np=6 и 8 нужен `--oversubscribe`, если OMPI видит меньше слотов, чем процессов.

## Файлы результатов

| Файл | Назначение |
|------|------------|
| `experiments/results/stats/*.stats` | сырой вывод `-statFile` |
| `experiments/results/run.log` | лог прогонов; байты inspect/load для BFS/PR/SSSP |
| `experiments/report.csv` | все метрики (60 строк) |
| `experiments/REPORT.md` | краткие сводные таблицы |
| `experiments/METRICS_GUIDE.md` | описание колонок CSV |

## Структура скриптов

```
experiments/
  config.sh              # общие пути и параметры
  run_all.sh             # основной прогон + build_report
  generate_commands.sh   # только COMMANDS.sh
  run_mpi2.sh            # перезапуск np=2
  parse_galois_stat.py   # парсер .stats
  parse_run_log.py       # байты из run.log
  build_report.py        # REPORT.md из .stats
```
