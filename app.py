from pathlib import Path
import streamlit as st
from modules.data_loader import load_dataframe

st.set_page_config(page_title="InsightIQ | AI Data Analyst", page_icon="📊", layout="wide")
css = Path(__file__).parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.session_state.df = None
if "source_name" not in st.session_state:
    st.session_state.source_name = None

st.sidebar.title("InsightIQ")
st.sidebar.caption("Autonomous AI Data Analyst Agent")
st.sidebar.page_link("app.py", label="Dashboard", icon="🏠")
st.sidebar.page_link("pages/1_Data_Cleaning.py", label="Data Cleaning", icon="🧹")
st.sidebar.page_link("pages/2_Exploratory_Analysis.py", label="Exploratory Analysis", icon="🔎")
st.sidebar.page_link("pages/3_Predictive_Modeling.py", label="Predictive Modeling", icon="🤖")
st.sidebar.page_link("pages/4_Generate_Charts.py", label="Generate Charts", icon="📈")
st.sidebar.page_link("pages/5_Statistical_Summary.py", label="Statistical Summary", icon="📊")
st.sidebar.page_link("pages/6_Anomaly_Detection.py", label="Anomaly Detection", icon="🚨")
st.sidebar.page_link("pages/7_Business_Insights.py", label="Business Insights", icon="💡")
st.sidebar.page_link("pages/8_Reports.py", label="Reports", icon="📄")
st.sidebar.page_link("pages/9_Settings.py", label="Settings", icon="⚙️")

st.title("InsightIQ – Autonomous AI Data Analyst Agent")
st.write("Upload your dataset and choose an analysis task. Each task opens on its own page.")

st.markdown("### Upload your data")
uploaded = st.file_uploader("Choose CSV, Excel or JSON file", type=["csv", "xlsx", "xls", "json"])
if uploaded is not None:
    try:
        df = load_dataframe(uploaded)
        st.session_state.df = df
        st.session_state.source_name = uploaded.name
        st.success(f"Successfully loaded {uploaded.name}")
    except Exception as e:
        st.error(str(e))

df = st.session_state.df
if df is not None:
    st.markdown("### Dataset overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{len(df.columns):,}")
    c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
    c4.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")
    st.caption(f"Current dataset: {st.session_state.source_name}")
    st.dataframe(df.head(10), use_container_width=True)
else:
    st.info("Upload a file to activate the analysis pages.")

tasks = [
    ("Data Cleaning", "pages/1_Data_Cleaning.py", "🧹"),
    ("Exploratory Analysis", "pages/2_Exploratory_Analysis.py", "🔎"),
    ("Predictive Modeling", "pages/3_Predictive_Modeling.py", "🤖"),
    ("Generate Charts", "pages/4_Generate_Charts.py", "📈"),
    ("Statistical Summary", "pages/5_Statistical_Summary.py", "📊"),
    ("Anomaly Detection", "pages/6_Anomaly_Detection.py", "🚨"),
    ("Business Insights", "pages/7_Business_Insights.py", "💡"),
    ("Reports", "pages/8_Reports.py", "📄"),
]


st.markdown("### Choose a Task")
for i in range(0, len(tasks), 3):
    cols = st.columns(3, gap="medium")

    for j in range(3):
        if i + j < len(tasks):
            label, page, icon = tasks[i + j]

            with cols[j]:
                st.page_link(
                    page,
                    label=f"{icon}  {label}",
                    use_container_width=False
                )
