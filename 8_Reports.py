import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Reports | InsightIQ", page_icon="📄", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Reports")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.business_insights import generate_insights
from modules.report_generator import create_pdf_report
st.write("Create a PDF report containing dataset size, automatically generated insights and a small data preview.")
if st.button("Generate PDF Report", type="primary"):
    try:
        pdf = create_pdf_report(df, generate_insights(df))
        st.success("PDF report generated.")
        st.download_button("Download InsightIQ PDF Report", pdf, "InsightIQ_Report.pdf", "application/pdf")
    except Exception as e:
        st.error(f"Report generation failed: {e}")
st.download_button("Download current dataset as CSV", df.to_csv(index=False).encode("utf-8-sig"),
                   "insightiq_dataset.csv", "text/csv")
