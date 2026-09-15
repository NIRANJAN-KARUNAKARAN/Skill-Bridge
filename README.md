# Job Market NLP and Skill Extraction Pipeline

## Overview

This project develops an NLP-based pipeline for processing and analysing job advertisements from **India and Malaysia**.

The objective is to transform raw job advertisement datasets into a consistent, cleaned and NLP-processed dataset that can be consumed by the backend for job-role and skill analysis.

The pipeline includes data preparation, dataset unification, duplicate removal, text cleaning, NLP preprocessing, skill extraction, skill normalization, cybersecurity vocabulary repair and skill categorisation.

---

## Countries Covered

* India
* Malaysia

The pipeline processes the available jobs from both datasets and does not restrict the data to a fixed number of jobs or a fixed set of job roles.

---

# Completed Work

## 1. Dataset Upload and Reading

The two datasets are uploaded separately because the India and Malaysia datasets are provided as separate Excel files.

### India Dataset

The India job dataset is loaded from the provided Excel workbook.

### Malaysia Dataset

The Malaysia job dataset is loaded separately from its Excel workbook.

The original datasets are preserved before further processing.

---

## 2. Column Standardisation

The datasets originally contain different column names.

The pipeline standardises important fields so that both datasets can be combined into one consistent structure.

Examples of standardised fields include:

* Job ID
* Job title
* Role
* Company name
* Country
* Location
* Job description
* Skills / tags

Different column names such as `suggested_role` and `suggestedRole` are mapped to a common `role` field.

Similarly, job title, company and job description fields are standardised where necessary.

---

## 3. Country Identification

Each job is assigned a country value:

* `India`
* `Malaysia`

This allows the final dataset to support country-level analysis.

---

## 4. Unified Dataset

The India and Malaysia datasets are combined into one unified dataset.

The pipeline does **not** filter the dataset to only selected roles.

All available jobs from both datasets are retained.

A unique `jobId` is generated for each job where a suitable unique ID is not already available.

Example:

```text
JOB_000001
JOB_000002
JOB_000003
...
```

---

## 5. Duplicate Removal

Duplicate job advertisements are checked and removed.

Duplicate detection considers available job information such as:

* Job title
* Company
* Country
* Location
* Job description

The purpose is to prevent the same advertisement from appearing multiple times in the final dataset.

Job IDs are regenerated after duplicate removal to ensure that the final dataset has unique identifiers.

---

## 6. Job Text Construction

A combined NLP text field is created from relevant job information.

The NLP text can contain information from:

* Job title
* Job description
* Existing skills/tags

This provides the skill extraction stage with a larger text representation of each job advertisement.

---

# NLP Preprocessing

## 7. HTML and Text Cleaning

Job descriptions may contain HTML tags and web-related content.

The preprocessing stage:

* Removes HTML tags
* Decodes HTML entities
* Removes URLs
* Normalises whitespace
* Cleans unnecessary formatting
* Converts text into a consistent representation

This prevents HTML fragments such as:

```text
<p>
</p>
<br>
```

from being incorrectly treated as meaningful NLP tokens.

---

## 8. Tokenisation

The cleaned job descriptions are processed using spaCy.

The pipeline creates cleaned tokens by removing:

* Stop words
* Punctuation
* Empty tokens
* Unnecessary spaces

The cleaned tokens are retained for further analysis.

---

## 9. Lemmatization

The NLP pipeline also generates lemmas.

Lemmatization converts words into their base forms where supported by the NLP model.

For example, different grammatical forms of a word can be represented using a common base form.

---

# Skill Extraction

## 10. Skill Vocabulary

A skill vocabulary is created to identify technical and professional skills appearing in job advertisements.

The vocabulary includes areas such as:

### Programming

* Python
* Java
* C
* C++
* C#
* R
* JavaScript
* TypeScript

### Data

* SQL
* MySQL
* PostgreSQL
* MongoDB
* Excel
* Power BI
* Tableau
* Pandas
* NumPy

### AI / Machine Learning

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Natural Language Processing

### Cloud

* AWS
* Microsoft Azure
* Google Cloud
* Kubernetes

### DevOps

* Docker
* Kubernetes
* CI/CD
* Linux

### Cybersecurity

* Cybersecurity
* Information Security
* Application Security
* Security Operations
* SIEM
* Digital Forensics
* Penetration Testing
* Intrusion Detection
* Intrusion Prevention
* Identity and Access Management
* Zero Trust
* Cryptography
* Encryption

The vocabulary can be extended as additional skills are identified during validation.

---

# Cybersecurity Vocabulary Repair

## 11. Cybersecurity Skill Vocabulary

A specific vocabulary repair step has been included for cybersecurity-related terminology.

