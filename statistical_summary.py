import pandas as pd
from scipy import stats

def calculate_statistics(df):
    rows = []
    for col in df.select_dtypes(include="number").columns:
        s = df[col].dropna()
        if s.empty:
            continue
        mode_values = s.mode()
        rows.append({
            "Column": col, "Count": int(s.count()), "Mean": float(s.mean()),
            "Median": float(s.median()),
            "Mode": float(mode_values.iloc[0]) if not mode_values.empty else None,
            "Std Dev": float(s.std()) if len(s) > 1 else 0.0,
            "Variance": float(s.var()) if len(s) > 1 else 0.0,
            "Minimum": float(s.min()), "Q1": float(s.quantile(.25)),
            "Q3": float(s.quantile(.75)), "Maximum": float(s.max()),
            "Skewness": float(stats.skew(s)) if len(s) > 2 else 0.0,
        })
    return pd.DataFrame(rows)
