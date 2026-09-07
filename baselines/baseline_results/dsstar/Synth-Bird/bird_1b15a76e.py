import pandas as pd

# Tables already loaded in scope as `tables`
cards = tables["table_1"]
rulings = tables["table_2"]

rq_target_iso = "2007-01-02"
rq_target_us = "01/02/2007"
target_dt = pd.to_datetime(rq_target_iso)

# --- Parse rq to datetime (best-effort ISO then US), matching reference logic ---
rulings_inspect = rulings.copy()
rulings_inspect["rq_str"] = rulings_inspect["rq"].astype(str).str.strip()

rulings_inspect["rq_dt_iso"] = pd.to_datetime(
    rulings_inspect["rq_str"], errors="coerce", infer_datetime_format=True
)
rulings_inspect["rq_dt_us"] = pd.to_datetime(
    rulings_inspect["rq_str"], errors="coerce", format="%m/%d/%Y"
)

rulings_inspect["rq_dt"] = rulings_inspect["rq_dt_iso"].fillna(rulings_inspect["rq_dt_us"])

# --- Filter rulings by parsed date == target date ---
rulings_dt = rulings_inspect.loc[
    rulings_inspect["rq_dt"].dt.normalize().eq(target_dt.normalize())
].copy()
rulings_dt = rulings_dt[rulings.columns]

# --- Count distinct cards with non-null rarity, joined via uuid, and with non-empty nr ---
rulings_f = rulings_dt.copy()
rulings_f["nr_clean"] = rulings_f["nr"].astype(str).str.strip()
rulings_f = rulings_f.loc[rulings_f["nr"].notna() & rulings_f["nr_clean"].ne("")].copy()

merged = cards.merge(
    rulings_f.drop(columns=["nr_clean"], errors="ignore"),
    on="uuid",
    how="inner",
    suffixes=("_card", "_ruling"),
)

merged_rarity_present = merged.loc[merged["rarity"].notna()].copy()
answer = int(merged_rarity_present["uuid"].nunique())

answer_df = pd.DataFrame({"cards_with_print_rarity_and_ruling_text_printed_on_01_02_2007": [answer]})

result = {"answer": answer_df}