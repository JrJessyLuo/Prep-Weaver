import pandas as pd

# Source tables (already loaded in-scope as `tables`)
cards = tables["table_1"]
status = tables["table_2"]

# Join on id
df = cards.merge(status, on="id", how="inner", suffixes=("", "_status"))

# 1) sts_premodern.notna() instead of == "Legal"
mask_premodern_present = df["sts_premodern"].notna()

# 2) Verify ruling-text match by searching `text` and `originalText` for "triggered mana ability" (case-insensitive)
text_series = df["text"].fillna("").astype(str)
orig_text_series = (
    df["originalText"].fillna("").astype(str)
    if "originalText" in df.columns
    else pd.Series("", index=df.index)
)

mask_triggered_mana_text = (
    text_series.str.contains("triggered mana ability", case=False, regex=False, na=False)
    | orig_text_series.str.contains("triggered mana ability", case=False, regex=False, na=False)
)

# 3) Exclude multi-face cards via otherFaceIds.isna() and layout not in listed multi-face layouts
multi_layouts = ["transform", "modal_dfc", "split", "flip", "adventure", "meld"]

mask_other_faces_absent = df["otherFaceIds"].isna() if "otherFaceIds" in df.columns else pd.Series(True, index=df.index)
mask_layout_single = ~df["layout"].isin(multi_layouts) if "layout" in df.columns else pd.Series(True, index=df.index)

mask_single_face = mask_other_faces_absent & mask_layout_single

# Apply filters
filtered = df[mask_premodern_present & mask_triggered_mana_text & mask_single_face]

# Final answer
answer_df = pd.DataFrame({"count": [int(len(filtered))]})
result = {"answer": answer_df}