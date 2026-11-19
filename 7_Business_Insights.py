import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Business Insights | InsightIQ", page_icon="💡", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Business Insights")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.business_insights import generate_insights, kpi_table
st.subheader("Key Performance Indicators")
st.dataframe(kpi_table(df), use_container_width=True, hide_index=True)
st.subheader("Automatically generated insights")
for i, insight in enumerate(generate_insights(df), start=1):
    st.markdown(f"{i}. {insight}")
st.caption("These are descriptive, data-derived insights. Validate business context before making decisions.")
