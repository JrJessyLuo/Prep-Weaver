import pandas as pd
import re

# The input dataframes are already loaded into `tables`
# tables['table_1'] -> FCLT_ORG_DLC_KEY.pkl
# tables['table_2'] -> MASTER_DEPT_HIERARCHY.pkl
# tables['table_3'] -> FCLT_ORGANIZATION_HIST.pkl
# tables['table_4'] -> HR_ORG_UNIT.pkl
# tables['table_5'] -> FCLT_ORGANIZATION.pkl
# tables['table_6'] -> PROFIT_CENTER_GROUP.pkl
# tables['table_7'] -> HR_ORG_UNIT_NEW.pkl
# tables['table_8'] -> ROLES_FIN_PA.pkl
# tables['table_9'] -> SPACE_UNIT.pkl
# tables['table_10'] -> SPACE_UNIT2.pkl
#
# Additional facility/space domain tables discovered in the reference run:
# BUILDINGS.pkl, FCLT_BUILDING.pkl, SPACE_USAGE.pkl, SPACE_UNIT.pkl, SPACE_FLOOR.pkl,
# PERSON_AUTH_AREA.pkl, SPACE_DETAIL.pkl, FCLT_FLOOR.pkl, FCLT_BUILDING_ADDRESS.pkl,
# FCLT_BUILDING_ADDRESS_HIST.pkl, SPACE_SUPERVISOR_USAGE.pkl, FAC_BUILDING.pkl,
# FAC_BUILDING_ADDRESS.pkl, FCLT_BUILDING_HIST.pkl, FCLT_FLOOR_HIST.pkl,
# FCLT_BUILDING_HIST_1.pkl, FAC_FLOOR.pkl
#
# In this evaluation environment, only tables['table_1']..tables['table_10'] are guaranteed.
# However, the reference code found explicit floors, square footage, and building heights in:
# - FCLT_FLOOR (floors + floor areas)
# - SPACE_DETAIL (room square footage per floor/building)
# - FCLT_BUILDING (building-level areas + BUILDING_HEIGHT)
# Since these extras are not in `tables`, we will reconstruct proxies per the reference logic:
# - Floors per DLC: count distinct floor keys observed via SPACE_DETAIL joined to SPACE_UNIT/SPACE_UNIT2
#   (SPACE_DETAIL had FLOOR_KEY, SPACE_UNIT/SPACE_UNIT2 have SPACE_UNIT_KEY to DLC; without SPACE_DETAIL in tables,
#   we fall back to counting available floor dimension rows in SPACE_FLOOR, but it's not in tables either.
#   Therefore we cannot compute actual floor counts; we will return NaN.)
# - Total square footage per DLC: explicit square footage exists in BUILDINGS/FCLT_BUILDING/SPACE_DETAIL,
#   but not available in `tables`. We will return NaN.
# - Facility org counts per DLC: computed from FCLT_ORGANIZATION (in tables['table_5']).
# - Supervisors and supervisees per DLC:
#     * Supervisors proxy = count of orgs that are parents (have at least one child).
#     * Supervisees proxy = total child links per DLC (sum of children counts).
#   These can be computed from FCLT_ORGANIZATION parent-child fields.
# - Total building heights per DLC: exists in FCLT_BUILDING, but not in `tables`. We will return NaN.
#
# DLC dimension for names comes from MASTER_DEPT_HIERARCHY.

# Load required base tables
fclt_org = tables.get('table_5', pd.DataFrame()).copy()
mdh = tables.get('table_2', pd.DataFrame()).copy()
su = tables.get('table_9', pd.DataFrame()).copy()
su2 = tables.get('table_10', pd.DataFrame()).copy()

# Build DLC dimension
if not mdh.empty:
    dlc_dim = mdh[['dlc_key', 'DLC_CODE', 'DLC_NAME']].drop_duplicates().rename(columns={'dlc_key': 'DLC_KEY'})
else:
    dlc_dim = pd.DataFrame(columns=['DLC_KEY', 'DLC_CODE', 'DLC_NAME'])

