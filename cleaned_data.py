import os
from pathlib import Path
import pandas as pd

folder = Path(__file__).resolve().parent

# Find the raw CSV file in the same folder
raw_file = None
for name in ("dataset_raw.csv", "dataset_raw (1).csv", "24_mobile_app_usage.csv"):
    candidate = folder / name
    if candidate.exists():
        raw_file = candidate
        break

if raw_file is None:
    raise FileNotFoundError(
        f"Could not find raw CSV file in {folder}. "
        "Make sure dataset_raw.csv or dataset_raw (1).csv is in that folder."
    )

# 1. Load data
df = pd.read_csv(raw_file)
print("Before cleaning:", df.shape)

# 2. Remove exact duplicate rows
df = df.drop_duplicates()

# 3. Fill missing numbers with the median (middle value)
df["Session_Duration_Mins"] = df["Session_Duration_Mins"].fillna(
    df["Session_Duration_Mins"].median()
)
df["User_Rating"] = df["User_Rating"].fillna(df["User_Rating"].median())

# 4. Convert Session_Date text into a real date format
df["Session_Date"] = pd.to_datetime(df["Session_Date"])

# 5. Save cleaned file (with fallback outside OneDrive if needed)
out_path = folder / "dataset_cleaned.csv"
try:
    df.to_csv(out_path, index=False)
except OSError:
    fallback_dir = Path(os.environ.get("USERPROFILE", "C:\\Users\\admin")) / "project_hcl"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    out_path = fallback_dir / "dataset_cleaned.csv"
    df.to_csv(out_path, index=False)

print("After cleaning:", df.shape)
print("Saved cleaned file to:", out_path)