The purpose is to improve recognition of cybersecurity skills that may appear using different abbreviations, spellings or terminology.

Examples include:

| Input / Variation | Normalised Skill               |
| ----------------- | ------------------------------ |
| `cyber security`  | Cybersecurity                  |
| `cybersecurity`   | Cybersecurity                  |
| `infosec`         | Information Security           |
| `appsec`          | Application Security           |
| `soc`             | Security Operations            |
| `siem`            | SIEM                           |
| `pentesting`      | Penetration Testing            |
| `pen testing`     | Penetration Testing            |
| `forensics`       | Digital Forensics              |
| `ids`             | Intrusion Detection            |
| `ips`             | Intrusion Prevention           |
| `iam`             | Identity and Access Management |
| `k8s`             | Kubernetes                     |
| `cicd`            | CI/CD                          |

This provides a consistent representation of cybersecurity skills in the final dataset.

---

# Skill Extraction Method

## 12. Phrase-Based Skill Extraction

The pipeline uses a spaCy `PhraseMatcher` to identify skills in the processed job text.

The matcher searches for known skill terms and maps recognised variations to their normalised skill names.

The extraction process also checks the existing skills/tags field when available.

The extracted skills are stored as individual skills rather than one large text string.

Example:

```text
["Python", "SQL", "AWS", "Machine Learning"]
```

---

# Skill Normalization

## 13. Skill Normalization

After extraction, skills are normalised using the repaired skill vocabulary.

This ensures that different representations of the same skill are mapped to one standard name.

For example:

```text
ML → Machine Learning
AI → Artificial Intelligence
NLP → Natural Language Processing
AWS → AWS
Amazon Web Services → AWS
GCP → Google Cloud
K8s → Kubernetes
```

This improves consistency for downstream backend processing and analysis.

---

# Skill Categorisation

## 14. Skill Categories

Normalised skills are assigned to broader skill categories where applicable.

Possible categories include:

* Programming
* Data
* AI/ML
* Data Science
* Cloud
* DevOps
* Cybersecurity
* Software
* Other

A job can contain multiple skill categories.

Example:

```text
Skills:
Python, SQL, AWS, Machine Learning

Categories:
Programming, Data, Cloud, AI/ML
```

---

# Null and Empty Data Handling

## 15. Null / Empty Skill Records

The final dataset is checked for null and empty skill values.

Rows containing null or empty skill data are removed from the final skill-ready dataset where required.

The final skill field should not contain:

```text
NaN
None
null
[]
blank values
```

This ensures that the backend receives usable skill records.

---

# Final Unified Backend Dataset

## 16. Final Output Schema

The final dataset is structured into a consistent schema for backend consumption.

Important fields include:

| Field               | Description                              |
| ------------------- | ---------------------------------------- |
| `jobId`             | Unique identifier for each job           |
| `title`             | Job title                                |
| `role`              | Job role where available                 |
| `companyName`       | Company / employer                       |
| `country`           | India or Malaysia                        |
| `location`          | Job location                             |
| `experience`        | Experience information where available   |
| `jobDescription`    | Original job description                 |
| `nlp_text`          | Combined NLP input text                  |
| `clean_text`        | Cleaned job text                         |
| `clean_tokens`      | Cleaned tokens                           |
| `lemmas`            | Lemmatized tokens                        |
| `tagsAndSkills`     | Original skills/tags where available     |
| `extracted_skills`  | Skills identified by the skill extractor |
| `normalized_skills` | Standardised skills                      |
| `skill_categories`  | Categories assigned to the skills        |

---

# Intermediate Outputs

The pipeline produces downloadable intermediate datasets after major processing stages.

Examples include:

```text
00_India_All_Jobs_Original.xlsx
00_Malaysia_All_Jobs_Original.xlsx

01_Unified_ALL_Jobs.xlsx

02_Unified_ALL_Jobs_Deduplicated.xlsx

03_Text_Constructed_ALL_Jobs.xlsx

04_Cleaned_NLP_Text_ALL_Jobs.xlsx

05_NLP_Tokens_ALL_Jobs.xlsx

06_Lemmatized_ALL_Jobs.xlsx

07_Repaired_Skill_Vocabulary.xlsx

08_Skill_Extracted_ALL_Jobs.xlsx

09_Skill_Normalized_ALL_Jobs.xlsx

10_Skill_Categorized_ALL_Jobs.xlsx
```

The final dataset is intended to be:

```text
FINAL_NLP_JOB_DATASET_NO_NULL_SKILLS.xlsx
```

---

# Current Status

## Completed

