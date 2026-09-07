import pandas as pd
import numpy as np
import re
import xml.etree.ElementTree as ET

# Targets
targets = ["Daan Smith", "Filipe Ferreira"]

# -----------------------------
# XML parsing for goal events (same logic as reference)
# -----------------------------
def _safe_int(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "" or x.lower() in {"none", "nan"}:
        return None
    return int(float(x))

def parse_goal_xml(goal_xml: str):
    if goal_xml is None:
        return []
    s = str(goal_xml).strip()
    if s == "" or s.lower() == "nan":
        return []
    if "<" not in s or ">" not in s:
        return []

    xml_str = s

    root = ET.fromstring(xml_str) if xml_str.lstrip().startswith("<") else ET.fromstring(f"<root>{xml_str}</root>")

    events = []
    value_nodes = list(root.findall(".//value"))
    if not value_nodes and str(root.tag).lower() == "value":
        value_nodes = [root]

    for v in value_nodes:
        team = v.findtext("team") or v.get("team")
        p1 = v.findtext("player1") or v.get("player1")
        elapsed = v.findtext("elapsed") or v.get("elapsed")

        events.append(
            {
                "team_api_id": _safe_int(team),
                "player_api_id": _safe_int(p1),
                "elapsed": _safe_int(elapsed),
                "raw": ET.tostring(v, encoding="unicode", method="xml") if v is not None else None,
            }
        )
    return events

# -----------------------------
# Helpers for column detection (as in reference)
# -----------------------------
def extract_team_goals_cols(df: pd.DataFrame):
    away_col = None
    home_col = None
    for c in df.columns:
        lc = str(c).lower()
        if lc == "away_team_goal":
            away_col = c
        if lc == "home_team_goal":
            home_col = c

    if away_col is None or home_col is None:
        num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        candidates = []
        for c in num_cols:
            s = df[c].dropna()
            if len(s) == 0:
                continue
            mx = s.max()
            mn = s.min()
            uniq = s.nunique(dropna=True)
            if mn >= 0 and mx <= 15 and uniq <= 16 and np.all(np.isclose(s, np.round(s))):
                candidates.append(c)

        def score(col):
            lc = str(col).lower()
            sc = 0
            if "goal" in lc:
                sc += 3
            if "team" in lc:
                sc += 1
            if "away" in lc:
                sc += 2
            if "home" in lc:
                sc += 2
            return sc

        sorted_cols = sorted(candidates, key=lambda x: score(x), reverse=True)
        if away_col is None:
            for c in sorted_cols:
                if "away" in str(c).lower() and "goal" in str(c).lower():
                    away_col = c
                    break
        if home_col is None:
            for c in sorted_cols:
                if "home" in str(c).lower() and "goal" in str(c).lower():
                    home_col = c
                    break
        if away_col is None and sorted_cols:
            away_col = sorted_cols[0]
        if home_col is None and len(sorted_cols) > 1:
            home_col = sorted_cols[1]

    return home_col, away_col

def detect_goal_xml_column(df: pd.DataFrame):
    for c in df.columns:
        if str(c).lower() == "goal":
            return c
    obj_cols = [c for c in df.columns if df[c].dtype == "object"]
    best = None
    best_score = -1
    for c in obj_cols:
        s = df[c].dropna().astype(str)
        if len(s) == 0:
            continue
        sample = s.head(200)
        score = int(sample.str.contains(r"<\s*goal[\s>]", case=False, regex=True).sum())
        if score > best_score:
            best_score = score
            best = c
    return best if best_score > 0 else None

# -----------------------------
# Load required tables from `tables` (NO disk I/O)
# -----------------------------
player_df = tables["table_2"]  # european_football_2_Player
match_df = tables["table_1"]   # european_football_2_Match

# Determine player id + name columns
lower_cols = {str(c).lower(): c for c in player_df.columns}
player_id_col = lower_cols["player_api_id"]
name_col = None
for cand in ["player_name", "xm", "name"]:
    if cand in lower_cols:
        name_col = lower_cols[cand]
        break

# Resolve target IDs (exact match preferred; fallback case-insensitive contains)
name_series = player_df[name_col].astype(str)

exact_ids = {}
for t in targets:
    m = name_series == t
    ids = player_df.loc[m, player_id_col].dropna().astype(int).unique().tolist()
    if ids:
        exact_ids[t] = ids

ci_ids = {}
for t in targets:
    m = name_series.str.contains(re.escape(t), case=False, na=False)
    ids = player_df.loc[m, player_id_col].dropna().astype(int).unique().tolist()
    if ids:
        ci_ids[t] = ids

target_ids = sorted(set(sum(exact_ids.values(), []) + sum(ci_ids.values(), [])))

# -----------------------------
# Reproduce the reference logic on the in-memory match table
# -----------------------------
home_goal_col, away_goal_col = extract_team_goals_cols(match_df)
goal_xml_col = detect_goal_xml_column(match_df)

# Team id columns
home_team_col = None
away_team_col = None
for c in match_df.columns:
    lc = str(c).lower()
    if lc == "home_team_api_id":
        home_team_col = c
    elif lc == "away_team_api_id":
        away_team_col = c

if away_team_col is None:
    for c in match_df.columns:
        lc = str(c).lower()
        if "away" in lc and "team" in lc and "api" in lc and "id" in lc:
            away_team_col = c
            break
if home_team_col is None:
    for c in match_df.columns:
        lc = str(c).lower()
        if "home" in lc and "team" in lc and "api" in lc and "id" in lc:
            home_team_col = c
            break

match_id_col = "match_api_id" if "match_api_id" in match_df.columns else ("id" if "id" in match_df.columns else None)

# If goal XML doesn't exist, then no parsable away-team target scorer matches
if goal_xml_col is None or match_id_col is None or away_team_col is None:
    away_goals_sum = 0.0
else:
    cols_needed = [
        c
        for c in [match_id_col, "date", away_team_col, home_team_col, away_goal_col, home_goal_col, goal_xml_col]
        if c in match_df.columns
    ]
    tmp = match_df[cols_needed].copy()
    tmp["_goal_events"] = tmp[goal_xml_col].apply(parse_goal_xml)
    exploded = tmp.explode("_goal_events", ignore_index=True)
    exploded = exploded[exploded["_goal_events"].notna()].copy()

    if exploded.empty:
        away_goals_sum = 0.0
    else:
        exploded["event_team_api_id"] = exploded["_goal_events"].apply(lambda d: d.get("team_api_id") if isinstance(d, dict) else None)
        exploded["event_player_api_id"] = exploded["_goal_events"].apply(lambda d: d.get("player_api_id") if isinstance(d, dict) else None)

        exploded["event_team_api_id"] = pd.to_numeric(exploded["event_team_api_id"], errors="coerce")
        exploded["event_player_api_id"] = pd.to_numeric(exploded["event_player_api_id"], errors="coerce")
        exploded[away_team_col] = pd.to_numeric(exploded[away_team_col], errors="coerce")

        away_team_mask = exploded["event_team_api_id"].notna() & (exploded["event_team_api_id"] == exploded[away_team_col])
        if target_ids:
            target_mask = exploded["event_player_api_id"].isin(target_ids)
        else:
            # If no IDs resolved, fall back to name match (rare)
            player_map = (
                player_df[[player_id_col, name_col]]
                .dropna(subset=[player_id_col, name_col])
                .drop_duplicates(subset=[player_id_col])
                .set_index(player_id_col)[name_col]
                .astype(str)
                .to_dict()
            )
            exploded["event_player_name"] = exploded["event_player_api_id"].map(player_map)
            pattern = "|".join(re.escape(t) for t in targets)
            target_mask = exploded["event_player_name"].fillna("").astype(str).str.contains(pattern, case=False, regex=True)

        away_target_events = exploded.loc[away_team_mask & target_mask].copy()
        matched_match_ids = away_target_events[match_id_col].dropna().unique().tolist()
        matched_matches = match_df[match_df[match_id_col].isin(matched_match_ids)].copy()

        if away_goal_col is not None and away_goal_col in matched_matches.columns:
            away_goals_sum = float(pd.to_numeric(matched_matches[away_goal_col], errors="coerce").fillna(0).sum())
        else:
            away_goals_sum = 0.0

# -----------------------------
# Final answer table
# -----------------------------
answer_df = pd.DataFrame({"sum_away_team_goal": [away_goals_sum]})
result = {"answer": answer_df}