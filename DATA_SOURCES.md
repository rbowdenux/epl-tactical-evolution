# Data Sources & Methodology
## The Shape of the Game — EPL Tactical Evolution 2009–2025

This document covers every data source, collection method, derivation formula, and known limitation for each dataset used in this project. It is intended to make the research fully reproducible and transparent.

---

## Data files in this repo

```
data/
├── verified/
│   ├── golden_boot_all_seasons.csv       — fully sourced from official records
│   └── league_metrics_by_season.csv      — goals per game + points thresholds, official sources
└── estimated/
    ├── tactical_estimates.csv            — formation share, PPDA proxy, possession aggregates
    └── possession_vs_ppda_snapshots.csv  — club-era snapshots for scatter chart
```

The distinction between `verified/` and `estimated/` is about **method**, not reliability. Verified data is taken directly from official records with no transformation. Estimated data is derived from real scraped match data using proxy formulas, or cross-referenced from published analyses where the scraping window did not cover that period.

---

## 1. Verified data

### 1a. Golden Boot — all seasons 2008-09 to 2024-25
**File:** `data/verified/golden_boot_all_seasons.csv`

**Source:** Premier League official records
**URL:** https://www.premierleague.com/stats/awards

All goal tallies, winner names, and shared boot instances are taken directly from the Premier League's official awards records and cross-referenced with Wikipedia's list of top Premier League goalscorers by season.

No transformation applied — these are the published final figures.

---

### 1b. League metrics by season
**File:** `data/verified/league_metrics_by_season.csv`

**Goals per game / total goals**
- **Source:** Premier League official statistics
- **URL:** https://www.premierleague.com/stats
- Season totals taken from end-of-season statistical summaries. 2023-24 figure (1,246 goals / 3.28 per game) cross-referenced with Opta published data.

**Survival points (17th place)**
- **Source:** Premier League historical league tables
- The points total for the 17th-placed team at end of season — the highest-placed relegated team's threshold.
- Cross-referenced with: https://www.premierleague.com/tables (archived seasons)
- Additional validation: Opta Analyst, OLBG, and GiveMeSport published analyses of relegation points history.

**UCL qualification points (4th / 5th place)**
- **Source:** Premier League historical league tables
- The points total for the 4th-placed team (Champions League qualifier) in each season.
- From 2024-25 onward, a 5th automatic UCL place became available via UEFA's European Performance Spot (EPS) mechanism.

---

## 2. Estimated / derived data

### 2a. Tactical estimates — formation share, PPDA proxy, possession
**File:** `data/estimated/tactical_estimates.csv`

#### Formation share percentages (2009-10 to 2022-23)
**Method:** Aggregated from WhoScored match-level scrape
**Scope:** Top 6 EPL clubs (Arsenal, Chelsea, Liverpool, Man City, Man Utd, Tottenham)
**What was scraped:** Primary declared formation per team per match, as published on WhoScored match centre pages
**Aggregation:** Count of each formation across all matches for top 6 clubs in a season, expressed as a percentage share

**Note on 2023-24 and 2024-25:** These seasons fall outside the scraping window (scraper covers 2009-10 to 2020-21). Formation percentages for these seasons are drawn from the Premier League's own tactical analysis publications and Total Football Analysis seasonal data reports. The 4-2-3-1 dominance figure for 2024-25 (51.6% of sides using it as primary shape) is sourced from official Premier League tactical analysis published at the start of the 2024-25 season.

---

#### PPDA proxy
**What is PPDA?** Passes Per Defensive Action — a pressing intensity metric. Lower = more aggressive pressing.

True PPDA = opponent passes in their own half ÷ defensive actions (tackles + interceptions) in that half.

**Why a proxy?** True PPDA from tracking data is not publicly available at match level from free sources. The formula below uses available scraped fields to approximate it.

**Proxy formula used:**
```
ppda_proxy = (possession_pct × 5) / (tackles_final_third + interceptions)
```

- `possession_pct × 5` is a rough scalar estimating pass volume from possession share
- `tackles_final_third + interceptions` is the available defensive action count from scraped data
- The result is median-aggregated across all top 6 matches per season

**Validation:** For seasons where official PPDA has been published (e.g. Liverpool 2024-25: 9.89 per Premier League Stats Centre), the proxy values are in the same range and directional order, confirming the formula is a reasonable approximation.

**Known limitations:**
- The possession scalar (×5) is a fixed estimate, not a calibrated coefficient
- Interception counts from WhoScored may include defensive third interceptions, not just opposition-half actions
- Should be treated as a directional trend indicator, not a precise PPDA figure

---

#### Possession percentages (top 6 average)
**Method:** Season-level mean of home + away possession% for top 6 clubs, aggregated from match-level scrape
**For 2023-24 and 2024-25:** Cross-referenced with published Opta / Total Football Analysis seasonal possession reports

---

### 2b. Possession vs PPDA scatter snapshots
**File:** `data/estimated/possession_vs_ppda_snapshots.csv`

These are club-era snapshots used for the scatter/bubble chart. Each point represents one club in one season range. Values are taken from the `tactical_estimates.csv` aggregates above, filtered to representative seasons that illustrate the era clearly.

**Bubble size (weight column)** is a relative indicator of that club's finishing position / points that season, used purely for visual scale in the chart. It is not a precise metric.

---

## 3. Data not in this repo

The following data was used in the piece but is drawn from published sources that are cited inline. It is not reproduced here.

| Data point | Source |
|------------|--------|
| Liverpool PPDA 9.89 (2024-25) | Premier League Stats Centre |
| 4-2-3-1 usage 51.6% (2024-25) | Premier League tactical analysis |
| Passing sequence length 9.6s (2025-26) | Premier League / Opta Analyst |
| Set-piece goal share 25% (2025-26) | Premier League official stats |
| Long throw xG 0.09/game (2025-26) | Premier League official stats |
| Progressive pass distance — Liverpool 93,682m | Total Football Analysis |

---

## 4. Scraping methodology

See `scraper/scraper.py` for the full documented structure of the data collection pipeline.

**Key points:**
- Python + Selenium, throttled with randomised delays (2.5–5s between requests)
- Only publicly visible statistics collected — no authentication required
- Data used solely for non-commercial research and portfolio purposes
- Site-specific parsing logic omitted from public repo — field schema documented in `data/raw/sample_matches.csv`

---

## 5. Known limitations summary

| Dataset | Limitation |
|---------|------------|
| Formation share | Reflects primary declared shape only — in-game shifts not captured |
| PPDA proxy | Approximation formula, not official tracking data |
| Possession scatter | Club-era snapshots, not continuous season data |
| 2023-25 formation data | Drawn from published analyses, not from this scraper |
| Cross-era comparisons | League rules, officiating, and team quality changed significantly over 16 seasons |

---

*Last updated: March 2026*
*Contact: [your email or GitHub profile]*
