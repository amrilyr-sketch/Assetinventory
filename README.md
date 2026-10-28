# Prototipe AI Chatbot RAG - Inventory Mutasi Aset IT

Aplikasi chatbot berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk melacak dan menjawab riwayat mutasi perangkat IT (laptop, PC desktop, monitor) berdasarkan dokumen **Berita Acara Serah Terima (BAST)**.

---

## 1. Arsitektur & Alur Kerja Sistem

Aplikasi ini menggunakan pendekatan RAG 2 tahap yang ringan:

```
[Dokumen BAST (.txt)] 
        │
        ▼ (Tahap 1: Indexing)
[ChromaDB Local Vector Store] (Model: all-MiniLM-L6-v2)
        │
        ▼ (Tahap 2: Retrieval)
  Query User ──> [Top-3 Kandidat BAST]
                        │
                        ▼ (Tahap 3: Generation)
                 [Groq API (Model: openai/gpt-oss-20b)] ──> [Jawaban Faktual]
```

1. **Indexing:** Membaca dokumen teks BAST dari folder `data/`, mengubahnya menjadi vektor embedding, dan menyimpannya secara persisten di folder `chroma_db/`.
2. **Retrieval:** Saat pengguna bertanya, sistem mencocokkan kemiripan pertanyaan dengan isi BAST dan mengambil 3 dokumen kandidat teratas (*Top-3*).
3. **Generation:** Potongan BAST kandidat disuntikkan ke prompt instruksi ketat untuk model Groq AI, menghasilkan jawaban faktual tanpa halusinasi.

---

## 2. Struktur Proyek

```
d:\RAG\
├── data\                   # Sumber dokumen BAST simulasi
│   ├── bast_001.txt        # Mutasi Lenovo ThinkPad (Jakarta)
│   ├── bast_002.txt        # Mutasi MacBook Pro (Jakarta)
│   └── bast_003.txt        # Mutasi PC Dell OptiPlex (Surabaya)
├── chroma_db\              # Database vektor lokal ChromaDB
├── .env                    # Penyimpanan aman GROQ_API_KEY
├── .gitignore              # Mengabaikan file kredensial dan cache
├── index_documents.py      # Skrip untuk membaca dan mengindeks dokumen BAST
├── test_retrieval.py       # Skrip uji mandiri modul pencarian dokumen
├── rag_chatbot.py          # Aplikasi utama chatbot RAG (Terminal interaktif)
├── run_tests.py            # Skrip evaluasi & perekaman pengujian otomatis
├── test_report.md          # Rekaman hasil uji coba komprehensif
└── README.md               # Dokumentasi panduan proyek
```

---

## 3. Prasyarat & Instalasi

* **Python:** Versi 3.10 – 3.12 (Direkomendasikan Python 3.12)
* **Pustaka Pendukung:**
  ```bash
  py -3.12 -m pip install chromadb groq
  ```
* **Kredensial:** Pastikan berkas `.env` sudah memuat API key:
  ```env
  GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
  ```

---

## 4. Cara Menjalankan Aplikasi

### Langkah 1: Indexing Dokumen BAST
Jalankan proses indexing jika ada penambahan dokumen baru di folder `data/`:
```bash
py -3.12 index_documents.py
```

### Langkah 2: Menjalankan Chatbot Interaktif
Jalankan sesi tanya-jawab langsung di terminal:
```bash
py -3.12 rag_chatbot.py
```
*Ketik pertanyaan Anda, atau ketik `exit`/`keluar` untuk mengakhiri sesi.*

Anda juga bisa menjalankan satu pertanyaan langsung melalui argumen baris perintah:
```bash
py -3.12 rag_chatbot.py "Siapa pemegang laptop nomor seri APP-MBP-2023-882?"
```

### Langkah 3: Menjalankan Pengujian Otomatis
Untuk menguji akurasi dan merekam hasil pengujian:
```bash
py -3.12 run_tests.py
```
Hasil rekaman akan otomatis diperbarui di file `test_report.md`.

---

## 5. Hasil Pengujian Sistem

Berdasarkan pengujian otomatis pada 4 skenario kunci:

| ID | Kategori Uji | Skenario | Hasil | Waktu Respons |
|---|---|---|:---:|:---:|
| **TC-01** | *Exact Serial Number* | Mencari pemegang laptop `APP-MBP-2023-882` & tanggal mutasi | **PASSED** | 1.74s |
| **TC-02** | *Semantic Location* | Menanyakan mutasi aset ke cabang Surabaya | **PASSED** | 1.24s |
| **TC-03** | *Relation Mapping* | Menanyakan perpindahan aset dari siapa ke siapa | **PASSED** | 1.17s |
| **TC-04** | *Anti-Hallucination* | Menanyakan perangkat yang tidak ada di inventaris | **PASSED** | 0.67s |

*Tingkat Keberhasilan: **100% (4/4 Lulus)***. Sistem terbukti tidak berhalusinasi saat ditanyakan data fiktif.

---

## 6. Keterbatasan Prototipe Saat Ini

1. **Format Input Masih Teks Polos (`.txt`):** Belum dilengkapi modul pembaca PDF atau OCR untuk BAST bertanda tangan basah/scan fisik.
2. **Ketergantungan Vektor Padat (Dense Embedding):** Model embedding bahasa umum terkadang kurang sensitif terhadap nomor seri yang rumit jika tidak menyertakan beberapa kandidat (`top_k >= 3`).
3. **Belum Ada Pelacakan Kronologis (Time-Series):** Jika satu laptop yang sama dimutasi 3 kali berturut-turut, sistem saat ini mengandalkan LLM untuk membedakan tanggal terbaru secara manual di antara dokumen yang ditarik.

---

## 7. Rekomendasi Pengembangan Selanjutnya

1. **Hybrid Search (BM25 + Dense Vectors):** Menggabungkan pencarian kata kunci eksak (BM25) untuk nomor seri/SN dan pencarian semantik vektor untuk kebutuhan percakapan.
2. **Dukungan File PDF & OCR:** Menambahkan pustaka seperti `pypdf` atau `tesseract-ocr` agar admin inventaris bisa langsung memasukkan scan PDF BAST asli.
3. **Penyortiran Kronologis Otomatis:** Menambahkan metadata tanggal (`metadata={"timestamp": ...}`) di ChromaDB sehingga sistem otomatis mengurutkan dokumen mutasi dari yang paling baru.
4. **Antarmuka Web (UI):** Membangun UI sederhana berbasis Streamlit atau Gradio agar staf non-teknis dapat menggunakan chatbot secara ramah pengguna di browser.

