# README.md

## What Brews a Winning Cup?
A data analysis project exploring what makes top‑quality coffee.

### Team Members
Bryan Larison • Gina Fuller • Alexandra Hagen • Garrett Williford

---

## Project Summary
This project analyzes 1,340 professional coffee reviews from the Coffee Quality Institute (CQI). We examine how sensory attributes, processing methods, harvest years, and altitude influence overall coffee quality.

---

## Dataset
Source: CQI reviews compiled by James Ledoux

The dataset contains 43 columns, including:
- Sensory scores (aroma, flavor, acidity, etc.)
- Bean metadata (species, color)
- Farm metadata (country, altitude, region)

---

## Tools Used
- pandas
- numpy
- scipy
- matplotlib
- seaborn

---

## Key Steps

### Data Cleaning
- Converted sensory attributes to numeric
- Dropped missing or irrelevant rows
- Fixed inconsistent harvest years
- Parsed altitude values (meters, feet, ranges)

### Feature Creation
- total_sensory_score
- altitude_m
- alt_band
- grading_year

---

## Main Findings

### Top Sensory Attributes
- Flavor is the strongest predictor of total cup score
- Aroma and acidity follow closely
- Sweetness shows almost no variation

### Flavor Over Time
- Early years show more outliers
- Recent years are more consistent

### Processing Methods (Highest Average Flavor Scores)
1. Semi‑washed / Semi‑pulped
2. Natural / Dry
3. Pulped natural / Honey

### Altitude Effects
- Coffees grown ≥1600 m have the highest flavor scores
- Higher altitude = better flavor consistency

### Country Highlights
- Colombia has the most high‑altitude samples (≈150)

---

## How to Run
1. Install required packages
2. Place `coffee_ratings.csv` in the same folder as the notebook file.
3. Open the notebook
4. Run all cells in order

