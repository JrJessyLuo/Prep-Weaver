import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="district_crime_1995", func="""
    # import pandas as pd
    # def process_tables(table_1: pd.DataFrame):
    #     # reshape to one row per district
    #     df = table_1.set_index('district_id').T.reset_index().rename(columns={'index':'district_id'})
    #     # pick the crime-1995 series if present under a known code (common in this dataset)
    #     for candidate in ['A16','A15','A14','A13','A12','A11','A10','A9','A8','A7','A6','A5','A4']:
    #         if candidate in df.columns:
    #             out = df[['district_id', candidate]].rename(columns={candidate: 'crime_1995'})
    #             return out
    #     # fallback: empty schema if not found
    #     return df[['district_id']].assign(crime_1995=pd.NA)
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame):
        # reshape to one row per district
        df = table_1.set_index('district_id').T.reset_index().rename(columns={'index':'district_id'})
        # pick the crime-1995 series if present under a known code (common in this dataset)
        for candidate in ['A16','A15','A14','A13','A12','A11','A10','A9','A8','A7','A6','A5','A4']:
            if candidate in df.columns:
                out = df[['district_id', candidate]].rename(columns={candidate: 'crime_1995'})
                return out
        # fallback: empty schema if not found
        return df[['district_id']].assign(crime_1995=pd.NA)
    district_crime_1995 = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="district_crime_1995", column="crime_1995", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = district_crime_1995['crime_1995'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = district_crime_1995['crime_1995']
    if _dtype == "datetime64":
        district_crime_1995['crime_1995'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        district_crime_1995['crime_1995'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        district_crime_1995['crime_1995'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        district_crime_1995['crime_1995'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="district_crime_1995", columns=['district_id', 'crime_1995'])
    # SelectCol
    _cols = [c for c in ['district_id', 'crime_1995'] if c in district_crime_1995.columns]
    district_crime_1995 = district_crime_1995[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['district_crime_1995'])
    # Terminate
    result = {'district_crime_1995': district_crime_1995}
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
    # DropNulls(table_name="table_1", subset=['district_id', 'fdm'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['district_id', 'fdm'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="fdm", date_format="%Y-%m-%d")
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
    table_1['fdm'] = table_1['fdm'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['fdm'] = table_1['fdm'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="has_account_from_1997", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     # fdm standardized as YYYY-MM-DD; treat anything unparseable as False
    #     try:
    #         dt = pd.to_datetime(row["fdm"], errors="coerce")
    #         if pd.isna(dt):
    #             return False
    #         return int(dt.year) >= 1997
    #     except Exception:
    #         return False
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        # fdm standardized as YYYY-MM-DD; treat anything unparseable as False
        try:
            dt = pd.to_datetime(row["fdm"], errors="coerce")
            if pd.isna(dt):
                return False
            return int(dt.year) >= 1997
        except Exception:
            return False
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["has_account_from_1997"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['district_id'], agg=[{'column': 'has_account_from_1997', 'agg_func': 'max'}])
    # GroupBy
    table_1 = table_1.groupby(['district_id'], as_index=False).agg({'has_account_from_1997': 'max'})

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['district_id', 'has_account_from_1997'])
    # SelectCol
    _cols = [c for c in ['district_id', 'has_account_from_1997'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_crime_by_district = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_accounts_by_district = prepared_table_2

# prepared_crime_by_district expected columns: ['district_id','crime_1995']
# prepared_accounts_by_district expected columns: ['district_id','has_account_from_1997']

# Join on district_id
target = prepared_crime_by_district.merge(prepared_accounts_by_district, on='district_id', how='inner')

# Filter districts with crime_1995 > 4000 and with at least one account opened in or after 1997
filtered = target[(pd.to_numeric(target['crime_1995'], errors='coerce') > 4000) & (target['has_account_from_1997'] == True)]

# Compute the average number of crimes in 1995 across the filtered districts
answer = filtered['crime_1995'].astype(float).mean()

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
