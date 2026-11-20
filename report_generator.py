from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def create_pdf_report(df, insights):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=35, leftMargin=35)
    styles = getSampleStyleSheet()
    story = [Paragraph("InsightIQ - Data Analysis Report", styles["Title"]), Spacer(1, 14)]
    story.append(Paragraph(f"Dataset size: {len(df)} rows × {len(df.columns)} columns", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Business Insights", styles["Heading2"]))
    for item in insights:
        story.append(Paragraph("• " + str(item), styles["BodyText"]))
        story.append(Spacer(1, 5))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Data Preview", styles["Heading2"]))
    preview = df.head(12).fillna("").astype(str)
    data = [list(map(str, preview.columns))] + preview.values.tolist()
    data = [row[:6] for row in data]
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#8f1730")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
