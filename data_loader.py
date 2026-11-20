from io import BytesIO
import json
import pandas as pd

SUPPORTED = (".csv", ".xlsx", ".xls", ".json")

def load_dataframe(uploaded_file):
    """Read CSV, Excel or JSON uploads safely into a DataFrame."""
    if uploaded_file is None:
        raise ValueError("Please upload a data file first.")
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()
    if not raw:
        raise ValueError("The uploaded file is empty.")
    try:
        if name.endswith(".csv"):
            try:
                df = pd.read_csv(BytesIO(raw))
            except UnicodeDecodeError:
                df = pd.read_csv(BytesIO(raw), encoding="latin-1")
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(raw))
        elif name.endswith(".json"):
            obj = json.loads(raw.decode("utf-8-sig"))
            if isinstance(obj, dict):
                if "data" in obj and isinstance(obj["data"], list):
                    obj = obj["data"]
                else:
                    obj = [obj]
            df = pd.json_normalize(obj)
        else:
            raise ValueError("Unsupported file type. Upload CSV, XLSX, XLS or JSON.")
    except Exception as exc:
        raise ValueError(f"Could not read this file: {exc}") from exc

    if df.empty:
        raise ValueError("The file has no rows to analyse.")
    df.columns = [str(c).strip() for c in df.columns]
    if df.columns.duplicated().any():
        df.columns = [f"{c}_{i}" if list(df.columns).count(c) > 1 else c
                      for i, c in enumerate(df.columns)]
    return df
