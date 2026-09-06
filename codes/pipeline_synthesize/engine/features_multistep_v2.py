"""History-aware features shared by V2 training and inference."""
from __future__ import annotations

import numpy as np

from features import FEATURE_NAMES as BASE_FEATURE_NAMES, featurize


OPS = (
    "Transpose", "Pivot", "Stack", "SplitColumn", "Concatenate", "Rename",
    "CastType", "StandardizeString", "StandardizeDatetime", "Explode",
    "WideToLong",
)

HISTORY_FEATURE_NAMES = (
    ["step_idx", "same_as_last_count", "rows_vs_initial", "cols_vs_initial",
     "rows_vs_previous", "cols_vs_previous", "schema_coverage_delta"]
    + [f"last_op__{op}" for op in OPS]
    + [f"used_count__{op}" for op in OPS]
)
FEATURE_NAMES_V2 = list(BASE_FEATURE_NAMES) + HISTORY_FEATURE_NAMES


def featurize_v2(df, schema, pk=frozenset(), history=(), initial_shape=None,
                 previous_shape=None, previous_coverage=None):
    """Append operation-history features to the existing table/schema features."""
    history = list(history or [])
    counts = {op: history.count(op) for op in OPS}
    last = history[-1] if history else None
    same_as_last = 0
    for op in reversed(history):
        if op != last:
            break
        same_as_last += 1
    base = featurize(df, schema, pk)
    initial_shape = initial_shape or df.shape
    previous_shape = previous_shape or df.shape
    current_coverage = float(base[BASE_FEATURE_NAMES.index("frac_present")])
    previous_coverage = current_coverage if previous_coverage is None else previous_coverage
    extra = [
        float(len(history)), float(same_as_last),
        float(df.shape[0] - initial_shape[0]), float(df.shape[1] - initial_shape[1]),
        float(df.shape[0] - previous_shape[0]), float(df.shape[1] - previous_shape[1]),
        float(current_coverage - previous_coverage),
    ]
    extra.extend(float(last == op) for op in OPS)
    extra.extend(float(counts[op]) for op in OPS)
    return np.concatenate([base, np.asarray(extra, dtype=float)])
