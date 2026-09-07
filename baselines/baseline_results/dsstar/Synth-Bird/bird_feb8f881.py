import pandas as pd
import re
import ast
import json

# Input tables are already loaded in `tables`
cards = tables["table_1"].copy()
kv = tables["table_2"].copy()

# Normalize id types for a safe join (string forms)
cards["_id_str"] = cards["id"].astype(str)
kv["_id_str"] = kv["id"].astype(str)

# Find the banned row(s) in kv (type looks like legality/banlist; value indicates banned)
type_series = kv["type"].astype(str)
value_series = kv["value"].astype(str)

type_keywords = r"(legal|legality|format|ban|banned|restricted|restriction)"
type_mask = type_series.str.contains(type_keywords, case=False, na=False)
banned_mask = value_series.str.contains(r"\bbanned\b", case=False, na=False)

banned_rows = kv.loc[type_mask & banned_mask, ["_id_str", "type", "value"]].copy()

def _parse_id_list_from_text(text: str):
    """
    Attempt to parse a list of ids embedded in a string, supporting:
      - Python-literal lists: "['1','2']" or "[1,2]"
      - JSON lists: ["1","2"]
      - Any bracketed list-like substring inside larger text.
      - Fallback: extract all integer tokens.
    Returns list of integer ids.
    """
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return []

    s = str(text).strip()

    # Try to isolate a bracketed list substring if present
    m = re.search(r"\[[\s\S]*\]", s)
    candidates = [s]
    if m:
        candidates.insert(0, m.group(0))

    # Try JSON / Python literal parsing first
    for cand in candidates:
        cand_stripped = cand.strip()
        obj = json.loads(cand_stripped)
        if isinstance(obj, list):
            out = []
            for x in obj:
                if x is None:
                    continue
                if isinstance(x, (int, float)) and not pd.isna(x):
                    out.append(int(x))
                else:
                    sx = str(x).strip()
                    if re.fullmatch(r"-?\d+", sx):
                        out.append(int(sx))
            if out:
                return out

    for cand in candidates:
        cand_stripped = cand.strip()
        obj = ast.literal_eval(cand_stripped)
        if isinstance(obj, list):
            out = []
            for x in obj:
                if x is None:
                    continue
                if isinstance(x, (int, float)) and not pd.isna(x):
                    out.append(int(x))
                else:
                    sx = str(x).strip()
                    if re.fullmatch(r"-?\d+", sx):
                        out.append(int(sx))
            if out:
                return out

    # Fallback: extract integers from the text
    nums = re.findall(r"-?\d+", s)
    return [int(n) for n in nums] if nums else []

# Aggregate ids from all banned_rows (in case there are multiple)
parsed_ids = []
for _, r in banned_rows.iterrows():
    parsed_ids.extend(_parse_id_list_from_text(r.get("_id_str", "")))
    parsed_ids.extend(_parse_id_list_from_text(r.get("value", "")))

parsed_ids_unique = sorted(set([i for i in parsed_ids if i is not None]))

parsed_ids_ser = pd.Series(parsed_ids_unique, dtype="int64") if parsed_ids_unique else pd.Series([], dtype="int64")
banned_cards_by_id = cards[cards["id"].isin(parsed_ids_ser)].copy()

white_banned_count = int(banned_cards_by_id.loc[banned_cards_by_id["borderColor"] == "white"].shape[0])

answer_df = pd.DataFrame({"white_bordered_banned_cards": [white_banned_count]})
result = {"answer": answer_df}