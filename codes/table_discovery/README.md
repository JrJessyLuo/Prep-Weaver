# Table Discovery

Given a natural-language question and a table collection, select the small set
of tables the question needs. This is the first module of Prep-Weaver; its
output (`exp_g_domain_{k}.json`) is the candidate pool the pipeline synthesis
module consumes.

## Two halves

**Retrieval** (stages 0–5) narrows a large collection to a top-k pool; it is
what Beaver needs, since its 96-table warehouse cannot fit in one prompt.
**Selection** (`meta_inferrence.py` + `table_selection.py`) picks the minimal
table set from a pool, and runs on all three datasets.

| | offline | online |
|---|---|---|
| retrieval | `build_join_graph` | `column_retrieval` → `table_rerank` → `llm_disambiguation` → `expand_compare` |
| selection | `meta_inferrence` | `table_selection` |

Synth-Bird and Synth-Spider ship a per-task candidate pool in `input_table`, so
they skip retrieval entirely and run only `meta_inferrence` → `table_selection`.
Beaver runs both halves, with `exp_g_domain_10.json` feeding the pool.

## Selection

### Offline: `meta_inferrence.py`

Profiles **every table in the collection** exactly once — cost is `|tables|`,
not `|tasks| x |tables per task|`. An LLM sees each table's header row plus its
first rows and returns the schema that best describes the attributes the table
actually provides. This matters because a raw header row is frequently not a
header: transposed tables put field names in the first column, pivoted tables
hide attribute names in cells, and warehouse tables use abbreviated names.

Beaver uses a warehouse-specific prompt variant that preserves table-family
prefixes (`FAC_`, `FCLT_`, `SIS_`, `TIP_`) and `KEY`/`CODE`/`ID` suffixes,
because those are what distinguish near-duplicate table families.

```bash
python -m table_discovery.meta_inferrence --dataset Beaver-Prep
python -m table_discovery.meta_inferrence --dataset Synth-Bird --limit 5
```

| dataset | tables to profile |
|---|---|
| Beaver-Prep | 96 |
| Synth-Bird | 374 |
| Synth-Spider | 347 |

Input: `datasets/<Dataset>/input_tables/*.pkl`.
Output: `results/table_discovery/metadata/<Dataset>/table_metadata.jsonl`, one
record per table (`original_headers`, `recovered_schema`, `potential_issue`,
`rationale`, `shape`, `llm_usage`). The output file is also the cache: a table
already present is skipped, so an interrupted run resumes for free.

### Online: `table_selection.py`

For each question, describes the candidate tables by their **recovered** schema
and asks the LLM for the minimal set, plus the subquestion each table supports.

```bash
python -m table_discovery.table_selection --dataset Beaver-Prep
python -m table_discovery.table_selection --dataset Synth-Bird --limit 5
```

Candidate pool:

| dataset | pool | cap on selected tables |
|---|---|---|
| Synth-Bird / Synth-Spider | the task's `input_table` | 4 |
| Beaver-Prep | top-10 from `exp_g_domain_10.json`, falling back to the task's `retrieved_table` | 7 |

Beaver additionally gets the predicted joinable file pairs from
`dw_join_keys_g_domain.json` as structural evidence, because its questions often
need a bridge table that supports no part of the question by itself.

`--on-missing` decides what happens to a table with no metadata: `error`
(default), `original` (fall back to raw headers), or `skip`. A fallback is
always listed in `fell_back_to_original`, so a run is never quietly
half-recovered.

Output: `results/table_discovery/selection/<Dataset>/table_selection.jsonl` —
`{task_id, question, candidate_tables, selected_tables, subquestions,
hallucinated_tables, usage}`. Also cached by `task_id`.

## Retrieval pipeline

| Stage | File | Input | Output | Cost |
|---|---|---|---|---|
| 0 | `build_join_graph.py` | `dev_tables.json`, `dev_semantic_col_sim.json`, `dev_uniqueness.json`, `dev_jaccard.json` | `dw_join_keys_g_domain.json`, `edge_conf_g_domain.json` | offline, free |
| 1 | `column_retrieval.py` | `dev.json`, `dev_tables.json` | `question_keywords.json`, `question_keywords_top{N}_columns.json`, embedding caches | 1 LLM call per question + local encoder |
| 2 | `table_rerank.py` | stage 1 output, `dev_tables.json` | `question_ranked_tables_only_C.json` | free |
| 3 | `llm_disambiguation.py` | stage 1 + stage 2 output | `question_ranked_tables_gated.json`, `question_ranked_tables_llm.json`, `gating_decisions.json` | 1 LLM call per **routed** question |
| 4–5 | `expand_compare.py` | stage 3 output + stage 0 graph, `dev.json` | `exp_g_domain_{5,10,15}.json` | free |

