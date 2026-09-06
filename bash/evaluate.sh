#!/usr/bin/env bash
# Export, score and report the four metrics for one dataset, twice: without and
# with self-correction.
#
#     bash/evaluate.sh Synth-Bird
#
# Scoring re-executes each exported script under a lineage tracer, so a run must
# be exported before it can be scored at all.
set -euo pipefail

DS="${1:-}"
if [[ -z "$DS" ]]; then
    echo "usage: $0 <Synth-Bird|Synth-Spider|Beaver-Prep>" >&2
    exit 1
fi

cd "$(dirname "$0")/../codes"
: "${DEEPPREP_EVAL_DIR:?point DEEPPREP_EVAL_DIR at the directory holding eval_all_oom.py}"

OUT="../results/eval/$DS"

echo "=== without self-correction ==="
python -m eval.export  --dataset "$DS"
python -m eval.score   --dataset "$DS" --method ours
python -m eval.metrics --dataset "$DS" --source selection \
       --out "$OUT/metrics_no_repair.csv"

echo
echo "=== with self-correction ==="
python -m eval.export  --dataset "$DS" --repaired
# A DISTINCT method key: the evaluator replaces every row of a method in its
# store, so scoring the repaired run as `ours` would destroy the baseline row it
# is meant to be compared against.
python -m eval.score   --dataset "$DS" --repaired
python -m eval.metrics --dataset "$DS" --source repair --method ours_repaired \
       --out "$OUT/metrics_repaired.csv"

echo
echo "compare:"
echo "  $OUT/metrics_no_repair.csv"
echo "  $OUT/metrics_repaired.csv"
