"""
PDF Assessment Report Generation Service using ReportLab
"""
import io
import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

class ReportService:
    @staticmethod
    def generate_assessment_pdf(result: Dict[str, Any], user_name: str) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1e293b"),
            alignment=1, # Center
            spaceAfter=15
        )

        sub_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#64748b"),
            alignment=1,
            spaceAfter=20
        )

        heading2 = ParagraphStyle(
            "DocH2",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#0f766e"),
            spaceBefore=15,
            spaceAfter=8
        )

        body_style = ParagraphStyle(
            "DocBody",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155")
        )

        disclaimer_style = ParagraphStyle(
            "DocDisclaimer",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#b91c1c"),
            alignment=1,
            spaceBefore=15
        )

        elements = []

        elements.append(Paragraph("MENTAL HEALTH SCREENING REPORT", title_style))
        elements.append(Paragraph("MindCare Assessment & Well-being Support Engine", sub_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=15))

        # Metadata Table
        data = [
            [Paragraph("<b>User Name:</b>", body_style), Paragraph(user_name, body_style)],
            [Paragraph("<b>Assessment:</b>", body_style), Paragraph(result.get("assessment_name", "Screening"), body_style)],
            [Paragraph("<b>Date:</b>", body_style), Paragraph(result.get("created_at", "")[:10], body_style)],
            [Paragraph("<b>Score:</b>", body_style), Paragraph(f"{result.get('score')} / {result.get('max_score')}", body_style)],
            [Paragraph("<b>Screening Interpretation:</b>", body_style), Paragraph(f"<b>{result.get('severity_level')}</b>", body_style)]
        ]

        if result.get("previous_score") is not None:
            data.append([
                Paragraph("<b>Previous Score:</b>", body_style),
                Paragraph(str(result.get("previous_score")), body_style)
            ])

        t = Table(data, colWidths=[160, 350])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 15))

        # What this means
        elements.append(Paragraph("Screening Summary", heading2))
        elements.append(Paragraph(result.get("interpretation", ""), body_style))
        elements.append(Spacer(1, 10))

        if result.get("trend_summary"):
            elements.append(Paragraph("Score Trend", heading2))
            elements.append(Paragraph(result.get("trend_summary"), body_style))
            elements.append(Spacer(1, 10))

        # Suggested Next Steps
        elements.append(Paragraph("Suggested Next Steps", heading2))
        steps = result.get("suggested_next_steps", [])
        for step in steps:
            elements.append(Paragraph(f"• {step}", body_style))
            elements.append(Spacer(1, 4))

        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=10, spaceAfter=15))

        # Mandatory Disclaimer
        elements.append(Paragraph("<b>IMPORTANT NOTICE</b>", disclaimer_style))
        elements.append(Paragraph(
            "This report is generated for mental health screening and well-being support purposes only. "
            "It does NOT constitute a medical diagnosis, clinical evaluation, or treatment plan, and does NOT replace care from a qualified healthcare professional.",
            disclaimer_style
        ))

        doc.build(elements)
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
