# Resume Screening and Ranking Demo

## Project Overview

This project is an NLP-based prototype that compares resume text with a job description and ranks resumes for human review.

For this example, it compares resumes in the **Information Technology** category with an **IT Support Technician** job listing.

It is a decision-support demonstration, not an automated hiring system.

## What the Project Does

The project:

1. Cleans resume and job-description text.
2. Checks for phrases related to skills listed in the job description.
3. Uses TF-IDF and text similarity to compare resumes with the job.
4. Scores resumes by the share of listed skill phrases found.
5. Ranks resumes by skill coverage, using text similarity to break ties.
6. Shows matching skill phrases and phrases that may need manual review.
7. Creates a chart of the top 10 results.

## How the Scoring Works

The program checks for eight skill phrase groups in the selected job description. Each group may include common alternative phrases.

**Job skill coverage** is the percentage of those listed skill groups that the program recognizes in a resume. For example, finding four of eight groups gives a score of 50%.

**TF-IDF text similarity** estimates how much the resume wording overlaps with the job description. It is used only to order resumes that have the same skill-coverage score.

These scores are text comparisons. They are not qualification probabilities, a measure of a candidate’s ability, or predictions of job success.

## Results and Skill Gaps

The output lists:

- Skill phrases found in each resume.
- Job skill phrases not found by the program and therefore worth checking manually.
- Each resume’s skill-coverage and text-similarity scores.
- The resulting rank for human review.

A phrase that the program does not find does not prove the candidate lacks that skill. They may have described it using different words.

The datasets do not include actual job outcomes, so this project cannot measure hiring accuracy.

## Datasets

This project uses:

- [Resume Dataset by Snehaan Bhawal](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
- [US Jobs on Monster.com dataset by PromptCloud](https://www.kaggle.com/datasets/PromptCloudHQ/us-jobs-on-monstercom)

Download and extract the datasets. Place these files in the project's `data/` folder:

```text
data/
├── Resume.csv
└── monster_com-job_sample.csv
```

The datasets are not included in this repository. Resume data can contain personal information, so do not upload raw resumes or candidate-level results to a public repository.

## Technologies

- Python
- Pandas
- Scikit-learn
- Matplotlib

## Setup in VS Code on Windows

Download the two dataset files and place them in the project's `data/` folder.

Open the project folder in VS Code. In the PowerShell terminal, create a virtual environment:

```powershell
python -m venv .venv
```

Install the required libraries:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Project

Optionally, inspect the data files without printing full resume text:

```powershell
.\.venv\Scripts\python.exe inspect_data.py
```

Compare resumes with the selected job and save the rankings:

```powershell
.\.venv\Scripts\python.exe screen_candidates.py
```

Create a chart of the top 10 results:

```powershell
.\.venv\Scripts\python.exe make_results_chart.py
```

The chart script uses the rankings created by `screen_candidates.py`.

## Output Files

The scripts save these files in `artifacts/`:

- `results_summary.png` — chart showing the top 10 results by skill coverage.
- `candidate_rankings.csv` — detailed scores, skill matches, skill phrases to review, and candidate IDs.

The rankings CSV is for local review only. It contains candidate IDs and should not be uploaded to a public repository. The chart does not show candidate IDs; check it before sharing to ensure it contains no identifying information.

## Limitations and Responsible Use

- Skill extraction uses a manually written list of phrases and alternatives. It may miss relevant skills expressed in different words.
- The scores measure text overlap, not a candidate’s actual capability or suitability.
- The project has not been evaluated against hiring outcomes.
- The ranking should support human review only. It must not make hiring decisions or be used as the sole reason to reject a candidate.
- Recruiters should review the full context and apply their own criteria fairly and consistently.

## Project Information

- **Program:** Future Interns Machine Learning Internship
- **Track:** Machine Learning
- **Task:** Task 3 — Resume / Candidate Screening System
- **Repository:** `FUTURE_ML_03`
