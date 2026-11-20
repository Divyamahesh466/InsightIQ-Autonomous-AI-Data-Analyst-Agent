import pandas as pd

def dataset_overview(df):
    return {
        "Rows": int(df.shape[0]),
        "Columns": int(df.shape[1]),
        "Duplicate rows": int(df.duplicated().sum()),
        "Missing cells": int(df.isna().sum().sum()),
        "Numeric columns": int(len(df.select_dtypes(include="number").columns)),
        "Categorical columns": int(len(df.select_dtypes(exclude="number").columns)),
    }

def numeric_summary(df):
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return pd.DataFrame()
    return numeric.describe().T.reset_index(names="Column")

def categorical_summary(df, max_categories=15):
    rows = []
    for col in df.select_dtypes(exclude="number").columns:
        counts = df[col].astype("string").fillna("(Missing)").value_counts().head(max_categories)
        for value, count in counts.items():
            rows.append({"Column": col, "Value": str(value), "Count": int(count)})
    return pd.DataFrame(rows)
