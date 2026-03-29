# The Shape of the Game
## EPL Tactical Evolution 2009–2025

A data-driven, narrative-led research piece tracing sixteen seasons of Premier League tactical change — from the possession era through the pressing revolution to the direct counter-revolution underway today.

**Live site:** `https://rbowdenux.github.io/epl-tactical-evolution`

---

## Repo structure

```
epl-tactical-evolution/
│
├── index.html                                   # The full interactive piece (self-contained)
│
├── scraper/
│   └── scraper.py                               # Selenium scraping pipeline (structure
│                                                # documented; parsing logic omitted — see
│                                                # DATA_SOURCES.md)
│
├── data/
│   ├── verified/
│   │   ├── golden_boot_all_seasons.csv          # All 17 seasons, official PL records
│   │   └── league_metrics_by_season.csv         # Goals per game + points thresholds
│   ├── estimated/
│   │   ├── tactical_estimates.csv               # Formation share, PPDA proxy, possession
│   │   └── possession_vs_ppda_snapshots.csv     # Club-era snapshots for scatter chart
│   └── raw/
│       └── sample_matches.csv                   # Representative raw scraper output shape
│
├── analysis/
│   └── process_data.py                          # Cleaning & aggregation (raw → processed)
│
├── DATA_SOURCES.md                              # Full source, method & limitation notes
└── README.md
```

> **On data transparency:** All data files are split into `verified/` (taken directly from official records, no transformation) and `estimated/` (derived from scraped data using proxy formulas, or cross-referenced from published analyses). See [DATA_SOURCES.md](DATA_SOURCES.md) for the full methodology, every formula used, and known limitations.

## Overview

This project frames Premier League tactical history across three distinct eras:

| Era | Period | Defining idea |
|-----|--------|---------------|
| I — The Possession Age | 2009–2015 | Ball retention as control; the influence of Guardiola's Barcelona |
| II — The Pressing Revolution | 2015–2021 | Gegenpressing; winning the ball as the attack |
| III — The Counter-Revolution | 2021–present | Directness, set pieces, and long balls as a rational response to ubiquitous pressing |

The piece combines historical data from a custom-built scraping pipeline with current official Premier League statistics, told through editorial narrative and interactive data visualisations.

---

## Research & Data Sources

### Historical dataset (2009–2021)
- **Source:** [WhoScored.com](https://www.whoscored.com)
- **Method:** Custom Python + Selenium scraping pipeline built to collect match-level statistics across full Premier League seasons
- **Coverage:** ~4,500 matches across 12 seasons
- **Fields captured:** Formation, possession %, pass completion %, pressing event proxies, match outcomes, team-level aggregates

### Current season data (2021–2026)
- **Source:** Official [Premier League Stats Centre](https://www.premierleague.com/stats) and Opta-derived analytics published in Premier League tactical analyses
- **Fields used:** PPDA (passes per defensive action), progressive pass distance, passing sequence length and duration, goalkeeper distribution splits, set-piece goal ratios, long throw xG, formation usage share, Golden Boot records

### Points threshold data
- **Sources:** Premier League historical tables, cross-referenced with published analyses from Opta Analyst, OLBG, and GiveMeSport
- **Coverage:** Relegation points (17th place) and Champions League qualification points (4th/5th place), 2009–10 to 2024–25

### Golden Boot data
- **Source:** Premier League official records, Wikipedia season pages
- **Coverage:** All seasons 2008–09 to 2024–25 — winner(s), goals scored, contextual notes

---

## Skills & Tools

### Data collection
- **Python** — scraping pipeline, data cleaning and aggregation
- **Selenium** — browser automation for dynamic page scraping from WhoScored
- **Pandas** — data wrangling and season-level aggregation

### Visualisation & front-end
- **Chart.js 4.4** — interactive charts (line, bar, stacked bar, bubble/scatter)
  - Custom plugin written for inline player name labels on the Golden Boot chart
  - Custom era-band background plugin for trend charts
- **Vanilla HTML / CSS / JavaScript** — fully self-contained single-file output, no build step required
- **Google Fonts** — Playfair Display (display/headings), DM Mono (data/labels), DM Sans (body)
- **Intersection Observer API** — scroll-triggered animations for timeline items and bar charts

### Research & analysis
- **Tactical frameworks:** Era periodisation informed by published analyses from Total Football Analysis, Breaking the Lines, and official Premier League tactical breakdowns
- **Metrics used:**
  - PPDA (passes per defensive action) — primary pressing intensity metric
  - Progressive pass distance — directness and verticality measure
  - xG from set pieces and long throws — current-era directness indicator
  - Passing sequence length (seconds) — tempo and directness proxy
  - Formation share — categorical formation data aggregated by season

---

## Design decisions

- **Three-era colour system:** Gold (`#d4a843`) for the possession age, teal (`#3a8c7e`) for the pressing era, red (`#c8392e`) for the counter-revolution — applied consistently across all charts, timeline items, section labels, and navigation
- **Dark editorial aesthetic:** Designed to feel like a long-read data journalism piece rather than a dashboard
- **Sticky navigation:** Era-anchored with active highlighting on scroll
- **Responsive layout:** Adapts to mobile with single-column chart grid

---

## Limitations & caveats

- WhoScored data reflects publicly visible match statistics — some pressing metrics (e.g. PPDA) are proxied rather than directly observed from tracking data
- Formation data reflects each team's primary declared system and does not capture in-game tactical shifts
- Top-six focus for historical era analysis; whole-league aggregates used for current-era comparisons
- Cross-era comparisons carry inherent noise — the league changed in size, rules, and officiating style across the period
- 2025–26 season data is partial (mid-season at time of writing)

---

## Project context

This piece is part of a research portfolio documenting a transition from UX design into data research and insight roles. It demonstrates:

- End-to-end research process from raw data collection to published output
- Ability to frame quantitative findings within a compelling narrative structure
- Front-end data communication skills (interactive visualisation, editorial design)
- Domain knowledge in football tactics and sports analytics

---

## Author

**Beka**
UX Designer → Research & Insight
[Portfolio](#) · [LinkedIn](#) · [GitHub](#)

---

*Data: WhoScored (2009–2021) · Premier League / Opta (2021–2026) · Premier League official records*
*Built with Chart.js, vanilla HTML/CSS/JS*
