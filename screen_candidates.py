from html import unescape
from pathlib import Path
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Find the project and data folders beside this script.
PROJECT_FOLDER = Path(__file__).parent
DATA_FOLDER = PROJECT_FOLDER / "data"
OUTPUT_FOLDER = PROJECT_FOLDER / "artifacts"

RESUME_FILE = DATA_FOLDER / "Resume.csv"
JOB_FILE = DATA_FOLDER / "monster_com-job_sample.csv"


# Skill phrases and common alternatives to search for.
# This is a transparent phrase list, not an advanced skill-understanding model.
SKILL_ALIASES = {
    "Call tracking software": [
        "call tracking software",
        "call logging software",
    ],
    "Phone-based technical support": [
        "phone based technical support",
        "phone technical support",
        "phone support",
        "help desk support",
        "helpdesk support",
    ],
    "Problem documentation": [
        "problem documentation",
        "issue documentation",
        "documenting issues",
        "documenting problems",
        "ticket documentation",
    ],
    "Communication": [
        "problem documentation and communication",
        "communication skills",
        "written communication",
        "verbal communication",
    ],
    "Remote desktop tools": [
        "remote desktop management tools",
        "remote desktop tools",
        "remote desktop",
        "remote support tools",
    ],
    "Customer support": [
        "respond to customer requests",
        "customer requests",
        "customer support",
        "customer service",
    ],
    "LANDesk": [
        "landesk",
    ],
    "Microsoft Office": [
        "microsoft office",
        "ms office",
    ],
}


def clean_text(value):
    """Remove web markup and normalize text for comparison."""
    if pd.isna(value):
        return ""

    text = unescape(str(value))

    # Remove scripts, styles, and HTML tags sometimes found in scraped listings.
    text = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r"<[^>]+>", " ", text)

    text = text.lower()
    text = re.sub(r"[^a-z0-9+#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def focus_on_job_requirements(description):
    """Cut off common promotional text after the job requirements."""
    description = str(description)

    # Monster listings may add company advertising after the actual job details.
    description = re.split(
        r"\b(find out why|why join|why work for|about us)\b",
        description,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    return description


def extract_skills(text):
    """Find which listed skill phrases appear in a piece of text."""
    cleaned_text = clean_text(text)
    found_skills = []

    for skill_name, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            cleaned_alias = clean_text(alias)
            pattern = r"\b" + re.escape(cleaned_alias) + r"\b"

            if re.search(pattern, cleaned_text):
                found_skills.append(skill_name)
                break

    return found_skills


def main():
    """Compare IT resumes with one IT Support Technician job listing."""

    if not RESUME_FILE.exists():
        raise FileNotFoundError(f"Resume file not found: {RESUME_FILE}")

    if not JOB_FILE.exists():
        raise FileNotFoundError(f"Job file not found: {JOB_FILE}")

    # Load only the columns used in this project.
    resumes = pd.read_csv(
        RESUME_FILE,
        usecols=["ID", "Resume_str", "Category"],
    )
    jobs = pd.read_csv(
        JOB_FILE,
        usecols=["job_title", "job_description"],
    )

    # Select the IT Support Technician job.
    title_match = jobs["job_title"].astype(str).str.contains(
        "IT Support Technician",
        case=False,
        na=False,
    )
    matching_jobs = jobs[title_match]

    if matching_jobs.empty:
        raise ValueError("No IT Support Technician job was found.")

    selected_job = matching_jobs.iloc[0]
    job_title = str(selected_job["job_title"])
    job_description = focus_on_job_requirements(
        selected_job["job_description"]
    )

    # Use the 120 resumes labeled for Information Technology.
    it_resumes = resumes[
        resumes["Category"].astype(str).str.upper()
        == "INFORMATION-TECHNOLOGY"
    ].dropna(subset=["Resume_str"]).copy()

    if it_resumes.empty:
        raise ValueError("No Information Technology resumes were found.")

    required_skills = extract_skills(job_description)

    if not required_skills:
        raise ValueError("No listed skills were found in the job description.")

    cleaned_job = clean_text(job_description)
    cleaned_resumes = it_resumes["Resume_str"].map(clean_text).tolist()

    # TF-IDF compares the job text with each resume's text.
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=30000,
    )
    text_vectors = vectorizer.fit_transform([cleaned_job] + cleaned_resumes)
    similarities = cosine_similarity(
        text_vectors[0:1],
        text_vectors[1:],
    ).flatten()

    results = []

    for position, (_, resume) in enumerate(it_resumes.iterrows()):
        found_skills = extract_skills(resume["Resume_str"])

        matching_skills = [
            skill for skill in required_skills if skill in found_skills
        ]
        skills_to_review = [
            skill for skill in required_skills if skill not in found_skills
        ]

        skill_coverage = (
            len(matching_skills) / len(required_skills)
        ) * 100

        results.append(
            {
                "Candidate ID": resume["ID"],
                "Category": resume["Category"],
                "Skills matched": len(matching_skills),
                "Skills checked": len(required_skills),
                "Job skill coverage (%)": round(skill_coverage, 1),
                "TF-IDF text similarity (%)": round(
                    float(similarities[position]) * 100,
                    1,
                ),
                "Matching skills": ", ".join(matching_skills) or "None found",
                "Skills to review": ", ".join(skills_to_review) or "None from list",
            }
        )

    rankings = pd.DataFrame(results)

    # Rank by the clear skill coverage score.
    # Use TF-IDF similarity only to order candidates with equal skill coverage.
    rankings = rankings.sort_values(
        by=["Job skill coverage (%)", "TF-IDF text similarity (%)"],
        ascending=[False, False],
    ).reset_index(drop=True)
    rankings.insert(0, "Rank", range(1, len(rankings) + 1))

    # Save scores and skill lists, but not the full resume text.
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    report_file = OUTPUT_FOLDER / "candidate_rankings.csv"
    rankings.to_csv(report_file, index=False)

    print(f"Job used: {job_title}")
    print(f"IT resumes compared: {len(rankings)}")
    print(f"Skills checked: {', '.join(required_skills)}")
    print(f"\nSaved ranking to: {report_file}")

    print("\nTop 10 candidate matches:")
    for _, result in rankings.head(10).iterrows():
        print(f"\nRank {int(result['Rank'])} | Candidate ID: {result['Candidate ID']}")
        print(
            f"Job skills found: {int(result['Skills matched'])} "
            f"of {int(result['Skills checked'])}"
        )
        print(f"Job skill coverage: {result['Job skill coverage (%)']}%")
        print(
            "TF-IDF text similarity: "
            f"{result['TF-IDF text similarity (%)']}%"
        )
        print(f"Matching skills: {result['Matching skills']}")
        print(f"Skills to review: {result['Skills to review']}")

    print(
        "\nThese are text-based comparisons for human review. "
        "They are not qualification probabilities or hiring decisions."
    )


if __name__ == "__main__":
    main()