"""PDF certificate generation for completed tracks (Pro users).

Generates a single A4 landscape certificate with the user's name, the track name,
date, and a verification ID. No external assets required — pure reportlab vector.
"""
from __future__ import annotations
from datetime import datetime
from io import BytesIO
from typing import Tuple

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# CodeFuturo palette
CF_SPACE = HexColor("#0A0F1E")
CF_PANEL = HexColor("#111827")
CF_LIME = HexColor("#A3E635")
CF_LIME_DARK = HexColor("#84CC16")
CF_VIOLET = HexColor("#7C3AED")
CF_TEXT = HexColor("#E5E7EB")
CF_MUTED = HexColor("#94A3B8")
CF_BORDER = HexColor("#1F2937")


def _safe_text(s: str) -> str:
    return (s or "").strip() or "—"


def render_certificate(
    *,
    student_name: str,
    track_name: str,
    completed_at: datetime,
    cert_id: str,
    total_lessons: int,
    xp_earned: int,
) -> bytes:
    """Return raw PDF bytes for the certificate."""
    buf = BytesIO()
    page_w, page_h = landscape(A4)
    c = canvas.Canvas(buf, pagesize=(page_w, page_h))

    # --- Background ---
    c.setFillColor(CF_SPACE)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Subtle decorative grid (very faint)
    c.setStrokeColor(Color(1, 1, 1, alpha=0.03))
    c.setLineWidth(0.4)
    step = 24
    y = 0
    while y < page_h:
        c.line(0, y, page_w, y)
        y += step
    x = 0
    while x < page_w:
        c.line(x, 0, x, page_h)
        x += step

    # Outer lime border frame
    margin = 28
    c.setStrokeColor(CF_LIME)
    c.setLineWidth(2)
    c.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin, fill=0, stroke=1)
    # Inner thin border
    c.setStrokeColor(CF_BORDER)
    c.setLineWidth(0.6)
    c.rect(margin + 8, margin + 8, page_w - 2 * (margin + 8), page_h - 2 * (margin + 8), fill=0, stroke=1)

    # Top-left brand
    c.setFillColor(CF_LIME)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin + 28, page_h - margin - 36, "</> CodeFuturo")
    c.setFillColor(CF_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(margin + 28, page_h - margin - 50, "DO ZERO AO DEPLOY")

    # Top-right small badge
    c.setFillColor(CF_LIME)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(page_w - margin - 28, page_h - margin - 36, "CERTIFICADO PRO")

    # --- Headline ---
    title_y = page_h - 180
    c.setFillColor(CF_TEXT)
    c.setFont("Helvetica", 13)
    c.drawCentredString(page_w / 2, title_y + 70, "Certificado de Conclusão")

    c.setFillColor(CF_LIME)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(page_w / 2, title_y + 20, _safe_text(track_name))

    # Decorative underline
    c.setStrokeColor(CF_LIME)
    c.setLineWidth(2.5)
    c.line(page_w / 2 - 90, title_y + 8, page_w / 2 + 90, title_y + 8)

    # Body
    c.setFillColor(CF_TEXT)
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w / 2, title_y - 30, "Conferido a")

    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(page_w / 2, title_y - 70, _safe_text(student_name))

    c.setFillColor(CF_MUTED)
    c.setFont("Helvetica", 12)
    msg = (
        f"Por concluir com êxito a trilha {_safe_text(track_name)} — "
        f"{total_lessons} lições · {xp_earned} XP conquistados."
    )
    c.drawCentredString(page_w / 2, title_y - 100, msg)

    # --- Footer area: date + cert id + signature line ---
    footer_y = margin + 70

    # Left block: date
    c.setFillColor(CF_TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 60, footer_y + 18, "Data de conclusão")
    c.setFillColor(CF_MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(margin + 60, footer_y + 4, completed_at.strftime("%d/%m/%Y"))
    c.setStrokeColor(CF_BORDER)
    c.line(margin + 60, footer_y - 6, margin + 220, footer_y - 6)

    # Center block: signature line
    c.setStrokeColor(CF_LIME)
    c.setLineWidth(1.2)
    sig_w = 260
    sig_x = (page_w - sig_w) / 2
    c.line(sig_x, footer_y - 6, sig_x + sig_w, footer_y - 6)
    c.setFillColor(CF_TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w / 2, footer_y + 18, "Equipe CodeFuturo")
    c.setFillColor(CF_MUTED)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(page_w / 2, footer_y + 4, "Assinatura digital")

    # Right block: certificate id
    c.setFillColor(CF_TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(page_w - margin - 60, footer_y + 18, "ID do certificado")
    c.setFillColor(CF_MUTED)
    c.setFont("Courier", 9)
    c.drawRightString(page_w - margin - 60, footer_y + 4, cert_id)
    c.setStrokeColor(CF_BORDER)
    c.line(page_w - margin - 220, footer_y - 6, page_w - margin - 60, footer_y - 6)

    # Verify hint
    c.setFillColor(CF_MUTED)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w / 2, margin + 20, f"Verifique a autenticidade em /verificar/{cert_id}")

    c.showPage()
    c.save()
    return buf.getvalue()


def cert_filename(track_slug: str, student_name: str) -> str:
    safe = "".join(ch if ch.isalnum() else "-" for ch in (student_name or "aluno").lower())[:40]
    return f"codefuturo-{track_slug}-{safe}.pdf"
