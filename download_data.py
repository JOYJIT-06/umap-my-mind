
import os
import urllib.request
from common import load_config, ensure_dirs

cfg = load_config()
ensure_dirs(cfg)

url = cfg["data"]["primary_url"]
dest = cfg["data"]["raw_h5"]

if not os.path.exists(dest):
    print(f"Downloading dataset to {dest}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        f.write(resp.read())
    print("Download complete.")
else:
    print("Data file already exists.")