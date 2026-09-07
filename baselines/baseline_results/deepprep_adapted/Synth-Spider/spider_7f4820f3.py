import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="boat_id", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     val = row.get('b')
    #     if pd.isna(val):
    #         return pd.NA
    #     try:
    #         return int(val)
    #     except Exception:
    #         return pd.NA
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        val = row.get('b')
        if pd.isna(val):
            return pd.NA
        try:
            return int(val)
        except Exception:
            return pd.NA
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["boat_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'name', 'new_name': 'boat_name'}])
    # Rename
    table_1 = table_1.rename(columns={'name': 'boat_name'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="color_norm", func="""
    # import pandas as pd
    # import re
    # 
    # def compute(row: pd.Series):
    #     val = row.get('clr')
    #     if pd.isna(val):
    #         return pd.NA
    #     s = str(val).lower()
    #     # keep only letters, spaces, underscores
    #     s = re.sub(r'[^a-z _]+', '', s)
    #     # normalize whitespace, then strip spaces/underscores from ends
    #     s = re.sub(r'\s+', ' ', s).strip(' _')
    #     # if underscores remain internally, collapse them (optional but helps matching)
    #     s = s.replace('_', '')
    #     s = s.strip()
    #     return s if s != '' else pd.NA
    # """)
    # AddNewColumn

    def compute(row: pd.Series):
        val = row.get('clr')
        if pd.isna(val):
            return pd.NA
        s = str(val).lower()
        # keep only letters, spaces, underscores
        s = re.sub(r'[^a-z _]+', '', s)
        # normalize whitespace, then strip spaces/underscores from ends
        s = re.sub(r'\s+', ' ', s).strip(' _')
        # if underscores remain internally, collapse them (optional but helps matching)
        s = s.replace('_', '')
        s = s.strip()
        return s if s != '' else pd.NA
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["color_norm"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['boat_id', 'boat_name', 'color_norm'])
    # SelectCol
    _cols = [c for c in ['boat_id', 'boat_name', 'color_norm'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
    # DropNulls(table_name="table_1", subset=['date_value_pairs'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['date_value_pairs'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Explode(table_name="table_1", column="date_value_pairs", split_comma=True)
    # Explode
    _ex_cols = 'date_value_pairs' if isinstance('date_value_pairs', list) else ['date_value_pairs']
    if all(_c in table_1.columns for _c in _ex_cols):
        try:
            for _col in _ex_cols:
                _nn = table_1[_col].dropna()
                _sample = _nn.iloc[0] if not _nn.empty else None
                if isinstance(_sample, str) or (pd.isna(_sample) and True):
                    if True:
                        table_1[_col] = table_1[_col].apply(lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) and x != '' else [])
                    else:
                        def _ex_parse(x):
                            if pd.isna(x) or x == '':
                                return []
                            try:
                                _r = ast.literal_eval(str(x))
                                return _r if isinstance(_r, list) else [_r]
                            except Exception:
                                return [i.strip() for i in str(x).split()]
                        table_1[_col] = table_1[_col].apply(_ex_parse)
                elif not isinstance(_sample, list) and _sample is not None:
                    table_1[_col] = table_1[_col].apply(lambda x: [x] if pd.notna(x) else [])
            if len(_ex_cols) == 1:
                table_1 = table_1.explode(_ex_cols[0]).reset_index(drop=True)
            else:
                table_1 = table_1.explode(_ex_cols).reset_index(drop=True)
        except Exception:
            pass

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="boat_id", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     pair = row['date_value_pairs']
    #     if pair is None or (isinstance(pair, float) and pd.isna(pair)):
    #         return None
    #     # expected like '9/12:102.0'
    #     val = str(pair).split(':', 1)[1].strip() if ':' in str(pair) else None
    #     return int(float(val)) if val not in (None, '') else None
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        pair = row['date_value_pairs']
        if pair is None or (isinstance(pair, float) and pd.isna(pair)):
            return None
        # expected like '9/12:102.0'
        val = str(pair).split(':', 1)[1].strip() if ':' in str(pair) else None
        return int(float(val)) if val not in (None, '') else None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["boat_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['sid', 'boat_id'])
    # SelectCol
    _cols = [c for c in ['sid', 'boat_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
prepared_boats = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_reservations = prepared_table_2

# prepared_boats creation
pb = table_1.copy()
pb = pb.rename(columns={'b':'boat_id','name':'boat_name','clr':'color_raw'})
# normalize color: lowercase, strip spaces, remove non-letters except spaces/underscore, then map common variants
pb['color_norm'] = (pb['color_raw']
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r'[^a-z_ ]','', regex=True)
    .str.replace(r'\s+',' ', regex=True)
    .str.strip())
# optional simple canonicalization of variants
pb['color_norm'] = pb['color_norm'].replace({'_red_':'red', ' red ':'red', ' blue ':'blue'})
pb['boat_id'] = pd.to_numeric(pb['boat_id'], errors='coerce').astype('Int64')
prepared_boats = pb[['boat_id','boat_name','color_norm']]

# prepared_reservations creation: explode date_value_pairs to rows
pr = table_2.copy()
pr = pr.rename(columns={'sid':'sid','date_value_pairs':'date_value_pairs'})
# split into list of pairs
pairs = pr['date_value_pairs'].astype(str).str.split(',')
pr = pr.loc[pr.index.repeat(pairs.str.len())].assign(pair=sum(pairs.tolist(), []))
# split 'date:boat' and cast boat to int
pr[['date','boat_str']] = pr['pair'].str.split(':', n=1, expand=True)
pr['boat_id'] = pd.to_numeric(pr['boat_str'], errors='coerce').astype('Int64')
prepared_reservations = pr[['sid','boat_id']].dropna(subset=['boat_id']).drop_duplicates()

# Integration
merged = prepared_reservations.merge(prepared_boats, on='boat_id', how='inner')

# Question-specific filter: boats that are red or blue
mask = merged['color_norm'].isin(['red','blue'])
result_sids = merged.loc[mask, 'sid'].drop_duplicates().sort_values()

answer = result_sids.tolist()
answer

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
