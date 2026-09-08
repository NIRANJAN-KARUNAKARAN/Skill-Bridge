import pandas as pd
import os
import re

# ============================================================
# SKILLBRIDGE - G1-A DATA ACQUISITION & ENGINEERING PIPELINE
# Raw Data → Profiling → Cleaning → Unified Schema → CSV
# ============================================================

# ------------------------------------------------------------
# 1. FILE PATHS
# ------------------------------------------------------------

INDIA_FILE = "/Users/tharuntejev/Desktop/DATASET OF INDIA.xlsx"
MALAYSIA_FILE = "/Users/tharuntejev/Desktop/DATASET OF MALAYSIA.xlsx"

OUTPUT_DIR = "/Users/tharuntejev/Desktop/OUTPUT DIRECTORY"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("SKILLBRIDGE G1-A DATA PIPELINE")
print("=" * 60)

print("\n[1] Loading datasets...")

try:
    india_df = pd.read_excel(INDIA_FILE)
    malaysia_df = pd.read_excel(MALAYSIA_FILE)

    print("India dataset loaded successfully.")
    print("Malaysia dataset loaded successfully.")

except FileNotFoundError as e:
    print("\nERROR: Excel file not found.")
    print("Check that your files are inside:")
    print("data/raw/")
    print(e)
    exit()


# ------------------------------------------------------------
# 3. DATA PROFILING FUNCTION
# ------------------------------------------------------------
# 🔴 MOVED UP: profiling now runs on truly raw data,
# before we touch columns at all (was originally after
# a "country" column had already been injected).

def profile_dataset(df, name):

    print("\n" + "-" * 60)
    print(f"DATA PROFILE: {name}")
    print("-" * 60)

    print(f"Number of rows    : {df.shape[0]}")
    print(f"Number of columns : {df.shape[1]}")

    print("\nColumns:")
    for column in df.columns:
        print(" -", column)

    print("\nMissing values:")
    missing = df.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            print(f" - {column}: {count}")

    if missing.sum() == 0:
        print("No missing values detected.")

    print("\nDuplicate rows:", df.duplicated().sum())

    if "job_id" in df.columns:
        print(
            "Duplicate Job IDs:",
            df["job_id"].duplicated().sum()
        )


profile_dataset(india_df, "INDIA")
profile_dataset(malaysia_df, "MALAYSIA")


# ------------------------------------------------------------
# 4. STANDARDIZE COLUMN NAMES
# ------------------------------------------------------------
# 🔴 FIX: this now runs BEFORE we add our own "country" column,
# and includes a guard that drops any duplicate column names
# created during standardization (e.g. a raw "Country" column
# lowercasing to "country" and colliding with anything else).

def clean_column_names(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
        .str.replace("-", "_")
    )

    # 🔴 FIX: remove duplicate columns (keeps first occurrence)
    df = df.loc[:, ~df.columns.duplicated()]

    return df


india_df = clean_column_names(india_df)
malaysia_df = clean_column_names(malaysia_df)


# ------------------------------------------------------------
# 5. ADD COUNTRY
# ------------------------------------------------------------
# 🔴 MOVED DOWN: now runs AFTER column-name cleanup, so this
# assignment is guaranteed to be the only "country" column,
# with the correct value, and can't collide with a raw-file
# column of the same name after lowercasing.

india_df["country"] = "India"
malaysia_df["country"] = "Malaysia"


# ------------------------------------------------------------
# 6. DISPLAY STANDARDIZED COLUMNS
# ------------------------------------------------------------

print("\n[2] Standardized column names")

print("\nIndia:")
print(list(india_df.columns))

print("\nMalaysia:")
print(list(malaysia_df.columns))


# ------------------------------------------------------------
# 7. RENAME COMMON FIELDS
# ------------------------------------------------------------

def rename_columns(df):

    rename_map = {}

    possible_titles = [
        "job_title",
        "title",
        "jobtitle",
        "job_role"
    ]

    possible_companies = [
        "company",
        "company_name",
        "employer"
    ]

    possible_locations = [
        "location",
        "job_location",
        "city"
    ]

    possible_descriptions = [
        "job_description",
        "description",
        "job_desc"
    ]

    for col in possible_titles:
        if col in df.columns:
            rename_map[col] = "original_title"
            break

    for col in possible_companies:
        if col in df.columns:
            rename_map[col] = "company"
            break

    for col in possible_locations:
        if col in df.columns:
            rename_map[col] = "location"
            break

    for col in possible_descriptions:
        if col in df.columns:
            rename_map[col] = "job_description"
            break

    df = df.rename(columns=rename_map)

    return df


