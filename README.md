# Prep-Weaver

Autonomous data preparation: from a natural-language question and a collection
of raw tables, produce the minimal set of *joinable* tables plus the
specification of how they join.

Two forward stages, followed by an execution-guided self-correction:

```
table_discovery  ->  pipeline_synthesize  ->  self_correction  ->  eval
```

---

## 1. Install

```bash
conda create -n prepweaver python=3.11
conda activate prepweaver
pip install -r requirements.txt
```

```bash
export OPENAI_API_KEY=...
export OPENAI_BASE_URL=...        # optional, for an OpenAI-compatible proxy
```

The key is needed to *run* the pipeline (section 3). Scoring an existing run
(section 4) makes no LLM calls and needs no key.

On first use `transformers` downloads and caches two encoders: about 600 MB for
`WhereIsAI/UAE-Large-V1` (retrieval) and the same for
`answerdotai/ModernBERT-base` (the repair localizer). Both run on CPU, Apple
Silicon or CUDA, chosen automatically.

## 2. Get the data

Download the datasets from

> https://drive.google.com/drive/u/0/folders/1sL9wdeCPw5HNEf7yD0hx3HlxzAc0K3lM

and unpack each dataset's folders **into its directory under `datasets/`** following the same subdirectory setting: 

```
datasets/Synth-Bird/*/
datasets/Synth-Spider/*/
datasets/Beaver-Prep/*/
```

`datasets/README.md` documents key fields of every `benchmark.jsonl`  and corresponding complexity labels.

---

## 3. Run it

All commands run from `codes/`. `$DS` is `Synth-Bird`, `Synth-Spider` or
`Beaver-Prep`.

### Table discovery

**This is the one stage where the datasets differ.** Synth-Bird and
Synth-Spider ship a per-task candidate pool in `input_table` (small table collections), so they go straight to LLM-based selection. Beaver-Prep contains a large table collection with 96 tables, so it must first be narrowed to a top-10 retrieved set:

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
threads **inside** one task.

### Self-correction

```bash
python -m self_correction.loop --dataset "$DS" --breadth 1 --max-nodes 4
```

`--breadth 1` reproduces the original three-round loop.

The localizer runs locally: trained heads over a frozen ModernBERT-base, an
86 KB checkpoint that ships in `models/`.


### Scripted

`bash/` wraps the same commands, with the Beaver retrieval stage handled
automatically:

```bash
bash/run_pipeline.sh Synth-Bird          # or Synth-Spider, Beaver-Prep
bash/evaluate.sh     Synth-Bird
```

---

## 4. Evaluate

One scorer covers this system and every baseline, with the same metric
definitions. It needs no external checkout and no separate export step: each run
prints the four metrics and writes `results/eval/<Dataset>/metrics_<method>.csv`
with a per-task breakdown.

### Our method

```bash
cd codes
python -m eval.scorer --dataset "$DS" --source no_self_correction
python -m eval.scorer --dataset "$DS" --source self_correction
```

Those two are the self-correction ablation: `no_self_correction` scores the
pipeline as synthesized, `self_correction` scores the state the repair tree
chose. Both are read from this run's own artefacts under `results/` — the
recorded operator chain is replayed on the raw tables, so what is scored is what
the pipeline actually produces.

### Baselines

Their generated code ships with the repository, one file per task:

```
baselines/baseline_results/<method>/<Dataset>/<task_id>.py      # pandas
baselines/baseline_results/<method>/<Dataset>/<task_id>.json    # SQL (pneuma)
```

| method | what it is | emits |
|---|---|---|
| `gpt-5.5` | an LLM writing pandas directly | pandas |
| `dsstar` | DS-Star | pandas |
| `pneuma` | Pneuma | SQL |
| `bat_adapted` | BAT, behind this project's staged interface | pandas |
| `deepprep_adapted` | DeepPrep, same interface | pandas |
| `text2pipeline_adapted` | Text-to-Pipeline, same interface | pandas |

A baseline hands us arbitrary code rather than a recorded operator chain, so
there is nothing to replay: the code is **executed** and watched.

```bash
python -m eval.scorer --list                       # list the available method comparison
python -m eval.scorer --dataset "$DS" --source all # this system + every baseline
```

`--source` takes a comma-separated list and prints one comparison table, so
`--source self_correction,gpt-5.5,dsstar` scores three methods side by side.
`--list` names everything that can go there. (`--task-ids` is the one flag that
is **space**-separated, not comma-separated.)

Executing a baseline is the expensive part, so each method's per-task scores are
cached under `results/eval/<Dataset>/baseline_cache/`; a second run reuses them.
Delete that file to force a re-run.


### The four metrics

| reported name | computed as |
|---|---|
| **Table identification accuracy** | the selected table set exactly equals the gold set |
| **Table correctness** | every gold value domain of every table is covered |
| **Relationship correctness** | every gold join-key value domain is covered |
| **Preparation correctness** | table correctness **and** relationship correctness, on the same task |


---

## 5. Repository layout

| directory | contents | in git |
|---|---|---|
| `codes/` | the system, one package per stage | yes |
| `datasets/` | `benchmark.jsonl` per dataset and the field documentation. Tables, answers, relations and Beaver's profiling come from Drive. | definitions only |
| `models/` | four trained artefacts | yes |
| `baselines/` | adaptation code for Text-to-Pipeline, BAT and DeepPrep — the staged interface turning `question + input tables` into each original method's expected input | yes |
| `results/` | everything a run writes; regenerated by running the pipeline | no |

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
├── self_correction/<Dataset>/repair.jsonl             the whole self-correction tree
└── eval/<Dataset>/
    ├── metrics_<method>.csv                           four metrics + per-task rows
    └── baseline_cache/<method>.jsonl                  executed baselines, cached
```

---