`group_select.py` is a library (candidate-solution generation and scoring); it
has no entry point. Path resolution, JSON helpers and the OpenAI-compatible
client live in `codes/common/` (`paths.py`, `dataset.py`, `io_utils.py`,
`llm_client.py`) and are shared with the other modules.

Stage 0 is independent of stages 1–3 and can run at any time before stage 4.

## Method in one paragraph

An LLM decomposes each question into keyphrases; each keyphrase is matched
against every column of the collection by embedding similarity (stage 1), and
the per-column scores are aggregated into a table ranking (stage 2). Because
a table can rank high purely because one column *name* resembles a keyphrase,
an LLM prunes distractors — but only for questions an ambiguity gate flags as
genuinely ambiguous, which keeps the LLM cost proportional to the hard cases
(stage 3). Separately, profiling statistics (value containment, column-name
embedding similarity, distinct ratios) yield a join graph with no ground-truth
join keys (stage 0). Finally, small table sets that cover every keyphrase are
enumerated and scored by coverage plus join connectivity, disconnected sets are
reconnected through bridge tables found in the join graph, and the tables that
recur across the top-scoring sets are promoted by confidence voting (stages
4–5).

## Running it

Everything is addressed by dataset name. Nothing needs to be copied.

```bash
cd Prep-Weaver/codes
export OPENAI_API_KEY=...        # needed by stages 1 and 3 only
python -m table_discovery.run_pipeline --dataset Beaver-Prep
```

Individual stages take the same arguments:

```bash
python -m table_discovery.build_join_graph    --dataset Beaver-Prep
python -m table_discovery.column_retrieval    --dataset Beaver-Prep --top-k 100
python -m table_discovery.table_rerank        --dataset Beaver-Prep --kc-top-k 100
python -m table_discovery.llm_disambiguation  --dataset Beaver-Prep
python -m table_discovery.expand_compare      --dataset Beaver-Prep
```

### Paths

| What | Default | Override |
|---|---|---|
| profiling inputs | `datasets/<Dataset>/profiles/` | `--profile-dir`, `PREPWEAVER_PROFILE_DIR` |
| table collection | `datasets/<Dataset>/input_tables/` | `--input-tables` |
| retrieval outputs | `results/table_discovery/offline_online/<Dataset>/` | `--out-dir`, `PREPWEAVER_TD_OUT_DIR` |
| table metadata | `results/table_discovery/metadata/<Dataset>/` | `--out` |
| table selection | `results/table_discovery/selection/<Dataset>/` | `--out` |

### Smoke test

Stages 0, 2 and 4 need no API key at all:

```bash
python -m table_discovery.run_pipeline --dataset Beaver-Prep --stages 0
```

A cheap end-to-end run over the first few questions:

```bash
export OPENAI_API_KEY=...
python -m table_discovery.run_pipeline --dataset Beaver-Prep --limit 5
```

`--limit` bounds stage 1 to the first N questions; every later stage then sees
only those N, so the whole run costs N keyphrase calls plus the (usually far
fewer) routed pruning calls.

### Caching

Nothing is recomputed unless you ask for it. Question keyphrases, column
embeddings, keyphrase embeddings and raw LLM pruning outputs are all cached in
the output directory and written incrementally, so an interrupted run resumes
where it stopped. Use `--force-regenerate-keywords`,
`--force-recompute-column-embeddings`, `--force-recompute-keyword-embeddings`
(stage 1) or `--regenerate-llm` / `--force-regenerate-records` (stage 3) to
override.

## Requirements

`torch`, `transformers`, `networkx`, `scipy`, `numpy`, `tqdm`, `openai`.

The stage 1 encoder (`WhereIsAI/UAE-Large-V1`, ~1.3 GB) runs on CUDA, Apple
Silicon (MPS) or CPU, chosen automatically. It is small enough to run locally:
a 97-table / 1.5k-column collection embeds in well under a minute, and the
result is cached.

## Credentials

`OPENAI_API_KEY` is read from the environment and never written to disk.
`OPENAI_BASE_URL` may point at an OpenAI-compatible proxy.
