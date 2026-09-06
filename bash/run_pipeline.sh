#!/usr/bin/env bash
# Run the full forward pipeline for one dataset.
#
#     bash/run_pipeline.sh Synth-Bird
#     bash/run_pipeline.sh Beaver-Prep
#
# Every stage caches per task (or per table) in its own output file, so an
# interrupted run resumes for free and re-running a finished stage costs
# nothing. That is why these are separate commands rather than one script: you
# can stop after any of them, inspect the output, and continue.
set -euo pipefail

DS="${1:-}"
if [[ -z "$DS" ]]; then
    echo "usage: $0 <Synth-Bird|Synth-Spider|Beaver-Prep> [--limit N]" >&2
    exit 1
fi
shift || true
EXTRA=("$@")            # e.g. --limit 5, or --task-ids <id> ...

cd "$(dirname "$0")/../codes"
: "${OPENAI_API_KEY:?export OPENAI_API_KEY first}"

# Beaver-Prep is a 96-table warehouse with no per-task candidate pool, so it
# must first be narrowed to a top-10 retrieved set. Synth-Bird and Synth-Spider
# ship that pool in `input_table` and skip this stage entirely.
if [[ "$DS" == "Beaver-Prep" ]]; then
    echo "=== 0/5  table retrieval (Beaver-Prep only) ==="
    python -m table_discovery.run_pipeline --dataset "$DS"
fi

echo "=== 1/5  table metadata  (offline, one LLM call per TABLE) ==="
# EXTRA is deliberately NOT passed here. This stage works per TABLE, not per
# task: it takes --tables and its --limit counts tables, so a task-level
# --task-ids or --limit would either be rejected or mean something else. It
# profiles the whole collection, which every later stage then reads.
python -m table_discovery.meta_inferrence --dataset "$DS"

echo "=== 2/5  table selection ==="
python -m table_discovery.table_selection --dataset "$DS" "${EXTRA[@]}"

echo "=== 3/5  relational schema ==="
python -m pipeline_synthesize.relational_schema --dataset "$DS" "${EXTRA[@]}"

echo "=== 4/5  pipeline synthesis  (the expensive stage) ==="
# --workers caps threads INSIDE one task. The default of 8 on top of several
# concurrent tasks is what once got a full run OOM-killed.
python -m pipeline_synthesize.synthesize --dataset "$DS" --workers 4 "${EXTRA[@]}"

echo "=== 5/5  self-correction ==="
# --breadth 1 reproduces the original three-round loop; 2 also tries the
# localizer's second-ranked action (four-class accuracy 0.618, hit@2 0.80).
python -m self_correction.loop --dataset "$DS" --breadth 1 --max-nodes 4 "${EXTRA[@]}"

echo
echo "done. Now score it:  bash/evaluate.sh $DS"
