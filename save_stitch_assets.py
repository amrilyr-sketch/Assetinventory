import os
import json
import urllib.request

OUT_DIR = r"d:\RAG\stitch_ui"
os.makedirs(OUT_DIR, exist_ok=True)

STEP193 = r"C:\Users\amril.rahman\.gemini\antigravity\brain\afa31032-7028-4dc7-969d-335a09744e32\.system_generated\steps\193\output.txt"
STEP197 = r"C:\Users\amril.rahman\.gemini\antigravity\brain\afa31032-7028-4dc7-969d-335a09744e32\.system_generated\steps\197\output.txt"

# 1. Simpan HTML Screen 1
with open(STEP193, "r", encoding="utf-8") as f:
    data1 = json.load(f)
    with open(os.path.join(OUT_DIR, "dashboard_asset_management.html"), "w", encoding="utf-8") as out:
        out.write(data1["html"])
print("Saved dashboard_asset_management.html")

# 2. Simpan HTML Screen 2
with open(STEP197, "r", encoding="utf-8") as f:
    data2 = json.load(f)
    with open(os.path.join(OUT_DIR, "detail_bast_signature.html"), "w", encoding="utf-8") as out:
        out.write(data2["html"])
print("Saved detail_bast_signature.html")

# 3. Download Screenshots
API_KEY = os.environ.get("STITCH_API_KEY", "")
headers = {"X-Goog-Api-Key": API_KEY}

SCREENSHOTS = [
    ("https://stitch.googleapis.com/v1/projects/14742868609960797249/files/8148937167581011279:download", "screen1_dashboard.jpg"),
    ("https://stitch.googleapis.com/v1/projects/14742868609960797249/files/screenshot_00065eddc63c1bc1022d654bc124f3e2:download", "screen2_detail_bast.png")
]

for url, filename in SCREENSHOTS:
    dest = os.path.join(OUT_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            # Cek jika response adalah json wrapper atau binary
            try:
                j = json.loads(content.decode("utf-8"))
                import base64
                if "image" in j:
                    content = base64.b64decode(j["image"])
                elif "data" in j:
                    content = base64.b64decode(j["data"])
            except Exception:
                pass
            with open(dest, "wb") as f_out:
                f_out.write(content)
        print(f"Berhasil mengunduh {filename} ({len(content)} bytes)")
    except Exception as e:
        print(f"Gagal mengunduh {filename}: {e}")

