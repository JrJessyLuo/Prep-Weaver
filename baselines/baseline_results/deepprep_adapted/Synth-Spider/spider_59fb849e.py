import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="aff_id", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['aff_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['aff_id']
    if _dtype == "datetime64":
        table_1['aff_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['aff_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['aff_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['aff_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="paper_aff_link", func="""
    # import pandas as pd
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Normalize aff_id missing markers that may be stored as strings
    #     df['aff_id'] = df['aff_id'].replace(
    #         to_replace=[r'^\s*nan\s*$', r'^\s*NaN\s*$', r'^\s*None\s*$', r'^\s*null\s*$', r'^\s*\s*$'],
    #         value=pd.NA,
    #         regex=True
    #     )
    # 
    #     # Cast to nullable integer for safe joins later
    #     df['aff_id'] = pd.to_numeric(df['aff_id'], errors='coerce').astype('Int64')
    # 
    #     # Keep only target columns (drop aid)
    #     return df[['paper_id', 'aff_id']]
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Normalize aff_id missing markers that may be stored as strings
        df['aff_id'] = df['aff_id'].replace(
            to_replace=[r'^\s*nan\s*$', r'^\s*NaN\s*$', r'^\s*None\s*$', r'^\s*null\s*$', r'^\s*\s*$'],
            value=pd.NA,
            regex=True
        )

        # Cast to nullable integer for safe joins later
        df['aff_id'] = pd.to_numeric(df['aff_id'], errors='coerce').astype('Int64')

        # Keep only target columns (drop aid)
        return df[['paper_id', 'aff_id']]
    paper_aff_link = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['paper_aff_link'])
    # Terminate
    result = {'paper_aff_link': paper_aff_link}
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['attribute']).strip().lower() == 'name'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['attribute']).strip().lower() == 'name'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'value', 'new_name': 'name'}])
    # Rename
    table_1 = table_1.rename(columns={'value': 'name'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['affiliation_id', 'name'])
    # SelectCol
    _cols = [c for c in ['affiliation_id', 'name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
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
papers_affiliations = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
affiliation_metadata = prepared_table_2

# Prepared tables assumed available: papers_affiliations, affiliation_metadata
# Clean types and drop missing affiliations
pa = papers_affiliations.copy()
pa = pa[pa['aff_id'].notna()]
# Ensure integer-compatible join keys
pa['aff_id'] = pa['aff_id'].astype('int64')
aff = affiliation_metadata.copy()
aff['affiliation_id'] = aff['affiliation_id'].astype('int64')

# Join affiliations to get names
merged = pa.merge(aff, left_on='aff_id', right_on='affiliation_id', how='inner')

# Count distinct papers per affiliation (use nunique to avoid double-counting same paper multiple rows)
result = (
    merged.groupby(['aff_id', 'name'])['paper_id']
    .nunique()
    .reset_index(name='total_papers')
)

# Sort optionally by descending count and name
result = result.sort_values(['total_papers', 'name'], ascending=[False, True]).reset_index(drop=True)

target = result

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
