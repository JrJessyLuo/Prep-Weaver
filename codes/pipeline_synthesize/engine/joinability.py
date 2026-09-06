from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

import pandas as pd

from data_loader import find_table_file
from table_executor import load_table

MAX_PROFILE_ROWS = 5000
MAX_DISTINCT_VALUES = 1000
MAX_CANDIDATE_COLUMNS = 40
MAX_PAIR_EVALUATIONS = 400
MIN_NAME_SIM_FOR_PAIR = 0.45
MIN_KEYLIKE_FOR_PAIR = 0.45


def normalize_name(name: Any) -> str:
    text = str(name or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def token_set(name: Any) -> set[str]:
    text = normalize_name(name)
    toks = set(text.split())
    raw = str(name or "")
    camel = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw)
    toks |= set(normalize_name(camel).split())
    return {t for t in toks if t and t not in {"id", "key", "code"}}


def name_similarity(left: Any, right: Any) -> float:
    l_raw = normalize_name(left)
    r_raw = normalize_name(right)
    if not l_raw or not r_raw:
        return 0.0
    if l_raw == r_raw:
        return 1.0
    if l_raw in r_raw or r_raw in l_raw:
        return 0.75
    lt = token_set(left)
    rt = token_set(right)
    if lt or rt:
        inter = len(lt & rt)
        union = len(lt | rt)
        if union:
            return inter / union
    return 0.0


def clean_values(series: pd.Series, max_values: int = MAX_DISTINCT_VALUES) -> set[str]:
    values = series.dropna()
    if len(values) > MAX_PROFILE_ROWS:
        values = values.sample(MAX_PROFILE_ROWS, random_state=42)
    out: set[str] = set()
    for value in values.tolist():
        text = str(value).strip().strip('"').strip("'")
        if text and text.lower() not in {"nan", "none", "null"}:
            out.add(text.lower())
            if len(out) >= max_values:
                break
    return out


def dtype_compatible(left: pd.Series, right: pd.Series) -> bool:
    if pd.api.types.is_numeric_dtype(left) and pd.api.types.is_numeric_dtype(right):
        return True
    if pd.api.types.is_datetime64_any_dtype(left) and pd.api.types.is_datetime64_any_dtype(right):
        return True
    return True  # string coercion can still join many data-lake keys.


def key_likeness(series: pd.Series) -> float:
    non_null = float(series.notna().mean()) if len(series) else 0.0
    values = series.dropna()
    if len(values) > MAX_PROFILE_ROWS:
        values = values.sample(MAX_PROFILE_ROWS, random_state=42)
    # Some raw tables contain list/dict cells; pandas nunique needs hashable
    # values, so profile uniqueness over a stable string representation.
    normalized = values.map(lambda x: str(x))
    nunique = normalized.nunique()
    unique_ratio = float(nunique / max(len(normalized), 1))
    # Join keys can be primary or foreign keys; reward non-null and moderate/high uniqueness.
    return 0.6 * non_null + 0.4 * min(unique_ratio, 1.0)


def column_profile(df: pd.DataFrame, col: Any, pos: int | None = None) -> dict[str, Any]:
    # Duplicate column labels make df[col] return a DataFrame. Use position so
    # joinability profiling always receives a single Series.
    series = df.iloc[:, pos] if pos is not None else df[col]
    if isinstance(series, pd.DataFrame):
        series = series.iloc[:, 0]
    values = clean_values(series)
    name = normalize_name(col)
    key_name_bonus = 1.0 if any(tok in name for tok in ["id", "key", "code", "name", "date", "year"]) else 0.0
    return {
        "col": col,
        "col_str": str(col),
        "values": values,
        "distinct": len(values),
        "dtype": series.dtype,
        "key_likeness": key_likeness(series),
        "name_key_bonus": key_name_bonus,
        "candidate_score": key_name_bonus + key_likeness(series),
    }


def profile_columns(df: pd.DataFrame, max_cols: int = MAX_CANDIDATE_COLUMNS) -> list[dict[str, Any]]:
    profiles = [column_profile(df, col, pos=i) for i, col in enumerate(df.columns)]
    if len(profiles) <= max_cols:
        return profiles
    profiles.sort(key=lambda x: x["candidate_score"], reverse=True)
    return profiles[:max_cols]


def profile_dtype_compatible(left: dict[str, Any], right: dict[str, Any]) -> bool:
    ldt = left["dtype"]
    rdt = right["dtype"]
    if pd.api.types.is_numeric_dtype(ldt) and pd.api.types.is_numeric_dtype(rdt):
        return True
    if pd.api.types.is_datetime64_any_dtype(ldt) and pd.api.types.is_datetime64_any_dtype(rdt):
        return True
    return True


