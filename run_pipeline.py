"""One-click runner: executes all 7 pipeline steps + auto-zip."""
import sys
import subprocess

STEPS = [
    ("download_data.py", "Downloading data..."),
    ("preprocess.py", "Preprocessing & QC..."),
    ("cluster.py", "Clustering & annotating..."),
    ("visualize.py", "Generating figures..."),
    ("report.py", "Writing text report..."),
    ("generate_narrative_report.py", "Writing plain-English guide..."),
    ("generate_html_report.py", "Generating HTML report..."),
    ("convert_html_to_pdf.py", "Converting HTML report to PDF..."),
]
print("=" * 50)
print("MOUSE BRAIN scRNA-seq PIPELINE")
print("=" * 50)

for script, desc in STEPS:
    print(f"\n>>> {desc}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\n!!! ERROR in {script}. Stopping pipeline.")
        sys.exit(1)

print("\n>>> Zipping all outputs...")
subprocess.run([sys.executable, "zip_outputs.py"])

print("\n" + "=" * 50)
print("ALL DONE!")
print("=" * 50)