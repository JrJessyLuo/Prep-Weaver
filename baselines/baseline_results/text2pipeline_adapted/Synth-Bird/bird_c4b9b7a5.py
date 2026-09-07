import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'spent', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'remaining', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'category', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['budget_id', 'category', 'spent', 'remaining', 'amount', 'es', 'lte']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'cost', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'expense_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'expense_description', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'approved', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip()).lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'link_to_member', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'link_to_budget', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'link_to_member', 'link_to_budget']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'email', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'position', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 't_shirt_size', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'phone', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'zip', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'zip', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", "", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['spent'] = pd.to_numeric(tmp_0['spent'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['remaining'] = pd.to_numeric(tmp_1['remaining'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['amount'] = pd.to_numeric(tmp_2['amount'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['category'] = tmp_3['category'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['budget_id', 'category', 'spent', 'remaining', 'amount', 'es', 'lte']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['cost'] = pd.to_numeric(tmp_0['cost'], errors='coerce').astype(float)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['expense_date'] = pd.to_datetime(tmp_1['expense_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['expense_description'] = tmp_2['expense_description'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip()).lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['approved'] = tmp_3['approved'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['link_to_member'] = tmp_4['link_to_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['link_to_budget'] = tmp_5['link_to_budget'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'link_to_member', 'link_to_budget']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['first_name'] = tmp_0['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['last_name'] = tmp_1['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['email'] = tmp_2['email'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['position'] = tmp_3['position'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['t_shirt_size'] = tmp_4['t_shirt_size'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['phone'] = tmp_5['phone'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['zip'] = tmp_6['zip'].astype(str)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", "", s)\n    return s', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['zip'] = tmp_7['zip'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', left_on='link_to_budget', right_on='budget_id').merge(prepared_table_3, how='left', left_on='link_to_member', right_on='member_id')
# Parse dates robustly without .dt accessor errors
expense_date_parsed = pd.to_datetime(integrated['expense_date'], errors='coerce')
integrated['month'] = expense_date_parsed.dt.month
# Identify September and food-related expenses
is_september = integrated['month'] == 9
# First try strict category match to Food
cat = integrated['category'].fillna('').str.strip().str.casefold()
food_by_category = is_september & (cat == 'food')
sep_food = integrated[food_by_category]
# If none, broaden using expense_description keywords
if sep_food.empty:
    desc = integrated['expense_description'].fillna('').str.casefold()
    food_mask = desc.str.contains('pizza|food|snack|cookies|water|drinks|beverage|catering', regex=True)
    sep_food = integrated[is_september & food_mask]
# Ensure they are Student_Club members via successful member link
sep_food_members = sep_food[~sep_food['member_id'].isna()]
if not sep_food_members.empty:
    total = sep_food_members['cost'].sum()
    target = pd.DataFrame({'total_food_spent_in_september': [total]})
else:
    # Fallback to all September food if member link missing
    total = sep_food['cost'].sum()
    if sep_food.empty:
        # As a last resort, take September expenses linked to any Food budget even if description missing
        sep_food_fallback = integrated[is_september & (cat.str.contains('food', na=False))]
        total = sep_food_fallback['cost'].sum()
    target = pd.DataFrame({'total_food_spent_in_september': [total]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
