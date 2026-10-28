import time
import unicodedata
from rag_chatbot import ask_asset_bot, collection

# Definisi Skenario Pengujian
TEST_CASES = [
    {
        "id": "TC-01",
        "category": "Ketepatan Data (Serial Number Exact Match)",
        "query": "Siapa pemegang aset dengan nomor seri APP-MBP-2023-882 dan kapan tanggal mutasinya?",
        "expected_doc": "bast_002.txt",
        "expected_keywords": ["Ahmad Fauzi", "10 Maret 2024", "bast_002.txt"]
    },
    {
        "id": "TC-02",
        "category": "Pencarian Semantik (Lokasi & Perangkat)",
        "query": "Aset apa yang dimutasi ke kantor cabang Surabaya dan siapa penerimanya?",
        "expected_doc": "bast_003.txt",
        "expected_keywords": ["Dell", "Siti Rahma", "Surabaya", "bast_003.txt"]
    },
    {
        "id": "TC-03",
        "category": "Ketepatan Relasi (Pihak Penyerah & Penerima)",
        "query": "Laptop Lenovo ThinkPad dipindahkan dari siapa ke siapa?",
        "expected_doc": "bast_001.txt",
        "expected_keywords": ["Budi Santoso", "Rina Wijaya", "bast_001.txt"]
    },
    {
        "id": "TC-04",
        "category": "Uji Halusinasi / Negative Test (Data Tidak Ada)",
        "query": "Siapa pemegang printer Epson L3210 di ruang rapat?",
        "expected_doc": None,
        "expected_keywords": ["tidak ditemukan", "tidak tercantum", "tidak ada"]
    }
]

def run_test_suite():
    print("=" * 70)
    print(" MENJALANKAN ULANG PENGUJIAN SISTEM RAG (Kandidat Top-3 / n_results=3)")
    print("=" * 70)

    report_lines = []
    report_lines.append("# Laporan Hasil Pengujian Sistem RAG Inventory Aset IT\n")
    report_lines.append(f"**Tanggal Pengujian:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("**Konfigurasi Retrieval:** `n_results = 3` (Multi-candidate context)\n")
    report_lines.append("| ID | Kategori | Pertanyaan | Dokumen Sumber Terpilih | Status |")
    report_lines.append("|---|---|---|---|---|")

    detailed_records = []

    for tc in TEST_CASES:
        print(f"\n[Menjalankan {tc['id']}] {tc['category']}...")
        print(f"Pertanyaan: '{tc['query']}'")

        start_time = time.time()
        ai_response = ask_asset_bot(tc["query"], n_results=3)
        elapsed = time.time() - start_time

        norm_resp = unicodedata.normalize("NFKD", ai_response).lower()

        # Evaluasi kecocokan kata kunci
        all_matched = all(kw.lower() in norm_resp for kw in tc["expected_keywords"])
        any_matched = any(kw.lower() in norm_resp for kw in tc["expected_keywords"])

        if tc["id"] == "TC-04":
            status = "PASSED" if any_matched else "FAILED"
            detected_source = "N/A (Data Tidak Ditemukan)"
        else:
            status = "PASSED" if all_matched else "FAILED"
            detected_source = tc["expected_doc"] if tc["expected_doc"] in norm_resp else "N/A"

        print(f"-> Status: {status} (Durasi: {elapsed:.2f}s, Sumber: {detected_source})")

        report_lines.append(f"| {tc['id']} | {tc['category']} | {tc['query']} | `{detected_source}` | **{status}** |")

        detailed_records.append(f"""
### {tc['id']} - {tc['category']}
* **Pertanyaan:** {tc['query']}
* **Dokumen Sumber Teridentifikasi:** `{detected_source}`
* **Waktu Respons:** {elapsed:.2f} detik
* **Status Evaluasi:** **{status}**

**Jawaban AI:**
> {ai_response.replace(chr(10), chr(10) + '> ')}

---
""")

    full_report = "\n".join(report_lines) + "\n\n## Rincian Rekaman Uji Coba\n" + "\n".join(detailed_records)

    with open("test_report.md", "w", encoding="utf-8") as f:
        f.write(full_report)

    print("\n" + "=" * 70)
    print(" PENGUJIAN SELESAI. Hasil rekaman telah diperbarui di 'test_report.md'.")
    print("=" * 70)

if __name__ == "__main__":
    run_test_suite()
