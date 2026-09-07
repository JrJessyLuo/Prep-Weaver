import pandas as pd
import numpy as np

# Access preloaded tables
fac = tables['table_1']            # FAC_BUILDING.pkl
addr = tables['table_9']           # FCLT_BUILDING_ADDRESS.pkl

# Columns of interest from FAC_BUILDING
fac_cols_needed = [
    'FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME_LONG',
    'PARENT_BUILDING_NUMBER', 'PARENT_BUILDING_NAME', 'PARENT_BUILDING_NAME_LONG',
    'BUILDING_TYPE', 'OWNERSHIP_TYPE', 'OCCUPANCY_CLASS', 'BUILDING_USE',
    'SITE', 'CAMPUS_SECTOR', 'BUILDING_HEIGHT', 'ACCESS_LEVEL_CODE', 'ACCESS_LEVEL_NAME',
    'EXT_GROSS_AREA', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA', 'BUILDING_SORT',
    'OCCUPANCY_DATE'
]
fac_existing_cols = [c for c in fac_cols_needed if c in fac.columns]
fac_view = fac[fac_existing_cols].copy()

# Filtering to exclude subdivisions (heuristics):
# - Prefer records with no parent (PARENT_BUILDING_NUMBER is null)
# - Exclude rows where BUILDING_TYPE contains 'SUBDIV' (case-insensitive)
is_parent_null = fac_view['PARENT_BUILDING_NUMBER'].isna() if 'PARENT_BUILDING_NUMBER' in fac_view.columns else pd.Series([True]*len(fac_view), index=fac_view.index)
if 'BUILDING_TYPE' in fac_view.columns:
    not_subdivision = ~fac_view['BUILDING_TYPE'].astype(str).str.contains('SUBDIV', case=False, na=False)
else:
    not_subdivision = pd.Series([True]*len(fac_view), index=fac_view.index)

fac_candidates = fac_view[is_parent_null & not_subdivision].copy()

# Address columns of interest
addr_cols_needed = [
    'FCLT_BUILDING_ADDRESS_KEY', 'FCLT_BUILDING_KEY', 'BUILDING_NUMBER',
    'ADDRESS_PURPOSE', 'IS_E911_ADDRESS',
    'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL',
    'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL',
    'CITY', 'STATE', 'POSTAL_CODE'
]
addr_existing_cols = [c for c in addr_cols_needed if c in addr.columns]
addr_view = addr[addr_existing_cols].copy()

# Prepare a joined view by BUILDING_NUMBER (common key present in both)
if 'BUILDING_NUMBER' in fac_candidates.columns and 'BUILDING_NUMBER' in addr_view.columns:
    # Prioritize primary or E911 addresses if available
    addr_view['_is_e911'] = addr_view['IS_E911_ADDRESS'].astype(str).str.upper().eq('Y') if 'IS_E911_ADDRESS' in addr_view.columns else False
    if 'ADDRESS_PURPOSE' in addr_view.columns:
        addr_view['_is_primary_purpose'] = addr_view['ADDRESS_PURPOSE'].astype(str).str.contains('PRIMARY|MAILING|STREET', case=False, na=False)
    else:
        addr_view['_is_primary_purpose'] = False

    # Rank addresses per building
    addr_view['_rank'] = (
        addr_view['_is_e911'].astype(int) * 2 +
        addr_view['_is_primary_purpose'].astype(int)
    )
    # Keep best address per building number
    addr_best = (
        addr_view.sort_values(['BUILDING_NUMBER', '_rank'], ascending=[True, False])
        .drop_duplicates(subset=['BUILDING_NUMBER'], keep='first')
        .drop(columns=['_is_e911', '_is_primary_purpose', '_rank'])
    )

    merged = fac_candidates.merge(addr_best, on='BUILDING_NUMBER', how='left', suffixes=('', '_ADDR'))
else:
    merged = fac_candidates.copy()

