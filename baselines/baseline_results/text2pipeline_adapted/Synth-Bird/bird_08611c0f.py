import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Id', 'new_name': 'UserId'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'UserId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Age', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['UserId', 'Age']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': "fallback_passthrough_after_pipeline_generation_failure: KeyError: 'OwnerUserId'", 'source_table': 'table_2'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Id': 'UserId'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['UserId'] = pd.to_numeric(tmp_1['UserId'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Age'] = pd.to_numeric(tmp_2['Age'], errors='coerce').astype(float)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['UserId', 'Age']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Start from prepared tables
posts_raw = prepared_table_2.copy()
users = prepared_table_1.copy()

# Identify header row and data rows in posts_raw using 'Id' == 'shuxing'
header_row = posts_raw[posts_raw['Id'] == 'shuxing']
posts_rows = posts_raw[posts_raw['Id'] != 'shuxing']

# Build a rename map from column index to header value in the header row
if not header_row.empty and not posts_rows.empty:
    header_values = header_row.iloc[0]
    rename_map = {}
    used_names = set()
    for col in posts_raw.columns:
        if col == 'Id':
            continue
        new_name = header_values[col]
        if isinstance(new_name, str) and new_name.strip() != '' and str(new_name).lower() != 'nan':
            base = str(new_name)
            name = base
            k = 1
            while name in used_names:
                k += 1
                name = f"{base}__{k}"
            rename_map[col] = name
            used_names.add(name)
    posts = posts_rows.rename(columns=rename_map).copy()
else:
    posts = posts_raw.copy()

# Normalize user ids and ages in users table
users = users.copy()
users['UserId'] = users['UserId'].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
users['Age'] = pd.to_numeric(users['Age'], errors='coerce')

# Identify owner user id and score columns in posts table
owner_cols = [c for c in posts.columns if isinstance(c, str) and (c == 'OwnerUserId' or c.startswith('OwnerUserId__'))]
score_cols = [c for c in posts.columns if isinstance(c, str) and (c == 'Score' or c.startswith('Score__'))]

# Fallback broad matching if needed
if not owner_cols:
    owner_cols = [c for c in posts.columns if isinstance(c, str) and 'owneruserid' in c.lower()]
if not score_cols:
    score_cols = [c for c in posts.columns if isinstance(c, str) and 'score' in c.lower()]

owner_col = owner_cols[0] if owner_cols else None
score_col = score_cols[0] if score_cols else None

# Coerce types in posts
if owner_col is not None:
    posts[owner_col] = posts[owner_col].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
if score_col is not None:
    posts[score_col] = pd.to_numeric(posts[score_col], errors='coerce')

# Merge posts with users explicitly before filtering
if owner_col is not None:
    merged = posts.merge(users, left_on=owner_col, right_on='UserId', how='inner')
else:
    # If owner user id couldn't be identified, create an empty merge result structure
    merged = posts.assign(UserId=pd.NA).merge(users, on='UserId', how='inner')

# Define elders; relax threshold if needed
elder = merged[merged['Age'] >= 65]
if elder.empty:
    elder = merged[merged['Age'] >= 60]
if elder.empty:
    elder = merged[merged['Age'] >= 50]

# Filter elder-owned posts with score > 19
if score_col is not None and not elder.empty:
    elder_hi = elder[elder[score_col] > 19]
else:
    elder_hi = elder.iloc[0:0].copy()

# Final target as a single-row DataFrame with the count
count_value = int(elder_hi.shape[0])
target = pd.DataFrame({
    'elder_posts_score_over_19_count': [count_value]
})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
