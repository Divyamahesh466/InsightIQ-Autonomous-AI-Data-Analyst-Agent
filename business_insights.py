import pandas as pd

def generate_insights(df):
    insights = []
    insights.append(f"The dataset contains {len(df):,} rows and {len(df.columns):,} columns.")
    missing = int(df.isna().sum().sum())
    if missing:
        insights.append(f"There are {missing:,} missing cells. Review them before building a model.")
    else:
        insights.append("No missing cells were detected.")
    dup = int(df.duplicated().sum())
    insights.append(f"{dup:,} duplicate rows were found.")
    for col in df.select_dtypes(include="number").columns[:8]:
        s = df[col].dropna()
        if not s.empty:
            insights.append(f"{col}: average {s.mean():,.2f}; minimum {s.min():,.2f}; maximum {s.max():,.2f}.")
    for col in df.select_dtypes(exclude="number").columns[:5]:
        counts = df[col].astype("string").fillna("(Missing)").value_counts()
        if not counts.empty:
            insights.append(f"{col}: most frequent category is '{counts.index[0]}' ({int(counts.iloc[0])} records).")
    return insights

def kpi_table(df):
    rows = [
        {"Metric": "Total Records", "Value": f"{len(df):,}"},
        {"Metric": "Total Columns", "Value": f"{len(df.columns):,}"},
        {"Metric": "Missing Cells", "Value": f"{int(df.isna().sum().sum()):,}"},
        {"Metric": "Duplicate Rows", "Value": f"{int(df.duplicated().sum()):,}"},
    ]
    return pd.DataFrame(rows)
