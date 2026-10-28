# What Brews a Winning Cup?
A data analysis of 1,338 professional coffee reviews from the Coffee Quality Institute (CQI): which sensory traits set
the best coffees apart, and how much of a coffee's score can be predicted from where and how it was grown.

**Team:** Bryan Larison • Gina Fuller • Alexandra Hagen • Garrett Williford

| File | What it is |
|---|---|
| `Coffee_Analysis_v2.ipynb` | Full analysis: cleaning, statistical tests, models |
| `Coffee_Analysis_v2.pptx` | 12-slide presentation of the findings (with speaker notes) |
| `figures/` | Every chart from the notebook as PNG |
| `coffee_ratings.csv` | The dataset |
| `Group_9_ClassProject_Final_Edit.ipynb`, `Group 9 Coffee Analysis Presentation.pptx` | Original v1 class submission |

---

## Key findings

| Question | Answer |
|---|---|
| What separates the top 10%? | Flavor, aftertaste and the cupper's overall impression (+0.57 to +0.64 points each). Uniformity, clean cup and sweetness are near 10/10 for almost everyone. |
| More consistent over time? | Yes. Flavor-score spread fell ~25% from 2010–12 to 2015–17 (Levene p < 0.001). |
| Does processing matter? | Significantly, but only slightly: natural/dry beats washed by ~0.09 flavor points; processing explains ~1% of variation. |
| Does altitude matter? | Yes. Spearman ρ = 0.28; coffees at ≥1,600 m average ~1.7 points more than those below 1,000 m. |
| Best origins? | Ethiopia (85.5), Kenya (84.3), Uganda (83.5). Mexico, Honduras and Nicaragua trail (~80.5–81). |
| Can we predict quality? | From farm data alone, a Random Forest explains **~26%** of score variation (cross-validated R²), with an average error of 1.57 points vs. 1.83 for guessing the average. |

**What carries the weight (Random Forest permutation importance):** altitude, country, category 2 bean defects, then
grading year and variety. Linear regression puts numbers on it: **+0.10 points per 100 m of altitude** and
**−0.11 points per category 2 defect**, holding country, processing and species constant.

### Why the model doesn't use sensory scores
`total_cup_points` is the exact sum of the 10 sensory scores, so predicting it from them would give R² ≈ 1.0 and teach
nothing. The model uses only information known *before* tasting: altitude, country, variety, species, processing,
moisture, bean color, defects and grading year.

---

## Method
**Data:** CQI reviews scraped by James Ledoux (2018), via
[TidyTuesday](https://github.com/rfordatascience/tidytuesday/blob/main/data/2020/2020-07-07/readme.md).
1,339 reviews (1,311 arabica, 28 robusta), 43 columns.

**Cleaning** (one function, used everywhere)
- Removed 1 review with a total score of 0
- Set 35 impossible altitudes (outside 100–3,000 m, e.g. 190,164 m) to missing
- Set 264 moisture readings of 0% to missing
- Parsed grading dates properly to get the grading year
- Grouped countries and varieties with fewer than 20 reviews into "Other"

**Statistics:** Kruskal-Wallis (processing, altitude bands, countries), Mann-Whitney, Spearman correlation, Levene test.

**Models:** a baseline that always predicts the average, linear regression, and a Random Forest (500 trees), compared
with 5-fold cross-validation. Permutation importance and partial dependence are measured on a 20% held-out test set.
An OLS regression (statsmodels) gives effect sizes with p-values.

## Limitations
- Coffees are self-submitted to CQI, not a random sample.
- Altitude is self-reported, and 17% of rows are missing it.
- Only 28 robusta samples.
- These are associations, not causes.

## How to run
```bash
pip install -r requirements.txt
jupyter notebook Coffee_Analysis_v2.ipynb
```
Keep `coffee_ratings.csv` in the same folder as the notebook and run all cells. Charts are saved to `figures/`.

## v2 changes
- Added significance tests, linear regression and a Random Forest model
- Fixed data errors (0-point review, altitude typos, zero moisture, grading-date parsing)
- Replaced the within-top-10% correlation (biased by range restriction) with a top-vs-rest comparison
- Replaced high-altitude sample counts with average scores by country
- Rebuilt the presentation around findings instead of code steps
