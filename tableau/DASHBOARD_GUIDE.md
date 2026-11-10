# Tableau Dashboard Guide: "What Brews a Winning Cup?"

A click-by-click guide for building a one-page interactive dashboard of the coffee analysis and publishing it to
Tableau Public. It's written for a Tableau beginner. Each step says where to click and what you should see.

**Time:** about 3–4 hours the first time.

---

## Know the screen first

| Name | Where it is | What it does |
|---|---|---|
| **Tabs** | Very bottom of the window, like Excel tabs | `Data Source`, then one tab per sheet. The small icons to the right of the tabs make a **New Worksheet**, **New Dashboard** or **New Story**. |
| **Data pane** | Far left | Your list of fields, grouped by file. A faint **gray line** inside each file's list separates **Dimensions** (above, blue: categories) from **Measures** (below, green: numbers). |
| **Filters shelf** | Middle-left column, top | Drag a field here to filter the sheet |
| **Marks card** | Middle-left column, under Filters | A dropdown (says **Automatic**) plus the buttons **Color, Size, Label, Detail, Tooltip** |
| **Columns / Rows** | Two strips across the top of the canvas | Fields placed here make the chart's axes |
| **Canvas** | The big middle area | Where the chart draws |
| **Pill** | Any field you've dropped onto a shelf or button | Click the small arrow on a pill to change how it's calculated (Sum, Average, Count…) |

**Two rules that prevent most problems:**
1. **Number formats:** set them in the **Data pane** → right-click the field → **Default Properties → Number Format**.
   That applies everywhere: tooltips, labels and KPI tiles.
2. **Linked files:** the two files are linked on `review_id`. If you change `review_id`'s type in one file
   (number ↔ text), change it in the other file too, or you'll get *"cannot compare 'text' and 'bigint'"*.

---

## The data

Run `python tableau/prepare_tableau_data.py` from the repo root (already done; rerun only if the CSV changes).
It applies the notebook's cleaning steps, so the dashboard matches the analysis.

| File | Rows | Use it for |
|---|---|---|
| `coffee_reviews_tableau.csv` | 1,338 (one per coffee) | KPI tiles, map, altitude, country ranking |
| `coffee_sensory_long.csv` | 13,380 (10 tasting scores per coffee) | Top 10% vs. other 90% chart |

## Colors

| Name | Hex | Use |
|---|---|---|
| Espresso | `#3B2418` | Main bars, "Top 10%", "Biggest gaps", big numbers |
| Caramel | `#C8873A` | Dots, reference lines, highlights |
| Crema | `#E9D3B4` | "Other 90%", light bars. Always add a **gray border** so it shows on white. |

The palette is colorblind-friendly because the colors differ in lightness. Don't add a green (red-green color blindness
makes orange and green look alike).

