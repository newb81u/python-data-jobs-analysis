
# Investigating Top Skills in Data Science

Which skills should an aspiring data analyst learn first? I analyzed **20,170 real data-job
postings** from 2023 (10 roles, 107 countries) with Python (pandas, NumPy, matplotlib) to find
the skills most in demand, how demand trended through the year, what each skill pays, and
which skills are *optimal* — both common and well-paid.

## The Question

Learning everything is impossible, so: *which skills offer the best return on learning
effort for a data analyst?* This project answers it with data across four parts:
**Skill Demand → Skill Trends → Salary Analysis → Optimal Skills.**

## Dataset

- **Source:** job-postings dataset from [Luke Barousse's Python for Data Analytics course](https://www.youtube.com/watch?v=wUSDVGivd-8),
  collected from real job boards in 2023 (also browsable at [datanerd.tech](https://datanerd.tech/)).
  A 20k-row sample of the full multi-million-row dataset is included at `data/raw/job_postings.csv`
  (a sample because GitHub caps files at 100 MB — the pipeline works identically on the full file).
- **Size:** 20,170 postings → 20,130 after cleaning; 10 job titles (Data Analyst, Senior Data
  Scientist, Data Engineer, …) across 107 countries, Jan–Dec 2023.
- **Key columns:** `job_title_short`, `job_posted_date`, `job_country`, `job_skills`
  (list of skills per posting), `salary_year_avg`.

## Methodology

1. **Cleaning** (`src/clean_data.py`): parse dates, coerce salary to numeric, remove duplicates
   and rows missing critical fields, parse `job_skills` from string-of-a-list into real Python
   lists with `ast.literal_eval`, and dedupe skills within each posting.
2. **Part 1 — Skill Demand** (`src/skill_demand.py`): explode the skills list and count
   mentions per role → top 10 skills.
3. **Part 2 — Skill Trends** (`src/skill_trends.py`): % of each month's postings mentioning
   each top skill (percentages, not raw counts, so months are comparable).
4. **Part 3 — Salary Analysis** (`src/salary_analysis.py`): median yearly salary of postings
   mentioning each top skill (median, not mean — robust to outliers).
5. **Part 4 — Optimal Skills** (`src/optimal_skills.py`): merge demand % and median salary;
   the upper-right of the scatter plot = optimal skills.

## Key Findings (Data Analyst role, 4,833 postings)

- **SQL is non-negotiable: 64% of analyst postings mention it** (3,069 of 4,833), ahead of
  Excel (44%), Python (38%), and Tableau (34%). Power BI (22%) and R (22%) form the next tier.
- **Python is both rising and the best-paying common skill**: its share of monthly postings
  climbed from 34.8% (Jan) to 40.2% (Dec, +5.4 pts) while SQL and Excel drifted down — and its
  median salary ($98.5k) beats every other top-10 skill.
- **Spreadsheet/Office skills are common but pay least**: Word ($80k), Excel ($84k), and
  PowerPoint ($85k) sit at the bottom of the top 10 despite high demand. Ubiquity ≠ value.
- **The optimal core: SQL + Python + Tableau** — together covering ~70% of postings, all paying
  $92.5k–$98.5k median.
- **Big-data platforms are the specialization lever**: Snowflake ($110k), Spark ($111k), Hadoop
  ($111k), and Databricks ($110k) pay ~15% more than the core trio but appear in only 2–5% of
  postings — a strong second-step bet, not a first step.

## Recommendations

1. Learn **SQL first, then Python** — SQL gets you interviewed; Python is where demand is growing and pays most.
2. Add **one BI tool (Tableau or Power BI)** to cover ~90% of analyst postings.
3. Later, specialize in a **cloud/big-data platform (Snowflake, Spark, Databricks)** for the ~15% salary bump.

## How to Run

```bash
git clone https://github.com/YOUR_USERNAME/python-data-jobs-analysis.git
cd python-data-jobs-analysis
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/clean_data.py        # cleaning → data/processed/
python src/skill_demand.py      # part 1 + chart
python src/skill_trends.py      # part 2 + chart
python src/salary_analysis.py   # part 3 + chart
python src/optimal_skills.py    # part 4 + chart
```
Or walk through everything interactively in `notebooks/01_skill_analysis.ipynb`.

## What I'd Do With More Time

- Run the same pipeline on the full multi-year dataset to separate structural trends from 2023 noise (December's SQL dip looks like holiday posting seasonality).
- Analyze skill *combinations* (e.g., SQL + Python together vs. either alone).
- Split by country/seniority — optimal skills likely differ between US senior roles and junior roles elsewhere.
- Automate a quarterly "skills report" from the live datanerd.tech feed.
