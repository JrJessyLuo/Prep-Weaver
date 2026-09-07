import pandas as pd

df1 = tables["table_1"].copy()
df2 = tables["table_2"].copy()

merged = df1.merge(df2[["CDSCode", "MailCity"]], left_on="cds", right_on="CDSCode", how="inner")

fresno_total = (
    merged.loc[
        (merged["rtype"].eq("S")) &
        (merged["MailCity"].astype(str).str.strip().str.lower().eq("fresno")),
        "NumTstTakr"
    ]
    .fillna(0)
    .sum()
)

result = {
    "test_takers_in_fresno_mail_city": pd.DataFrame(
        {"total_test_takers": [int(fresno_total)]}
    )
}
