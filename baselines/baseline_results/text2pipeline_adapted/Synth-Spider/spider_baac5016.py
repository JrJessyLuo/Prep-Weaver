import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ygh', 'new_name': 'employee_id'}, {'old_name': 'Name', 'new_name': 'employee_name'}, {'old_name': 'zw', 'new_name': 'position_title'}, {'old_name': 'Salary', 'new_name': 'salary'}, {'old_name': 'bz', 'new_name': 'notes'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'employee_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'salary', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'employee_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['employee_id', 'employee_name']}, 'table_indices': [0]}], [{'op': 'CodeGeneration', 'params': {'func': "def transform(tables):\n    import pandas as pd\n    df = tables[0].copy()\n    # 1) Rename duplicate-numbered columns to unique strings preserving numeric meaning\n    # Original columns are physically ordered; use positions to avoid duplicate label ambiguity\n    cols = list(df.columns)\n    new_cols = []\n    seen = {}\n    for i, c in enumerate(cols):\n      if i == 0:\n        new_cols.append('Employee')\n        continue\n      # numeric label string from the original label\n      base = str(cols[i])\n      # map numeric base to col_{n}_{a/b/...} while preserving numeric meaning\n      if base not in seen:\n        seen[base] = 0\n      seen[base] += 1\n      suffix = chr(ord('a') + seen[base] - 1)\n      new_cols.append(f'col_{base}_{suffix}')\n    df.columns = new_cols\n\n    # 2) StandardizeString: trim in Employee\n    df['Employee'] = df['Employee'].astype(str).str.strip()\n\n    # 3) WideToLong equivalent: unpivot all numeric-id columns into ['employee_id_str','value']\n    value_cols = [c for c in df.columns if c.startswith('col_')]\n    long_df = df.melt(id_vars=['Employee'], value_vars=value_cols, var_name='col_key', value_name='value')\n    # derive employee_id_str by stripping 'col_' prefix and any suffix after last underscore\n    # col format: col_<number>_<suffix>\n    employee_id_str = long_df['col_key'].str.replace('^col_', '', regex=True).str.replace('_[^_]+$', '', regex=True)\n    long_df['employee_id_str'] = employee_id_str\n\n    # 4) Cast types\n    # Coerce to numeric; errors='coerce' then drop NaNs\n    long_df['employee_id'] = pd.to_numeric(long_df['employee_id_str'], errors='coerce').astype('Int64')\n    long_df['level_value'] = pd.to_numeric(long_df['value'], errors='coerce').astype('Int64')\n\n    # 5) Select and rename\n    out = long_df[['Employee', 'employee_id', 'level_value']].rename(columns={'Employee': 'attribute', 'level_value': 'level'})\n\n    # 6) Filter only Level rows\n    out = out[out['attribute'] == 'Level']\n\n    # 7) Drop attribute column\n    out = out.drop(columns=['attribute'])\n\n    # Ensure int dtype for final columns\n    out = out.dropna(subset=['employee_id', 'level'])\n    out['employee_id'] = out['employee_id'].astype(int)\n    out['level'] = out['level'].astype(int)\n    # Final columns order\n    return out[['employee_id', 'level']]"}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ygh': 'employee_id', 'Name': 'employee_name', 'zw': 'position_title', 'Salary': 'salary', 'bz': 'notes'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['employee_id'] = pd.to_numeric(tmp_1['employee_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['salary'] = pd.to_numeric(tmp_2['salary'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['employee_name'] = tmp_3['employee_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['employee_id', 'employee_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CodeGeneration
    _ns_1 = {}
    exec("def transform(tables):\n    import pandas as pd\n    df = tables[0].copy()\n    # 1) Rename duplicate-numbered columns to unique strings preserving numeric meaning\n    # Original columns are physically ordered; use positions to avoid duplicate label ambiguity\n    cols = list(df.columns)\n    new_cols = []\n    seen = {}\n    for i, c in enumerate(cols):\n      if i == 0:\n        new_cols.append('Employee')\n        continue\n      # numeric label string from the original label\n      base = str(cols[i])\n      # map numeric base to col_{n}_{a/b/...} while preserving numeric meaning\n      if base not in seen:\n        seen[base] = 0\n      seen[base] += 1\n      suffix = chr(ord('a') + seen[base] - 1)\n      new_cols.append(f'col_{base}_{suffix}')\n    df.columns = new_cols\n\n    # 2) StandardizeString: trim in Employee\n    df['Employee'] = df['Employee'].astype(str).str.strip()\n\n    # 3) WideToLong equivalent: unpivot all numeric-id columns into ['employee_id_str','value']\n    value_cols = [c for c in df.columns if c.startswith('col_')]\n    long_df = df.melt(id_vars=['Employee'], value_vars=value_cols, var_name='col_key', value_name='value')\n    # derive employee_id_str by stripping 'col_' prefix and any suffix after last underscore\n    # col format: col_<number>_<suffix>\n    employee_id_str = long_df['col_key'].str.replace('^col_', '', regex=True).str.replace('_[^_]+$', '', regex=True)\n    long_df['employee_id_str'] = employee_id_str\n\n    # 4) Cast types\n    # Coerce to numeric; errors='coerce' then drop NaNs\n    long_df['employee_id'] = pd.to_numeric(long_df['employee_id_str'], errors='coerce').astype('Int64')\n    long_df['level_value'] = pd.to_numeric(long_df['value'], errors='coerce').astype('Int64')\n\n    # 5) Select and rename\n    out = long_df[['Employee', 'employee_id', 'level_value']].rename(columns={'Employee': 'attribute', 'level_value': 'level'})\n\n    # 6) Filter only Level rows\n    out = out[out['attribute'] == 'Level']\n\n    # 7) Drop attribute column\n    out = out.drop(columns=['attribute'])\n\n    # Ensure int dtype for final columns\n    out = out.dropna(subset=['employee_id', 'level'])\n    out['employee_id'] = out['employee_id'].astype(int)\n    out['level'] = out['level'].astype(int)\n    # Final columns order\n    return out[['employee_id', 'level']]", globals(), _ns_1)
    _cg_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    result = _cg_func_1([df])
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='employee_id', how='inner')
# Omega III corresponds to level 3
filtered = integrated[integrated['level'] == 3]
# Deduplicate employee names in case of multiple rows per employee
target = filtered[['employee_name']].drop_duplicates().sort_values('employee_name').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
