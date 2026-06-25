---
marp: true
theme: default
paginate: true
size: 16:9
---

# Оценка масштабируемости распределенной обработки графов с помощью Galois

**Усольцев Данил**

---

## Постановка задачи

**Цель:** исследовать, как меняется время выполнения графовых алгоритмов при росте числа MPI-процессов в Galois Distributed.

**Алгоритмы:**

- BFS
- PageRank
- SSSP
- Triangle Counting

**Основной вопрос:** когда распределённое выполнение сокращает полное время запуска, а когда накладные расходы MPI, синхронизации и репликации делают его медленнее?

---

## Экспериментальная методология

Параметры запусков:

- MPI-процессы: `1, 2, 4, 6, 8`
- Количество повторов: `--runs=20`
- Запуск: `mpirun --hostfile experiments/hostfile --oversubscribe --bind-to none`

---

## Аппаратная и программная среда

- ОС: Ubuntu 24.04.3 LTS
- CPU: 11th Gen Intel Core i5-1135G7 @ 2.40 GHz, 4 ядра, 8 потоков, RAM: 32GB
- Кэш L1: 320 KiB, Кэш L2: 5 MiB, Кэш L3: 8 MiB

---

## Наборы данных

<style scoped>
.datasets-table th:nth-child(2),
.datasets-table th:nth-child(3),
.datasets-table td:nth-child(2),
.datasets-table td:nth-child(3) {
  white-space: nowrap;
}
</style>

<div class="datasets-table">

| Граф | Вершин | Рёбер | Структура |
|---|---:|---:|---|
| `roadNet-PA` | 1 090 920 | 3 083 796 | дорожная сеть: вершины связаны почти равномерно, дальние точки соединяются длинными путями |
| `web-Google` | 916 428 | 5 105 039 | web-граф: есть страницы-хабы с большим числом ссылок, остальные имеют мало связей |
| `wiki-talk-temporal` | 1 140 149 | 7 833 140 | граф обсуждений: активность распределена неравномерно, есть очень активные участники и темы |

</div>

---

## Метрики

<style scoped>
.small {
  font-size: 0.78em;
}
.small table {
  margin: 0;
}
.small th,
.small td {
  padding: 0.25em 0.45em;
}
</style>

<div class="small">


| Метрика | Что означает 
|---|---|
| `total_time_exec` | среднее время одного run алгоритма |
| `sync_time` | время синхронизаций Gluon между MPI-процессами | 
| `sync_bytes` | объём данных, переданных в фазе sync 
| `replication_factor` | среднее число копий вершины на границах разбиения | 
| `inspect_bytes` | объём служебного обмена при согласовании распределения графа |
| `load_bytes` | объём переданных рёбер при подготовке распределённого графа |

</div>

---

# BFS

---

## BFS: roadNet-PA

![height:560px BFS roadNet-PA](plots/bfs/by_dataset/bfs_roadNet-PA.png)

---

## BFS: web-Google

![height:560px BFS web-Google](plots/bfs/by_dataset/bfs_web-Google.png)

---

## BFS: wiki-talk-temporal

![height:560px BFS wiki-talk-temporal](plots/bfs/by_dataset/bfs_wiki-talk-temporal.png)

---

## BFS: почему roadNet сильно деградирует

Для roadNet-PA:

- `total_time_exec`: 2800 ms -> 85824 ms
- `sync_time`: 1.5 ms -> 49 534 ms
- количество BFS-раундов: около 317

Причина:

```text
total sync cost ~= число BFS-уровней * стоимость sync одного уровня
```

Дорожный граф имеет большой диаметр, поэтому даже маленькая стоимость одной синхронизации умножается на сотни раундов.

---

# PageRank

---

## PageRank: roadNet-PA

![height:560px PageRank roadNet-PA](plots/pr/by_dataset/pr_roadNet-PA.png)

---

## PageRank: web-Google

![height:560px PageRank web-Google](plots/pr/by_dataset/pr_web-Google.png)

---

## PageRank: wiki-talk-temporal

![height:560px PageRank wiki-talk-temporal](plots/pr/by_dataset/pr_wiki-talk-temporal.png)

