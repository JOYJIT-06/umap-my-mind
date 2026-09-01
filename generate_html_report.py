
"""Compiles text summary and embedded figures into a single standalone HTML report."""
import os
import base64

html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Mouse Brain scRNA-seq Analysis Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; margin: 0; padding: 40px; background: #f8f9fa; color: #212529; }
        .container { max-width: 900px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        h1 { text-align: center; color: #1a252f; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 30px; }
        h2 { color: #2c3e50; margin-top: 35px; border-bottom: 1px solid #dee2e6; padding-bottom: 8px; }
        pre { background: #f1f3f5; padding: 18px; border-radius: 8px; font-family: monospace; font-size: 14px; white-space: pre-wrap; overflow-x: auto; }
        .fig-box { text-align: center; margin: 25px 0; }
        img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border: 1px solid #e9ecef; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Mouse Brain scRNA-seq Analysis Report</h1>
"""

if os.path.exists("results/analysis_summary.txt"):
    with open("results/analysis_summary.txt", "r", encoding="utf-8") as f:
        text = f.read()
    html_content += f"<h2>Analysis Summary</h2><pre>{text}</pre>\n"

figures = [
    ("figures/umap_cell_types.png", "UMAP Plot: Identified Cell Types"),
    ("figures/qc_violin_plots.png", "Quality Control Metrics"),
    ("figures/marker_genes_dotplot.png", "Marker Gene Expression"),
]

for fig_path, title in figures:
    if os.path.exists(fig_path):
        with open(fig_path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode("utf-8")
        html_content += f"<h2>{title}</h2>\n<div class='fig-box'><img src='data:image/png;base64,{b64_str}' alt='{title}'></div>\n"

html_content += """
    </div>
</body>
</html>
"""

os.makedirs("results", exist_ok=True)
with open("results/analysis_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML report successfully created: results/analysis_report.html")