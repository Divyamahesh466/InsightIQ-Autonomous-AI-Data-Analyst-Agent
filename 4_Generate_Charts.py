import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Generate Charts | InsightIQ", page_icon="📈", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Generate Charts")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.chart_generator import make_chart
numeric_cols = df.select_dtypes(include="number").columns.tolist()
all_cols = df.columns.tolist()
chart = st.selectbox("Chart type", ["Bar Chart", "Line Chart", "Pie Chart", "Histogram", "Scatter Plot", "Box Plot"])
x = st.selectbox("X / Category column", all_cols)
y_options = numeric_cols if numeric_cols else all_cols
y = st.selectbox("Y / Numeric column", y_options) if chart in ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot"] else None
color = st.selectbox("Color grouping (optional)", ["None"] + all_cols)
if st.button("Generate Chart", type="primary"):
    try:
        fig = make_chart(df, chart, x, y, None if color == "None" else color)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(str(e))
