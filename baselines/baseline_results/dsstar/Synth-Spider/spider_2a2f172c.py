import pandas as pd

# The input tables are provided in a dict named `tables`
# Mapping:
# tables['table_1'] -> spider_2a2f172c_input_0.pkl (authors)
# tables['table_2'] -> spider_2a2f172c_input_1.pkl (paper_author)
# tables['table_3'] -> spider_2a2f172c_input_2.pkl (papers)

# Load DataFrames from provided tables dict
authors_df = tables['table_1'].copy()
pa_df = tables['table_2'].copy()
papers_df = tables['table_3'].copy()

# 1) Get 2009 paper_ids (note the year values have quotes in this dataset)
paper_ids_2009 = set(papers_df.loc[papers_df['year'] == '"2009"', 'paper_id'])

# 2) Split paper_author_combined into paper_id and author_id, then keep only 2009 papers
split_df = pa_df['paper_author_combined'].str.split('|', n=1, expand=True)
split_df.columns = ['paper_id', 'author_id']
split_2009 = split_df[split_df['paper_id'].isin(paper_ids_2009)].copy()

# 3) Group by author_id and count papers
author_paper_counts_2009 = (
    split_2009.groupby('author_id', as_index=False)
    .size()
    .rename(columns={'size': 'paper_count_2009'})
    .sort_values('paper_count_2009', ascending=False)
)

# 4) Map the top author_id to the authors DataFrame to retrieve the corresponding author name
author_paper_counts_2009['author_id_str'] = author_paper_counts_2009['author_id'].astype(str)
authors_df_clean = authors_df.copy()
authors_df_clean['author_id_str'] = authors_df_clean['author_id'].astype(str)

merged_top = author_paper_counts_2009.merge(
    authors_df_clean[['author_id_str', 'name']],
    on='author_id_str',
    how='left'
)

# Keep only the top row (most papers in 2009)
top_row_df = merged_top.head(1)[['author_id', 'name', 'paper_count_2009']]

# Prepare final result as required: dict[str, pandas.DataFrame]
result = {
    "top_author_2009": top_row_df.reset_index(drop=True)
}