import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row['id']) == 'superhero_name'
    # """)
    # Filter
    def filter_func(row):
        return str(row['id']) == 'superhero_name'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_superhero_names", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Unpivot all hero columns into a single column of names
    #     value_vars = [c for c in df.columns if c != 'id']
    #     long_df = df.melt(id_vars=['id'], value_vars=value_vars, var_name='hero_col', value_name='superhero_name')
    # 
    #     # Keep only non-null, non-empty names
    #     long_df['superhero_name'] = long_df['superhero_name'].astype(str)
    #     long_df['superhero_name'] = long_df['superhero_name'].where(~long_df['superhero_name'].isin(['nan', 'None']), None)
    #     long_df['superhero_name'] = long_df['superhero_name'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    # 
    #     long_df = long_df.dropna(subset=['superhero_name'])
    #     long_df = long_df[long_df['superhero_name'] != '']
    # 
    #     # Output only the required column
    #     out = long_df[['superhero_name']].drop_duplicates().reset_index(drop=True)
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Unpivot all hero columns into a single column of names
        value_vars = [c for c in df.columns if c != 'id']
        long_df = df.melt(id_vars=['id'], value_vars=value_vars, var_name='hero_col', value_name='superhero_name')

        # Keep only non-null, non-empty names
        long_df['superhero_name'] = long_df['superhero_name'].astype(str)
        long_df['superhero_name'] = long_df['superhero_name'].where(~long_df['superhero_name'].isin(['nan', 'None']), None)
        long_df['superhero_name'] = long_df['superhero_name'].apply(lambda x: x.strip() if isinstance(x, str) else x)

        long_df = long_df.dropna(subset=['superhero_name'])
        long_df = long_df[long_df['superhero_name'] != '']

        # Output only the required column
        out = long_df[['superhero_name']].drop_duplicates().reset_index(drop=True)
        return out
    prepared_superhero_names = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['prepared_superhero_names'])
    # Terminate
    result = {'prepared_superhero_names': prepared_superhero_names}
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
    # ErrorDetection(table_name="table_1", column_name="hero_power", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return '-' in s and len(s.split('-', 1)[0].strip()) > 0 and len(s.split('-', 1)[1].strip()) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return '-' in s and len(s.split('-', 1)[0].strip()) > 0 and len(s.split('-', 1)[1].strip()) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['hero_power'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     val = row['hero_power']
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     if '-' not in s:
    #         return False
    #     left, right = s.split('-', 1)
    #     return left.strip() != '' and right.strip() != ''
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        val = row['hero_power']
        if val is None:
            return False
        s = str(val).strip()
        if '-' not in s:
            return False
        left, right = s.split('-', 1)
        return left.strip() != '' and right.strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="hero_power", target_columns=['superhero_name', 'power_name'], func="""
    # def split(val):
    #     s = str(val).strip()
    #     left, right = s.split('-', 1)
    #     return {"superhero_name": left.strip(), "power_name": right.strip()}
    # """)
    # SplitColumn
    def split(val):
        s = str(val).strip()
        left, right = s.split('-', 1)
        return {"superhero_name": left.strip(), "power_name": right.strip()}
    for _c in ['superhero_name', 'power_name']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['hero_power']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['superhero_name', 'power_name']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['hero_power'])

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['superhero_name', 'power_name'])
    # SelectCol
    _cols = [c for c in ['superhero_name', 'power_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['superhero_name', 'power_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['superhero_name', 'power_name'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
hero_powers = prepared_table_2

# prepared tables assumed: heroes(superhero_name), hero_powers(superhero_name, power_name)

# 1) Join to align names (inner join keeps only heroes with listed powers)
joined = hero_powers.merge(heroes, on='superhero_name', how='inner')

# 2) Filter to the specific hero Amazo (case-sensitive match as in table_1 sample)
amazo_powers = joined[joined['superhero_name'] == 'Amazo']

# 3) Count distinct powers
answer = amazo_powers['power_name'].nunique()

result = int(answer)

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
