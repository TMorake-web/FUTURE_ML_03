from pathlib import Path
import pandas as pd

# Find the data folder beside this script.
DATA_FOLDER = Path(__file__).parent / "data"

# Read resume text and category labels.
# We don't load the HTML version because the plain text is enough.
resumes = pd.read_csv(
    DATA_FOLDER / "Resume.csv",
    usecols=["ID", "Resume_str", "Category"],
)

# Read a few job rows to inspect their columns and sample titles.
jobs = pd.read_csv(
    DATA_FOLDER / "monster_com-job_sample.csv",
    nrows=5,
)

print("Resume dataset columns:")
print(list(resumes.columns))

print("\nResume counts by category:")
print(resumes["Category"].value_counts().to_string())

print("\nJob dataset columns:")
print(list(jobs.columns))

# Show short summaries instead of printing full resume or job text.
print("\nFirst five resume summaries:")
for _, row in resumes.head(5).iterrows():
    resume_text = str(row.get("Resume_str", ""))
    print(
        f"Category: {row.get('Category', 'Unknown')} | "
        f"Text length: {len(resume_text)} characters"
    )

print("\nFive job summaries:")
for _, row in jobs.iterrows():
    description = str(row.get("job_description", ""))
    print(
        f"Title: {row.get('job_title', 'Unknown')} | "
        f"Description length: {len(description)} characters"
    )