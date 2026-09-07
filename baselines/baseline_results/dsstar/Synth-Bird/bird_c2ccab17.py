import pandas as pd

# tables['table_2'] corresponds to bird_c2ccab17_input_1.pkl (consumption table)
df = tables["table_2"]

# Filter to September 2013
df_sep_2013 = df[(df["Year"] == "2013") & (df["Month"] == "09")].copy()

# tables['table_1'] corresponds to bird_c2ccab17_input_0.pkl (customer segment/currency table)
df_seg = tables["table_1"].copy()

# Extract CustomerID and Segment by splitting on '-'
df_seg[["CustomerID", "Segment"]] = df_seg["CustomerID_Segment"].str.split("-", n=1, expand=True)
df_seg["CustomerID"] = df_seg["CustomerID"].astype(int)

# Merge and find least-consuming segment
df_joined = df_sep_2013.merge(df_seg[["CustomerID", "Segment"]], on="CustomerID", how="inner")
least_consuming_segment = df_joined.groupby("Segment")["Consumption"].sum().idxmin()

# Final answer as a DataFrame
answer_df = pd.DataFrame({"least_consuming_segment": [least_consuming_segment]})

# Assign final output
result = {"least_consuming_segment_sep_2013": answer_df}