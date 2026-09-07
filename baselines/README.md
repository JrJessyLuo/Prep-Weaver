# Adapted Baseline Implementations

This directory contains the core adaptation code for extending three existing
table-preparation baselines to question-conditioned tabular data preparation:

- Text-to-Pipeline
- BAT
- DeepPrep

The key adaptation is the same across the three methods:

```text
benchmark.jsonl
  -> load question
  -> load input_table candidates
  -> Stage 1: select relevant tables
  -> Stage 2: infer per-table preparation specification / target metadata
              plus answer_code for integrating the prepared tables
  -> Stage 3: call the original baseline backend to synthesize executable
              table-preparation pipelines
```

The main contribution here is the staged interface that converts
`question + input tables` into the inputs expected by the original preparation
methods.

## Files

```text
baselines/
  text-to-pipeline-adapted/
    run_staged.py
  bat-adapted/
    run_staged.py
  deepprep-adapted/
    run_staged.py
```


## Stage 1: Relevant Table Selection

Stage 1 takes:

```text
question + input_table candidates
```

and produces:

```text
selected relevant tables
```

The selected tables are represented by their indices/files from the original
`input_table` candidate set. The same Stage 1 logic is reused by all three
adapted baselines so that the table-identification cost and decision can be
shared across methods.

In the runners, this logic is implemented in the Text-to-Pipeline adapted file
and imported by BAT/DeepPrep:

```text
text-to-pipeline-adapted/run_staged.py
  selector_prompt(...)
  normalize_file_selection(...)
```

## Stage 2: Requirement / Specification Inference

Stage 2 takes:

```text
question + selected tables
```

and produces method-specific preparation requirements.

For Text-to-Pipeline adapted, Stage 2 produces one natural-language preparation
specification for each selected table:

```text
selected table_i + question
  -> preparation specification_i
```

It also produces `answer_code`, which integrates the prepared tables to answer
the question.

Implemented in:

```text
text-to-pipeline-adapted/run_staged.py
  specification_prompt(...)
  normalize_stage2_plan(...)
```

For BAT adapted and DeepPrep adapted, Stage 2 produces one target table
metadata/schema for each selected table:

```text
selected table_i + question
  -> target metadata/schema_i
```

It also produces `answer_code`, which integrates the prepared tables to answer
the question.

Implemented in:

```text
bat-adapted/run_staged.py
  TARGET_SCHEMA_PROMPT
  get_or_generate_stage2_plan(...)
  normalize_plan(...)
```

DeepPrep adapted reuses the BAT adapted Stage 2 target-metadata generation.

## Stage 3: Baseline Pipeline Synthesis

After Stage 2, each method calls its original backend:

```text
Text-to-Pipeline:
  selected table + natural-language preparation specification
  -> transform_chain
  -> pandas code

BAT:
  selected table + target metadata/schema
  -> BAT pipeline synthesis
  -> pandas code

DeepPrep:
  selected table + target metadata/schema
  -> DeepPrep pipeline synthesis
  -> pandas code
```

The per-table prepared outputs are named:

```text
prepared_table_1
prepared_table_2
...
```

The generated `answer_code` is appended after these prepared tables and must
produce the final `target`.

## Running Text-to-Pipeline Adapted

```bash
cd /path/to/Prep-Weaver/baselines/text-to-pipeline-adapted

python run_staged.py \
  --benchmark_path /path/to/benchmark.jsonl \
  --benchmark_name nl2sql-bird \
  --table_dir /path/to/table/root \
  --model_name gpt \
  --reasoning_effort minimal \
  --sample_rows 3 \
  --max_cell_chars 200 \
  --max_refine 3
```

## Running BAT Adapted

```bash
cd /path/to/Prep-Weaver/baselines/bat-adapted

python run_staged.py \
  --benchmark_path /path/to/benchmark.jsonl \
  --benchmark_name nl2sql-bird \
  --table_dir /path/to/table/root \
  --model_name gpt \
  --reasoning_effort minimal \
  --sample_rows 3 \
  --max_cell_chars 200 \
  --max_rollout_steps 4 \
  --max_depth 4
```

## Running DeepPrep Adapted

DeepPrep adapted requires the original DeepPrep backend/server to be available.
After the backend is running:

```bash
cd /path/to/Prep-Weaver/baselines/deepprep-adapted

python run_staged.py \
  --benchmark_path /path/to/benchmark.jsonl \
  --benchmark_name nl2sql-bird \
  --table_dir /path/to/table/root \
  --model_name gpt \
  --reasoning_effort minimal \
  --sample_rows 3 \
  --max_cell_chars 200 \
  --max_steps 3
```


## `baseline_results/`

The generated output of each baseline, one file per task:

```
baseline_results/<method>/<Dataset>/<task_id>.py     # or .json for SQL methods
```

These are the artefacts the evaluation scores, so a comparison can be reproduced
without re-running any baseline. Score them with the repository's own scorer:

```bash
cd ../codes
python -m eval.scorer --list
python -m eval.scorer --dataset Synth-Bird --source gpt-5.5
python -m eval.scorer --dataset Synth-Bird --source all
```

Note that not every method can have the output result due to the pipeline generation fails.

