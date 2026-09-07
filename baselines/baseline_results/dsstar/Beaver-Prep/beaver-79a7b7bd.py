import pandas as pd
import re

# Source tables from the provided `tables` dict
moira_owner = tables['table_1']  # MOIRA_LIST_OWNER.pkl
moira_detail = tables['table_2']  # MOIRA_LIST_DETAIL.pkl
moira_list = tables['table_4']  # MOIRA_LIST.pkl
subject_grouping = tables['table_9']  # SUBJECT_GROUPING.pkl

# 1) Reproduce joins: DETAIL + LIST + OWNER
detail_with_list = moira_detail.merge(
    moira_list[['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_PUBLIC', 'IS_HIDDEN']],
    on='MOIRA_LIST_KEY',
    how='left',
    validate='m:1'
)

detail_full = detail_with_list.merge(
    moira_owner[['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']],
    on='MOIRA_LIST_OWNER_KEY',
    how='left',
    validate='m:1'
)

# 2) Build canonical set of department names starting with 'Computer Science' from SUBJECT_GROUPING
dept_cols = ['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME']
for col in dept_cols:
    if col not in subject_grouping.columns:
        subject_grouping[col] = pd.Series(dtype='object')

def starts_with_cs(x: str) -> bool:
    if pd.isna(x):
        return False
    return str(x).strip().lower().startswith('computer science')

cs_depts = set()
if not subject_grouping.empty:
    cs_depts.update(subject_grouping.loc[subject_grouping['DEPARTMENT_NAME'].apply(starts_with_cs), 'DEPARTMENT_NAME'].dropna().unique().tolist())
    cs_depts.update(subject_grouping.loc[subject_grouping['DEPARTMENT_FULL_NAME'].apply(starts_with_cs), 'DEPARTMENT_FULL_NAME'].dropna().unique().tolist())

cs_depts_norm = {str(d).strip().lower() for d in cs_depts if isinstance(d, str)}

# 3) Heuristic matcher for OWNER or LIST name mentioning CS departments/abbreviations
def text_matches_cs(text: str) -> bool:
    if not isinstance(text, str):
        return False
    t = text.lower()
    if t.startswith('computer science'):
        return True
    for dept in cs_depts_norm:
        if dept and dept in t:
            return True
    patterns = [
        r'\beecs\b',
        r'\bcs\b',
        r'\bc s\b',
        r'\bcourse\s*6\b',
        r'\bcomp(uter)?\s*sci(ence)?\b'
    ]
    return any(re.search(p, t) for p in patterns)

# 4) Filter to mailing lists plausibly associated to CS departments
detail_full['is_mailing_list'] = detail_full['IS_MOIRA_MAILING_LIST'].fillna('N').eq('Y')
detail_full['owner_matches_cs'] = detail_full['OWNER'].apply(text_matches_cs)
detail_full['listname_matches_cs'] = detail_full['MOIRA_LIST_NAME'].apply(text_matches_cs)

filtered = detail_full[
    detail_full['is_mailing_list'] &
    (detail_full['owner_matches_cs'] | detail_full['listname_matches_cs'])
].copy()

# If nothing matches, we still need to return an empty but well-formed result
if filtered.empty:
    final_cols = ['OWNER_TYPE', 'MOIRA_LIST_NAME', 'NUM_OWNERS', 'NUM_SUBSCRIBERS']
    result_df = pd.DataFrame(columns=final_cols + ['_order_group', '_order_within'])
