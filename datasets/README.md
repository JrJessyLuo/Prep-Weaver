# Prep-Weaver Benchmarks

Three data-preparation benchmarks. Each directory holds one `benchmark.jsonl`,
one JSON object per line, one line per task.

| Directory | Source benchmark | Tasks | Character |
|---|---|---|---|
| `Synth-Bird/` | nl2sql-bird | 141 | Synthetic prep tasks over BIRD databases |
| `Synth-Spider/` | nl2sql-spider | 103 | Synthetic prep tasks over Spider databases |
| `Beaver-Prep/` | beaver | 119 | Real enterprise data warehouse (MIT), 96-table collection |

**Task**: given a natural-language question and a pool of candidate tables,
produce the minimal joinable subtables plus a joinability specification
(which columns join which tables).

Only `benchmark.jsonl` is in this repository. The table data (`*.pkl` pandas
DataFrames), the gold answers, the relation files and Beaver's column profiling
are **downloaded separately** — see below. The fields documented here reference
them by file name.

---

## 0. Getting the data

Download from:

> https://drive.google.com/drive/u/0/folders/1sL9wdeCPw5HNEf7yD0hx3HlxzAc0K3lM

and unpack each dataset's folders **into its directory here**, so the result is:

```
datasets/
├── README.md                     this file            (in the repo)
├── Synth-Bird/
│   ├── benchmark.jsonl           141 tasks            (in the repo)
│   ├── input_tables/             374 candidate tables (download)
│   ├── answer/                   gold answer tables   (download)
│   └── tables_rels/              gold subtables + sqlite (download)
├── Synth-Spider/
│   ├── benchmark.jsonl           103 tasks            (in the repo)
│   ├── input_tables/             347 candidate tables (download)
│   ├── answer/                                        (download)
│   └── tables_rels/                                   (download)
└── Beaver-Prep/
    ├── benchmark.jsonl           119 tasks            (in the repo)
    ├── profiles/                 column profiling     (download)
    ├── input_tables/             96 warehouse tables  (download)
    ├── answer/                                        (download)
    └── tables_rels/                                   (download)
```

Nothing else has to be configured: every stage finds its data here by dataset
name. Check what resolved before running anything expensive:

```bash
cd ../codes
python -c "from common import dataset as D; d = D.resolve('Synth-Bird'); \
           print(d.input_tables); print('missing:', d.missing() or 'nothing')"
```

`missing: nothing` means the dataset is ready. Anything listed is a folder that
was not unpacked to the right place.

If the data has to live elsewhere (a shared scratch disk, say), point at it
instead of copying:

```bash
export PREPWEAVER_DATA_ROOT=/path/holding/<Dataset>/...
```

`Beaver-Prep/profiles/` is only read by `table_discovery.run_pipeline`, the
retrieval stage that Beaver alone needs. It is 81 MB, dominated by
`dev_jaccard.json` (the pairwise value-containment profile), which is why it is
distributed rather than committed.

---

## 1. Task identity and inputs

| Field | Type | Meaning |
|---|---|---|
| `task_id` | str | Unique id. `bird_<hex>` / `spider_<hex>` / `beaver-<hex>`. Note Beaver uses a hyphen. |
| `question` | str | The natural-language question. |
| `db_id` | str | Source database (`card_games`, `video_game`, `dw`, …). |
| `origin_idx` | int | Row index in the original NL2SQL benchmark this task was derived from. |
| `input_table` | list[str] | Candidate table files, e.g. `bird_058b8e3b_input_0.pkl`. In Synth-* the **first `relevant_table_num` entries are the gold tables** (positional convention). |
| `difficulty` | str | Difficulty label inherited from the source benchmark (Synth-* only; `none` where unlabelled). |
| `sampled` | bool | Whether the task was drawn by sampling (Synth-Bird only). |

### Beaver-only input fields

| Field | Type | Meaning |
|---|---|---|
| `table_collection` | list[str] | The full warehouse table list (96 tables) the retriever searches over. |
| `retrieved_table` | list[str] | Top-10 tables returned by retrieval. **This is the candidate pool our system consumes**; baselines read `input_table` instead. The two pools differ on all 119 tasks. |
| `gold_tables` | list[str] | Gold tables in `dw#sep#FCLT_ROOMS` form. Convert with `name.split("#sep#")[-1] + ".pkl"` before matching against `retrieved_table` / `input_table`. |
| `join_keys` | list[list[str]] | Annotated join key pairs, `[["T1.COL", "T2.COL"], …]`. |

