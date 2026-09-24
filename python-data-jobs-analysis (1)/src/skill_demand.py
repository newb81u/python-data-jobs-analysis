
"""PART 1 — Skill Demand: which skills appear most in job postings?"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data" / "processed" / "job_postings_clean.csv",
                       parse_dates=["job_posted_date"],
                       converters={"job_skills": eval})


def top_skills(df: pd.DataFrame, role: str = "Data Analyst", n: int = 10) -> pd.Series:
    """Count skill mentions across one job role, return top n."""
    counts = (df[df["job_title_short"] == role]["job_skills"]
              .explode().value_counts().head(n))
    print(f"\n=== Top {n} skills for {role} ===\n{counts}")
    return counts


def plot(counts: pd.Series, role: str) -> None:
    plt.figure(figsize=(9, 5))
    counts.sort_values().plot(kind="barh", color="#4878cf")
    plt.title(f"Top {len(counts)} Skills for {role} Postings")
    plt.xlabel("Number of Postings")
    plt.tight_layout()
    out = ROOT / "outputs" / "figures" / "skill_demand.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=150); plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    df = load()
    plot(top_skills(df), "Data Analyst")