**How to type an exact color:** Marks card → **Color → Edit Colors…** → double-click an item on the left → in the
color picker, type the hex code (without #) in the **Hex** box → OK.

---

## Step 1: Connect the data

1. Open Tableau → on the start page under **Connect → To a File**, click **Text file** → choose
   `coffee_reviews_tableau.csv`.
2. In the left panel under **Files**, drag `coffee_sensory_long.csv` onto the canvas next to the first file.
   A line appears between them. This is a **relationship**.
3. Click the line. In the box that opens, make sure it says `review_id` = `review_id`.
4. **Set field types** (in the data grid at the bottom of the Data Source tab, each column has a small icon above its name):
   - Click the reviews file box → click the **#** above `review_id` → **String**. Do the same for `grading_year`.
   - Click the long file box → click the **#** above `review_id` → **String**. (**Both files must match.**)
   - Click the reviews file box → click the **Abc** above `country_map` → **Geographic Role → Country/Region**.
     A globe icon appears.
5. Set the number format once: go to any sheet → Data pane → right-click `total_cup_points` →
   **Default Properties → Number Format… → Number (Custom)** → 1 decimal → OK.

---

## Step 2: KPI tiles (4 small sheets)

Four big numbers across the top of the dashboard: **1,338 · 82.2 · 84.67 · 36**.

### Tile 1: Coffees reviewed
1. Rename **Sheet 1**: double-click its tab → type `KPI Reviews`.
2. Drag `review_id` (reviews file) onto **Text** on the Marks card. A long list of IDs appears.
3. Click the arrow on the `review_id` pill → **Measure → Count (Distinct)**. ✅ Shows **1,338**.
4. Marks dropdown (**Automatic**) → **Text**.
5. Click **Text** → **…** button → in the editor:
   - Select the field line → size **28**, **bold**, color **3B2418**.
   - Press Enter → type `Coffees reviewed` → size **11**, gray → **OK**.
6. Right-click the sheet title at the top → **Hide Title**.

### Tile 2: Average score
1. Right-click the `KPI Reviews` tab → **Duplicate** → rename the copy `KPI Average`.
2. Drag the `CNTD(review_id)` pill off the Marks card into empty space.
3. Drag `total_cup_points` onto **Text** → pill arrow → **Measure → Average**.
4. **Text → …** → delete everything → **Insert → AVG(total_cup_points)** → format as in Tile 1 →
   second line `Average score` → OK. ✅ Shows **82.2** (82.15 rounded).

### Tile 3: Top 10% cutoff
1. Duplicate → rename `KPI Cutoff`.
2. **Analysis → Create Calculated Field…** → name `Top 10% Cutoff` → formula:
   ```
   {FIXED : PERCENTILE([total_cup_points], 0.90)}
   ```
   → "The calculation is valid" → **OK**. (If it errors, use `84.67` as the whole formula instead.)
3. Remove the old pill → drag `Top 10% Cutoff` onto **Text** (if it looks huge, pill arrow → **Measure → Average**).
4. **Text → …** → Insert the field → format → second line `Top 10% cutoff` → OK.
5. Data pane → right-click `Top 10% Cutoff` → **Default Properties → Number Format → Number (Custom)** → 2 decimals.
   ✅ About **84.67** (84.6 is fine; Tableau rounds percentiles slightly differently from Python).

**Meaning:** any coffee scoring 84.67 or higher is in the top 10% (144 of 1,338).

### Tile 4: Countries
1. Duplicate → rename `KPI Countries`.
2. Remove the old pill → drag `country` onto **Text** → pill arrow → **Measure → Count (Distinct)**. Shows 37.
3. Drag `country` onto the **Filters** shelf → uncheck **Unknown** → OK. ✅ Shows **36**.
4. **Text → …** → Insert the field → format → second line `Countries` → OK.

---

## Step 3: Map ("Where the best coffee grows")

1. **New Worksheet** icon → rename `Map`.
2. **Double-click `country_map`** (globe icon). A world map with dots appears, and Latitude/Longitude fill in by
   themselves. Leave them.
3. Marks dropdown → **Map**. The dots become shaded countries.
4. Drag `total_cup_points` onto **Color** → pill arrow → **Measure → Average**.
   (SUM would make Mexico look best just because it has the most coffees.)
5. **Color → Edit Colors…** → click the **left square** of the color bar → Hex `E9D3B4` → OK →
   click the **right square** → Hex `3B2418` → OK → OK.
6. Bottom-right corner of the map: click **"1 null"** (or "unknown") → **Filter data**.
7. Drag `review_id` onto **Tooltip** → pill arrow → **Measure → Count (Distinct)**.
8. Click **Tooltip** → delete everything → type the following, using **Insert** for each field:
   ```
   <country_map>
   Average score: <AVG(total_cup_points)>
   Coffees reviewed: <CNTD(review_id)>
   ```
   → OK.
9. Double-click the title → `Where the best coffee grows` → Enter → smaller line:
   `Darker = higher average score. Hover for details.` → OK.

✅ **Check:** Ethiopia and Kenya are among the darkest. Mexico is fairly light. Hovering shows name, average and count.

---

## Step 4: Top 10% vs. the rest ("What sets the best apart")

1. **New Worksheet** → rename `Top 10 Gap`.
2. **Analysis → Create Calculated Field…** → name `Gap` → formula:
   ```
   AVG(IF [top_10_pct] = "Top 10%" THEN [score] END)
   - AVG(IF [top_10_pct] = "Other 90%" THEN [score] END)
   ```
   If Tableau suggests `top_10_pct (coffee_sensory_long.csv)`, pick that one. → **OK**.
3. From the **long file** section of the Data pane, drag `attribute` onto **Rows**.
4. Drag `Gap` onto **Columns**. Ten horizontal bars appear.
5. Hover over the Gap axis at the bottom → click the small **sort icon** until the longest bar is on top.
6. **Analysis → Create Calculated Field…** → name `Gap Group` → formula:
   ```
   IF [Gap] >= 0.55 THEN "Biggest gaps" ELSE "Others" END
   ```
   → OK → drag `Gap Group` onto **Color**.
7. **Color → Edit Colors…** → "Biggest gaps" = `3B2418`, "Others" = `E9D3B4` → OK.
   Then **Color → Border** → light gray.
8. Drag `Gap` onto **Label**. In the Data pane, right-click `Gap` → **Default Properties → Number Format → Custom** →
   type `+0.00;-0.00` → OK.
9. Title: `Flavor, aftertaste and overall impression separate the top 10%` → smaller second line:
   `Average score gap between the top 10% and the other 90%`.

✅ **Check:**

| Trait | Gap | Color |
|---|---|---|
| Cupper points (overall) | +0.63 | Espresso |
| Flavor | +0.57 | Espresso |
| Aftertaste | +0.57 | Espresso |
| Acidity | +0.53 | Crema |
| Balance | +0.50 | Crema |
| Aroma | +0.49 | Crema |
| Body | +0.44 | Crema |
| Clean cup | +0.17 | Crema |
| Uniformity | +0.15 | Crema |
| Sweetness | +0.12 | Crema |

If every bar is the same, the formula used the wrong `top_10_pct`. Redo step 2 and pick the long file's field.

---

## Step 5: Altitude ("Higher farms score higher")

A bar chart of average score by altitude band. This is easier to read than a scatter plot.

1. **New Worksheet** → rename `Altitude`.
2. Drag `altitude_band` (reviews file) onto **Columns**. Five labels appear across the top.
3. Drag `total_cup_points` onto **Rows** → pill arrow → **Measure → Average**. Five vertical bars appear.
4. **Hide Unknown:** right-click the **Unknown** label at the bottom → **Exclude**.
5. **Put the bands in order** (Tableau sorts text alphabetically, which puts them out of order):
   right-click the `altitude_band` pill on Columns → **Sort…** → Sort By: **Manual** → use the up/down arrows to order:
   `<1000 m`, `1000–1299 m`, `1300–1599 m`, `≥1600 m` → OK.
6. **Make differences visible:** right-click the left axis → **Edit Axis…** → Range: **Fixed** →
   Start `80`, End `84` → close the box.
7. Color: click **Color** on the Marks card → pick Caramel (or type `C8873A` under More Colors). Highlighting the top band
   in Espresso is optional: drag `altitude_band` onto **Color** → Edit Colors → `≥1600 m` = `3B2418`, others = `C8873A`.
8. Drag `total_cup_points` onto **Label** → pill arrow → **Measure → Average**.
9. Title: `Coffees grown above 1,600 m average 1.7 points more` → smaller second line:
   `Average score by farm altitude (axis starts at 80)`.

✅ **Check:**

| Band | Average | Coffees |
|---|---|---|
| <1000 m | 81.7 | 206 |
| 1000–1299 m | 81.6 | 303 |
| 1300–1599 m | 82.0 | 311 |
| ≥1600 m | 83.4 | 253 |

**Why the axis note matters:** starting the axis at 80 instead of 0 makes small differences look big. Saying so in the
subtitle keeps the chart honest.

---

## Step 6: Country ranking ("Best origins")

1. **New Worksheet** → rename `Countries`.
2. Drag `country_group` onto **Rows**. Drag `total_cup_points` onto **Columns** → pill arrow → **Measure → Average**.
3. Hide groups that aren't countries: right-click **Other** in the list → **Exclude**. Do the same for **Unknown**.
4. Sort: hover over the bottom axis → click the **sort icon** until the highest average is on top.
5. Color: **Color** → Espresso (`3B2418`).
6. Drag `total_cup_points` onto **Label** → **Measure → Average**.
7. Drag `review_id` onto **Tooltip** → **Measure → Count (Distinct)**.
8. **Average line:** at the top of the left column, click the **Analytics** tab (next to **Data**) → drag
   **Reference Line** onto the chart → drop it on **Table** → in the box: Value = `AVG(total_cup_points)`,
   Label = **Custom** → type `Overall average` → Line: dashed, Caramel → OK.
   Click the **Data** tab to go back to your fields.
9. Axis: right-click the bottom axis → **Edit Axis…** → **Fixed** → Start `78`, End `86`.
10. Title: `Ethiopia, Kenya and Uganda lead` → second line:
    `Average score, countries with 20+ coffees (axis starts at 78)`.

✅ **Check (top and bottom):** Ethiopia 85.5 (44 coffees), Kenya 84.3 (25), Uganda 83.5 (36) … Mexico 80.9 (236),
Honduras 80.9 (52), Nicaragua 80.5 (26). The overall average line is at **82.2**.

---

## Step 7: Build the dashboard

1. Click the **New Dashboard** icon (second icon right of the tabs) → rename the tab `Coffee Dashboard`.
2. **Size:** on the left under **Size**, choose **Fixed size → Custom** → Width `1200`, Height `950`.
3. **Title:** check **Show dashboard title** (bottom left) → double-click the title →
   `What Brews a Winning Cup?` → Enter → smaller line:
   `1,338 professional coffee reviews (Coffee Quality Institute)` → OK.
4. **KPI row:** in the left panel under **Objects**, drag a **Horizontal** container to the top of the dashboard.
   Then drag your four KPI sheets (`KPI Reviews`, `KPI Average`, `KPI Cutoff`, `KPI Countries`) into it one at a time,
   side by side.
5. **Middle row:** drag a **Horizontal** container under the KPI row → drag in `Map` (left) and `Top 10 Gap` (right).
6. **Bottom row:** another **Horizontal** container → `Altitude` (left) and `Countries` (right).
7. **Even out the widths:** click a container's gray edge → small arrow menu → **Distribute Contents Evenly**.
8. **Remove extra legends:** Tableau adds legends on the right. Keep the map's color legend if you like, and remove the
   others (click the legend → **X**).
9. **Footer:** drag a **Text** object to the bottom → type:
   `Data: Coffee Quality Institute via TidyTuesday (2020). Team: Bryan Larison, Gina Fuller, Alexandra Hagen, Garrett Williford.`

### Make the map filter the other charts
1. Top menu: **Dashboard → Actions… → Add Action → Filter…**
2. Source Sheets: check **Map** only. Run action on: **Select**. Target Sheets: check `Top 10 Gap`, `Altitude`, `Countries`.
3. Clearing the selection will: **Show all values** → OK → OK.
4. Test: click Ethiopia on the map. The other charts should change to Ethiopia only. Click empty ocean to reset.

### Add dropdown filters (optional)
1. Click the **Map** sheet on the dashboard → its small arrow menu (top right of the sheet) → **Filters** → `processing`.
   A filter box appears.
2. Click that filter's arrow menu → **Apply to Worksheets → All Using Related Data Sources**.
3. Repeat for `species` and `grading_year` if you want them.

---

## Step 8: Publish to Tableau Public

1. Make a free account at **public.tableau.com**.
2. In Tableau: top menu **Server → Tableau Public → Save to Tableau Public As…** → sign in → name it
   `What Brews a Winning Cup` → Save. Your browser opens the live dashboard.
   - If that menu isn't there, install the free **Tableau Public** desktop app, open your workbook (.twb) in it, and
     save from there.
   - If it asks to **extract** the data, say yes.
3. On the web page: click **Edit Details** → add a one-sentence description → Save. Copy the link from the address bar.
4. Take a screenshot of the dashboard (Windows: **Win + Shift + S**) and save it as `figures/tableau_dashboard.png`
   in this repo.

Everything on Tableau Public is public. That's fine here because the dataset is already public.

---

## Step 9: Show it off

**README:** add near the top:
```markdown
## Interactive dashboard
[![Tableau dashboard](figures/tableau_dashboard.png)](YOUR_TABLEAU_PUBLIC_LINK)
Explore the data by country, altitude and processing method on **[Tableau Public](YOUR_TABLEAU_PUBLIC_LINK)**.
```

**Resume bullet** (Projects → Coffee Quality Analysis):
> Built an interactive Tableau dashboard of 1,338 professional coffee reviews, showing how origin, altitude and
> tasting traits drive quality scores, and published it to Tableau Public

**LinkedIn post** (draft, put it in your own words):
> What makes a great cup of coffee? Our team analyzed 1,338 professional coffee reviews, and I turned the findings into
> an interactive Tableau dashboard.
> - Ethiopia, Kenya and Uganda produce the highest-rated coffees.
> - Farms above 1,600 m average about 1.7 points higher than farms below 1,000 m.
> - Flavor, aftertaste and overall impression are what set the top 10% apart.
> Explore it here: [link]  #DataAnalytics #Tableau #DataVisualization

**LinkedIn profile:** add the dashboard to **Featured** and add **Tableau** under Skills.
