# InsightIQ – Autonomous AI Data Analyst Agent

A multi-page Python + Streamlit data analysis application.

## Features
- CSV, Excel and JSON upload
- Data cleaning and downloadable cleaned CSV
- Exploratory data analysis
- Random Forest classification and regression
- Interactive Plotly charts
- Statistical summaries
- Isolation Forest anomaly detection
- Automatically generated descriptive business insights
- Downloadable PDF report

## Requirements
- Python 3.10 or later
- VS Code

## Setup on Windows

1. Extract the ZIP file.
2. Open the `InsightIQ` folder in VS Code.
3. Open Terminal -> New Terminal.
4. Create a virtual environment:

   ```powershell
   py -3.10 -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

6. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

7. Run the application from the project root folder:

   ```powershell
   python -m streamlit run app.py
   ```

8. Open the Local URL printed in the terminal, usually http://localhost:8501.

## Important
- Always run Streamlit from the folder containing `app.py` and `requirements.txt`.
- Upload the dataset on the Dashboard first. Then open any task page.
- Predictive modeling requires a target column and enough usable rows.
- Anomaly detection requires numeric columns and at least five rows.
- This project uses machine learning and statistical methods; it is not an LLM-powered agent and does not make causal claims.
