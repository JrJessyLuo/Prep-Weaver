import pandas as pd

# Tables are already loaded in a dict named `tables`
clients_df = tables["table_1"]   # bird_87751f28_input_0.pkl
district_df = tables["table_2"]  # bird_87751f28_input_1.pkl
acct_df = tables["table_3"]      # financial_account.pkl
disp_df = tables["table_5"]      # financial_disp.pkl

# Parse birth year from personal_info format like: "F#1927-10-01#24"
birth_year = pd.to_datetime(
    clients_df["personal_info"].astype(str).str.split("#").str[1],
    errors="coerce",
).dt.year

clients_1920 = clients_df.loc[birth_year.eq(1920), ["client_id"]].drop_duplicates()

joined = (
    clients_1920
    .merge(disp_df[["client_id", "account_id"]], on="client_id", how="inner")
    .merge(acct_df[["account_id", "district_id"]], on="account_id", how="inner")
    .merge(district_df[["district_id", "kraj"]], on="district_id", how="inner")
)

distinct_client_count = joined.loc[joined["kraj"].eq("east Bohemia"), "client_id"].nunique()

answer_df = pd.DataFrame({"distinct_client_count": [distinct_client_count]})
result = {"clients_born_1920_in_east_bohemia": answer_df}