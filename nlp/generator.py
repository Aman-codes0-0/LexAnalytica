"""
Module for generating PDF and DOCX versions of legal analysis results.
"""

import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Font Registration (Unicode Support for Hindi) ──────────────────────────────

def _register_unicode_fonts():
    """
    Search for and register Unicode fonts that support Devanagari script.
    Checks common Linux paths for Noto Sans, Lohit, or FreeSerif.
    """
    possible_fonts = [
        ("/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf", "NotoSans"),
        ("/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Regular.ttf", "NotoSerif"),
        ("/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf", "Lohit"),
        ("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", "FreeSerif"),
        # Fallbacks for other distributions
        ("/usr/share/fonts/noto/NotoSansDevanagari-Regular.ttf", "NotoSans"),
    ]
    
    for path, name in possible_fonts:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                print(f"[INFO] Registered Unicode font: {name} from {path}")
                return name
            except Exception as e:
                print(f"[WARNING] Failed to register font {name}: {e}")
    
    return "Helvetica" # Absolute fallback

FONT_NAME = _register_unicode_fonts()

def generate_pdf(data: dict) -> io.BytesIO:
    """Generate a professional PDF report from analysis results."""
    lang = "hi" if data.get("output_language") == "Hindi" else "en"
    # Use Unicode font for Hindi, standard or Unicode for English
    active_font = FONT_NAME if lang == "hi" or FONT_NAME != "Helvetica" else "Helvetica"
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    # Adjust leading and spacing for Hindi (Devanagari matras need more height)
    base_leading = 14 if lang == "en" else 18
    base_fontSize = 10 if lang == "en" else 11

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName=active_font,
        fontSize=22,
        leading=28,
        spaceAfter=12,
        textColor=colors.HexColor("#6366f1")
    )
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontName=active_font,
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#1e293b")
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName=active_font,
        fontSize=base_fontSize,
        leading=base_leading
    )
    
    elements = []
    
    # 1. Header
    elements.append(Paragraph("LexAnalytica Analysis Report", title_style))
    elements.append(Paragraph(f"Document: {data.get('filename', 'Unknown')}", body_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    elements.append(Paragraph(f"Output Language: {data.get('output_language', 'English')}", body_style))
    elements.append(Spacer(1, 24))
    
    # 2. Executive Summary
    summary = data.get("summary", {})
    if summary.get("extractive") or summary.get("abstractive"):
        elements.append(Paragraph("Executive Summary", section_style))
        if summary.get("abstractive"):
            elements.append(Paragraph("<b>AI Synthesis:</b>", body_style))
            elements.append(Paragraph(summary["abstractive"], body_style))
            elements.append(Spacer(1, 12))
        if summary.get("extractive"):
            elements.append(Paragraph("<b>Key Findings (Extractive):</b>", body_style))
            elements.append(Paragraph(summary["extractive"], body_style))
        elements.append(Spacer(1, 12))
    
    # 3. Entities
    entities = data.get("entities", {})
    if any(entities.values()):
        elements.append(Paragraph("Identified Legal Entities", section_style))
        
        entity_data = [["Type", "Extraction"]]
        for key, label in [
            ("persons", "Persons"),
            ("organizations", "Organizations"),
            ("dates", "Dates"),
            ("locations", "Locations"),
            ("case_numbers", "Case Numbers"),
            ("law_sections", "Law Sections")
        ]:
            items = entities.get(key, [])
            if items:
                entity_data.append([label, ", ".join(items)])
        
        if len(entity_data) > 1:
            t = Table(entity_data, colWidths=[100, 350])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#475569")),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), active_font), # Use active_font for whole table
                ('FONTNAME', (0, 0), (-1, 0), f"{active_font}-Bold" if active_font == "Helvetica" else active_font),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0"))
            ]))
            elements.append(t)
        elements.append(Spacer(1, 12))
        
    # 4. Metrics
    elements.append(Paragraph("Document Metrics", section_style))
    metrics = [
        ["Metric", "Value"],
        ["Word Count", str(data.get("word_count", 0))],
        ["Sentence Count", str(data.get("sentence_count", 0))],
        ["Character Length", str(data.get("text_length", 0))]
    ]
    t_metrics = Table(metrics, colWidths=[150, 100])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('FONTNAME', (0, 0), (-1, -1), active_font),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(t_metrics)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
