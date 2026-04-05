# Курс: сравнение графовых алгоритмов через линейную алгебру

В репозитории настроено **сравнение производительности** двух линеарно-алгебраических стеков:

| Стек | Роль в эксперименте | Где выполняется работа |
|------|---------------------|-------------------------|
| **SuiteSparse:GraphBLAS + LAGraph** | «Классика» GraphBLAS: BFS, SSSP, TC, **PageRank** (`gappagerank_demo`) | **CPU** (мультипоточная реализация GraphBLAS; число потоков задаётся внутри демо LAGraph, по умолчанию видно в логе, напр. `threads 8`) |
| **Spla** | BFS, SSSP, TC и **PageRank** ([`spla/examples/pr.cpp`](spla/examples/pr.cpp)), бэкенд **OpenCL** | Ускоритель выбирается автоматически или вручную: **GPU (OpenCL)** или **CPU через POCL** (Portable Computing Language), если отдельной GPU нет |

Инфраструктура замеров: каталог [`spla-bench/`](spla-bench/). Исходники Spla для сборки берутся из корня репозитория [`spla/`](spla/), если эта папка есть; иначе — из `spla-bench/deps/spla` (см. `spla-bench/scripts/config.py`).

---

## 1. Что именно измеряется

- **LAGraph**: время серии запусков из демо (`bfs_demo`, `sssp_demo`, `tc_demo`, `gappagerank_demo`). Скрипт парсит строки вида `Avg: ...` / `trial ...` и переводит в миллисекунды для отчёта. Для **PageRank** демо внутри всегда выполняет **16 trial**; параметр `niters` бенчмарка на это не влияет (см. `gappagerank_demo.c`).
- **Spla**: для честного сравнения с «ускорителем» в драйвере бенчмарка отключены эталон и чисто-CPU путь примеров: передаются флаги `--run-cpu=false --run-ref=false --run-gpu=true`. В отчёт попадают **лапы по строке `gpu(ms):`** (время шагов на стороне хоста вокруг OpenCL-исполнения; это не чистый GPU kernel time, но согласованная метрика для прогонов). Для **PR** используется тот же формат вывода, что у `bfs`/`tc` ([`pr.cpp`](spla/examples/pr.cpp)); параметры `alpha` и `eps` — значения по умолчанию из `options.hpp`.

**Важно для защиты:** вы сравниваете *реализации на разном железе*: многопоточный GraphBLAS на CPU против Spla на выбранном OpenCL-устройстве. Итог зависит от машины, драйверов и размера графа.

---

## 2. Какие данные используются

### 2.1. Локальная папка `graphs-theory-datasets/`

Если в **родительском** каталоге относительно `spla-bench` есть папка `graphs-theory-datasets/`, она автоматически становится источником матриц (см. `DATASET_FOLDER` в `spla-bench/scripts/config.py`).

Ожидаемый формат: **Matrix Market** (`.mtx`). Имя набора в конфиге должно совпадать с именем файла **без** `.mtx` (например, `coAuthorsCiteseer` → `coAuthorsCiteseer.mtx`).

Типичный набор для отчёта:

| Имя в конфиге | Файл | Комментарий |
|---------------|------|-------------|
| `coAuthorsCiteseer` | `coAuthorsCiteseer.mtx` | co-authorship, pattern symmetric |
| `coPapersDBLP` | `coPapersDBLP.mtx` | крупнее |
| `hollywood-2009` | `hollywood-2009.mtx` | очень крупный для TC |
| `rgg_n_2_23_s0` | `rgg_n_2_23_s0.mtx` | **очень тяжёлый** (миллионы вершин); по умолчанию **не входит** в список замеров |

Графы из коллекции чаще **неориентированные / симметричные**; алгоритмы в демо ориентированы на работу с матрицей смежности как с разреженной структурой.

### 2.2. Автозагрузка с Suite Sparse Matrix Collection

