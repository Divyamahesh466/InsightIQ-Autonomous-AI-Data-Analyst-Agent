import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Statistical Summary | InsightIQ", page_icon="📊", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Statistical Summary")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.statistical_summary import calculate_statistics
result = calculate_statistics(df)
if result.empty:
    st.warning("No numeric columns are available for statistical calculations.")
else:
    st.dataframe(result, use_container_width=True)
    st.download_button("Download statistical summary", result.to_csv(index=False).encode("utf-8-sig"),
                       "insightiq_statistical_summary.csv", "text/csv")
