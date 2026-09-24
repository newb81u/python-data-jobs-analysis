
# Interview Notes — Investigating Top Skills in Data Science

## What was the business problem and why does it matter?
Time and attention are limited, so which skills should an aspiring data analyst learn first?
The "business" is a personal learning roadmap, but the method is the same as any market
analysis: quantify demand, pay, and trend before committing resources. Data: 20,170 real
2023 job postings across 10 roles and 107 countries.

## Walk through one finding end-to-end: Python rising AND best-paying
- **What I measured:** (a) % of Data Analyst postings each month that mention "python";
  (b) median yearly salary of postings that mention it.
- **How:** filtered to the role, bucketed by month, counted postings containing the skill
  divided by that month's postings (percentages, so months are comparable); median via
  pandas groupby-median.
- **Result:** 34.8% (Jan) → 40.2% (Dec), +5.4 pts — the only top-5 skill with a clear climb,
  while SQL drifted from 62% to 50% and Excel slipped ~4 pts. Median salary: $98.5k, the
  highest of any top-10 skill.
- **What it means:** employers are shifting analyst work from spreadsheets to code. Python is
  the rare skill that is both growing in demand and pays a premium — top of my learning list.

## Why this cleaning approach / metric / chart?
- **`ast.literal_eval` + within-posting dedupe:** the CSV stores lists as strings; parsing makes
  per-skill counting trivial. Real rows repeat skills (`['sas', 'sas']`), so I dedupe per
  posting to avoid double-counting one mention as two.
- **Percentages for trends:** raw counts rise and fall with monthly posting volume;
  percentages isolate the skill's popularity, not the market's size.
- **Median salary, not mean:** salaries are right-skewed (a $300k posting would drag a mean
  around); medians represent the typical posting.
- **Bar charts for ranking, line for trends, scatter for the 2-D "optimal" view** — each
  chart type matches the question it answers.

## Most surprising / counter-intuitive result
Excel appears in 44% of analyst postings — more than Python — yet pays among the least
($84k median vs Python's $98.5k). Ubiquity doesn't equal value; being expected makes a
skill table stakes, not a premium. The premium sits in Python and, further out, niche
big-data platforms (Spark/Hadoop ~$111k).

## What would you do differently with more time/data?
- Use the full multi-year dataset to check whether the December SQL dip is holiday
  seasonality or a real downtrend.
- Model skill combinations instead of single skills (SQL + Python + a BI tool as a bundle).
- Split by seniority and country — the optimal set for a senior US role likely differs from
  a junior role elsewhere.