В `spla-bench/scripts/config.py` в словаре **`DATASET_URL`** заданы URL архивов с [sparse.tamu.edu](https://sparse.tamu.edu/). Если локального файла нет, скрипт может скачать архив и извлечь `.mtx` (имя ключа = имя `.mtx` в архиве).

### 2.3. Кэш свойств графов

При первом обращении к матрице скрипт вычисляет (и кэширует в **`graphs-theory-datasets/properties.json`**, если используется эта папка):

- ориентированность (по структуре матрицы);
- тип значений: `void` (pattern), `float`, `int` — от этого зависит, **какой алгоритм можно запустить** (см. ниже).

---

## 3. Какой алгоритм на каких данных допустим

Логика в драйверах `spla-bench/scripts/drivers/driver_lagraph.py` и `driver_spla.py`:

| Алгоритм | Условие на `.mtx` |
|----------|-------------------|
| **BFS** | тип значений **pattern / void** (есть только структура рёбер) |
| **SSSP** | тип значений **float** (веса рёбер) |
| **TC** (треугольники) | запускается на доступных матрицах по правилам драйвера (для ваших pattern-графов — да) |
| **PR** (PageRank) | **pattern / void**, как и BFS: в [`pr.cpp`](spla/examples/pr.cpp) из структуры рёбер считаются степени вершин и строится взвешенная `float`-матрица для итераций PageRank |

Поэтому на текущих наборах из `graphs-theory-datasets/` **SSSP обычно пропускается** (в логе: `not runnable on some drivers, skipping`). Чтобы замерить SSSP, добавьте матрицу с вещественными весами и имя в список датасетов.

Число **повторов** одного алгоритма на графе зависит от числа рёбер: в `config.py` заданы пороги `DatasetSize` (tiny / small / …), а в `drivers/driver.py` вызывается `dataset.get_category().iterations()`.

Стартовая вершина для BFS/SSSP: **`DEFAULT_SOURCE`** в `config.py` (по умолчанию `0`).

---

## 4. Что проверяется: CPU vs GPU / POCL

### 4.1. LAGraph

Всегда используется связка **LAGraph + libgraphblas** из сборки под вашу ОС. Вычисления — **на CPU** (параллелизм внутри SuiteSparse).

### 4.2. Spla (OpenCL)

1. При старте драйвера один раз вызывается **`clinfo -l`** (если доступен).
2. В `spla-bench/scripts/lib/opencl_pick.py` выбирается платформа/устройство:
   - предпочтение **не-POCL** платформам, похожим на GPU (в т.ч. Intel Graphics, NVIDIA, AMD и т.д.);
   - если подходящего нет — остаётся **POCL** (CPU как OpenCL-устройство).
3. В примеры Spla передаются `--platform=…` и `--device=…`.

**Принудительно POCL (или другая платформа):**

```bash
export SPLA_OPENCL_PLATFORM=1   # номер из `clinfo -l`
export SPLA_OPENCL_DEVICE=0
```

**Проверка списка устройств:**

```bash
clinfo -l
```

---

## 5. Подготовка окружения (Linux)

Установите (имена пакетов зависят от дистрибутива):

- **Сборка:** `cmake`, `make`, `g++` (C++17), `git`
- **OpenCL:** заголовки и ICD-loader; для GPU — драйвер с OpenCL; для CPU без GPU — **POCL**
- **Python 3** для скриптов в `spla-bench/scripts/`
- **GraphBLAS** подтянется при сборке LAGraph согласно `SUITESPARSE` в `config.py` (по умолчанию — клонирование и сборка из репозитория, см. раздел ниже)

---

## 6. Сборка (первый раз и после изменений кода)

Рабочая директория для команд — **`spla-bench/scripts/`** или корень `spla-bench` с путём к скриптам.

### 6.1. Только LAGraph и GraphBLAS

```bash
cd /path/to/graph-theory-course/spla-bench
./scripts/build_tool.py lagraph
```

При необходимости правьте в **`scripts/config.py`** блок **`SUITESPARSE`**: ровно один способ — локальные пути, сборка из `repo`, или `download` из conda (см. комментарии в файле).

### 6.2. Только Spla (из корневого `spla/`)

Сборка запускается тем же скриптом (пути берутся из `config.py`):

```bash
./scripts/build_tool.py spla
```

Или вручную:

```bash
cd /path/to/graph-theory-course/spla
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)
```

Должны появиться бинарники: `spla/build/bfs`, `spla/build/sssp`, `spla/build/tc`.

### 6.3. Параллельная сборка и компиляторы

В `config.py` секция **`BUILD`**: `jobs`, при необходимости `cc` / `cxx`. Флаги `./scripts/build_tool.py -j 8` переопределяют число потоков make.

---

## 7. Запуск замеров

### 7.1. Сравнение LAGraph и Spla за один прогон (рекомендуется для отчёта)

Из каталога **`spla-bench/scripts`**:

```bash
cd /path/to/graph-theory-course/spla-bench/scripts
python3 benchmark.py --tools lagraph spla
```

- Если **не** указывать `--algo`, по очереди выполняются **bfs**, **sssp**, **tc**, **pr**; для каждого датасета, где не все инструменты могут работать, комбинация **пропускается** (например, SSSP на pattern-матрицах).
- Результаты одного такого запуска попадают в **одну** временную папку; в ней будет несколько файлов: `bfs.csv`, `tc.csv`, `pr.csv` и т.д.

### 7.2. Только один алгоритм

```bash
python3 benchmark.py --tools lagraph spla --algo bfs
python3 benchmark.py --tools lagraph spla --algo tc
python3 benchmark.py --tools lagraph spla --algo pr
```

### 7.3. Формат вывода

```bash
python3 benchmark.py --tools lagraph spla --format csv --printer all
```

- **`--printer all`** — в CSV попадает строка с warm-up, средним, медианой, std.
- **`--printer median`** — только медиана.

### 7.4. Куда пишутся результаты

- Каталог: **`spla-bench/benchmarks/<дата-время>/`**
- Симлинк на последний прогон: **`spla-bench/benchmarks/recent/`** → указывает на последнюю папку (после **каждого** запуска пересоздаётся).

Старые папки с временем в имени **не удаляются** — для защиты можно открыть конкретный каталог, например `benchmarks/Sun Apr  5 22:58:48 2026/tc.csv`.

---

## 8. Настройка списка графов без правки `config.py`

По умолчанию в замерах **три** графа (без `rgg_n_2_23_s0`), чтобы прогон укладывался в разумное время.

**Полный список из четырёх файлов:**

```bash
export SPLA_BENCH_DATASETS_JSON='["coAuthorsCiteseer","coPapersDBLP","hollywood-2009","rgg_n_2_23_s0"]'
cd /path/to/graph-theory-course/spla-bench/scripts
python3 benchmark.py --tools lagraph spla
```

**Только быстрая проверка на одном графе:**

```bash
export SPLA_BENCH_DATASETS_JSON='["coAuthorsCiteseer"]'
python3 benchmark.py --tools lagraph spla --algo bfs
```

---

## 9. Как интерпретировать CSV на защите

- Столбцы: **`dataset`**, затем по одному столбцу на инструмент (**`lagraph`**, **`spla`**).
- В ячейке — агрегаты по серии запусков (медиана и др. при `--printer all`).
- **Прямое сравнение чисел** имеет смысл как «на этой машине, на этих датасетах, с такими настройками OpenCL»; для другого ПК перезапустите тот же сценарий.

Краткая качественная картина (может отличаться на вашем железе):

- На **малых** графах Spla на OpenCL иногда выигрывает за счёт ускорителя и меньшего оверхеда относительно тяжёлого CPU-пути.
- На **крупных** графах и **TC** зрелая реализация **LAGraph + GraphBLAS** на CPU часто оказывается быстрее **Spla на встроенной GPU / OpenCL** — это нормальный результат для учебного сравнения, его важно уметь объяснить (пропускная способность памяти, оптимизации SuiteSparse, неидеальное использование GPU на нерегулярных графах).

---

## 10. Типичные проблемы

| Симптом | Что проверить |
|---------|----------------|
| Нет `clinfo` | Установить пакет `clinfo`; иначе выбор платформы упрётся в `(0,0)` |
| Spla падает при OpenCL | Драйвер GPU, переменные `OCL_ICD_VENDORS`, установка POCL |
| LAGraph не собирается | Ветка GraphBLAS в `SUITESPARSE.repo`, версия компилятора, зависимости |
| «Dataset not found» | Имя в `BENCHMARK_DATASETS` / JSON = имя файла `.mtx` без расширения; путь `graphs-theory-datasets/` |
| Пустой или странный SSSP | Нужны `.mtx` с **вещественными** весами, не pattern |
| Старый кэш свойств | Удалить или поправить `graphs-theory-datasets/properties.json` при смене файла с тем же именем |

---

## 11. Структура репозитория (для ориентации)

```
graph-theory-course/
├── README.md                 ← этот файл
├── spla/                     ← Spla (OpenCL), сборка build/
├── graphs-theory-datasets/   ← локальные .mtx для замеров
└── spla-bench/               ← скрипты, deps/lagraph, результаты benchmarks/
    ├── scripts/
    │   ├── config.py         ← пути, датасеты, GraphBLAS, BUILD
    │   ├── benchmark.py      ← запуск замеров
    │   └── drivers/          ← lagraph vs spla, парсинг времени
    └── benchmarks/           ← выходные CSV по времени запуска
```

Оригинальное описание апстрим-проекта `spla-bench` (Gunrock, GraphBLAST и т.д.) см. в [`spla-bench/README.md`](spla-bench/README.md); для курсового сценария «LAGraph vs Spla» достаточно команд из разделей 6–8 этого файла.

---

## 12. Шпаргалка одним блоком (для демонстрации)

```bash
# 1) Сборка (один раз)
cd graph-theory-course/spla-bench
./scripts/build_tool.py lagraph
./scripts/build_tool.py spla

# 2) Замеры LAGraph (CPU) vs Spla (OpenCL)
cd scripts
python3 benchmark.py --tools lagraph spla --format csv --printer all

# 3) Результаты
ls -la ../benchmarks/recent/
```

На защите отдельно проговорите: **какие графы**, **что считается временем**, **где CPU (LAGraph)**, **где OpenCL (Spla)** и при необходимости покажите `clinfo -l` и выбор POCL через `SPLA_OPENCL_PLATFORM`.
