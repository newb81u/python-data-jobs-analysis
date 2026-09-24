
"""PART 2 — Skill Trends: how does demand for the top skills change through 2023?

We use the % of that month's postings mentioning each skill (not raw counts),
because posting volume varies month to month — percentages make months comparable.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from skill_demand import load, top_skills

ROOT = Path(__file__).resolve().parent.parent


def monthly_trend(df: pd.DataFrame, role: str = "Data Analyst", n: int = 5) -> pd.DataFrame:
    sub = df[df["job_title_short"] == role].copy()
    sub["month"] = sub["job_posted_date"].dt.to_period("M").astype(str)
    monthly_totals = sub.groupby("month")["job_skills"].count()   # postings per month
    top = top_skills(df, role, n).index.tolist()

    trend = pd.DataFrame(index=sorted(sub["month"].unique()))
    for skill in top:
        has = (sub["job_skills"].apply(lambda x: skill in x)
                 .groupby(sub["month"]).sum())
        trend[skill] = (has / monthly_totals * 100).round(1)
    print("\n=== Monthly skill mention % ===\n", trend)
    return trend


def plot(trend: pd.DataFrame, role: str) -> None:
    plt.figure(figsize=(11, 5))
    for col in trend.columns:
        plt.plot(trend.index, trend[col], marker="o", label=col)
    plt.title(f"Trending Top Skills for {role} (% of monthly postings)")
    plt.xlabel("Month"); plt.ylabel("% of postings")
    plt.xticks(rotation=45); plt.legend(); plt.tight_layout()
    out = ROOT / "outputs" / "figures" / "skill_trends.png"
    plt.savefig(out, dpi=150); plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    df = load()
    plot(monthly_trend(df), "Data Analyst")