def column_pair_score(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_values = left["values"]
    right_values = right["values"]
    inter = left_values & right_values
    union = left_values | right_values
    containment_lr = len(inter) / max(len(left_values), 1)
    containment_rl = len(inter) / max(len(right_values), 1)
    jaccard = len(inter) / max(len(union), 1)
    ns = name_similarity(left["col"], right["col"])
    dt = profile_dtype_compatible(left, right)
    kl = max(left["key_likeness"], right["key_likeness"])
    score = (
        0.25 * ns
        + 0.35 * max(containment_lr, containment_rl)
        + 0.20 * jaccard
        + 0.10 * (1.0 if dt else 0.0)
        + 0.10 * kl
    )
    confidence = "high" if score >= 0.75 and len(inter) >= 10 else "medium" if score >= 0.55 and len(inter) >= 3 else "low"
    return {
        "left_col": left["col_str"],
        "right_col": right["col_str"],
        "name_similarity": round(ns, 4),
        "value_overlap_jaccard": round(jaccard, 4),
        "containment_left_in_right": round(containment_lr, 4),
        "containment_right_in_left": round(containment_rl, 4),
        "dtype_compatible": bool(dt),
        "key_likeness": round(kl, 4),
        "joinability_score": round(score, 4),
        "confidence": confidence,
        "overlap_size": len(inter),
        "left_distinct": len(left_values),
        "right_distinct": len(right_values),
    }


def candidate_profile_pairs(
    left_profiles: list[dict[str, Any]],
    right_profiles: list[dict[str, Any]],
    max_pairs: int = MAX_PAIR_EVALUATIONS,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    candidates = []
    for left in left_profiles:
        for right in right_profiles:
            ns = name_similarity(left["col"], right["col"])
            key_score = max(left["key_likeness"], right["key_likeness"])
            # Always keep exact/near-name matches; otherwise focus on key-like columns.
            if ns >= MIN_NAME_SIM_FOR_PAIR or key_score >= MIN_KEYLIKE_FOR_PAIR:
                rough = 0.65 * ns + 0.35 * key_score
                candidates.append((rough, left, right))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [(left, right) for _, left, right in candidates[:max_pairs]]


def score_table_pair(left_df: pd.DataFrame, right_df: pd.DataFrame, top_k: int = 5) -> dict[str, Any]:
    pairs = []
    left_profiles = profile_columns(left_df)
    right_profiles = profile_columns(right_df)
    candidate_pairs = candidate_profile_pairs(left_profiles, right_profiles)
    for left, right in candidate_pairs:
        pair = column_pair_score(left, right)
        if pair["joinability_score"] > 0:
            pairs.append(pair)
    pairs.sort(key=lambda x: x["joinability_score"], reverse=True)
    return {
        "best_joinability_score": pairs[0]["joinability_score"] if pairs else 0.0,
        "best_column_pairs": pairs[:top_k],
        "profiled_left_columns": len(left_profiles),
        "profiled_right_columns": len(right_profiles),
        "evaluated_pairs": len(candidate_pairs),
    }


def load_neighbor_tables(
    benchmark_dir: Path,
    input_tables: list[str],
    current_table_file: str,
) -> dict[str, pd.DataFrame]:
    cache: dict[str, Path | None] = {}
    out = {}
    for file_name in input_tables:
        if str(file_name) == str(current_table_file):
            continue
        path = find_table_file(benchmark_dir, str(file_name), cache=cache)
        if path is None:
            continue
        try:
            out[str(file_name)] = load_table(path)
        except Exception:
            continue
    return out


def compute_joinability_signal(
    current_df: pd.DataFrame,
    original_df: pd.DataFrame,
    neighbor_tables: dict[str, pd.DataFrame],
    previous_signal: dict[str, Any] | None = None,
    top_neighbors: int = 5,
) -> dict[str, Any]:
    current_cols = {str(c) for c in current_df.columns}
    original_scores = []
    current_scores = []
    for file_name, neighbor_df in neighbor_tables.items():
        before = score_table_pair(original_df, neighbor_df, top_k=3)
        after = score_table_pair(current_df, neighbor_df, top_k=3)
        original_scores.append((file_name, before))
        current_scores.append((file_name, after))

    current_scores.sort(key=lambda x: x[1]["best_joinability_score"], reverse=True)
    original_scores.sort(key=lambda x: x[1]["best_joinability_score"], reverse=True)

    originally_strong_cols: set[str] = set()
    for _, score in original_scores[:top_neighbors]:
        if score["best_joinability_score"] >= 0.55:
            for pair in score["best_column_pairs"][:2]:
                if pair.get("confidence") in {"medium", "high"}:
                    originally_strong_cols.add(pair["left_col"])
    dropped = sorted(col for col in originally_strong_cols if col not in current_cols)

    best_neighbors = []
    for file_name, after in current_scores[:top_neighbors]:
        before = next((s for fn, s in original_scores if fn == file_name), {"best_joinability_score": 0.0})
        best_neighbors.append(
            {
                "neighbor_table_file": file_name,
                "score_before": before["best_joinability_score"],
                "score_after": after["best_joinability_score"],
                "score_delta": round(after["best_joinability_score"] - before["best_joinability_score"], 4),
                "best_column_pairs": after["best_column_pairs"],
            }
        )

    warning = ""
    if dropped:
        warning = "Potential join/entity keys were dropped: " + ", ".join(dropped)

    must_keep = set(dropped)
    for item in best_neighbors:
        if item["score_after"] >= 0.55:
            for pair in item["best_column_pairs"][:2]:
                same_name_with_overlap = (
                    normalize_name(pair["left_col"]) == normalize_name(pair["right_col"])
                    and int(pair.get("overlap_size") or 0) > 0
                )
                if pair.get("confidence") == "high" or same_name_with_overlap:
                    must_keep.add(pair["left_col"])

    return {
        "best_neighbors": best_neighbors,
        "dropped_join_key_candidates": dropped,
        "must_keep_columns": sorted(col for col in must_keep if col in current_cols or col in dropped),
        "must_keep_policy": "conservative: high-confidence or same-name join candidates only",
        "warning": warning,
    }


def compact_joinability_for_prompt(signal: dict[str, Any] | None, top_neighbors: int = 3, top_pairs: int = 2) -> dict[str, Any]:
    if not signal:
        return {}
    compact: dict[str, Any] = {
        "must_keep_columns": signal.get("must_keep_columns", []),
    }
    if signal.get("spec_sql_join_keys"):
        compact["spec_sql_join_keys"] = signal.get("spec_sql_join_keys")
    if signal.get("spec_sql_join_key_status"):
        compact["spec_sql_join_key_status"] = signal.get("spec_sql_join_key_status")
    return compact
