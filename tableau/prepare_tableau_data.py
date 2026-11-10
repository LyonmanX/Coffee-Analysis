"""Build Tableau-ready CSVs from coffee_ratings.csv.

Applies the same cleaning as Coffee_Analysis.ipynb (clean()) so the dashboard numbers
match the notebook. Uses only the standard library, so it runs without pandas.

Run from the repo root:  python tableau/prepare_tableau_data.py
Outputs (in tableau/):
  coffee_reviews_tableau.csv   one row per review, cleaned, with helper fields
  coffee_sensory_long.csv      one row per review x sensory attribute (for top-10% comparison)
"""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

SENSORY = ["aroma", "flavor", "aftertaste", "acidity", "body", "balance",
           "uniformity", "clean_cup", "sweetness", "cupper_points"]
LABELS = {"clean_cup": "Clean cup", "cupper_points": "Cupper points (overall)"}

# Names Tableau's built-in map recognises
MAP_NAMES = {
    "Tanzania, United Republic Of": "Tanzania",
    "United States (Hawaii)": "United States",
    "United States (Puerto Rico)": "Puerto Rico",
    "Cote d?Ivoire": "Côte d'Ivoire",
}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def quantile(values, q):
    """Linear interpolation, same as pandas' default."""
    s = sorted(values)
    pos = (len(s) - 1) * q
    lo, frac = int(pos), pos - int(pos)
    return s[lo] if frac == 0 else s[lo] + (s[lo + 1] - s[lo]) * frac


def alt_band(m):
    if m is None:
        return "Unknown"
    if m <= 1000:
        return "<1000 m"
    if m <= 1300:
        return "1000–1299 m"
    if m <= 1600:
        return "1300–1599 m"
    return "≥1600 m"


def missing(v):
    return v is None or v.strip() in ("", "NA")


with open(ROOT / "coffee_ratings.csv", encoding="utf-8", newline="") as f:
    raw = list(csv.DictReader(f))

# 1. Remove the review scored 0 (data-entry error)
rows = [r for r in raw if (num(r["total_cup_points"]) or 0) > 0]

# 2. Group countries / varieties with fewer than 20 reviews into "Other" (as in the notebook)
def grouper(col):
    counts = Counter(r[col] for r in rows if not missing(r[col]))
    keep = {k for k, n in counts.items() if n >= 20}
    return lambda v: "Unknown" if missing(v) else (v if v in keep else "Other")

group_country, group_variety = grouper("country_of_origin"), grouper("variety")

cutoff = quantile([num(r["total_cup_points"]) for r in rows], 0.90)

reviews, long_rows = [], []
for i, r in enumerate(rows, start=1):
    total = num(r["total_cup_points"])
    alt = num(r["altitude_mean_meters"])
    alt = alt if alt is not None and 100 <= alt <= 3000 else None   # typos like 190,164 m -> missing
    moisture = num(r["moisture"])
    moisture = None if moisture == 0 else moisture                   # 0% is impossible
    year = re.search(r"(\d{4})\s*$", r["grading_date"] or "")
    country_raw = None if missing(r["country_of_origin"]) else r["country_of_origin"]
    top10 = total >= cutoff

    rec = {
        "review_id": i,
        "total_cup_points": total,
        "top_10_pct": "Top 10%" if top10 else "Other 90%",
        "species": r["species"],
        "country": country_raw or "Unknown",
        "country_map": MAP_NAMES.get(country_raw, country_raw) if country_raw else "",
        "country_group": group_country(r["country_of_origin"]).replace(
            "Tanzania, United Republic Of", "Tanzania"),
        "region": "" if missing(r["region"]) else r["region"],
        "variety_group": group_variety(r["variety"]),
        "processing": "Unknown" if missing(r["processing_method"]) else r["processing_method"],
        "color": "Unknown" if missing(r["color"]) else r["color"],
        "altitude_m": "" if alt is None else round(alt, 1),
        "altitude_band": alt_band(alt),
        "grading_year": year.group(1) if year else "",
        "moisture": "" if moisture is None else moisture,
        "category_one_defects": num(r["category_one_defects"]),
        "category_two_defects": num(r["category_two_defects"]),
        "quakers": "" if num(r["quakers"]) is None else num(r["quakers"]),
    }
    for s in SENSORY:
        rec[s] = num(r[s])
        long_rows.append({
            "review_id": i,
            "attribute": LABELS.get(s, s.replace("_", " ").capitalize()),
            "score": num(r[s]),
            "top_10_pct": rec["top_10_pct"],
            "country_group": rec["country_group"],
        })
    reviews.append(rec)

for name, data in (("coffee_reviews_tableau.csv", reviews), ("coffee_sensory_long.csv", long_rows)):
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)

print(f"Reviews: {len(reviews):,} (removed {len(raw) - len(rows)})  |  top-10% cutoff: {cutoff:.2f}")
print(f"Top 10%: {sum(r['top_10_pct'] == 'Top 10%' for r in reviews)} reviews")
print(f"Wrote {OUT / 'coffee_reviews_tableau.csv'} and {OUT / 'coffee_sensory_long.csv'} ({len(long_rows):,} rows)")
