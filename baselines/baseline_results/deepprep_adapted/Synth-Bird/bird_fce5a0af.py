import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'id', 'new_name': 'id'}, {'old_name': 'name', 'new_name': 'name'}])
    # Rename
    table_1 = table_1.rename(columns={'id': 'id', 'name': 'name'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'name'])
    # SelectCol
    _cols = [c for c in ['id', 'name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'name'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="table_1_prepared", func="""
    # import pandas as pd
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    #     key = df['id'].astype(str).str.strip().str.lower()
    #     df = df[key.isin(['season'])].reset_index(drop=True)
    #     return df
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()
        key = df['id'].astype(str).str.strip().str.lower()
        df = df[key.isin(['season'])].reset_index(drop=True)
        return df
    table_1_prepared = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1_prepared'], target_table="league_season_map", func="""
    # import pandas as pd
    # def process_tables(table_1_prepared: pd.DataFrame):
    #     df = table_1_prepared.copy()
    # 
    #     # Ensure we only use the 'season' row (should already be true from history)
    #     df['id'] = df['id'].astype(str).str.strip().str.lower()
    #     season_df = df[df['id'] == 'season']
    #     if season_df.empty:
    #         # Return empty with correct schema if not found
    #         return pd.DataFrame(columns=['id', 'season'])
    # 
    #     # Convert wide league_id columns into long mapping rows
    #     season_series = season_df.drop(columns=['id']).iloc[0]
    #     out = season_series.reset_index()
    #     out.columns = ['id', 'season']  # id is league_id (was column header)
    # 
    #     # Normalize id as string (safe for later joins/integration)
    #     out['id'] = out['id'].astype(str).str.strip()
    # 
    #     return out
    # """)
    # CodeGeneration
    def process_tables(table_1_prepared: pd.DataFrame):
        df = table_1_prepared.copy()

        # Ensure we only use the 'season' row (should already be true from history)
        df['id'] = df['id'].astype(str).str.strip().str.lower()
        season_df = df[df['id'] == 'season']
        if season_df.empty:
            # Return empty with correct schema if not found
            return pd.DataFrame(columns=['id', 'season'])

        # Convert wide league_id columns into long mapping rows
        season_series = season_df.drop(columns=['id']).iloc[0]
        out = season_series.reset_index()
        out.columns = ['id', 'season']  # id is league_id (was column header)

        # Normalize id as string (safe for later joins/integration)
        out['id'] = out['id'].astype(str).str.strip()

        return out
    league_season_map = process_tables(table_1_prepared)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="league_season_map", columns=['id', 'season'])
    # SelectCol
    _cols = [c for c in ['id', 'season'] if c in league_season_map.columns]
    league_season_map = league_season_map[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['league_season_map'])
    # Terminate
    result = {'league_season_map': league_season_map}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
countries = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
league_season_matrix = prepared_table_2

# Inputs: prepared tables
countries = countries  # columns: ['id','name']
lsm = league_season_matrix  # two-row frame with index ['id','season'] and columns as league_ids

# We need to count matches held in Scotland Premier League in 2015/2016.
# However, from the selected tables we only have: (a) country id-name mapping, and (b) a season string per league_id (column labels), without league names or match counts.
# There is no table providing league names (e.g., 'Scotland Premier League') nor match counts per league/season.
# Thus, the required integration and counting cannot be completed with the selected tables alone.

# Placeholder to illustrate how it would work if a leagues table and a matches fact existed:
# leagues: columns ['league_id','league_name','country_id']
# matches: columns ['league_id','season','match_id']
# target = (matches[matches['season']=='2015/2016']
#           .merge(leagues[leagues['league_name']=='Scotland Premier League'], on='league_id')
#          )
# answer = len(target)

answer = None  # Insufficient data to compute

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
