
"""PART 3 — Salary Analysis: which skills pay the most?"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from skill_demand import load, top_skills

ROOT = Path(__file__).resolve().parent.parent


def skill_salary(df: pd.DataFrame, role: str = "Data Analyst", n: int = 10) -> pd.Series:
    """Median yearly salary of postings mentioning each of the top-n demanded skills."""
    sub = df[df["job_title_short"] == role]
    top = top_skills(df, role, n).index.tolist()
    med = {s: sub[sub["job_skills"].apply(lambda x: s in x)]["salary_year_avg"].median()
           for s in top}
    out = pd.Series(med).sort_values(ascending=False)
    print(f"\n=== Median salary by skill ({role}) ===\n{out.round(0)}")
    return out


def plot(med: pd.Series, role: str) -> None:
    plt.figure(figsize=(9, 5))
    med.sort_values().plot(kind="barh", color="#2ca02c")
    plt.title(f"Median Yearly Salary by Skill ({role})")
    plt.xlabel("Median Salary (USD)")
    plt.tight_layout()
    out = ROOT / "outputs" / "figures" / "salary_analysis.png"
    plt.savefig(out, dpi=150); plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    df = load()
    plot(skill_salary(df), "Data Analyst")
