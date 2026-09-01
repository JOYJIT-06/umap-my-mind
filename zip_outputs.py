import os
import zipfile
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_name = f"mouse_brain_analysis_{timestamp}.zip"

# Only zip output folders to prevent recursive loops and avoid huge raw data files
output_folders = ["figures", "results"]

with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for folder in output_folders:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for file in files:
                    if not file.startswith("."):
                        filepath = os.path.join(root, file)
                        zipf.write(filepath, arcname=filepath)

print(f"Archive created successfully: {zip_name}")