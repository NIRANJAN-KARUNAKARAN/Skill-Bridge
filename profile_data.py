import pandas as pd

xl_india = pd.ExcelFile("data/raw/india_jobs.xlsx")
xl_my = pd.ExcelFile("data/raw/malaysia_jobs.xlsx")

print("India sheets:", xl_india.sheet_names)
print("Malaysia sheets:", xl_my.sheet_names)

df_india = pd.read_excel(xl_india, sheet_name=0)
df_my = pd.read_excel(xl_my, sheet_name=0)

def inspect(df, name):
    print(f"\n===== {name} =====")
    print("Shape:", df.shape)
    print("\nColumns & dtypes:")
    print(df.dtypes)
    print("\nSample rows:")
    print(df.head())
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nUnique counts per column:")
    print(df.nunique())

inspect(df_india, "India Jobs")
inspect(df_my, "Malaysia Jobs")