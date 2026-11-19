import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Predictive Modeling | InsightIQ", page_icon="🤖", layout="wide")
css = Path(__file__).resolve().parents[1] / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.sidebar.title("InsightIQ")
st.sidebar.page_link("app.py", label="← Dashboard")
df = st.session_state.get("df")
st.title("Predictive Modeling")
st.caption("Upload a dataset from the Dashboard. Your uploaded dataset is shared across all analysis pages.")
if df is None:
    st.warning("No dataset found. Go to Dashboard and upload a CSV, Excel or JSON file.")
    st.page_link("app.py", label="Go to Dashboard", icon="🏠")
    st.stop()

from modules.predictive_modeling import train_model
st.write("Train a Random Forest model using one selected target column. Auto mode chooses classification or regression based on the target.")
target = st.selectbox("Select target column", list(df.columns))
task = st.selectbox("Model type", ["Auto", "Classification", "Regression"])
test = st.slider("Test data proportion", 0.1, 0.4, 0.2, 0.05)
if st.button("Train Predictive Model", type="primary"):
    try:
        with st.spinner("Training model..."):
            model, metrics, preview = train_model(df, target, task, test)
        st.session_state.trained_model = model
        st.session_state.model_target = target
        st.success("Model training completed.")
        st.json(metrics)
        st.subheader("Actual vs Predicted")
        st.dataframe(preview, use_container_width=True)
        st.download_button("Download predictions", preview.to_csv(index=False).encode("utf-8-sig"),
                           "insightiq_predictions.csv", "text/csv")
    except Exception as e:
        st.error(str(e))