Synth-* have no `retrieved_table`: their candidate pool is `input_table`.
They also have no explicit `gold_tables` — use the positional convention above.

---

## 2. Ground truth

| Field | Type | Meaning |
|---|---|---|
| `sql` | str | Gold SQL answering the question. |
| `target_table` | str | Gold answer table file, e.g. `bird_f3041c4a_target.pkl`. Beaver uses a double underscore: `beaver-6083e9ec__target.pkl`. Present for all tasks in all three benchmarks. |
| `dc_ops` | list[str] | **Gold preparation operator sequence.** Each entry is a call string carrying the operator name, its `table_name`, and full parameters (including Python `func` bodies for split/concat/standardise). This is the reference for operator-sequence accuracy. |
| `ops` | list[obj] | Compact view of `dc_ops`: `{"op": "SplitColumn", "tag": "mixed"}`. `tag` marks what the operator serves — `join_key`, `attribute`, or `mixed`. |

Tag distribution differs sharply by benchmark: Beaver is join-key dominated
(285 `join_key` vs 71 `attribute`), Synth-* are attribute dominated.

---

## 3. Size and difficulty counters (from the source benchmark)

| Field | Type | Meaning |
|---|---|---|
| `relevant_table_num` | int | Number of gold tables. Median 2 / 2 / 4 (Bird / Spider / Beaver). |
| `join_num` | int | Number of joins in the gold SQL. |
| `prep_num` | int | Number of preparation operators = `len(dc_ops)`. Median 2 / 2 / 3. |
| `total_ops_num` | int | Preparation plus query-side operators. |

---

## 4. Benchmark characteristics (added annotations)

Computed per task from the gold annotations; identical for every method.

| Field | Type | Meaning |
|---|---|---|
| `relevant_tables` | int | Gold table count used by the characterisation pipeline. Normally equals `relevant_table_num`. |
| `nonrel_relevant_tables` | int | Gold tables that are **not in relational form** and require reshaping (transpose, pivot, wide-to-long, …) before they can be joined. |
| `nonrel_relevant_table_ratio` | float | `nonrel_relevant_tables / relevant_tables`. `0.0` means every gold table is already relational. |
| `relationships` | int | Number of join relationships among the gold tables. Beaver reaches 8; Synth-* are usually 1. |
| `max_single_table_op_seq_len` | int | Longest preparation operator chain required for any single gold table — how deep the per-table pipeline must go. |

---

## 5. Complexity labels (`low` / `high`)

Three independent factors plus one derived label. Thresholds come from the
factor analysis; each is a binary split over the corresponding characteristic.

| Field | Splits on | `high` counts (Bird / Spider / Beaver) |
|---|---|---|
| `relevant_table_complexity` | Number of relevant tables | 19 / 29 / 114 |
| `pipeline_rel_complexity` | Join relationships (originally `join_complexity`) | 23 / 38 / 116 |
| `pipeline_ops_complexity` | Longest single-table operator chain (originally `single_table_ops_complexity`) | 45 / 7 / 60 |
| `error_accumulation_complexity` | Derived — see below | 62 / 42 / 116 |

`error_accumulation_complexity` is **derived**:

```python
num_high = sum(x == "high" for x in [relevant_table_complexity,
                                     pipeline_rel_complexity,
                                     pipeline_ops_complexity])
error_accumulation_complexity = "low" if num_high == 0 else "high"
```

That is, `low` only when **all three** factors are low. It is intended as a
proxy for how many stages can compound errors.

---

## 6. Directory layout

See [section 0](#0-getting-the-data). In short, per dataset:

```
<Dataset>/
├── benchmark.jsonl              task definitions (fields documented above)
├── input_tables/                candidate tables the system selects from
├── answer/                      gold answer tables (<task_id>_target.pkl)
├── tables_rels/
│   ├── outputs/<task_id>.json   gold subtables + join column pairs
│   └── databases/<db_id>.sqlite source DB, for gold column values
└── profiles/                    Beaver-Prep only: column profiling for retrieval
```
