import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Anomaly Detection | InsightIQ", page_icon="🚨", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Anomaly Detection")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.anomaly_detection import detect_anomalies
contamination = st.slider("Expected anomaly proportion", 0.01, 0.20, 0.05, 0.01)
if st.button("Detect Anomalies", type="primary"):
    try:
        result = detect_anomalies(df, contamination)
        anomalies = result[result["Anomaly Status"] == "Anomaly"]
        normal = len(result) - len(anomalies)
        a, b = st.columns(2)
        a.metric("Normal records", f"{normal:,}")
        b.metric("Anomalies", f"{len(anomalies):,}")
        st.dataframe(result, use_container_width=True)
        st.download_button("Download anomaly results", result.to_csv(index=False).encode("utf-8-sig"),
                           "insightiq_anomaly_results.csv", "text/csv")
    except Exception as e:
        st.error(str(e))
