import pandas as pd

def cleaning_profile(df):
    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(x) for x in df.dtypes],
        "Missing Values": [int(x) for x in df.isna().sum().values],
        "Missing %": [(float(x) / max(len(df), 1)) * 100 for x in df.isna().sum().values],
        "Unique Values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })

def clean_dataframe(df, missing_strategy="Keep unchanged", duplicate_strategy="Remove duplicates"):
    clean = df.copy()
    duplicate_count = int(clean.duplicated().sum())
    if duplicate_strategy == "Remove duplicates":
        clean = clean.drop_duplicates()
    if missing_strategy == "Drop rows with missing values":
        clean = clean.dropna()
    elif missing_strategy == "Fill numeric with median":
        for col in clean.select_dtypes(include="number").columns:
            if clean[col].isna().any():
                clean[col] = clean[col].fillna(clean[col].median())
    elif missing_strategy == "Fill with mode":
        for col in clean.columns:
            if clean[col].isna().any():
                modes = clean[col].mode(dropna=True)
                if not modes.empty:
                    clean[col] = clean[col].fillna(modes.iloc[0])
    return clean, duplicate_count
