"""Converts the generated HTML report directly into a clean PDF document."""
import os
from xhtml2pdf import pisa

html_path = "results/analysis_report.html"
pdf_path = "results/analysis_report.pdf"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

    if not pisa_status.err:
        print(f"PDF successfully converted: {pdf_path}")
    else:
        print("Error converting HTML to PDF.")
else:
    print(f"File not found: {html_path}")