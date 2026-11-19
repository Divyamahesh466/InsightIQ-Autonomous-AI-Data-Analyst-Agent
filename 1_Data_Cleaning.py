import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Data Cleaning | InsightIQ", page_icon="🧹", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Data Cleaning")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.data_cleaning import cleaning_profile, clean_dataframe
st.subheader("Data quality profile")
st.dataframe(cleaning_profile(df), use_container_width=True)
st.subheader("Cleaning options")
missing = st.selectbox("Missing value strategy", [
    "Keep unchanged", "Drop rows with missing values", "Fill numeric with median", "Fill with mode"
])
duplicates = st.selectbox("Duplicate strategy", ["Remove duplicates", "Keep duplicates"])
if st.button("Run Data Cleaning", type="primary"):
    cleaned, duplicate_count = clean_dataframe(df, missing, duplicates)
    st.session_state.cleaned_df = cleaned
    st.success(f"Cleaning completed. Duplicate rows detected before cleaning: {duplicate_count}.")
    st.write(f"Original shape: {df.shape} | Cleaned shape: {cleaned.shape}")
    st.dataframe(cleaned.head(30), use_container_width=True)
    st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode("utf-8-sig"),
                       "insightiq_cleaned_data.csv", "text/csv")
