import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_universities", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     # Long form first, then filter to names
    #     id_cols = [c for c in table_1.columns if c != 'University_ID']
    #     long_df = table_1.melt(id_vars=['University_ID'], value_vars=id_cols,
    #                            var_name='uni_id', value_name='val')
    #     long_df = long_df[long_df['University_ID'].astype(str) == 'University_Name'].copy()
    #     long_df['uni_id'] = long_df['uni_id'].astype(int)
    #     long_df = long_df.rename(columns={'val':'University_Name'})[['uni_id','University_Name']]
    #     return long_df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        # Long form first, then filter to names
        id_cols = [c for c in table_1.columns if c != 'University_ID']
        long_df = table_1.melt(id_vars=['University_ID'], value_vars=id_cols,
                               var_name='uni_id', value_name='val')
        long_df = long_df[long_df['University_ID'].astype(str) == 'University_Name'].copy()
        long_df['uni_id'] = long_df['uni_id'].astype(int)
        long_df = long_df.rename(columns={'val':'University_Name'})[['uni_id','University_Name']]
        return long_df
    prepared_universities = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="prepared_universities", column_name="University_Name", func="""
    # def transform_func(s: str) -> str:
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     # collapse repeated internal whitespace
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str) -> str:
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        # collapse repeated internal whitespace
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    prepared_universities["University_Name"] = prepared_universities["University_Name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="prepared_universities", subset=['uni_id'], keep="first")
    # Deduplicate
    prepared_universities = prepared_universities.drop_duplicates(subset=['uni_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['prepared_universities'])
    # Terminate
    result = {'prepared_universities': prepared_universities}
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
    # ErrorDetection(table_name="table_1", column_name="uni_id", func="""
    # def is_valid(val):
    #     try:
    #         return val is not None and str(val).strip() != '' and int(float(val)) >= 0
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        try:
            return val is not None and str(val).strip() != '' and int(float(val)) >= 0
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['uni_id'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['uni_id', 'Reputation_point', 'cit_p'])
    # SelectCol
    _cols = [c for c in ['uni_id', 'Reputation_point', 'cit_p'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="uni_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['uni_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['uni_id']
    if _dtype == "datetime64":
        table_1['uni_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['uni_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['uni_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['uni_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Reputation_point", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Reputation_point'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Reputation_point']
    if _dtype == "datetime64":
        table_1['Reputation_point'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Reputation_point'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Reputation_point'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Reputation_point'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="cit_p", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['cit_p'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['cit_p']
    if _dtype == "datetime64":
        table_1['cit_p'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['cit_p'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['cit_p'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['cit_p'] = _series.astype(str)

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
universities = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
uni_scores = prepared_table_2

# Assume prepared tables are provided as DataFrames: universities, uni_scores
# Join scores to names
joined = uni_scores.merge(universities, on='uni_id', how='inner')

# Ensure numeric types
joined['Reputation_point'] = pd.to_numeric(joined['Reputation_point'], errors='coerce')
joined['cit_p'] = pd.to_numeric(joined['cit_p'], errors='coerce')

# Get top 3 by reputation (breaking ties by higher cit_p, then by uni_id for determinism)
result = (
    joined.sort_values(by=['Reputation_point', 'cit_p', 'uni_id'], ascending=[False, False, True])
          .loc[:, ['University_Name', 'cit_p']]
          .head(3)
)

target = result.rename(columns={'University_Name': 'name', 'cit_p': 'citation_point'})

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
