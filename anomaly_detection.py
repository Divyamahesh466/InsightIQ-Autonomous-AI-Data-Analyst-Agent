import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

def detect_anomalies(df, contamination=0.05):
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] == 0:
        raise ValueError("Anomaly detection needs at least one numeric column.")
    if len(df) < 5:
        raise ValueError("At least 5 rows are required for anomaly detection.")
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        IsolationForest(contamination=contamination, random_state=42)
    )
    labels = model.fit_predict(numeric)
    result = df.copy()
    result["Anomaly Status"] = ["Anomaly" if x == -1 else "Normal" for x in labels]
    return result
