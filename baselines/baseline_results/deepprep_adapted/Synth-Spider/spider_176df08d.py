import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Title_Part1", mode="mode")
    # MissingValueImputation
    table_1["Title_Part1"] = table_1["Title_Part1"].fillna(table_1["Title_Part1"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['Title_Part1', 'Title_Part2'], target_column="Title", func="""
    # import pandas as pd
    # def concat(row: pd.Series) -> str:
    #     p1 = "" if pd.isna(row["Title_Part1"]) else str(row["Title_Part1"]).strip()
    #     p2 = "" if pd.isna(row["Title_Part2"]) else str(row["Title_Part2"]).strip()
    #     return (p1 + " " + p2).strip()
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        p1 = "" if pd.isna(row["Title_Part1"]) else str(row["Title_Part1"]).strip()
        p2 = "" if pd.isna(row["Title_Part2"]) else str(row["Title_Part2"]).strip()
        return (p1 + " " + p2).strip()
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["Title"] = table_1[['Title_Part1', 'Title_Part2']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['Title_Part1', 'Title_Part2'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Code', 'Title'])
    # SelectCol
    _cols = [c for c in ['Code', 'Title'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
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
    # CodeGeneration(table_names=['table_1'], target_table="prepared_table", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    #     id_col = df.columns[0]
    #     value_cols = [c for c in df.columns if c != id_col]
    # 
    #     # Make Code values the index so we can select Name/Movie rows easily
    #     df2 = df.set_index(id_col)
    #     # Ensure both rows exist
    #     names = df2.loc["Name", value_cols]
    #     movies = df2.loc["Movie", value_cols]
    # 
    #     out = pd.DataFrame({
    #         "TheaterName": names.values,
    #         "MovieCode": pd.to_numeric(movies.values, errors="coerce")
    #     })
    #     out = out.dropna(subset=["MovieCode"])
    #     out["MovieCode"] = out["MovieCode"].astype(int)
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()
        id_col = df.columns[0]
        value_cols = [c for c in df.columns if c != id_col]

        # Make Code values the index so we can select Name/Movie rows easily
        df2 = df.set_index(id_col)
        # Ensure both rows exist
        names = df2.loc["Name", value_cols]
        movies = df2.loc["Movie", value_cols]

        out = pd.DataFrame({
            "TheaterName": names.values,
            "MovieCode": pd.to_numeric(movies.values, errors="coerce")
        })
        out = out.dropna(subset=["MovieCode"])
        out["MovieCode"] = out["MovieCode"].astype(int)
        return out
    prepared_table = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Terminate(result=['prepared_table'])
    # Terminate
    result = {'prepared_table': prepared_table}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
movies = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
theater_movie_map = prepared_table_2

# movies: from table_1
# - keep Code
# - Title = Title_Part1 + ' ' + Title_Part2 (handle missing parts gracefully)
movies = table_1.copy()
movies['Title_Part1'] = movies['Title_Part1'].fillna('')
movies['Title_Part2'] = movies['Title_Part2'].fillna('')
movies['Title'] = (movies['Title_Part1'] + ' ' + movies['Title_Part2']).str.strip()
movies = movies[['Code', 'Title']]

# theater_movie_map: from table_2
# Unpivot columns 1..n into rows using the 'Name' and 'Movie' entries
wide = table_2.copy()
# Identify theater columns (exclude the first 'Code' column)
theater_cols = [c for c in wide.columns if c != 'Code']
# Create mapping from column -> (theater name, movie code)
name_row = wide[wide['Code'] == 'Name'][theater_cols].iloc[0]
movie_row = wide[wide['Code'] == 'Movie'][theater_cols].iloc[0]
long_df = pd.DataFrame({
    'TheaterName': name_row.values,
    'MovieCode_raw': movie_row.values
})
# Clean and cast movie codes, drop NaNs
long_df['MovieCode'] = pd.to_numeric(long_df['MovieCode_raw'], errors='coerce').dropna().astype(int)
# Align TheaterName with non-null MovieCode
theater_movie_map = long_df.loc[long_df['MovieCode_raw'].notna(), ['TheaterName', 'MovieCode']].copy()

# Integrate: join on MovieCode (theater_movie_map) == Code (movies)
merged = theater_movie_map.merge(movies, left_on='MovieCode', right_on='Code', how='inner')

# Question-specific filtering: theaters named 'Odeon'
result = merged[merged['TheaterName'].str.strip().str.casefold() == 'odeon']

# Final answer: movie titles for ones that are played in the Odeon theater
answer = result['Title'].dropna().drop_duplicates().tolist()

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