* [x] India dataset loaded
* [x] Malaysia dataset loaded
* [x] Separate dataset upload process
* [x] Column standardisation
* [x] Country identification
* [x] Unified dataset creation
* [x] Processing of all available jobs
* [x] Unique job ID generation
* [x] Duplicate checking and removal
* [x] NLP text construction
* [x] HTML cleaning
* [x] URL removal
* [x] Tokenisation
* [x] Lemmatization
* [x] Skill vocabulary creation
* [x] Cybersecurity vocabulary repair
* [x] Abbreviation and synonym normalization
* [x] Skill extraction
* [x] Skill normalization
* [x] Skill categorisation
* [x] Null / empty skill handling
* [x] Unified backend-ready schema
* [x] Intermediate Excel outputs
* [x] Final processed dataset generation

---

# Remaining Work

The following work is still required to complete the broader evaluation and validation stage.

## 1. Manually Validated Benchmark

A manually validated benchmark should be created using real job advertisements from both:

* India
* Malaysia

The benchmark should contain manually verified expected skills for each selected advertisement.

The manually annotated skills will be treated as the ground truth.

---

## 2. Baseline Skill Extraction Method

A simple baseline method should be implemented.

For example, the baseline can use direct keyword or dictionary matching without the stronger semantic approach.

The baseline results should be compared with the stronger NLP/semantic method.

---

## 3. Stronger NLP / Semantic Method

At least one stronger NLP or semantic skill extraction method should be implemented and evaluated against the baseline.

Possible approaches can include semantic similarity or embedding-based matching.

The exact method should be selected based on the project's requirements and available computational resources.

---

## 4. Precision, Recall and F1 Evaluation

The skill extraction systems should be evaluated using:

* Precision
* Recall
* F1-score

The evaluation should not only report one overall score.

Results should be reported:

* Overall
* By job role
* By country

For example:

```text
India
    Precision
    Recall
    F1

Malaysia
    Precision
    Recall
    F1
```

and, where sufficient benchmark data exists:

```text
Data Scientist
Software Engineer
AI/ML Engineer
Data Analyst
Cybersecurity
Cloud Engineer
```

The role-level evaluation should be based on the actual roles represented in the validated benchmark rather than restricting the main dataset to those roles.

---

## 5. Cybersecurity Vocabulary Validation

The repaired cybersecurity vocabulary should be manually reviewed against real job advertisements.

Additional cybersecurity abbreviations, synonyms and terminology should be added when necessary.

Normalization rules should be documented so that the same skill is consistently represented.

---

## 6. Skill Extraction Error Analysis

The extracted skills should be compared against the manually validated benchmark to identify:

* False positives
* False negatives
* Missing skills
* Incorrect normalization
* Abbreviation errors
* Ambiguous skill terms

The vocabulary and extraction rules can then be refined based on these errors.

---

## 7. Final Backend Integration

The final validated dataset should be connected to the backend.

The backend should consume the consistent unified schema rather than separate India and Malaysia schemas.

The backend should use the normalised skill representation for downstream analysis.

---

# Reproducibility

The pipeline is implemented in Python and is designed to run in Google Colab.

Main libraries/tools used include:

* Python
* Pandas
* NumPy
* spaCy
* spaCy PhraseMatcher
* openpyxl
* Google Colab file upload/download utilities

The processing pipeline should be executed in the documented order so that each intermediate output can be reproduced.

---

# Project Structure

A suggested GitHub structure is:

```text
project-root/
│
├── README.md
│
├── notebooks/
│   └── NLP_Job_Skill_Extraction.ipynb
│
├── data/
│   └── README.md
│
├── output/
│   └── README.md
│
├── benchmark/
│   └── README.md
│
└── results/
    └── README.md
```

Large Excel datasets do not necessarily need to be committed directly to GitHub. If they are too large, they can be stored separately and the README can document where they are maintained.

---

# Data Privacy and Responsible Use

The dataset contains job advertisement information collected for research and analysis.

Before publishing datasets to a public GitHub repository, verify that the data can legally and appropriately be redistributed.

Where necessary, keep the raw datasets private and publish only the processing code, schema, documentation and permitted derived data.

---

# Development Branch

This work is being maintained in a separate Git branch during development.

The branch contains the current NLP data-processing implementation and documentation.

Future commits will add the benchmark creation, stronger semantic extraction method, evaluation metrics and error analysis.

---

# Conclusion

The current implementation establishes a unified NLP processing pipeline for job advertisements from India and Malaysia.

The major completed components are:

1. Dataset preparation
2. Dataset unification
3. Duplicate handling
4. Text cleaning
5. NLP preprocessing
6. Skill extraction
7. Skill normalization
8. Cybersecurity vocabulary repair
9. Skill categorisation
10. Null / empty skill handling
11. Consistent backend schema

The main remaining stage is **validation and evaluation**, including the manually validated benchmark, baseline comparison, stronger semantic method, Precision/Recall/F1 reporting by role and country, and final error analysis.
