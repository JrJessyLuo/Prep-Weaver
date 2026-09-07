import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['artist', 'availability', 'borderColor', 'cardKingdomFoilId', 'cardKingdomId', 'colorIdentity', 'colorIndicator', 'colors', 'convertedManaCost', 'duelDeck', 'edhrecRank', 'faceConvertedManaCost', 'flavorName', 'flavorText', 'frameEffects', 'frameVersion', 'hand', 'hasAlternativeDeckLimit', 'hasContentWarning', 'hasFoil', 'hasNonFoil', 'isAlternative', 'isFullArt', 'isOnlineOnly', 'isOversized', 'isPromo', 'isReprint', 'isReserved', 'isStarter', 'isStorySpotlight', 'isTextless', 'isTimeshifted', 'keywords', 'layout', 'leadershipSkills', 'life', 'loyalty', 'manaCost', 'mcmId', 'mcmMetaId', 'mtgArenaId', 'mtgjsonV4Id', 'mtgoFoilId', 'mtgoId', 'multiverseId', 'number', 'originalReleaseDate', 'originalText', 'originalType', 'otherFaceIds', 'power', 'printings', 'promoTypes', 'purchaseUrls', 'scryfallId', 'scryfallIllustrationId', 'scryfallOracleId', 'setCode', 'side', 'subtypes', 'supertypes', 'tcgplayerProductId', 'text', 'toughness', 'type', 'types', 'variations', 'watermark'])
    # DropColumn
    table_1 = table_1.drop(columns=['artist', 'availability', 'borderColor', 'cardKingdomFoilId', 'cardKingdomId', 'colorIdentity', 'colorIndicator', 'colors', 'convertedManaCost', 'duelDeck', 'edhrecRank', 'faceConvertedManaCost', 'flavorName', 'flavorText', 'frameEffects', 'frameVersion', 'hand', 'hasAlternativeDeckLimit', 'hasContentWarning', 'hasFoil', 'hasNonFoil', 'isAlternative', 'isFullArt', 'isOnlineOnly', 'isOversized', 'isPromo', 'isReprint', 'isReserved', 'isStarter', 'isStorySpotlight', 'isTextless', 'isTimeshifted', 'keywords', 'layout', 'leadershipSkills', 'life', 'loyalty', 'manaCost', 'mcmId', 'mcmMetaId', 'mtgArenaId', 'mtgjsonV4Id', 'mtgoFoilId', 'mtgoId', 'multiverseId', 'number', 'originalReleaseDate', 'originalText', 'originalType', 'otherFaceIds', 'power', 'printings', 'promoTypes', 'purchaseUrls', 'scryfallId', 'scryfallIllustrationId', 'scryfallOracleId', 'setCode', 'side', 'subtypes', 'supertypes', 'tcgplayerProductId', 'text', 'toughness', 'type', 'types', 'variations', 'watermark'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_cards", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # synthesize printable name from available fields
    #     def pick_name(row):
    #         for col in ["name", "asciiName", "faceName"]:
    #             v = row.get(col, None)
    #             if pd.notna(v) and str(v).strip().lower() != "nan" and str(v).strip() != "":
    #                 return str(v)
    #         return None
    # 
    #     df["name"] = df.apply(pick_name, axis=1)
    # 
    #     # split UUID into 5 parts (standard UUID has 5 hyphen-separated groups)
    #     def split_uuid(u):
    #         if pd.isna(u) or str(u).strip().lower() == "nan" or str(u).strip() == "":
    #             return [None, None, None, None, None]
    #         parts = str(u).split("-")
    #         # pad/truncate defensively
    #         parts = (parts + [None]*5)[:5]
    #         return parts
    # 
    #     uuid_parts = df["uuid"].apply(split_uuid)
    #     df["uuid_part1"] = uuid_parts.str[0]
    #     df["uuid_part2"] = uuid_parts.str[1]
    #     df["uuid_part3"] = uuid_parts.str[2]
    #     df["uuid_part4"] = uuid_parts.str[3]
    #     df["uuid_part5"] = uuid_parts.str[4]
    # 
    #     # final column set
    #     out = df[["id", "name", "rarity", "uuid_part1", "uuid_part2", "uuid_part3", "uuid_part4", "uuid_part5"]].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # synthesize printable name from available fields
        def pick_name(row):
            for col in ["name", "asciiName", "faceName"]:
                v = row.get(col, None)
                if pd.notna(v) and str(v).strip().lower() != "nan" and str(v).strip() != "":
                    return str(v)
            return None

        df["name"] = df.apply(pick_name, axis=1)

        # split UUID into 5 parts (standard UUID has 5 hyphen-separated groups)
        def split_uuid(u):
            if pd.isna(u) or str(u).strip().lower() == "nan" or str(u).strip() == "":
                return [None, None, None, None, None]
            parts = str(u).split("-")
            # pad/truncate defensively
            parts = (parts + [None]*5)[:5]
            return parts

        uuid_parts = df["uuid"].apply(split_uuid)
        df["uuid_part1"] = uuid_parts.str[0]
        df["uuid_part2"] = uuid_parts.str[1]
        df["uuid_part3"] = uuid_parts.str[2]
        df["uuid_part4"] = uuid_parts.str[3]
        df["uuid_part5"] = uuid_parts.str[4]

        # final column set
        out = df[["id", "name", "rarity", "uuid_part1", "uuid_part2", "uuid_part3", "uuid_part4", "uuid_part5"]].copy()
        return out
    prepared_cards = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['prepared_cards'])
    # Terminate
    result = {'prepared_cards': prepared_cards}
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
    # SelectCol(table_name="table_1", columns=['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5', 'date', 'text'])
    # SelectCol
    _cols = [c for c in ['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5', 'date', 'text'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5', 'date', 'text'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5', 'date', 'text'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5', 'date', 'text'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5', 'date', 'text'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_rulings = prepared_table_2

# Join cards to rulings using composite uuid parts
cards_rulings = prepared_cards.merge(
    prepared_rulings,
    how='inner',
    on=['uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5']
)

# Filter to uncommon rarity
uncommons = cards_rulings[cards_rulings['rarity'].str.lower() == 'uncommon']

# For each card, find the earliest ruling date
uncommons['date'] = pd.to_datetime(uncommons['date'], errors='coerce')
earliest = (
    uncommons.sort_values('date')
             .groupby(['uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5','name','rarity'], as_index=False)
             .agg(first_ruling_date=('date','first'))
)

# Sort by earliest ruling date ascending and pick first 3
result = earliest.sort_values('first_ruling_date', ascending=True).head(3)[['name']]

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