india_df = rename_columns(india_df)
malaysia_df = rename_columns(malaysia_df)


# ------------------------------------------------------------
# 8. CREATE MISSING STANDARD FIELDS
# ------------------------------------------------------------

required_fields = [
    "job_id",
    "original_title",
    "normalized_title",
    "country",
    "company",
    "location",
    "category",
    "subcategory",
    "role_type",
    "salary_min",
    "salary_max",
    "currency",
    "salary_period",
    "job_description",
    "posting_date",
    "source",
    "source_record",
    "data_note",
    "purpose",
    "reliability",
    "limitations"
]


def create_missing_fields(df):

    for field in required_fields:

        if field not in df.columns:

            if field == "normalized_title":

                if "original_title" in df.columns:
                    df[field] = df["original_title"]
                else:
                    df[field] = "Not available"

            elif field == "currency":

                if "country" in df.columns:
                    df[field] = df["country"].map({
                        "India": "INR",
                        "Malaysia": "MYR"
                    })
                else:
                    df[field] = "Not available"

            elif field == "salary_period":

                df[field] = "Not available"

            elif field == "purpose":

                df[field] = "SkillBridge job market analysis"

            elif field == "reliability":

                df[field] = "Moderate"

            elif field == "limitations":

                df[field] = "Missing or source-dependent fields"

            elif field == "data_note":

                df[field] = "Standardized by G1-A"

            else:

                df[field] = "Not available"

    return df


india_df = create_missing_fields(india_df)
malaysia_df = create_missing_fields(malaysia_df)


# ------------------------------------------------------------
# 9. CLEAN TEXT FIELDS
# ------------------------------------------------------------

text_fields = [
    "original_title",
    "normalized_title",
    "company",
    "location",
    "category",
    "subcategory",
    "role_type",
    "source"
]


