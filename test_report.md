# Laporan Hasil Pengujian Sistem RAG Inventory Aset IT

**Tanggal Pengujian:** 2026-10-28 09:41:34

**Konfigurasi Retrieval:** `n_results = 3` (Multi-candidate context)

| ID | Kategori | Pertanyaan | Dokumen Sumber Terpilih | Status |
|---|---|---|---|---|
| TC-01 | Ketepatan Data (Serial Number Exact Match) | Siapa pemegang aset dengan nomor seri APP-MBP-2023-882 dan kapan tanggal mutasinya? | `bast_002.txt` | **PASSED** |
| TC-02 | Pencarian Semantik (Lokasi & Perangkat) | Aset apa yang dimutasi ke kantor cabang Surabaya dan siapa penerimanya? | `bast_003.txt` | **PASSED** |
| TC-03 | Ketepatan Relasi (Pihak Penyerah & Penerima) | Laptop Lenovo ThinkPad dipindahkan dari siapa ke siapa? | `bast_001.txt` | **PASSED** |
| TC-04 | Uji Halusinasi / Negative Test (Data Tidak Ada) | Siapa pemegang printer Epson L3210 di ruang rapat? | `N/A (Data Tidak Ditemukan)` | **PASSED** |

## Rincian Rekaman Uji Coba

### TC-01 - Ketepatan Data (Serial Number Exact Match)
* **Pertanyaan:** Siapa pemegang aset dengan nomor seri APP-MBP-2023-882 dan kapan tanggal mutasinya?
* **Dokumen Sumber Teridentifikasi:** `bast_002.txt`
* **Waktu Respons:** 1.74 detik
* **Status Evaluasi:** **PASSED**

**Jawaban AI:**
> **Pemegang aset APP‐MBP‐2023‐882**  
> - **Merk / Tipe**: Apple MacBook Pro 14 Inch M2 Pro  
> - **Serial Number (SN)**: APP‐MBP‐2023‐882  
> - **Pihak Terkait**:  
>   - Penyerah: Rian Pratama (Divisi UI/UX Design)  
>   - Penerima/Pemegang Terakhir: **Ahmad Fauzi (Digital Marketing Lead)**  
> - **Tanggal Mutasi**: **10 Maret 2024**  
> - **Lokasi / Unit Kerja Baru**: Divisi Digital Marketing, Gedung B, Lantai 2, Ruang Creative Hub, Kantor Pusat Jakarta  
> - **Dokumen Sumber**: bast_002.txt

---


### TC-02 - Pencarian Semantik (Lokasi & Perangkat)
* **Pertanyaan:** Aset apa yang dimutasi ke kantor cabang Surabaya dan siapa penerimanya?
* **Dokumen Sumber Teridentifikasi:** `bast_003.txt`
* **Waktu Respons:** 1.24 detik
* **Status Evaluasi:** **PASSED**

**Jawaban AI:**
> **Aset yang dimutasi ke kantor cabang Surabaya**  
> - **Merk / Tipe Aset**: Dell OptiPlex 7090 MT + Monitor Dell 24 Inch  
> - **Serial Number (SN)**: DLL-OPT-2022-301  
> - **Pihak Terkait**:  
>   - Penyerah: Hendra Kurniawan (IT Asset & Inventory)  
>   - Penerima: **Siti Rahma** (HR Recruitment Officer)  
> - **Tanggal Mutasi**: 05 Juni 2024  
> - **Lokasi / Unit Kerja Baru**: Human Resources Department (HRD), Gedung Utama, Lantai 1, Ruang 104 HRD, **Kantor Cabang Surabaya**  
> - **Dokumen Sumber**: bast_003.txt

---


### TC-03 - Ketepatan Relasi (Pihak Penyerah & Penerima)
* **Pertanyaan:** Laptop Lenovo ThinkPad dipindahkan dari siapa ke siapa?
* **Dokumen Sumber Teridentifikasi:** `bast_001.txt`
* **Waktu Respons:** 1.17 detik
* **Status Evaluasi:** **PASSED**

**Jawaban AI:**
> **Mutasi Laptop Lenovo ThinkPad T14 Gen 3**
> 
> | Merk / Tipe Aset | Serial Number (SN) | Pihak Terkait (Penyerah & Penerima) | Tanggal Mutasi | Lokasi / Unit Kerja Baru | Dokumen Sumber |
> |------------------|--------------------|-------------------------------------|----------------|--------------------------|----------------|
> | Lenovo ThinkPad T14 Gen 3 | LNV‐TP‐2023‐014 | Penyerah: **Budi Santoso** (IT Operations) <br>Penerima: **Rina Wijaya** (Staf Divisi Keuangan) | 15 Januari 2024 | Divisi Keuangan – Gedung A, Lantai 3, Ruang Finance 302, Kantor Pusat Jakarta | **bast_001.txt** |
> 
> > **Jawaban:** Laptop Lenovo ThinkPad dipindahkan **dari Budi Santoso ke Rina Wijaya**.

---


### TC-04 - Uji Halusinasi / Negative Test (Data Tidak Ada)
* **Pertanyaan:** Siapa pemegang printer Epson L3210 di ruang rapat?
* **Dokumen Sumber Teridentifikasi:** `N/A (Data Tidak Ditemukan)`
* **Waktu Respons:** 0.67 detik
* **Status Evaluasi:** **PASSED**

**Jawaban AI:**
> Data tidak ditemukan di catatan mutasi aset.

---
