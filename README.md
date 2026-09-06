# Prep-Weaver

Autonomous data preparation: from a natural-language question and a collection
of raw tables, produce the minimal set of *joinable* subtables plus the
specification of how they join.

Three forward stages, followed by an execution-guided repair loop:

```
table_discovery  ->  pipeline_synthesize  ->  self_correction  ->  eval
  which tables         what shape they          diagnose, revise,     four
  does the question    should have, and         keep what helps       metrics
  need                 the pipeline that
                       produces it
```

---

## 1. Install

```bash
conda create -n prepweaver python=3.11
conda activate prepweaver
pip install -r requirements.txt
```

The stages that call an LLM read the key from the environment; it is never
written to disk.

```bash
export OPENAI_API_KEY=...
export OPENAI_BASE_URL=...        # optional, for an OpenAI-compatible proxy
```

On first use `transformers` downloads and caches two encoders: about 600 MB for
`WhereIsAI/UAE-Large-V1` (retrieval) and the same for
`answerdotai/ModernBERT-base` (the repair localizer). Both run on CPU, Apple
Silicon or CUDA, chosen automatically.

## 2. Get the data

Only `benchmark.jsonl` ships with this repository. Download the tables from

> https://drive.google.com/drive/u/0/folders/1sL9wdeCPw5HNEf7yD0hx3HlxzAc0K3lM

and unpack each dataset's folders **into its directory under `datasets/`**:

```
datasets/Synth-Bird/{input_tables,answer,tables_rels}/
datasets/Synth-Spider/{input_tables,answer,tables_rels}/
datasets/Beaver-Prep/{input_tables,answer,tables_rels,profiles}/
```

Nothing else needs configuring — every stage finds its data by dataset name.
Check before spending anything:

```bash
cd codes
python -c "from common import dataset as D; d = D.resolve('Synth-Bird'); \
           print(d.input_tables); print('missing:', d.missing() or 'nothing')"
```

`missing: nothing` means it is ready. `datasets/README.md` documents every
`benchmark.jsonl` field and the exact layout.

---

## 3. Run it

All commands run from `codes/`. `$DS` is `Synth-Bird`, `Synth-Spider` or
`Beaver-Prep`.

### Table discovery

**This is the one stage where the datasets differ.** Synth-Bird and
Synth-Spider ship a per-task candidate pool in `input_table` (median 7 and 4
tables), so they go straight to selection. Beaver-Prep is a 96-table warehouse
with no per-task pool, so it must first be narrowed to a top-10 retrieved set:

```bash
cd codes

# Beaver-Prep — retrieval FIRST, then the common two stages
python -m table_discovery.run_pipeline     --dataset Beaver-Prep
python -m table_discovery.meta_inferrence  --dataset Beaver-Prep
python -m table_discovery.table_selection  --dataset Beaver-Prep

# Synth-Spider / Synth-Bird — no retrieval stage
python -m table_discovery.meta_inferrence  --dataset Synth-Spider
python -m table_discovery.table_selection  --dataset Synth-Spider

python -m table_discovery.meta_inferrence  --dataset Synth-Bird
python -m table_discovery.table_selection  --dataset Synth-Bird
```

`run_pipeline` builds a join graph from `profiles/` using **no ground-truth join
keys**, extracts question keyphrases, retrieves columns, ranks tables, prunes
distractors behind an ambiguity gate, and expands through join bridges.

`meta_inferrence` is offline and costs one LLM call **per table, not per task**:
it reads each table's header row plus its first rows and returns the schema that
describes what the table actually provides. This matters because a raw header is
often not a header — transposed tables put field names in the first column,
pivoted tables hide them in cells.

### Pipeline synthesis

Identical for all three datasets.

```bash
python -m pipeline_synthesize.relational_schema --dataset "$DS"
python -m pipeline_synthesize.synthesize        --dataset "$DS" --workers 4
```

`relational_schema` declares the `CREATE TABLE` each selected table should have
*after* preparation, plus the join keys between them. `synthesize` searches the
operator chain that materialises it — the expensive stage. `--workers` caps
threads **inside** one task; the default of 8 on top of several concurrent tasks
is what once got a run OOM-killed.

### Self-correction

```bash
python -m self_correction.loop --dataset "$DS" --breadth 1 --max-nodes 4
```

`--breadth 1` reproduces the original three-round loop. `--breadth 2` also tries
the localizer's second-ranked action, which is worth it because its four-class
accuracy is 0.618 while hit@2 is 0.80. `--max-nodes` is the real cost cap.

The localizer runs locally: trained heads over a frozen ModernBERT-base, an
86 KB checkpoint that ships in `models/`.

### Running one task first

Every task-level stage takes `--task-ids`, and all take `--limit N`:

```bash
python -m table_discovery.table_selection       --dataset "$DS" --task-ids bird_058b8e3b
python -m pipeline_synthesize.relational_schema --dataset "$DS" --task-ids bird_058b8e3b
python -m pipeline_synthesize.synthesize        --dataset "$DS" --task-ids bird_058b8e3b
```

`meta_inferrence` is the exception — it works per **table**, so it takes
`--tables <file.pkl> ...` and its `--limit` counts tables. To find the tables
one task needs:

```bash
python -c "from common import dataset as D; \
           t = [x for x in D.resolve('Synth-Bird').tasks() if x['task_id']=='bird_058b8e3b'][0]; \
           print(' '.join(t['input_table']))"
```

Every stage caches per task (or per table) in its own output file, so an
interrupted run resumes for free and re-running a finished stage costs nothing.

### Scripted

`bash/` wraps the same commands, with the Beaver retrieval stage handled
automatically:

