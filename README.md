# Resume Screening and Ranking Demo

This project compares resume text with a job description and ranks resumes for human review. It uses the Resume Dataset and a Monster job listings dataset.

## What the project does

For this example, the program compares resumes in the **Information Technology** category with an **IT Support Technician** job listing.

It:

1. Cleans resume and job description text.
2. Checks for phrases related to skills listed in the job.
3. Uses TF-IDF to compare the text.
4. Ranks resumes by the share of listed skill phrases found. Text similarity breaks ties.
5. Lists matching phrases and phrases that may need review.
6. Creates a chart of the top 10 results.

## How to read the results

The skill coverage percentage is the share of the eight skill phrases recognized in a resume. The text similarity percentage measures how much the resume wording overlaps with the job description.

These are simple text comparisons. A missing phrase does not prove that someone lacks a skill; they may describe it differently. The scores are not qualification probabilities and should not be used to make hiring decisions.

The datasets do not link applicants to actual job outcomes, so this project cannot measure hiring accuracy.

## Datasets

- [Resume Dataset by Snehaan Bhawal](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
- [US Jobs on Monster.com dataset by PromptCloud](https://www.kaggle.com/datasets/PromptCloudHQ/us-jobs-on-monstercom)

Download and extract the datasets. Place these files in the project's `data` folder:

```text
data/
├── Resume.csv
└── monster_com-job_sample.csv