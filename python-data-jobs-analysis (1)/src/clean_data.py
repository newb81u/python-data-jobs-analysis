
"""Clean the raw job-postings CSV.

WHY: the raw export stores `job_skills` as a *string* of a Python list
("['SQL', 'Python']") — we parse it into a real list with ast.literal_eval
so we can count and explode skills. Dates are parsed to datetime, duplicate
postings removed, and rows missing critical fields (skills or salary) dropped —
imputing salaries would invent data, so dropping <1% of rows is safer.
"""
import ast
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "raw" / "job_postings.csv")
    print("Raw shape:", df.shape)

    df["job_posted_date"] = pd.to_datetime(df["job_posted_date"], errors="coerce")
    df["salary_year_avg"] = pd.to_numeric(df["salary_year_avg"], errors="coerce")

    # Dedupe/drop BEFORE parsing job_skills into lists (lists aren't hashable).
    before = len(df)
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "job_skills"])
    df = df.dropna(subset=["job_posted_date", "salary_year_avg"])
    print(f"Removed {before - len(df)} unusable rows.")

    df["job_skills"] = df["job_skills"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    df = df[df["job_skills"].str.len() > 0]      # analysis needs at least one skill

    out = ROOT / "data" / "processed" / "job_postings_clean.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows -> {out}")
    return df


if __name__ == "__main__":
    main()