```bash
bash/run_pipeline.sh Synth-Bird          # or Synth-Spider, Beaver-Prep
bash/evaluate.sh     Synth-Bird
```

Extra arguments are forwarded to the task-level stages, so a small trial is:

```bash
bash/run_pipeline.sh Synth-Bird --limit 3
```

---

## 4. Evaluate

Scoring re-executes each exported script under a lineage tracer, so a run must
be **exported** before it can be scored. The evaluator is a separate checkout
and is not part of this repository:

```bash
export DEEPPREP_EVAL_DIR=/path/to/DeepPrep/evaluation      # holds eval_all_oom.py
```

```bash
# without self-correction
python -m eval.export  --dataset "$DS"
python -m eval.score   --dataset "$DS" --method ours
python -m eval.metrics --dataset "$DS" --source selection \
       --out ../results/eval/"$DS"/metrics_no_repair.csv

# with self-correction. A DISTINCT method key: the evaluator replaces every row
# of a method in its store, so scoring the repaired run as `ours` would destroy
# the baseline it is meant to be compared against.
python -m eval.export  --dataset "$DS" --repaired
python -m eval.score   --dataset "$DS" --repaired
python -m eval.metrics --dataset "$DS" --source repair --method ours_repaired \
       --out ../results/eval/"$DS"/metrics_repaired.csv
```

### The four metrics

| reported name | computed as |
|---|---|
| **Table identification accuracy** | the selected table set exactly equals the gold set |
| **Table correctness** | every gold value domain of every table is covered |
| **Relationship correctness** | every gold join-key value domain is covered |
| **Preparation correctness** | table correctness **and** relationship correctness, on the same task |

Three things worth knowing:

- **Preparation correctness is a per-task conjunction, not a product.** If half
  the tasks get the tables right and a *different* half get the relationships
  right, the product is 0.25 while the truth is 0.00 — no single task was fully
  prepared.
- **Table identification uses exact set equality, not recall.** Selecting the
  gold tables plus three distractors is not a correct identification; a
  recall-only score would rate "select everything" as perfect.
- **Table and relationship correctness come from the external evaluator**, read
  from its per-task CSV rather than recomputed. An internal scorer also exists
  and the two have disagreed on the same run, so the reported numbers come from
  one authority only.

Report `results/eval/<Dataset>/metrics.csv`, not the evaluator's screen output:
the evaluator aggregates over its own full benchmark (120 Spider tasks) while
`eval.metrics` uses `benchmark.jsonl` (the 103-task subset).

---

## 5. Repository layout

| directory | contents | in git |
|---|---|---|
| `codes/` | the system, one package per stage | yes |
| `datasets/` | `benchmark.jsonl` per dataset and the field documentation. Tables, answers, relations and Beaver's profiling come from Drive. | definitions only |
| `models/` | four trained artefacts, 16 MB total | yes |
| `baselines/` | adaptation code for Text-to-Pipeline, BAT and DeepPrep — the staged interface turning `question + input tables` into each original method's expected input | yes |
| `results/` | everything a run writes; regenerated by running the pipeline | no |
| `technical_report.pdf` | the method write-up | yes |

### `codes/`

| package | what it does | details |
|---|---|---|
| `common/` | dataset and path resolution, JSON helpers, the LLM client | — |
| `table_discovery/` | table metadata, question-to-table selection, and Beaver's retrieval | `table_discovery/README.md` |
| `pipeline_synthesize/` | relational schema, then the operator pipeline. Joint candidate selection is posed as maximum-weight clique on a complete multipartite graph. | `pipeline_synthesize/README.md` |
| `self_correction/` | diagnose, revise, keep what helps — an explicit search tree with depth and breadth expansion | `self_correction/README.md` |
| `eval/` | export, score, report the four metrics | — |

### `models/`

| file | size | used by |
|---|---|---|
| `model_multistep_m4_prefix_history.joblib` | 12 MB | next-operator policy, given the chain prefix |
| `model.joblib` | 3.2 MB | single-operation classifier |
| `localizer_staged.pt` | 86 KB | repair localizer: trained heads over a **frozen** ModernBERT-base |
| `localizer_staged.meta.json` | 2.6 KB | its tokenizer special tokens — from the same training run |

### `results/`

```
results/
├── table_discovery/
│   ├── metadata/<Dataset>/table_metadata.jsonl        one record per table
│   ├── offline_online/<Dataset>/                      Beaver retrieval only
│   └── selection/<Dataset>/table_selection.jsonl      selected tables per task
├── pipeline_synthesize/
│   ├── schema/<Dataset>/relational_schema.jsonl       CREATE TABLE + join edges
│   └── pipeline/<Dataset>/pipeline.jsonl              ops, params, columns
├── self_correction/<Dataset>/repair.jsonl             the whole repair tree
└── eval/<Dataset>/
    ├── codes/<benchmark>/*.py                         executable per task
    ├── eval_all.csv                                   per-task raw scores
    └── metrics.csv                                    the four reported metrics
```

---

## 6. Cost and runtime

| stage | LLM calls |
|---|---|
| table metadata | one per **table** (374 / 347 / 96) |
| table selection | one per task |
| relational schema | one per task |
| pipeline synthesis | a beam search per task — the dominant cost |
| self-correction | up to `--max-nodes` per task, only where the localizer flags a problem |

Two measured notes. About **80% of wall-clock time is not spent in the API** —
the hotspot is whole-table string conversion inside the diagnostic and
observation code, which is GIL-serialized. And `--limit` / `--task-ids` exist so
the expensive stages can be sized on a few tasks before committing.
