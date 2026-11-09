from pathlib import Path

import matplotlib

# Use a non-window mode so Python can save the chart without opening a display.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


# Find the project and results folders beside this script.
PROJECT_FOLDER = Path(__file__).parent
RESULTS_FILE = PROJECT_FOLDER / "artifacts" / "candidate_rankings.csv"
CHART_FILE = PROJECT_FOLDER / "artifacts" / "results_summary.png"


# Check that the ranking file has been created first.
if not RESULTS_FILE.exists():
    raise FileNotFoundError(
        "The ranking file was not found. Run screen_candidates.py first."
    )


# Read the results and keep only the top 10 candidates.
results = pd.read_csv(RESULTS_FILE)
top_ten = results.head(10).copy()

if top_ten.empty:
    raise ValueError("The ranking file has no candidate results.")


# Reverse the order so Rank 1 appears at the top of the chart.
top_ten = top_ten.iloc[::-1].reset_index(drop=True)
labels = [f"Rank {int(rank)}" for rank in top_ten["Rank"]]


# Draw a bar for each candidate's job skill coverage.
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(
    labels,
    top_ten["Job skill coverage (%)"],
    color="#2878A5",
)


# Write the number of matched skill phrases beside each bar.
for bar, (_, row) in zip(bars, top_ten.iterrows()):
    ax.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{int(row['Skills matched'])} of {int(row['Skills checked'])} phrases",
        va="center",
        fontsize=9,
    )


# Add labels and a short explanation to the chart.
ax.set_title("IT Support Technician: listed skill phrases found")
ax.set_xlabel("Share of listed job skill phrases found (%)")
ax.set_ylabel("Candidate rank")
ax.set_xlim(0, 115)
ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

fig.text(
    0.5,
    0.02,
    "Phrase matching can miss skills written differently. "
    "Use this chart to support human review, not to make hiring decisions.",
    ha="center",
    fontsize=9,
    wrap=True,
)

fig.tight_layout(rect=[0, 0.07, 1, 1])


# Save the image in the artifacts folder.
CHART_FILE.parent.mkdir(exist_ok=True)
fig.savefig(CHART_FILE, dpi=200, bbox_inches="tight")
plt.close(fig)

print(f"Saved the chart to: {CHART_FILE}")