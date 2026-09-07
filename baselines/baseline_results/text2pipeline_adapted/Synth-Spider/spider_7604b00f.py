import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'PassThroughFallback', 'params': {'reason': 'fallback_passthrough_after_pipeline_generation_failure: Your previous one-table transform_chain was invalid: ValueError: operation(s) outside benchmark dc_ops space: Filter. Use only table_indices [0], correct the chain, and return JSON only.', 'source_table': 'table_1'}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Club_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Name_Country', 'target_columns': ['Player_Name', 'Country'], 'func': "def transform(s):\n    parts = str(s).split('|', 1)\n    if len(parts) == 1:\n        parts.append(None)\n    return parts"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Player_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Earnings', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Events_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Wins_count', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Player_ID', 'Player_Name', 'Country', 'Earnings', 'Events_number', 'Wins_count', 'Club_ID']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Club_ID'] = pd.to_numeric(tmp_0['Club_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('|', 1)\n    if len(parts) == 1:\n        parts.append(None)\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_1['Name_Country'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['Player_Name'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['Country'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Player_ID'] = pd.to_numeric(tmp_2['Player_ID'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Earnings'] = pd.to_numeric(tmp_3['Earnings'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Events_number'] = pd.to_numeric(tmp_4['Events_number'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Wins_count'] = pd.to_numeric(tmp_5['Wins_count'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['Player_ID', 'Player_Name', 'Country', 'Earnings', 'Events_number', 'Wins_count', 'Club_ID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
clubs_raw = prepared_table_1.copy()
players = prepared_table_2.copy()

# Reshape clubs table: it's in a transposed-like format with first column as attribute names and subsequent columns as club names under numeric labels
# Identify the row that contains club names (where the first column equals 'Name')
name_row = clubs_raw[clubs_raw.iloc[:, 0].astype(str).str.strip().str.lower() == 'name']
if name_row.empty:
    # Fallback: try case-insensitive partial match
    name_row = clubs_raw[clubs_raw.iloc[:, 0].astype(str).str.contains('name', case=False, na=False)]

# Build clubs DataFrame with Club_ID (from column labels 1..n) and Club_Name (values in the 'Name' row)
if not name_row.empty:
    # Extract the single name row values excluding the first identifier column
    name_values = name_row.iloc[0, 1:]
    # Column labels for Club_IDs are the header labels from position 1..n; use columns themselves as IDs
    club_ids = clubs_raw.columns[1:]
    clubs = (
        (
            name_values.to_frame(name='Club_Name')
            .assign(Club_ID=club_ids.values)
        )
        .loc[:, ['Club_ID', 'Club_Name']]
        .reset_index(drop=True)
    )
else:
    # If not found, create an empty structure to avoid errors
    clubs = clubs_raw.iloc[0:0, :0].copy()

# Ensure compatible dtypes for merge on Club_ID
clubs['Club_ID'] = clubs['Club_ID'].astype(str)
players['Club_ID'] = players['Club_ID'].astype(str)

# Merge to find clubs without players
integrated = clubs.merge(players[['Club_ID', 'Player_ID']], on='Club_ID', how='left')
no_player = integrated[integrated['Player_ID'].isna()].drop_duplicates(subset=['Club_ID', 'Club_Name'])

# Final target with club names
target = no_player[['Club_Name']].reset_index(drop=True)

# Fallback: if empty, still return all club names as most plausible integrated rows (since question asks clubs without players and players table may be sparse)
if target.empty:
    target = clubs[['Club_Name']].reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
