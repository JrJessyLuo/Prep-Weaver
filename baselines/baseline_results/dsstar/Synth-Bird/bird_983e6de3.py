import pandas as pd
import re

# Input tables (already loaded)
df0 = tables["table_1"]
df1 = tables["table_2"]

def find_wbc_columns(df: pd.DataFrame):
    candidates = []
    for c in df.columns:
        cl = str(c).strip().lower()
        if cl in {"wbc"} or "wbc" in cl or "white blood" in cl:
            candidates.append(c)
    return candidates

def normalize_id_series(s: pd.Series) -> pd.Series:
    s_str = s.astype("string").str.strip()
    num = pd.to_numeric(s_str, errors="coerce")
    out = s_str.copy()
    mask_num = num.notna()
    if mask_num.any():
        num_int = num[mask_num].round(0).astype("Int64")
        out.loc[mask_num] = num_int.astype("string")
    out = out.replace({"<NA>": pd.NA, "nan": pd.NA, "None": pd.NA})
    return out

def _clean_header_to_id(x):
    s = pd.Series([x], dtype="string").str.strip()
    s = s.str.replace(r'^[\'"]+|[\'"]+$', '', regex=True)
    s = normalize_id_series(s)
    return s.iloc[0]

def build_acceptance_indicator_from_transposed_df0(df0: pd.DataFrame, id_col: str = "ID"):
    header_cols = [c for c in df0.columns if str(c) != id_col]
    id_candidates = []
    for c in header_cols:
        cid = _clean_header_to_id(c)
        if cid is not None and cid is not pd.NA and str(cid).strip() != "":
            id_candidates.append(cid)

    seen = set()
    id_candidates_unique = []
    for cid in id_candidates:
        if cid not in seen:
            seen.add(cid)
            id_candidates_unique.append(cid)

    if len(id_candidates_unique) == 0:
        return None

    df0_t = df0.T.copy()
    df0_t.index = df0_t.index.astype("string")
    idx_to_clean = {idx: _clean_header_to_id(idx) for idx in df0_t.index}
    df0_t["ID_norm"] = pd.Series(idx_to_clean)

    df0_t_ids = df0_t.dropna(subset=["ID_norm"]).copy()
    df0_t_ids = df0_t_ids[df0_t_ids["ID_norm"].isin(set(id_candidates_unique))].copy()

    pos_tokens = {
        "admit", "admitted", "accept", "accepted", "inpatient", "hospitalized",
        "入院", "受け入れ", "受入", "受診"
    }
    neg_tokens = {"outpatient", "discharged", "外来"}

    pos_re = re.compile(r"(?:^|\b)(admit(?:ted)?|accept(?:ed)?|inpatient|hospitalized)(?:\b|$)", re.IGNORECASE)
    neg_re = re.compile(r"(?:^|\b)(outpatient|discharged)(?:\b|$)", re.IGNORECASE)
    jp_pos_re = re.compile(r"(入院|受け入れ|受入|受診)")
    jp_neg_re = re.compile(r"(外来)")

    results = []
    scan_cols = [c for c in df0_t_ids.columns if c != "ID_norm"]

    for _, row in df0_t_ids.iterrows():
        pid = row["ID_norm"]
        vals = row[scan_cols]

        s = vals.astype("string").str.strip().str.lower()
        s = s.replace({"<NA>": pd.NA, "nan": pd.NA, "none": pd.NA, "": pd.NA})

        pos_count = 0
        neg_count = 0

        pos_count += int(s.isin({t.lower() for t in pos_tokens}).sum())
        neg_count += int(s.isin({t.lower() for t in neg_tokens}).sum())

        s_nn = s.dropna()
        if not s_nn.empty:
            pos_count += int(s_nn.str.contains(pos_re).sum())
            neg_count += int(s_nn.str.contains(neg_re).sum())
            pos_count += int(s_nn.str.contains(jp_pos_re).sum())
            neg_count += int(s_nn.str.contains(jp_neg_re).sum())

        pos_count += int((s == "+").sum())
        neg_count += int((s == "-").sum())

        num = pd.to_numeric(s, errors="coerce")
        numeric_pos = int((num.notna() & (num > 0)).sum())
        numeric_zero = int((num.notna() & (num == 0)).sum())

        admitted = pd.NA
        if (pos_count + numeric_pos) > 0:
            admitted = 1
        elif (neg_count + numeric_zero) > 0:
            admitted = 0

        if admitted is not pd.NA:
            results.append({"ID_norm": str(pid), "admission_indicator": admitted})

    if not results:
        return None

    accept_df = pd.DataFrame(results)
    accept_df["admission_indicator"] = accept_df["admission_indicator"].astype("Int64")
    accept_df = (
        accept_df.groupby("ID_norm", as_index=False)
        .agg(admission_indicator=("admission_indicator", "max"))
    )
    return accept_df

# Build admitted/accepted indicator mapping from df0
accept_df_t = build_acceptance_indicator_from_transposed_df0(df0, id_col="ID")

# If no mapping found, admitted set is empty
if accept_df_t is None or accept_df_t.empty:
    admitted = df1.iloc[0:0].copy()
else:
    df1_joined = df1.copy()
    df1_joined["ID_norm"] = normalize_id_series(df1_joined["ID"])
    df1_joined = df1_joined.merge(
        accept_df_t[["ID_norm", "admission_indicator"]],
        how="left",
        on="ID_norm"
    )
    admitted = df1_joined[df1_joined["admission_indicator"] == 1].copy()

# WBC column selection (prefer df1)
wbc_cols = find_wbc_columns(df1)
wbc_col = wbc_cols[0] if wbc_cols else None

# Define "normal WBC" using a common adult reference range (4.0–11.0 x10^9/L)
# Also handle datasets where WBC might be stored as counts/µL by converting if values look large.
normal_count = 0
if wbc_col is not None and wbc_col in admitted.columns:
    w = pd.to_numeric(admitted[wbc_col], errors="coerce")

    # Heuristic: if median WBC > 100, assume units are /µL and convert to x10^9/L by dividing by 1000.
    med = w.median(skipna=True)
    if pd.notna(med) and med > 100:
        w = w / 1000.0

    normal_mask = w.between(4.0, 11.0, inclusive="both")
    normal_count = int(admitted.loc[normal_mask, "ID_norm"].nunique())

answer_df = pd.DataFrame({"normal_wbc_accepted_patients": [normal_count]})
result = {"answer": answer_df}