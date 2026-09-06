"""
features.py
-----------
Feature extraction for the single-table "next operation" predictor (schema-conditioned).
Features = structural features (16, table only) + schema-difference fingerprint (14, T vs

Public interface:
    sanitize(df)               -> clean a dirty table (de-duplicate column names, stringify list cells)
    featurize(df, schema, pk)  -> np.ndarray (length = len(FEATURE_NAMES))
    FEATURE_NAMES              -> the feature names, in the same order featurize emits
"""
from __future__ import annotations
import os
import re
import numpy as np
import pandas as pd

MAX_COLS, MAX_ROWS = 60, 300


def sanitize(df: pd.DataFrame) -> pd.DataFrame:
    """De-duplicate column names and stringify list/dict/set cells (otherwise nunique/to_numeric raise)."""
    df = df.copy()
    seen, newcols = {}, []
    for c in df.columns:
        key = str(c)
        if key in seen:
            seen[key] += 1; newcols.append(f"{key}.{seen[key]}")
        else:
            seen[key] = 0; newcols.append(c)
    df.columns = newcols
    for c in df.columns:
        col = df[c]
        if col.dtype == object and _may_hold_containers(col):
            df[c] = col.map(lambda v: str(v) if isinstance(v, (list, dict, set)) else v)
    return df


# pandas' C-level type inference settles the common case without touching a
# single cell from Python. The guard it replaces ran `isinstance` over EVERY
# cell of EVERY object column purely to discover that the answer was no: on one
# beaver task that was 202 million lambda calls and 48 of the script's 110
# seconds. Columns that are plainly homogeneous cannot hold a list/dict/set, so
# only genuinely mixed ones still pay for the scan.
_SCALAR_INFERRED = frozenset({
    "string", "unicode", "bytes", "empty", "floating", "integer", "boolean",
    "decimal", "complex", "mixed-integer-float", "datetime", "datetime64",
    "date", "time", "timedelta", "timedelta64", "period", "categorical",
})


def _may_hold_containers(col: pd.Series) -> bool:
    try:
        if pd.api.types.infer_dtype(col, skipna=True) in _SCALAR_INFERRED:
            return False
    except Exception:
        pass
    return bool(col.map(lambda v: isinstance(v, (list, dict, set))).any())


def _num_ratio(s): return float(pd.to_numeric(s, errors="coerce").notna().mean())
def _norm(x): return re.sub(r"[^a-z0-9]", "", str(x).lower())
_DATE_LIKE_RE = re.compile(
    r"^(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}|\d{1,2}[-/][A-Za-z]{3,9}[-/]?\d{2,4})$"
)


def _canon(s):
    x = pd.to_numeric(s, errors="coerce")
    if x.notna().mean() > 0.9:
        return "int" if (x.dropna() % 1 == 0).all() else "float"

    # Avoid pandas/dateutil's very slow per-cell parser on arbitrary categorical
    # strings. Only run datetime inference when a cheap sample check suggests the
    # column is actually date-like. This preserves date features while preventing
    # candidate search from stalling on text-heavy raw tables.
    sample = s.dropna().astype(str).str.strip().head(50)
    if len(sample) and sample.map(lambda v: bool(_DATE_LIKE_RE.match(v))).mean() > 0.5:
        if pd.to_datetime(sample, errors="coerce").notna().mean() > 0.9:
            return "date"
    return "str"


