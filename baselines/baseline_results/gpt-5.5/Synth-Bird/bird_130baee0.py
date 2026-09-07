import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

players = tables["table_1"].copy()
matches = tables["table_2"].copy()

players["birthday"] = pd.to_datetime(players["birthday"], errors="coerce")
matches["date"] = pd.to_datetime(matches["date"], errors="coerce")

players_birth = players[["player_api_id", "birthday"]].dropna().drop_duplicates("player_api_id")

def _parse_goal_xml(goal_xml):
    if pd.isna(goal_xml) or not isinstance(goal_xml, str) or goal_xml.strip() == "":
        return []
    try:
        root = ET.fromstring(goal_xml)
    except Exception:
        return []
    out = []
    for v in root.findall("value"):
        team = v.findtext("team")
        scorer = v.findtext("player1")
        if team is None or scorer is None:
            continue
        out.append({"team_id": team, "player_api_id": scorer})
    return out

goal_events = matches[["date", "htid", "goal"]].copy()
goal_events["events"] = goal_events["goal"].apply(_parse_goal_xml)
goal_events = goal_events.drop(columns=["goal"]).explode("events", ignore_index=True)
goal_events = goal_events.dropna(subset=["events"])

goal_events = pd.concat(
    [goal_events.drop(columns=["events"]), goal_events["events"].apply(pd.Series)],
    axis=1
)

goal_events["team_id"] = pd.to_numeric(goal_events["team_id"], errors="coerce")
goal_events["player_api_id"] = pd.to_numeric(goal_events["player_api_id"], errors="coerce")
goal_events = goal_events.dropna(subset=["date", "htid", "team_id", "player_api_id"])

# Home team goals only (goals where scoring team == home team id)
home_goals = goal_events[goal_events["team_id"].astype(int) == goal_events["htid"].astype(int)].copy()

home_goals = home_goals.merge(players_birth, on="player_api_id", how="inner")
home_goals["age_years"] = (home_goals["date"] - home_goals["birthday"]).dt.days / 365.25

total_home_goals_age_le_30 = int((home_goals["age_years"] <= 30).sum())

result = {
    "total_home_team_goals_by_players_age_le_30": pd.DataFrame(
        {"total_home_team_goals": [total_home_goals_age_le_30]}
    )
}
