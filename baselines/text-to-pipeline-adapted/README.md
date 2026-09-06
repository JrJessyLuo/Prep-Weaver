# Text-to-Pipeline Adapted

This runner implements the staged extension used in the paper discussion:

1. an upstream retriever supplies `benchmark.jsonl.input_table` as candidate tables;
2. an LLM explicitly selects relevant tables;
3. an LLM writes a natural-language preparation specification over only those tables;
4. the existing Text-to-Pipeline DSL adapter generates and compiles the pipeline.

The runner does not perform retrieval itself. For Beaver, `table_collection` is the full
lake and `input_table` is expected to contain the candidates produced by the upstream
retriever. Spider and BIRD follow the same `input_table` candidate interface.

## Outputs

- `results/codes/<benchmark>/<task_id>.py`: executable code for `eval_all_oom.py`
- `results/artifacts/<benchmark>/<task_id>.json`: all three stage outputs
- `results/records/<benchmark>.jsonl`: run status, usage, and table-selection metrics

Spider/BIRD gold table indices are the first `relevant_table_num` input tables. Beaver
gold indices are obtained by matching `gold_tables` to candidate filenames. Beaver recall
therefore also exposes relevant tables missed by the upstream retriever.

## Run

Run from this directory. Start with one task before a complete run:

```bash
python run_staged.py \
  --benchmark_path <DATA_ROOT>/nl2sql-spider/dev/benchmark.jsonl \
  --benchmark_name nl2sql-spider \
  --table_dir <DATA_ROOT>/nl2sql-spider/dev \
  --max_tasks 1
```

Complete benchmark commands are shown in `run_all.sh`.

## Selection analysis

After a run, summarize table selection by relevant-table count and non-relational type:

```bash
python analyze_selection.py \
  --benchmark_path <DATA_ROOT>/nl2sql-spider/dev/benchmark.jsonl \
  --benchmark_name nl2sql-spider \
  --records results/records/nl2sql-spider.jsonl
```

The non-relational grouping separates structural forms (Pivot, Transpose, Stack,
WideToLong, Unpivot, Explode) from packed-cell forms (SplitColumn, Concatenate,
Decompose). Value cleaning alone is not classified as non-relational.

## Evaluation

The generated code layout is:

```text
text-to-pipeline-adapted/results/codes/<benchmark>/<task_id>.py
```

Use the `text2pipeline_adapted` method added to `evaluation/eval_all_oom.py`, and use
`--count-missing` so generation failures remain in the denominator.
