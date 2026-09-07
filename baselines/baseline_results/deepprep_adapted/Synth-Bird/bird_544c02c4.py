import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IGG", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IGG'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IGG']
    if _dtype == "datetime64":
        table_1['IGG'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IGG'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IGG'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IGG'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
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
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'IGG'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'IGG'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['IGG'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IGG'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID', 'Date'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID', 'Date'], keep='last').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['ID', 'Admission'])
    # SelectCol
    _cols = [c for c in ['ID', 'Admission'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Admission", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # normalize common encodings
    #     if s in ["＋", "+"]:
    #         return "+"
    #     if s in ["－", "-"]:
    #         return "-"
    #     if s == "" or s.lower() in ["nan", "none", "null"]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # normalize common encodings
        if s in ["＋", "+"]:
            return "+"
        if s in ["－", "-"]:
            return "-"
        if s == "" or s.lower() in ["nan", "none", "null"]:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Admission"] = table_1["Admission"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Admission", mode="mode")
    # MissingValueImputation
    table_1["Admission"] = table_1["Admission"].fillna(table_1["Admission"].mode().iloc[0])

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
labs_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
patients_prepared = prepared_table_2

# Assume labs_prepared and patients_prepared are the synthesized tables per targets above
# Define a helper to determine normal IGG; if a reference range is known, adjust here.
# As the question only asks for 'normal level of IGG' without a given range, we conservatively treat rows with non-null IGG and an accompanying normal flag if available.
# If no flag exists, you may need to supply a normal-range function. Here we demonstrate with an example adult reference range 700-1600 mg/dL.

def is_normal_igg(val):
    try:
        if pd.isna(val):
            return False
        v = float(val)
        return 700.0 <= v <= 1600.0
    except Exception:
        return False

labs = labs_prepared.copy()
patients = patients_prepared.copy()

# Determine per-patient normal IGG status if any lab record shows normal IGG
labs['is_normal_IGG'] = labs['IGG'].apply(is_normal_igg)
normal_igg_by_patient = (
    labs.groupby('ID', as_index=False)['is_normal_IGG']
        .max()  # True if any record normal
)

# Join with admissions
merged = normal_igg_by_patient.merge(patients[['ID','Admission']], on='ID', how='left')

# Define admission-positive values; in samples '-' indicates not admitted
def admitted_flag(x):
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    # Treat common positive indicators as admission
    return s in {'yes','y','admitted','1','true','t','inpatient','ip','admit','hospitalized'}

merged['is_admitted'] = merged['Admission'].apply(admitted_flag)

# Count patients with normal IGG who were admitted
answer = int((merged['is_normal_IGG'] & merged['is_admitted']).sum())

result = pd.DataFrame({'count_admitted_with_normal_IGG': [answer]})

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
