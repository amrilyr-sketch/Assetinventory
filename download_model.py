import os
import sys
import hashlib
import tarfile
import urllib.request

URL = "https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz"
TARGET_DIR = os.path.expanduser(r"~\.cache\chroma\onnx_models\all-MiniLM-L6-v2")
TAR_PATH = os.path.join(TARGET_DIR, "onnx.tar.gz")
EXPECTED_SHA256 = "913d7300ceae3b2dbc2c50d1de4baacab4be7b9380491c27fab7418616a16ec3"

def verify_sha256(filepath):
    if not os.path.exists(filepath):
        return False
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest() == EXPECTED_SHA256

def download_with_resume():
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # Cek jika sudah utuh
    if verify_sha256(TAR_PATH):
        print("File onnx.tar.gz sudah lengkap dan terverifikasi!")
        return True

    existing_size = os.path.getsize(TAR_PATH) if os.path.exists(TAR_PATH) else 0
    headers = {"User-Agent": "Mozilla/5.0"}
    if existing_size > 0:
        headers["Range"] = f"bytes={existing_size}-"
        print(f"Melanjutkan download dari byte ke-{existing_size} ({existing_size / (1024*1024):.2f} MB)...")
    else:
        print("Memulai download onnx.tar.gz...")

    req = urllib.request.Request(URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            # Periksa apakah server mendukung Range (status 206)
            mode = "ab" if resp.status == 206 else "wb"
            if resp.status != 206 and existing_size > 0:
                print("Server tidak menerima range, download ulang dari awal...")
                existing_size = 0

            total_size = int(resp.headers.get("Content-Length", 0)) + existing_size
            downloaded = existing_size

            with open(TAR_PATH, mode) as f:
                while True:
                    chunk = resp.read(64 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size * 100) if total_size else 0
                    sys.stdout.write(f"\rDownload: {downloaded / (1024*1024):.1f}/{total_size / (1024*1024):.1f} MB ({percent:.1f}%)")
                    sys.stdout.flush()

        print("\nDownload selesai. Melakukan verifikasi SHA256...")
        if verify_sha256(TAR_PATH):
            print("Verifikasi SHA256 berhasil!")
            return True
        else:
            print("Verifikasi gagal, hash tidak cocok.")
            return False

    except Exception as e:
        print(f"\nTerjadi kesalahan saat download: {e}")
        return False

def extract_tar():
    print("Mengekstrak berkas onnx.tar.gz...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(path=TARGET_DIR)
    print("Ekstraksi selesai! Model ONNX siap digunakan oleh ChromaDB.")

if __name__ == "__main__":
    if download_with_resume():
        extract_tar()
    else:
        print("Gagal menyiapkan model ONNX.")