---

## PageRank: почему графы деградируют

<style scoped>
.small {
  font-size: 0.78em;
}
.small p,
.small ul {
  margin: 0.25em 0;
}
</style>

<div class="small">

Для roadNet-PA:

- `replication_factor`: 1.0 -> 1.03
- `sync_bytes`: 0 -> 3.8 MB
- `total_time_exec`: 2280 ms -> 10453 ms

Для web-Google:

- `replication_factor`: 1.0 -> 2.98
- `sync_bytes`: 0 -> 136 MB
- `total_time_exec`: 2805 ms -> 17660 ms

Для wiki-talk:

- `replication_factor`: 1.0 -> 2.49
- `sync_bytes`: 0 -> 152 MB
- `total_time_exec`: 5618 ms -> 23950 ms

PageRank передаёт значения рангов на границах разбиения. Поэтому рост числа MPI-процессов увеличивает не только параллелизм, но и объём коммуникации.

</div>

---

# SSSP

---

## SSSP: roadNet-PA

![height:560px SSSP roadNet-PA](plots/sssp/by_dataset/sssp_roadNet-PA.png)

---

## SSSP: web-Google

![height:560px SSSP web-Google](plots/sssp/by_dataset/sssp_web-Google.png)

---

## SSSP: wiki-talk-temporal

![height:560px SSSP wiki-talk-temporal](plots/sssp/by_dataset/sssp_wiki-talk-temporal.png)

---

## SSSP: почему `total_time_exec` деградирует

- `roadNet-PA`: большой диаметр и лимит `maxIterations=200`, поэтому стоимость синхронизаций накапливается: `sync_time` 2 ms -> 31 334 ms.
- `web-Google`: из-за вершин-хабов граф плохо делится на независимые части. Одни и те же вершины приходится хранить на нескольких MPI-процессах, поэтому растёт обмен данными: `sync_bytes` 0 -> 10.4 MB.
- `wiki-talk`: сам запуск очень короткий, поэтому даже 495 ms `sync_time` при MPI=8 полностью доминируют над `total_time_exec`.

Итог: во всех случаях MPI добавляет синхронизации, proxy-данные и ожидание rank'ов быстрее, чем сокращает полное время одного run.

---

# Triangle Counting

---

## Triangle Counting: roadNet-PA

![height:560px TC roadNet-PA](plots/tc/by_dataset/tc_roadNet-PA.png)

---

## Triangle Counting: web-Google

![height:560px TC web-Google](plots/tc/by_dataset/tc_web-Google.png)

---

## Triangle Counting: wiki-talk-temporal

![height:560px TC wiki-talk-temporal](plots/tc/by_dataset/tc_wiki-talk-temporal.png)

---

## TC: отличие от BFS/PR/SSSP

Для Triangle Counting:

- `sync_time = 0`
- `sync_bytes = 0`
- основное время уходит на `inspect_bytes`, `load_bytes`, proxy-рёбра и global reduce

---

## TC: ключевые наблюдения

| Граф | MPI=1 | MPI=8 | Главная причина |
|---|---:|---:|---|
| roadNet-PA | 120 ms | 327 ms | граф простой для TC: треугольников мало, поэтому накладные расходы MPI заметнее самой работы |
| web-Google | 1972 ms | 2356 ms | из-за страниц-хабов появляются копии рёбер и больше служебных данных между процессами |
| wiki-talk | 7082 ms | 13974 ms | нагрузка делится неравномерно: часть процессов получает более тяжёлые участки графа |

Во всех трёх случаях лучший `total_time_exec` — MPI=1.

---


## Сравнение алгоритмов: лучший `total_time_exec`

| Алгоритм | roadNet-PA | web-Google | wiki-talk |
|---|---:|---:|---:|
| BFS | MPI=1 | MPI=1 | MPI=1 |
| PageRank | MPI=1 | MPI=1 | MPI=1 |
| SSSP | MPI=1 | MPI=1 | MPI=1 |
| TC | MPI=1 | MPI=1 | MPI=1 |

Итог: распределённое выполнение увеличивает накладные расходы быстрее, чем сокращает полное время запуска.