def struct_features(df: pd.DataFrame) -> dict:
    n_rows, n_cols = df.shape
    cols = list(df.columns)
    sdf = df.iloc[:MAX_ROWS, :MAX_COLS]; scols = list(sdf.columns)
    header_is_data = np.mean([str(c).strip().replace(".", "", 1).isdigit() for c in cols]) if cols else 0.0
    numeric_block = np.mean([_num_ratio(sdf[c]) > 0.8 for c in scols[1:]]) if len(scols) > 1 else 0.0
    first_col_str = (_canon(sdf.iloc[:, 0]) == "str") if len(scols) else False
    wide = 1.0 if n_cols > n_rows else 0.0
    transpose_sig = float(first_col_str) * 0.5 + numeric_block * 0.3 + wide * 0.2
    long_sig = 0.0
    for c in scols:
        if sdf[c].dtype == object and 1 < sdf[c].nunique() <= max(3, len(sdf) // 2):
            long_sig = 1.0
    stubs = {}
    for c in cols:
        mm = re.match(r"(.+?)[_\-](\w+)$", str(c))
        if mm: stubs[mm.group(1)] = stubs.get(mm.group(1), 0) + 1
    sibling_groups = max(list(stubs.values()) + [0])
    split_sig = 0.0
    for c in scols:
        s = sdf[c].astype(str)
        for d in ["-", "_", "/", "|"]:
            if s.str.contains(d, regex=False).mean() > 0.8:
                p = s.str.split(d).map(len)
                if p.nunique() == 1 and p.iloc[0] >= 2: split_sig = 1.0
    explode_sig = float(any(sdf[c].astype(str).str.contains(",", regex=False).mean() > 0.5 for c in scols))
    str_incons = 0.0
    for c in scols:
        if sdf[c].dtype == object:
            s = sdf[c].astype(str)
            if (s != s.str.strip().str.lower()).mean() > 0.3: str_incons = 1.0
    date_like = float(any(sdf[c].astype(str).str.contains(r"\d{1,4}[/\-]\d{1,2}[/\-]\d{1,4}", regex=True).mean() > 0.5 for c in scols))
    frac_nulls = float(sdf.isna().mean().mean())
    dup_frac = float(1 - sdf.drop_duplicates().shape[0] / max(len(sdf), 1))
    mean_card = float(np.mean([sdf[c].nunique() for c in scols])) / max(len(sdf), 1)
    frac_num_cols = np.mean([_num_ratio(sdf[c]) > 0.8 for c in scols]) if scols else 0.0
    # Discriminative features: sibling wide columns (Stack/WideToLong vs Rename)
    strc = [str(c) for c in cols]
    # Linear approximation of "does this column belong to a repeated wide
    # sibling group?". The previous pairwise common-prefix check is O(n^2) and
    # stalls on ultra-wide raw tables with 20k+ columns.
    prefix_counts = {}
    for c in strc:
        prefix = re.sub(r"[\W_]*\d+(?:\.\d+)?$", "", c)[:12]
        if len(prefix) >= 3:
            prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
    sib = sum(1 for c in strc
              if len((p := re.sub(r"[\W_]*\d+(?:\.\d+)?$", "", c)[:12])) >= 3
              and prefix_counts.get(p, 0) > 1)
    sibling_ratio = sib / max(len(strc), 1)                       # fraction of columns with a shared-prefix sibling -> Stack/WideToLong
    numeric_suffix_frac = np.mean([bool(re.search(r"\d+$", c)) for c in strc]) if strc else 0.0  # column names ending in a digit -> a wide group
    delim_col_frac = np.mean([sdf[c].astype(str).str.contains(r"[-_/|]", regex=True).mean() > 0.8
                              for c in scols]) if scols else 0.0   # fraction of columns holding a separator -> Split vs Cast
    return dict(n_rows=float(n_rows), n_cols=float(n_cols), aspect_wide=n_cols / max(n_rows, 1),
                header_is_data=float(header_is_data), numeric_block=float(numeric_block),
                transpose_sig=transpose_sig, long_sig=long_sig, sibling_groups=float(sibling_groups),
                split_sig=split_sig, explode_sig=explode_sig, str_incons=str_incons, date_like=date_like,
                frac_nulls=frac_nulls, dup_frac=dup_frac, mean_card=mean_card, frac_num_cols=float(frac_num_cols),
                sibling_ratio=float(sibling_ratio), numeric_suffix_frac=float(numeric_suffix_frac),
                delim_col_frac=float(delim_col_frac))


def schema_features(df: pd.DataFrame, schema: dict, pk) -> dict:
    sdf = df.iloc[:MAX_ROWS, :MAX_COLS]; scols = list(sdf.columns)
    cur_norm = {_norm(c): c for c in df.columns}
    tgt_norm = {_norm(c): c for c in schema}
    tgt_type = {_norm(c): t for c, t in schema.items()}
    present = [k for k in tgt_norm if k in cur_norm]
    frac_present = len(present) / max(len(schema), 1)
    extra = [k for k in cur_norm if k not in tgt_norm]
    frac_extra = len(extra) / max(len(df.columns), 1)
    same_count = 1.0 if len(df.columns) == len(schema) else 0.0
    rename_sig = same_count * (1 - frac_present)
    type_mism = date_unnorm = str_target_incons = 0
    for k in present:
        col = cur_norm[k]; want = tgt_type[k]; have = _canon(df[col])
        if want != have: type_mism += 1
        if want == "date":
            s = df[col].dropna().astype(str).str.strip()
            sample = s.head(50)
            looks_date = len(sample) and sample.map(lambda v: bool(_DATE_LIKE_RE.match(v))).mean() > 0.5
            if looks_date and pd.to_datetime(sample, errors="coerce").notna().mean() > 0.5 and \
               sample.str.fullmatch(r"\d{4}-\d{2}-\d{2}").mean() < 0.8:
                date_unnorm += 1
        if want == "str" and have == "str":
            s = df[col].astype(str)
            if (s != s.str.strip().str.lower()).mean() > 0.3: str_target_incons += 1
    n_t = max(len(schema), 1)
    packed_multi = 0.0
    for c in scols:
        s = sdf[c].astype(str)
        for d in ["-", "_", "/", "|", " "]:
            parts_norm = set()
            for v in s.head(20):
                for pp in str(v).split(d): parts_norm.add(_norm(pp))
            if len(parts_norm & set(tgt_norm)) >= 2: packed_multi = 1.0
    names_in_cells = 0.0
    for c in scols:
        if sdf[c].dtype == object:
            vals = {_norm(v) for v in sdf[c].astype(str).unique()}
            names_in_cells = max(names_in_cells, len(vals & set(tgt_norm)) / n_t)
    concat_sig = float((1 - frac_present) > 0 and len(df.columns) > len(schema) and packed_multi == 0)
    pk_norm = {_norm(c) for c in pk}
    pk_present = (len(pk_norm & set(cur_norm)) / len(pk_norm)) if pk_norm else 0.0
    return dict(n_target_cols=float(len(schema)), n_pk=float(len(pk)),
                frac_present=frac_present, frac_missing=1 - frac_present, frac_extra=frac_extra,
                same_count=same_count, rename_sig=rename_sig,
                type_mism=type_mism / n_t, date_unnorm=float(date_unnorm),
                str_target_incons=float(str_target_incons), packed_multi=packed_multi,
                names_in_cells=names_in_cells, concat_sig=concat_sig, pk_present=pk_present)


SN = list(struct_features(pd.DataFrame({"a": [1]})).keys())
CN = list(schema_features(pd.DataFrame({"a": [1]}), {"a": "int"}, set()).keys())
FEATURE_NAMES = SN + CN


def featurize(df: pd.DataFrame, schema: dict, pk=frozenset()) -> np.ndarray:
    df = sanitize(df)
    sf = struct_features(df); cf = schema_features(df, schema, pk)
    x = np.array([sf[k] for k in SN] + [cf[k] for k in CN], float)
    return np.where(np.isinf(x), np.nan, x)
