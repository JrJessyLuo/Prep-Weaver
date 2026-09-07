import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['income_id', 'date_received', 'amount', 'source', 'link_to_member'])
    # SelectCol
    _cols = [c for c in ['income_id', 'date_received', 'amount', 'source', 'link_to_member'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date_received", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['date_received'] = table_1['date_received'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date_received'] = table_1['date_received'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="amount", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['amount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['amount']
    if _dtype == "datetime64":
        table_1['amount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['amount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['amount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['amount'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['income_id', 'date_received', 'amount', 'source', 'link_to_member'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['income_id', 'date_received', 'amount', 'source', 'link_to_member'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['income_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['income_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'rec1x5zBFIqoOuPW8', 'rec280Sk7o31iG0Tx', 'rec28ORZgcm1dtqBZ', 'rec2a03QXbFQAUZ7X', 'rec3pH4DxMcWHMRB7', 'rec4BLdZHS2Blfp4v', 'rec4O9rmGnLx3j8vt', 'rec75vvFxgYtHmqxY', 'recD078PnS3x2doBe', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recJMazpPVexyFYTc', 'recL4aEZBZoPk9NYx', 'recL94zpn6Xh6kQii', 'recP6DJPyi5donvXL', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recTjHY5xXhvkCdVT', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'recWh2lJVOT6HjChK', 'recZ4PkGERzl9ziHO', 'recZN8afUWlE5fZHG', 'reccSUPwy30AeZLEb', 'reccW7q1KkhSKZsea', 'recf4UKTfipCzgcSA', 'recjHj4BS5A541n9v', 'reco0mr8dXTgs5wWA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'recttfySfQnYb68u3', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS'])
    # SelectCol
    _cols = [c for c in ['member_id', 'rec1x5zBFIqoOuPW8', 'rec280Sk7o31iG0Tx', 'rec28ORZgcm1dtqBZ', 'rec2a03QXbFQAUZ7X', 'rec3pH4DxMcWHMRB7', 'rec4BLdZHS2Blfp4v', 'rec4O9rmGnLx3j8vt', 'rec75vvFxgYtHmqxY', 'recD078PnS3x2doBe', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recJMazpPVexyFYTc', 'recL4aEZBZoPk9NYx', 'recL94zpn6Xh6kQii', 'recP6DJPyi5donvXL', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recTjHY5xXhvkCdVT', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'recWh2lJVOT6HjChK', 'recZ4PkGERzl9ziHO', 'recZN8afUWlE5fZHG', 'reccSUPwy30AeZLEb', 'reccW7q1KkhSKZsea', 'recf4UKTfipCzgcSA', 'recjHj4BS5A541n9v', 'reco0mr8dXTgs5wWA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'recttfySfQnYb68u3', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="member_dim_prepared", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Keep only the two attributes we need
    #     df = df[df["member_id"].isin(["first_name", "last_name"])]
    # 
    #     # member_id values become columns; rec* columns become rows after transpose
    #     df = df.set_index("member_id").T.reset_index()
    # 
    #     # Rename index column to required key
    #     df = df.rename(columns={"index": "member_record_id"})
    # 
    #     # Keep only required output columns (preserve for later integration)
    #     return df[["member_record_id", "first_name", "last_name"]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Keep only the two attributes we need
        df = df[df["member_id"].isin(["first_name", "last_name"])]

        # member_id values become columns; rec* columns become rows after transpose
        df = df.set_index("member_id").T.reset_index()

        # Rename index column to required key
        df = df.rename(columns={"index": "member_record_id"})

        # Keep only required output columns (preserve for later integration)
        return df[["member_record_id", "first_name", "last_name"]]
    member_dim_prepared = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['member_dim_prepared'])
    # Terminate
    result = {'member_dim_prepared': member_dim_prepared}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_income = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_members = prepared_table_2

# prepared_income already selected columns
income = prepared_income.copy()
# Keep only dues-related rows for identifying who paid dues
income_dues = income[income['source'].str.lower() == 'dues'].copy()
# Coerce date for ordering
income_dues['date_received'] = pd.to_datetime(income_dues['date_received'], errors='coerce')

# prepared_members is in long/narrow form with columns: member_record_id, first_name, last_name
members = prepared_members.copy()

# Join dues receipts to member names
df = income_dues.merge(members, left_on='link_to_member', right_on='member_record_id', how='left')

# Find the earliest dues payment
df_sorted = df.sort_values(['date_received', 'income_id'], ascending=[True, True])
first_row = df_sorted.iloc[0]

# Compose full name
target = first_row['first_name'] + ' ' + first_row['last_name']

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