# Construct street address string
def _clean_part(x):
    x = '' if pd.isna(x) else str(x).strip()
    return x

def build_street_line(row):
    parts = []
    snum = _clean_part(row.get('STREET_NUMBER', ''))
    snum_sfx = _clean_part(row.get('STREET_NUMBER_SUFFIX', ''))
    pre = _clean_part(row.get('PRE_DIRECTIONAL', ''))
    name = _clean_part(row.get('STREET_NAME', ''))
    sfx = _clean_part(row.get('STREET_SUFFIX', ''))
    post = _clean_part(row.get('POST_DIRECTIONAL', ''))
    # Street number and suffix
    if snum:
        parts.append(snum)
    if snum_sfx:
        if parts:
            parts[-1] = (parts[-1] + snum_sfx).strip()
        else:
            parts.append(snum_sfx)
    if pre:
        parts.append(pre)
    if name:
        parts.append(name)
    if sfx:
        parts.append(sfx)
    if post:
        parts.append(post)
    street = " ".join([p for p in parts if p])
    city = _clean_part(row.get('CITY', ''))
    state = _clean_part(row.get('STATE', ''))
    postal = _clean_part(row.get('POSTAL_CODE', ''))
    locality = ", ".join([seg for seg in [city, state] if seg])
    if postal:
        if locality:
            locality = f"{locality} {postal}"
        else:
            locality = postal
    if street and locality:
        return f"{street}, {locality}"
    elif street:
        return street
    else:
        return locality if locality else ''

merged['STREET_ADDRESS'] = merged.apply(build_street_line, axis=1)

# Select and rename required columns
select_cols_map = {
    'BUILDING_NUMBER': 'BUILDING_NUMBER',
    'BUILDING_NAME_LONG': 'BUILDING_NAME_LONG',
    'STREET_ADDRESS': 'STREET_ADDRESS',
    'BUILDING_TYPE': 'BUILDING_TYPE',
    'OCCUPANCY_DATE': 'OCCUPANCY_DATE',
    'OWNERSHIP_TYPE': 'OWNERSHIP_TYPE',
    'SITE': 'SITE'
}
existing_select = {k: v for k, v in select_cols_map.items() if k in merged.columns}
detail = merged[list(existing_select.keys())].rename(columns=existing_select).copy()

# Create summary rows (owned, leased, all) filtered to non-subdivisions
def summarize(df):
    own_series = df['OWNERSHIP_TYPE'].astype(str).str.upper()
    owned_mask = own_series.str.contains('OWN', na=False)
    leased_mask = own_series.str.contains('LEASE', na=False)
    owned_ct = int(owned_mask.sum())
    leased_ct = int(leased_mask.sum())
    all_ct = int(len(df))
    summ = pd.DataFrame(
        [
            {'BUILDING_NUMBER': None, 'BUILDING_NAME_LONG': f'{owned_ct} Buildings', 'STREET_ADDRESS': None,
             'BUILDING_TYPE': None, 'OCCUPANCY_DATE': None, 'OWNERSHIP_TYPE': None, 'SITE': None},
            {'BUILDING_NUMBER': None, 'BUILDING_NAME_LONG': f'{leased_ct} Buildings', 'STREET_ADDRESS': None,
             'BUILDING_TYPE': None, 'OCCUPANCY_DATE': None, 'OWNERSHIP_TYPE': None, 'SITE': None},
            {'BUILDING_NUMBER': None, 'BUILDING_NAME_LONG': f'{all_ct} Buildings', 'STREET_ADDRESS': None,
             'BUILDING_TYPE': None, 'OCCUPANCY_DATE': None, 'OWNERSHIP_TYPE': None, 'SITE': None},
        ]
    )
    return summ

summary_rows = summarize(detail)

final_df = pd.concat([detail, summary_rows], ignore_index=True)

# Package final result
result = {
    'buildings_with_address_and_summary': final_df
}