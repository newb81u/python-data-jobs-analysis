
"""PART 4 — Optimal Skills: skills that are BOTH in high demand AND high paying.

Combines Parts 1 & 3 into one table and a scatter plot:
  x = demand (% of role's postings mentioning the skill)
  y = median salary of postings mentioning the skill
Upper-right = optimal skills (frequent + well paid).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from skill_demand import load
from salary_analysis import skill_salary

ROOT = Path(__file__).resolve().parent.parent


def optimal_table(df: pd.DataFrame, role: str = "Data Analyst", min_share: float = 2.0) -> pd.DataFrame:
    sub = df[df["job_title_short"] == role]
    n = len(sub)
    rows = []
    for skill in sorted({s for sk in sub["job_skills"] for s in sk}):
        mask = sub["job_skills"].apply(lambda x: skill in x)
        share = mask.mean() * 100
        if share >= min_share:                       # ignore one-off skills
            rows.append({"skill": skill,
                         "demand_pct": round(share, 1),
                         "median_salary": sub[mask]["salary_year_avg"].median()})
    out = pd.DataFrame(rows).sort_values("median_salary", ascending=False)
    print(f"\n=== Optimal skills table ({role}) ===\n{out.round(0)}")
    return out


def plot(tbl: pd.DataFrame, role: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.scatter(tbl["demand_pct"], tbl["median_salary"],
                s=90, alpha=0.7, color="#9467bd", edgecolors="black")
    med_y = tbl["median_salary"].median()
    plt.axhline(med_y, ls="--", lw=0.8, color="gray")
    plt.axvline(tbl["demand_pct"].median(), ls="--", lw=0.8, color="gray")
    for _, r in tbl.iterrows():
        plt.annotate(r["skill"], (r["demand_pct"], r["median_salary"]),
                     textcoords="offset points", xytext=(5, 5), fontsize=8)
    plt.title(f"Optimal Skills ({role}): demand vs. salary\nupper-right = frequent AND well paid")
    plt.xlabel("% of postings mentioning skill"); plt.ylabel("Median yearly salary (USD)")
    plt.tight_layout()
    out = ROOT / "outputs" / "figures" / "optimal_skills.png"
    plt.savefig(out, dpi=150); plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    df = load()
    plot(optimal_table(df), "Data Analyst")