else:
    # 5) Compute number of owners per list and number of subscribers per list
    # Owners: distinct OWNER per (MOIRA_LIST_KEY)
    owners_per_list = (
        filtered[['MOIRA_LIST_KEY', 'OWNER_TYPE', 'OWNER']]
        .dropna(subset=['MOIRA_LIST_KEY'])
        .groupby(['MOIRA_LIST_KEY', 'OWNER_TYPE'], as_index=False)['OWNER']
        .nunique()
        .rename(columns={'OWNER': 'NUM_OWNERS'})
    )

    # Subscribers: count of rows with moira_list_member where OWNER_TYPE is not needed; use MOIRA_LIST_KEY
    subs_per_list = (
        filtered[['MOIRA_LIST_KEY', 'moira_list_member']]
        .dropna(subset=['MOIRA_LIST_KEY'])
        .groupby('MOIRA_LIST_KEY', as_index=False)['moira_list_member']
        .nunique(dropna=True)
        .rename(columns={'moira_list_member': 'NUM_SUBSCRIBERS'})
    )

    # Bring in list name
    list_names = filtered[['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME']].drop_duplicates()

    # Combine aggregates
    agg_df = owners_per_list.merge(subs_per_list, on='MOIRA_LIST_KEY', how='left')
    agg_df = agg_df.merge(list_names, on='MOIRA_LIST_KEY', how='left')

    # Fill missing with 0 for counts
    agg_df['NUM_OWNERS'] = agg_df['NUM_OWNERS'].fillna(0).astype(int)
    agg_df['NUM_SUBSCRIBERS'] = agg_df['NUM_SUBSCRIBERS'].fillna(0).astype(int)

    # 6) Prepare detail rows per OWNER_TYPE, MOIRA_LIST_NAME
    detail_rows = agg_df[['OWNER_TYPE', 'MOIRA_LIST_NAME', 'NUM_OWNERS', 'NUM_SUBSCRIBERS']].copy()

    # 7) Subtotals per OWNER_TYPE
    subtotals = (
        detail_rows
        .groupby('OWNER_TYPE', as_index=False)[['NUM_OWNERS', 'NUM_SUBSCRIBERS']]
        .sum()
        .assign(MOIRA_LIST_NAME='SUBTOTAL')
    )

    # 8) Grand total across all OWNER_TYPE
    grand_total = pd.DataFrame({
        'OWNER_TYPE': ['TOTAL'],
        'MOIRA_LIST_NAME': ['TOTAL'],
        'NUM_OWNERS': [detail_rows['NUM_OWNERS'].sum()],
        'NUM_SUBSCRIBERS': [detail_rows['NUM_SUBSCRIBERS'].sum()]
    })

    # 9) Order rows: group by OWNER_TYPE, sort list names ascending, append subtotal, then final total
    # Determine sort order of OWNER_TYPE alphabetically for deterministic output
    owner_types_order = sorted(detail_rows['OWNER_TYPE'].dropna().unique().tolist())

    ordered_parts = []
    order_counter = 0
    for ot in owner_types_order:
        part = detail_rows[detail_rows['OWNER_TYPE'] == ot].copy()
        part = part.sort_values(['MOIRA_LIST_NAME'], kind='mergesort').reset_index(drop=True)
        part['_order_group'] = order_counter
        part['_order_within'] = range(len(part))
        ordered_parts.append(part)

        # Append subtotal for this OWNER_TYPE
        sub = subtotals[subtotals['OWNER_TYPE'] == ot].copy()
        sub['_order_group'] = order_counter
        sub['_order_within'] = len(part)  # after details
        ordered_parts.append(sub)

        order_counter += 1

    ordered = pd.concat(ordered_parts, ignore_index=True) if ordered_parts else pd.DataFrame(columns=detail_rows.columns.tolist() + ['_order_group', '_order_within'])

    # Append grand total at the end
    grand_total['_order_group'] = order_counter
    grand_total['_order_within'] = 0

    result_df = pd.concat([ordered, grand_total], ignore_index=True, sort=False)

    # 10) Display ownership type only when it differs from previous entry
    # Sort by the constructed order
    result_df = result_df.sort_values(['_order_group', '_order_within'], kind='mergesort').reset_index(drop=True)

    # Mask OWNER_TYPE for repeated consecutive values except for SUBTOTAL and TOTAL rows:
    # We keep OWNER_TYPE for the first row in each group, for 'SUBTOTAL', and for 'TOTAL'.
    display_owner_type = []
    prev = None
    for _, row in result_df.iterrows():
        name = str(row['MOIRA_LIST_NAME'])
        ot = row['OWNER_TYPE']
        if name in ('SUBTOTAL', 'TOTAL'):
            display_owner_type.append(ot)
            prev = None  # reset after subtotal/total
        else:
            if ot != prev:
                display_owner_type.append(ot)
                prev = ot
            else:
                display_owner_type.append('')
    result_df['OWNER_TYPE'] = display_owner_type

# Final selection and column order
final_cols = ['OWNER_TYPE', 'MOIRA_LIST_NAME', 'NUM_OWNERS', 'NUM_SUBSCRIBERS']
result_table = result_df[final_cols].copy()

# Package into the expected `result` dict
result = {'mailing_lists_cs_with_subtotals': result_table}