def clean_text(df):

    for field in text_fields:

        if field in df.columns:

            df[field] = (
                df[field]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

    return df


india_df = clean_text(india_df)
malaysia_df = clean_text(malaysia_df)


# ------------------------------------------------------------
# 10. NORMALIZE JOB TITLES
# ------------------------------------------------------------

def normalize_title(title):

    if pd.isna(title):
        return "Not available"

    title = str(title).strip()

    # Remove excessive spaces
    title = re.sub(r"\s+", " ", title)

    # Basic title normalization
    replacements = {
        "Sr.": "Senior",
        "Sr ": "Senior ",
        "Jr.": "Junior",
        "Jr ": "Junior ",
        "S/W": "Software"
    }

    for old, new in replacements.items():
        title = title.replace(old, new)

    return title


india_df["normalized_title"] = (
    india_df["original_title"]
    .apply(normalize_title)
)

malaysia_df["normalized_title"] = (
    malaysia_df["original_title"]
    .apply(normalize_title)
)


# ------------------------------------------------------------
# 11. CLEAN JOB IDS
# ------------------------------------------------------------

def clean_job_id(df):

    if "job_id" in df.columns:

        df["job_id"] = (
            df["job_id"]
            .astype(str)
            .str.strip()
        )

    return df


india_df = clean_job_id(india_df)
malaysia_df = clean_job_id(malaysia_df)


# ------------------------------------------------------------
# 12. REMOVE DUPLICATE RECORDS
# ------------------------------------------------------------

print("\n[3] Removing duplicate records...")

india_before = len(india_df)
malaysia_before = len(malaysia_df)

india_df = india_df.drop_duplicates()

malaysia_df = malaysia_df.drop_duplicates()

print(
    "India duplicates removed:",
    india_before - len(india_df)
)

print(
    "Malaysia duplicates removed:",
    malaysia_before - len(malaysia_df)
)


# ------------------------------------------------------------
# 13. REMOVE DUPLICATE JOB IDS
# ------------------------------------------------------------

if "job_id" in india_df.columns:

    india_df = india_df.drop_duplicates(
        subset=["job_id"],
        keep="first"
    )

if "job_id" in malaysia_df.columns:

    malaysia_df = malaysia_df.drop_duplicates(
        subset=["job_id"],
        keep="first"
    )


# ------------------------------------------------------------
# 14. SALARY CLEANING
# ------------------------------------------------------------

def clean_salary(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value.lower() in [
        "not disclosed",
        "not available",
        "n/a",
        "na",
        "none",
        "-"
    ]:
        return None

    # Remove currency symbols and commas
    value = re.sub(r"[₹$RM,]", "", value)

    # Extract first number
    numbers = re.findall(r"\d+(?:\.\d+)?", value)

    if len(numbers) == 0:
        return None

    return float(numbers[0])


# Only process if salary columns exist
if "salary_min" in india_df.columns:

    india_df["salary_min"] = (
        india_df["salary_min"]
        .apply(clean_salary)
    )

if "salary_max" in india_df.columns:

    india_df["salary_max"] = (
        india_df["salary_max"]
        .apply(clean_salary)
    )


if "salary_min" in malaysia_df.columns:

    malaysia_df["salary_min"] = (
        malaysia_df["salary_min"]
        .apply(clean_salary)
    )

if "salary_max" in malaysia_df.columns:

    malaysia_df["salary_max"] = (
        malaysia_df["salary_max"]
        .apply(clean_salary)
    )


# ------------------------------------------------------------
# 15. COUNTRY-BASED CURRENCY
# ------------------------------------------------------------

india_df["currency"] = "INR"
malaysia_df["currency"] = "MYR"


# ------------------------------------------------------------
# 16. SELECT FINAL SCHEMA
# ------------------------------------------------------------

india_df = india_df[required_fields]

malaysia_df = malaysia_df[required_fields]


# ------------------------------------------------------------
# 17. COMBINE INDIA + MALAYSIA
# ------------------------------------------------------------

print("\n[4] Combining datasets...")

unified_df = pd.concat(
    [india_df, malaysia_df],
    ignore_index=True
)


# ------------------------------------------------------------
# 18. FINAL VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA VALIDATION")
print("=" * 60)

print("\nTotal records:", len(unified_df))

print(
    "India records:",
    len(unified_df[unified_df["country"] == "India"])
)

print(
    "Malaysia records:",
    len(unified_df[unified_df["country"] == "Malaysia"])
)

print(
    "\nDuplicate rows:",
    unified_df.duplicated().sum()
)

print(
    "Duplicate Job IDs:",
    unified_df["job_id"].duplicated().sum()
)

print("\nRecords by country:")

print(
    unified_df["country"]
    .value_counts()
)


# ------------------------------------------------------------
# 19. SAVE PROCESSED DATA
# ------------------------------------------------------------

output_file = (
    f"{OUTPUT_DIR}/unified_job_data.csv"
)

unified_df.to_csv(
    output_file,
    index=False
)


# Also save Excel version
excel_output = (
    f"{OUTPUT_DIR}/unified_job_data.xlsx"
)

unified_df.to_excel(
    excel_output,
    index=False
)


# ------------------------------------------------------------
# 20. SAVE DATA QUALITY REPORT
# ------------------------------------------------------------

quality_report = []

for country in ["India", "Malaysia"]:

    country_df = unified_df[
        unified_df["country"] == country
    ]

    quality_report.append({
        "country": country,
        "total_records": len(country_df),
        "duplicate_rows": country_df.duplicated().sum(),
        "duplicate_job_ids":
            country_df["job_id"].duplicated().sum(),
        "missing_values":
            country_df.isnull().sum().sum(),
        "unique_companies":
            country_df["company"].nunique(),
        "unique_locations":
            country_df["location"].nunique()
    })


quality_df = pd.DataFrame(quality_report)

quality_file = (
    f"{OUTPUT_DIR}/data_quality_report.csv"
)

quality_df.to_csv(
    quality_file,
    index=False
)


# ------------------------------------------------------------
# 21. DISPLAY FINAL SAMPLE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA SAMPLE")
print("=" * 60)

print(
    unified_df[
        [
            "job_id",
            "original_title",
            "normalized_title",
            "country",
            "company",
            "location",
            "currency"
        ]
    ].head(10).to_string(index=False)
)


# ------------------------------------------------------------
# 22. COMPLETION MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("G1-A PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nGenerated files:")

print("1.", output_file)
print("2.", excel_output)
print("3.", quality_file)

print("\nPipeline:")
print(
    "Raw Data → Profiling → Cleaning → "
    "Unified Schema → Validation → Processed Data"
)

print("\nReady for G2-A database/API integration.")

