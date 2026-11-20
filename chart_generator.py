import pandas as pd
import plotly.express as px

def make_chart(df, chart_type, x_col=None, y_col=None, color_col=None):
    if chart_type == "Histogram":
        col = x_col or df.columns[0]
        return px.histogram(df, x=col, color=color_col, title=f"Distribution of {col}")
    if chart_type == "Box Plot":
        col = y_col or x_col or df.columns[0]
        return px.box(df, y=col, x=color_col, title=f"Box plot of {col}")
    if chart_type == "Pie Chart":
        col = x_col or df.columns[0]
        counts = df[col].astype("string").fillna("(Missing)").value_counts().head(20).reset_index()
        counts.columns = ["Category", "Count"]
        return px.pie(counts, names="Category", values="Count", title=f"{col} composition")
    if chart_type == "Scatter Plot":
        if not y_col:
            raise ValueError("Choose both X and Y columns for a scatter plot.")
        return px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
    if chart_type == "Line Chart":
        if not y_col:
            raise ValueError("Choose a Y column for a line chart.")
        return px.line(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} by {x_col}")
    if chart_type == "Bar Chart":
        if y_col and pd.api.types.is_numeric_dtype(df[y_col]):
            grouped = df.groupby(x_col, dropna=False)[y_col].mean().reset_index()
            return px.bar(grouped, x=x_col, y=y_col, color=color_col, title=f"Average {y_col} by {x_col}")
        counts = df[x_col].astype("string").fillna("(Missing)").value_counts().head(30).reset_index()
        counts.columns = [x_col, "Count"]
        return px.bar(counts, x=x_col, y="Count", title=f"Count by {x_col}")
    raise ValueError("Unsupported chart type.")
