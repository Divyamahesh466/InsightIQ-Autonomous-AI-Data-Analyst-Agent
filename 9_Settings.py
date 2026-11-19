import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Settings | InsightIQ", page_icon="⚙️", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Settings")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

st.subheader("Application settings")
st.write("Current dataset:", st.session_state.get("source_name", "Uploaded dataset"))
st.write("Rows:", len(df))
st.write("Columns:", len(df.columns))
st.checkbox("Show dataset preview by default", value=True, key="show_preview_setting")
st.selectbox("Default chart theme", ["plotly", "plotly_white", "ggplot2", "simple_white"], key="chart_theme_setting")
if st.button("Clear uploaded dataset"):
    for key in ["df", "source_name", "cleaned_df", "trained_model", "model_target"]:
        st.session_state.pop(key, None)
    st.success("Dataset cleared. Return to Dashboard to upload another file.")
