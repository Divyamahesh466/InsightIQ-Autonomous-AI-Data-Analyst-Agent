import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Exploratory Data Analysis | InsightIQ", page_icon="🔎", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Exploratory Data Analysis")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.exploratory_analysis import dataset_overview, numeric_summary, categorical_summary
st.subheader("Dataset overview")
overview = dataset_overview(df)
cols = st.columns(3)
for i, (key, value) in enumerate(overview.items()):
    cols[i % 3].metric(key, f"{value:,}")
st.subheader("Numeric summary")
num = numeric_summary(df)
if num.empty:
    st.info("No numeric columns found.")
else:
    st.dataframe(num, use_container_width=True)
st.subheader("Categorical frequency")
cat = categorical_summary(df)
if cat.empty:
    st.info("No categorical columns found.")
else:
    st.dataframe(cat, use_container_width=True)
