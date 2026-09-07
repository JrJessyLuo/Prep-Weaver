import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'event_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['event_id', 'event_name', 'event_date']}, 'table_indices': [0]}], [{'op': 'StandardizeDatetime', 'params': {'column_name': 'expense_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'cost', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_budget', 'new_name': 'budget_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'link_to_member', 'budget_id']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_event', 'new_name': 'event_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'remaining', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'spent', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['budget_id', 'category', 'event_status', 'event_id', 'amount', 'remaining', 'spent']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['event_date'] = pd.to_datetime(tmp_0['event_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['event_id', 'event_name', 'event_date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['expense_date'] = pd.to_datetime(tmp_0['expense_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['cost'] = pd.to_numeric(tmp_1['cost'], errors='coerce').astype(float)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'link_to_budget': 'budget_id'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'link_to_member', 'budget_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'link_to_event': 'event_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['amount'] = pd.to_numeric(tmp_1['amount'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['remaining'] = pd.to_numeric(tmp_2['remaining'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['spent'] = pd.to_numeric(tmp_3['spent'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['budget_id', 'category', 'event_status', 'event_id', 'amount', 'remaining', 'spent']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
events = prepared_table_1.copy()
budgets = prepared_table_4.copy()
expenses = prepared_table_2.copy()

# Merge in the correct relational order: budgets -> events, then expenses -> budgets_events
budgets_events = budgets.merge(events, on='event_id', how='left')
full = expenses.merge(budgets_events, on='budget_id', how='left')

# Ensure event_date is parsed as datetime for year extraction
full['event_date_parsed'] = __import__('pandas').to_datetime(full['event_date'], errors='coerce')
full['year'] = full['event_date_parsed'].dt.year

# Aggregate total cost by year (use sum with min_count=1 to avoid all-NaN collapsing)
agg = full.groupby('year', dropna=False)['cost'].sum(min_count=1).reset_index()

# Safely extract totals for 2019 and 2020 (default to 0.0 if not present)
total_2019 = float(agg.loc[agg['year'] == 2019, 'cost'].sum()) if (agg['year'] == 2019).any() else 0.0
total_2020 = float(agg.loc[agg['year'] == 2020, 'cost'].sum()) if (agg['year'] == 2020).any() else 0.0

# Compute difference: 2019 minus 2020
diff = total_2019 - total_2020

target = __import__('pandas').DataFrame([
    {
        'year_2019_total': total_2019,
        'year_2020_total': total_2020,
        'difference_2019_minus_2020': diff
    }
])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
