import json
from time import sleep
from loguru import logger
import pandas as pd
import requests

POSITIONS = ["QB", "RB", "WR", "TE", "FLX", "K", "DST"]
CONSENSUS_RANKINGS_URL = (
    "https://api.fantasypros.com/v2/json/nfl/2024/consensus-rankings"
)


def get_ranking_data(
    position: str, week: int, url: str = CONSENSUS_RANKINGS_URL
) -> requests.Response:
    logger.debug(f"Fetching ranking data for position {position} for week {week}")
    params = {
        "type": "weekly",
        "scoring": "PPR",
        "position": position,
        "week": week,
        "experts": "available",
        "sport": "NFL",
    }

    headers = {
        "X-Api-Key": "zjxN52G3lP4fORpHRftGI2mTU8cTwxVNvkjByM3j",
    }

    return requests.get(url, params=params, headers=headers)


def fetch_all_rankings(week: int, positions: list[str] = POSITIONS) -> pd.DataFrame:
    all_data = []

    for position in positions:
        response = get_ranking_data(position, week)
        response.raise_for_status()

        data = response.json()

        for player in data["players"]:
            player_record = {
                "player_id": player["player_id"],
                "position": position,
                "name": player["player_name"],
                "last_updated": data["last_updated"],
                "team": player["player_team_id"],
                "rank_ecr": player["rank_ecr"],
                "rank_min": player["rank_min"],
                "rank_max": player["rank_max"],
                "rank_ave": player["rank_ave"],
                "rank_std": player["rank_std"],
                "opponent": player["player_opponent_id"],
            }
            all_data.append(player_record)

        sleep(0.2)

    df = pd.DataFrame(all_data)

    assert not df.empty, "df.empty is True"
    return df