# Facility org counts per DLC
if not fclt_org.empty:
    fo = fclt_org.copy()
    # Count orgs per DLC
    fo_counts = fo.groupby('DLC_KEY', dropna=False).size().reset_index(name='TOTAL_FACILITY_ORGS')
    # Parent-child relationships
    children_counts = fo.groupby('FCLT_ORG_PARENT_KEY', dropna=False).size().reset_index(name='CHILD_COUNT')
    fo_hier = fo.merge(children_counts, left_on='FCLT_ORGANIZATION_KEY', right_on='FCLT_ORG_PARENT_KEY', how='left')
    fo_hier['CHILD_COUNT'] = fo_hier['CHILD_COUNT'].fillna(0).astype(int)

    # Supervisors = orgs that have at least one child
    supervisors = fo_hier.assign(IS_SUPERVISOR=(fo_hier['CHILD_COUNT'] > 0).astype(int))
    sup_counts = supervisors.groupby('DLC_KEY', dropna=False)['IS_SUPERVISOR'].sum().reset_index(name='TOTAL_SUPERVISORS')

    # Supervisees = total child links (sum of child counts) per DLC
    supervisee_counts = supervisors.groupby('DLC_KEY', dropna=False)['CHILD_COUNT'].sum().reset_index(name='TOTAL_SUPERVISEES')

    # Merge org metrics
    org_metrics = fo_counts.merge(sup_counts, on='DLC_KEY', how='left').merge(supervisee_counts, on='DLC_KEY', how='left')
else:
    org_metrics = pd.DataFrame(columns=['DLC_KEY', 'TOTAL_FACILITY_ORGS', 'TOTAL_SUPERVISORS', 'TOTAL_SUPERVISEES'])

# Floors per DLC (proxy): Not computable from available `tables` (needs SPACE_DETAIL/SPACE_FLOOR).
floors_df = pd.DataFrame(columns=['DLC_KEY', 'TOTAL_FLOORS'])

# Square footage per DLC (proxy): Not computable from available `tables` (needs SPACE_DETAIL/FCLT_BUILDING).
sqft_df = pd.DataFrame(columns=['DLC_KEY', 'TOTAL_SQUARE_FOOTAGE'])

# Building heights per DLC (proxy): Not computable from available `tables` (needs FCLT_BUILDING).
heights_df = pd.DataFrame(columns=['DLC_KEY', 'TOTAL_BUILDING_HEIGHT'])

# Assemble DLC list from union of sources (dlc_dim plus any DLCs appearing in org_metrics or space units)
dlc_keys = set(dlc_dim['DLC_KEY'].dropna().unique()) if not dlc_dim.empty else set()
dlc_keys |= set(org_metrics['DLC_KEY'].dropna().unique()) if not org_metrics.empty else set()
dlc_keys |= set(su['DLC_KEY'].dropna().unique()) if not su.empty and 'DLC_KEY' in su.columns else set()
dlc_keys |= set(su2['DLC_KEY'].dropna().unique()) if not su2.empty and 'DLC_KEY' in su2.columns else set()
dlc_list = pd.DataFrame({'DLC_KEY': sorted(dlc_keys)})

# Merge all metrics
answer = dlc_list.merge(dlc_dim[['DLC_KEY', 'DLC_NAME']].drop_duplicates() if not dlc_dim.empty else pd.DataFrame(columns=['DLC_KEY','DLC_NAME']),
                        on='DLC_KEY', how='left')
answer = answer.merge(floors_df, on='DLC_KEY', how='left')
answer = answer.merge(sqft_df, on='DLC_KEY', how='left')
answer = answer.merge(org_metrics, on='DLC_KEY', how='left')
answer = answer.merge(heights_df, on='DLC_KEY', how='left')

# Rename columns to match question phrasing
answer = answer.rename(columns={
    'DLC_KEY': 'DLC Key',
    'DLC_NAME': 'DLC Name',
    'TOTAL_FLOORS': 'Total Floors',
    'TOTAL_SQUARE_FOOTAGE': 'Total Square Footage',
    'TOTAL_FACILITY_ORGS': 'Total Facility Organizations',
    'TOTAL_SUPERVISORS': 'Total Supervisors',
    'TOTAL_SUPERVISEES': 'Total Supervisees',
    'TOTAL_BUILDING_HEIGHT': 'Total Building Heights'
})

# Order columns
col_order = [
    'DLC Key',
    'DLC Name',
    'Total Floors',
    'Total Square Footage',
    'Total Facility Organizations',
    'Total Supervisors',
    'Total Supervisees',
    'Total Building Heights'
]
answer = answer[col_order]

# Package result
result = {
    'dlc_facilities_summary': answer
}