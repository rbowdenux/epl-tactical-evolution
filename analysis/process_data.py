"""
EPL Tactical Data — Processing Pipeline
========================================
Reads raw per-match CSVs produced by scraper.py, aggregates to season level,
and writes the cleaned summary used by the visualisation layer.

Input:  data/raw/raw_YYYY_YY.csv  (one file per season)
Output: data/processed/epl_tactical_summary.csv

Usage
-----
    python process_data.py

    # or for a single season:
    python process_data.py --season 2019-20
"""

import os
import glob
import argparse
import pandas as pd
import numpy as np


# ── CONFIGURATION ─────────────────────────────────────────────────────────────

RAW_DIR       = "../data/raw/"
PROCESSED_DIR = "../data/processed/"
OUTPUT_FILE   = "epl_tactical_summary.csv"

TOP_6 = [
    "Arsenal", "Chelsea", "Liverpool",
    "Man City", "Man Utd", "Tottenham"
]

ERA_MAP = {
    "2009-10": "Possession Age",
    "2010-11": "Possession Age",
    "2011-12": "Possession Age",
    "2012-13": "Possession Age",
    "2013-14": "Possession Age",
    "2014-15": "Transition",
    "2015-16": "Pressing Revolution",
    "2016-17": "Pressing Revolution",
    "2017-18": "Pressing Revolution",
    "2018-19": "Pressing Revolution",
    "2019-20": "Pressing Revolution",
    "2020-21": "Pressing Revolution",
    "2021-22": "Counter-Revolution",
    "2022-23": "Counter-Revolution",
    "2023-24": "Counter-Revolution",
    "2024-25": "Counter-Revolution",
}


# ── HELPERS ───────────────────────────────────────────────────────────────────

def load_raw_season(path: str) -> pd.DataFrame:
    """Load a single raw season CSV and perform basic type coercion."""
    df = pd.read_csv(path)

    numeric_cols = [
        "home_possession", "away_possession",
        "home_pass_completion", "away_pass_completion",
        "home_shots_on_target", "away_shots_on_target",
        "home_tackles_final_third", "away_tackles_final_third",
        "home_interceptions", "away_interceptions",
        "home_score", "away_score",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    return df


def melt_to_team_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reshape from one-row-per-match to one-row-per-team-per-match.
    Makes it easier to filter and aggregate by team.
    """
    home = df.rename(columns={
        "home_team": "team", "away_team": "opponent",
        "home_score": "goals_for", "away_score": "goals_against",
        "home_formation": "formation",
        "home_possession": "possession",
        "home_pass_completion": "pass_completion",
        "home_shots_on_target": "shots_on_target",
        "home_tackles_final_third": "tackles_f3",
        "home_interceptions": "interceptions",
    }).assign(venue="home")

    away = df.rename(columns={
        "away_team": "team", "home_team": "opponent",
        "away_score": "goals_for", "home_score": "goals_against",
        "away_formation": "formation",
        "away_possession": "possession",
        "away_pass_completion": "pass_completion",
        "away_shots_on_target": "shots_on_target",
        "away_tackles_final_third": "tackles_f3",
        "away_interceptions": "interceptions",
    }).assign(venue="away")

    keep = [
        "season", "match_id", "match_date", "team", "opponent", "venue",
        "goals_for", "goals_against", "formation", "possession",
        "pass_completion", "shots_on_target", "tackles_f3", "interceptions"
    ]

    return pd.concat([home[keep], away[keep]], ignore_index=True)


def compute_ppda_proxy(df: pd.DataFrame) -> pd.Series:
    """
    Approximate PPDA (passes per defensive action) from available fields.

    True PPDA = opponent passes in own half / (tackles + interceptions in that half).
    Proxy here uses tackles_f3 + interceptions as the defensive action denominator,
    with possession-derived pass volume as the numerator estimate.

    This is an approximation — treat as directionally correct, not precise.
    """
    defensive_actions = df["tackles_f3"] + df["interceptions"]
    # Avoid division by zero
    defensive_actions = defensive_actions.replace(0, np.nan)
    # Possession as proxy for pass volume (higher possession ≈ more passes to defend against)
    pass_volume_proxy = df["possession"] * 5  # rough scalar
    return (pass_volume_proxy / defensive_actions).round(2)


# ── AGGREGATION ───────────────────────────────────────────────────────────────

def season_summary(df_team: pd.DataFrame, season: str) -> dict:
    """
    Aggregate team-level match data to a single season-level summary row.

    Parameters
    ----------
    df_team : DataFrame in team-per-match format (output of melt_to_team_level)
    season  : str, e.g. "2019-20"

    Returns
    -------
    Dict of aggregated metrics for the season.
    """
    top6 = df_team[df_team["team"].isin(TOP_6)]

    # Formation share across all teams
    form_counts = df_team["formation"].value_counts(normalize=True) * 100

    # Goals per game (league-wide)
    total_goals  = df_team["goals_for"].sum()
    total_matches = len(df_team["match_id"].unique())
    goals_per_game = round(total_goals / total_matches, 2) if total_matches else None

    # PPDA proxy for top 6
    top6 = top6.copy()
    top6["ppda_proxy"] = compute_ppda_proxy(top6)

    return {
        "season":                     season,
        "era":                        ERA_MAP.get(season, "Unknown"),
        "avg_possession_top6":        round(top6["possession"].mean(), 1),
        "avg_pass_completion_top6":   round(top6["pass_completion"].mean(), 1),
        "avg_formation_442_pct":      round(form_counts.get("4-4-2", 0), 1),
        "avg_formation_4231_pct":     round(form_counts.get("4-2-3-1", 0), 1),
        "avg_formation_433_pct":      round(form_counts.get("4-3-3", 0), 1),
        "avg_formation_352_pct":      round(form_counts.get("3-5-2", 0), 1),
        "avg_formation_other_pct":    round(
            100 - sum(form_counts.get(f, 0) for f in ["4-4-2","4-2-3-1","4-3-3","3-5-2"]), 1
        ),
        "approx_ppda_top6":           round(top6["ppda_proxy"].median(), 1),
        "goals_per_game_league":      goals_per_game,
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────

def process_all(season_filter: str = None) -> None:
    """Load all raw season files, aggregate, and write processed summary."""

    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "raw_*.csv")))

    if not raw_files:
        print(f"No raw files found in {RAW_DIR}. Run scraper.py first.")
        return

    summaries = []

    for path in raw_files:
        season_slug = os.path.basename(path).replace("raw_", "").replace(".csv", "")
        season = season_slug.replace("_", "-")  # e.g. "2019_20" → "2019-20"

        if season_filter and season != season_filter:
            continue

        print(f"Processing {season}...")

        raw_df   = load_raw_season(path)
        team_df  = melt_to_team_level(raw_df)
        summary  = season_summary(team_df, season)
        summaries.append(summary)

    if not summaries:
        print("No seasons matched. Check --season argument.")
        return

    out_df = pd.DataFrame(summaries)
    outpath = os.path.join(PROCESSED_DIR, OUTPUT_FILE)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_df.to_csv(outpath, index=False)
    print(f"\nProcessed {len(out_df)} seasons → {outpath}")
    print(out_df[["season", "era", "avg_possession_top6", "approx_ppda_top6", "goals_per_game_league"]].to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate raw EPL match data to season summaries")
    parser.add_argument("--season", type=str, default=None,
                        help="Process a single season only, e.g. '2019-20'")
    args = parser.parse_args()
    process_all(season_filter=args.season)
