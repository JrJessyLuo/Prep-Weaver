import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['author_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['author_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="authors_prepared", func="""
    # import pandas as pd
    # import numpy as np
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # --- author_id (stable key) ---
    #     # Keep as-is, but ensure it exists
    #     if 'author_id' not in df.columns:
    #         raise ValueError("Input table must contain 'author_id'")
    # 
    #     # --- author_name extraction / decoding ---
    #     # 1) Prefer explicit name-like columns if present
    #     name_candidates = [c for c in df.columns if str(c).lower() in ['author_name','name','author','full_name']]
    #     if name_candidates:
    #         author_name = df[name_candidates[0]].astype(str)
    #     else:
    #         # 2) Attempt decode from numerically-named glyph/token columns:
    #         #    concatenate non-null, non-empty string-ish tokens in ascending column order.
    #         numeric_named_cols = []
    #         for c in df.columns:
    #             if c == 'author_id':
    #                 continue
    #             # headers could be int or str digits
    #             if isinstance(c, (int, np.integer)) or (isinstance(c, str) and re.fullmatch(r'\d+', c)):
    #                 numeric_named_cols.append(c)
    # 
    #         # sort numeric columns by integer value
    #         def _col_key(x):
    #             return int(x) if isinstance(x, str) else int(x)
    #         numeric_named_cols = sorted(numeric_named_cols, key=_col_key)
    # 
    #         def decode_row(row: pd.Series) -> str:
    #             parts = []
    #             for c in numeric_named_cols:
    #                 v = row.get(c, None)
    #                 if pd.isna(v):
    #                     continue
    #                 # keep only meaningful tokens (strings or small ints that might represent chars)
    #                 if isinstance(v, str):
    #                     token = v.strip()
    #                     if token:
    #                         parts.append(token)
    #                 else:
    #                     # if it's an int in plausible unicode range, try chr; otherwise ignore for name
    #                     try:
    #                         iv = int(v)
    #                         if 32 <= iv <= 0x10FFFF:
    #                             parts.append(chr(iv))
    #                     except Exception:
    #                         pass
    #             name = ''.join(parts).strip()
    #             return name
    # 
    #         author_name = df.apply(decode_row, axis=1)
    #         # 3) Fallback: use author_id as string if name is empty
    #         author_name = author_name.where(author_name.astype(str).str.len() > 0, df['author_id'].astype(str))
    # 
    #     # --- total_citations ---
    #     # Prefer an explicit citations column if present; else sum numeric values across non-key columns.
    #     citation_candidates = [c for c in df.columns if str(c).lower() in ['total_citations','citations','n_citations','citedby','citation_count']]
    #     if citation_candidates:
    #         total_citations = pd.to_numeric(df[citation_candidates[0]], errors='coerce').fillna(0)
    #     else:
    #         # sum all numeric-convertible columns except author_id and any explicit name column
    #         exclude = set(['author_id']) | set(name_candidates)
    #         cols_to_sum = [c for c in df.columns if c not in exclude]
    #         num_df = df[cols_to_sum].apply(pd.to_numeric, errors='coerce')
    #         total_citations = num_df.sum(axis=1, skipna=True).fillna(0)
    # 
    #     out = pd.DataFrame({
    #         'author_id': df['author_id'],
    #         'author_name': author_name.astype(str),
    #         'total_citations': pd.to_numeric(total_citations, errors='coerce').fillna(0).astype(float)
    #     })
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # --- author_id (stable key) ---
        # Keep as-is, but ensure it exists
        if 'author_id' not in df.columns:
            raise ValueError("Input table must contain 'author_id'")

        # --- author_name extraction / decoding ---
        # 1) Prefer explicit name-like columns if present
        name_candidates = [c for c in df.columns if str(c).lower() in ['author_name','name','author','full_name']]
        if name_candidates:
            author_name = df[name_candidates[0]].astype(str)
        else:
            # 2) Attempt decode from numerically-named glyph/token columns:
            #    concatenate non-null, non-empty string-ish tokens in ascending column order.
            numeric_named_cols = []
            for c in df.columns:
                if c == 'author_id':
                    continue
                # headers could be int or str digits
                if isinstance(c, (int, np.integer)) or (isinstance(c, str) and re.fullmatch(r'\d+', c)):
                    numeric_named_cols.append(c)

            # sort numeric columns by integer value
            def _col_key(x):
                return int(x) if isinstance(x, str) else int(x)
            numeric_named_cols = sorted(numeric_named_cols, key=_col_key)

            def decode_row(row: pd.Series) -> str:
                parts = []
                for c in numeric_named_cols:
                    v = row.get(c, None)
                    if pd.isna(v):
                        continue
                    # keep only meaningful tokens (strings or small ints that might represent chars)
                    if isinstance(v, str):
                        token = v.strip()
                        if token:
                            parts.append(token)
                    else:
                        # if it's an int in plausible unicode range, try chr; otherwise ignore for name
                        try:
                            iv = int(v)
                            if 32 <= iv <= 0x10FFFF:
                                parts.append(chr(iv))
                        except Exception:
                            pass
                name = ''.join(parts).strip()
                return name

            author_name = df.apply(decode_row, axis=1)
            # 3) Fallback: use author_id as string if name is empty
            author_name = author_name.where(author_name.astype(str).str.len() > 0, df['author_id'].astype(str))

        # --- total_citations ---
        # Prefer an explicit citations column if present; else sum numeric values across non-key columns.
        citation_candidates = [c for c in df.columns if str(c).lower() in ['total_citations','citations','n_citations','citedby','citation_count']]
        if citation_candidates:
            total_citations = pd.to_numeric(df[citation_candidates[0]], errors='coerce').fillna(0)
        else:
            # sum all numeric-convertible columns except author_id and any explicit name column
            exclude = set(['author_id']) | set(name_candidates)
            cols_to_sum = [c for c in df.columns if c not in exclude]
            num_df = df[cols_to_sum].apply(pd.to_numeric, errors='coerce')
            total_citations = num_df.sum(axis=1, skipna=True).fillna(0)

        out = pd.DataFrame({
            'author_id': df['author_id'],
            'author_name': author_name.astype(str),
            'total_citations': pd.to_numeric(total_citations, errors='coerce').fillna(0).astype(float)
        })

        return out
    authors_prepared = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="authors_prepared", columns=['author_id', 'author_name', 'total_citations'])
    # SelectCol
    _cols = [c for c in ['author_id', 'author_name', 'total_citations'] if c in authors_prepared.columns]
    authors_prepared = authors_prepared[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['authors_prepared'])
    # Terminate
    result = {'authors_prepared': authors_prepared}
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
    # DropNulls(table_name="table_1", subset=None, how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=None, how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
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

prepared_table_1 = _prep_1(tables['table_1'])
authors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
paper_authors = prepared_table_2

# Join authorship mapping to author info
joined = paper_authors.merge(authors, on='author_id', how='inner')

# If authors.total_citations is already the per-author metric, just pick the max by that field
best = authors.loc[authors['total_citations'].astype('float64').idxmax(), ['author_name', 'total_citations']]
result = pd.DataFrame([{'author_name': best['author_name'], 'total_citations': best['total_citations']}])

target = result

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
