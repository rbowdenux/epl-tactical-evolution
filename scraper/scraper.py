"""
EPL Tactical Data Scraper
=========================
Collects match-level statistics from publicly available football data sources
for Premier League seasons 2009-10 to 2020-21.

Approach
--------
Uses Selenium to navigate season and match pages, extracting:
  - Team formations (primary declared shape)
  - Possession percentage (home / away)
  - Pass completion percentage (home / away)
  - Shots on target (home / away)
  - Pressing proxy: tackles + interceptions in the final third
  - Match outcome and scoreline

Output
------
One row per team per match. Raw output written to data/raw/.
See data/raw/sample_matches.csv for representative field structure.

Usage
-----
    python scraper.py --season 2019-20 --output ../data/raw/

Dependencies
------------
    pip install selenium pandas tqdm
    ChromeDriver >= 114 (must match installed Chrome version)

Notes
-----
- Scraping is throttled with randomised delays to avoid server load.
- Only publicly visible statistics are collected (no login required).
- Data is used solely for non-commercial research and portfolio purposes.
- Users should review the terms of service of any data source before scraping.
"""

import time
import random
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# ── CONFIGURATION ─────────────────────────────────────────────────────────────

SEASONS = [
    "2009-10", "2010-11", "2011-12", "2012-13", "2013-14",
    "2014-15", "2015-16", "2016-17", "2017-18", "2018-19",
    "2019-20", "2020-21"
]

OUTPUT_FIELDS = [
    "season",
    "match_id",
    "match_date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "home_formation",
    "away_formation",
    "home_possession",
    "away_possession",
    "home_pass_completion",
    "away_pass_completion",
    "home_shots_on_target",
    "away_shots_on_target",
    "home_tackles_final_third",   # pressing proxy
    "away_tackles_final_third",
    "home_interceptions",
    "away_interceptions",
]

DELAY_MIN = 2.5   # seconds between requests
DELAY_MAX = 5.0


# ── BROWSER SETUP ─────────────────────────────────────────────────────────────

def init_driver(headless: bool = True) -> webdriver.Chrome:
    """Initialise a headless Chrome WebDriver instance."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


# ── SCRAPING LOGIC (STRUCTURE ONLY) ───────────────────────────────────────────

def get_season_match_urls(driver, season: str) -> list[str]:
    """
    Navigate to the season index page and collect URLs for all 380 matches.

    Parameters
    ----------
    driver  : Selenium WebDriver
    season  : str, e.g. "2019-20"

    Returns
    -------
    List of match page URLs for the given season.
    """
    # Navigation and URL collection logic intentionally omitted.
    # Structure: paginate through season fixture list, extract match hrefs.
    raise NotImplementedError


def parse_match_page(driver, url: str, season: str) -> dict:
    """
    Extract statistical fields from a single match page.

    Parameters
    ----------
    driver  : Selenium WebDriver
    url     : str, full match page URL
    season  : str

    Returns
    -------
    Dict with keys matching OUTPUT_FIELDS.
    """
    # Parsing logic intentionally omitted.
    # Structure: locate stat containers by CSS selector, extract text, cast types.
    raise NotImplementedError


def scrape_season(driver, season: str, output_dir: str) -> None:
    """
    Scrape all matches for a given season and write raw CSV to output_dir.

    Parameters
    ----------
    driver     : Selenium WebDriver
    season     : str
    output_dir : str, path to write output file
    """
    urls = get_season_match_urls(driver, season)
    records = []

    for url in tqdm(urls, desc=f"Scraping {season}"):
        try:
            record = parse_match_page(driver, url, season)
            records.append(record)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"  Skipped {url}: {e}")

        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    df = pd.DataFrame(records, columns=OUTPUT_FIELDS)
    outpath = f"{output_dir}/raw_{season.replace('-', '_')}.csv"
    df.to_csv(outpath, index=False)
    print(f"  Saved {len(df)} records → {outpath}")


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="EPL match data scraper")
    parser.add_argument("--season", type=str, default="all",
                        help="Season to scrape, e.g. '2019-20', or 'all'")
    parser.add_argument("--output", type=str, default="../data/raw/",
                        help="Output directory for raw CSV files")
    args = parser.parse_args()

    driver = init_driver(headless=True)

    try:
        seasons = SEASONS if args.season == "all" else [args.season]
        for season in seasons:
            print(f"\nStarting season: {season}")
            scrape_season(driver, season, args.output)
    finally:
        driver.quit()
        print("\nDone.")
