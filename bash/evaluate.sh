#!/usr/bin/env bash
# Score one dataset.
#
#     bash/evaluate.sh Synth-Bird              this system, both arms
#     bash/evaluate.sh Synth-Bird all          this system + every baseline
#     bash/evaluate.sh Synth-Bird dsstar,pneuma
#
# The scorer is self-contained: no external checkout, no separate export step.
# Baselines are scored by executing their generated code, so the dataset's
# input tables must already be in place under datasets/<Dataset>/.
set -euo pipefail

DS="${1:-}"
if [[ -z "$DS" ]]; then
    echo "usage: $0 <Synth-Bird|Synth-Spider|Beaver-Prep> [sources]" >&2
    exit 1
fi
SRC="${2:-}"

cd "$(dirname "$0")/../codes"
OUT="../results/eval/$DS"

if [[ -n "$SRC" ]]; then
    python -m eval.scorer --dataset "$DS" --source "$SRC" --out "$OUT/metrics.csv"
    exit 0
fi

# Default: the self-correction ablation, as two separate tables.
echo "=== without self-correction ==="
python -m eval.scorer --dataset "$DS" --source no_self_correction \
       --out "$OUT/metrics_no_repair.csv"

echo
echo "=== with self-correction ==="
python -m eval.scorer --dataset "$DS" --source self_correction \
       --out "$OUT/metrics_repaired.csv"

echo
echo "compare:"
echo "  $OUT/metrics_no_repair.csv"
echo "  $OUT/metrics_repaired.csv"
