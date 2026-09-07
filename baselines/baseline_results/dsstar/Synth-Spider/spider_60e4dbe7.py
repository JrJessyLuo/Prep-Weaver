import pandas as pd

# Tables are provided in a dict named `tables`
df_products = tables['table_1'].copy()
df_orders = tables['table_2'].copy()
df_order_items = tables['table_3'].copy()

# Normalize products if list-like stored in single rows
def normalize_products(df):
    sample = df.iloc[0] if len(df) > 0 else None
    if sample is not None and isinstance(sample['product_id'], (list, tuple)):
        cols = ['product_id', 'parent_product_id', 'product_name', 'product_price', 'product_color', 'product_size', 'product_description']
        lists = {c: sample[c] for c in cols}
        lengths = [len(lists[c]) for c in cols]
        if len(set(lengths)) == 1:
            norm = pd.DataFrame({c: lists[c] for c in cols})
            for c in ['product_id', 'parent_product_id']:
                norm[c] = pd.to_numeric(norm[c], errors='coerce').astype('Int64')
            norm['product_price'] = pd.to_numeric(norm['product_price'], errors='coerce')
            return norm
    return df

df_products_norm = normalize_products(df_products)

# Perform merges mirroring the reference logic
merged_items_products = df_order_items.merge(
    df_products_norm,
    on='product_id',
    how='left',
    suffixes=('', '_prod')
)

merged_full = merged_items_products.merge(
    df_orders,
    on='order_id',
    how='left',
    suffixes=('', '_order')
)

# Aggregate and filter: products listed in less than two distinct orders
agg = (
    merged_full
    .groupby('product_id', as_index=False)
    .agg(
        order_count=('order_id', lambda s: s.dropna().nunique()),
        product_name=('product_name', 'first'),
        product_price=('product_price', 'first'),
        product_color=('product_color', 'first')
    )
)
final_df = agg.loc[agg['order_count'] < 2, ['product_id', 'product_name', 'product_price', 'product_color']]

# Package result as required
result = {
    'products_listed_in_less_than_two_orders': final_df
}