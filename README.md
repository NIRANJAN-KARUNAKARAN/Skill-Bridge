# Skill-Bridge — Job Market Datasets

Cleaned and unified job market datasets for India and Malaysia, built as part of the SkillBridge project.

# Folder Structure
ALL_CLEANED_DATA/
├── INDIA_JOB_MARKET_FULL_CLEANSED.xlsx # Cleaned job market data for India
├── MALAYSIA_DATA_FULL_CLEANSED.xlsx # Cleaned job market data for Malaysia
└── UNIFIED_JOB_FULL_CLEANSED.xlsx # Combined/merged dataset (India + Malaysia)


## About the Data

These datasets contain job listing/market information sourced from public job market data, cleaned and standardized for analysis and downstream use in the SkillBridge project.

## Cleaning & Processing

- Removed rows with all-zero / null values
- Standardized column names across both country datasets
- Removed duplicate entries
- Merged India and Malaysia datasets into a unified schema (`UNIFIED_JOB_FULL_CLEANSED`)

## 📑 Column Overview

| Column Name | Description |
|---|---|
| *(add your columns here)* | *(e.g. Job Title, Company, Location, Salary, Skills Required, etc.)* |

## How to Use

```python
import pandas as pd

df_india = pd.read_excel("ALL_CLEANED_DATA/INDIA_JOB_MARKET_FULL_CLEANSED.xlsx")
df_malaysia = pd.read_excel("ALL_CLEANED_DATA/MALAYSIA_DATA_FULL_CLEANSED.xlsx")
df_unified = pd.read_excel("ALL_CLEANED_DATA/UNIFIED_JOB_FULL_CLEANSED.xlsx")
```

## Tools Used

- Python (Pandas, OpenPyXL)

## Notes

- This branch (`DATASETS`) is maintained separately from `main` and contains only processed/cleaned data files, not raw data or source code.
