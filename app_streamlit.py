import os
import glob
import streamlit as st
from rag_chatbot import ask_asset_bot, collection

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="PT BSP - Asset Management & BAST AI",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling CSS Terpadu (Mengadopsi Palet Warna PT Bumi Siak Pusako dari Desain Stitch)
st.markdown("""
<style>
    /* Global Styling */
    .main-header {
        background-color: #FFFFFF;
        padding: 1.25rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        padding: 1.25rem;
        border-radius: 0.75rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .kpi-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0.25rem 0;
    }
    .badge-bsp {
        background-color: #E8F5E9;
        color: #005128;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
    }
    .badge-migas {
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
    }
    .stButton>button {
        border-radius: 0.5rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (Identitas Organisasi & Dokumen BAST)
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
        <div style="background-color: #005128; color: white; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px;">B</div>
        <div>
            <div style="font-weight: 700; font-size: 16px; color: #005128; line-height: 1.1;">PT BSP</div>
            <div style="font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 600;">Bumi Siak Pusako</div>
        </div>
    </div>
    <div style="margin-bottom: 1.25rem;">
        <span class="badge-migas">SKK MIGAS REGULATED</span>
        <span class="badge-bsp" style="margin-left: 4px;">WK CPP</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Mesin AI & Database")
    st.caption("• **LLM:** Groq (`openai/gpt-oss-20b`)")
    st.caption("• **Vector DB:** ChromaDB (`all-MiniLM-L6-v2`)")
    st.caption(f"• **Dokumen Terindeks:** {collection.count()} Berkas BAST")

    st.markdown("---")
    st.markdown("### 📄 Berkas BAST Fisik")
    bast_files = sorted(glob.glob("data/*.txt"))
    if bast_files:
        selected_file = st.selectbox(
            "Pratinjau Dokumen BAST:",
            [os.path.basename(f) for f in bast_files]
        )
        if selected_file:
            with open(os.path.join("data", selected_file), "r", encoding="utf-8") as f:
                content = f.read()
            st.text_area("Isi Dokumen:", content, height=220)
    else:
        st.info("Tidak ada dokumen di folder data/")

# 4. Header Utama Dashboard
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span class="badge-bsp">RAG ENGINE v4.2</span>
                <span style="font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase;">Wilayah Kerja CPP • Sistem Terpadu</span>
            </div>
            <h1 style="font-size: 24px; font-weight: 700; color: #0F172A; margin: 0;">Sistem Informasi Manajemen Aset & BAST</h1>
            <p style="font-size: 13px; color: #64748B; margin: 4px 0 0 0;">Konsolidasi inventaris mutasi berketetapan hukum dan audit pelaporan aset PT Bumi Siak Pusako.</p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <div style="background-color: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600;">
                ● Sync Server: Aktif (100% Valid)
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Kartu Metrik KPI (Mengadopsi Desain Stitch)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Total Aset Terdaftar</div>
        <div class="kpi-value">1,428</div>
        <div style="font-size: 12px; color: #059669; font-weight: 600;">+3.2% MoM (Terverifikasi)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Aset Dialokasikan</div>
        <div class="kpi-value">1,284</div>
        <div style="font-size: 12px; color: #005128; font-weight: 600;">89.9% Utilisasi Terikat BAST</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Mutasi Bulan Ini</div>
        <div class="kpi-value">42</div>
        <div style="font-size: 12px; color: #D97706; font-weight: 600;">+8 Dokumen Berjalan</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Pool Cadangan / Servis</div>
        <div class="kpi-value">144</div>
        <div style="font-size: 12px; color: #475569; font-weight: 600;">Kondisi Baik & Siap Pakai</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Modul AI Smart Asset Assistant (Interactive RAG Chatbot)
st.markdown("### 🤖 Tanya AI Asset Intelligence (RAG)")
st.caption("Pencarian dokumen BAST mutasi, nomor seri perangkat, penanggung jawab, dan lokasi unit kerja secara instan.")

# Quick Suggestion Chips
col_q1, col_q2, col_q3, col_q4 = st.columns(4)
quick_query = None

if col_q1.button("🔍 Cek Lokasi Rina Wijaya", use_container_width=True):
    quick_query = "departemen apa Rina wijaya dan lokasi kerja rina wijaya?"
if col_q2.button("💻 Cek MacBook Pro (SN-882)", use_container_width=True):
    quick_query = "Siapa pemegang aset dengan nomor seri APP-MBP-2023-882 dan kapan tanggal mutasinya?"
if col_q3.button("🏢 Cek Mutasi Surabaya", use_container_width=True):
    quick_query = "Aset apa yang dimutasi ke kantor cabang Surabaya dan siapa penerimanya?"
if col_q4.button("🔄 Cek Perpindahan ThinkPad", use_container_width=True):
    quick_query = "Laptop Lenovo ThinkPad dipindahkan dari siapa ke siapa?"

# Inisialisasi State Percakapan
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Saya Asisten AI Inventory Aset PT Bumi Siak Pusako. Silakan tanyakan data mutasi perangkat IT, nomor seri, pihak penerima, atau lokasi aset."
        }
    ]

# Tampilkan Riwayat Percakapan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Tangani Input Pertanyaan (Dari Text Input atau Quick Button)
user_input = st.chat_input("Ketik pertanyaan mengenai lokasi aset, nomor seri, atau riwayat BAST...")

active_prompt = quick_query if quick_query else user_input

if active_prompt:
    # 1. Tampilkan pertanyaan pengguna
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    # 2. Ambil jawaban dari RAG Engine
    with st.chat_message("assistant"):
        with st.spinner("Mencari dokumen BAST di ChromaDB & menghasilkan jawaban via Groq..."):
            response = ask_asset_bot(active_prompt, n_results=3)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 7. Tabel Ringkasan Rekapitulasi Dokumen Mutasi
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("### 📋 Log Transaksi & Dokumen BAST Aktif")

data_rows = [
    {
        "No. BAST": "BAST/IT-OPS/2024/01/014",
        "Nama Perangkat": "Lenovo ThinkPad T14 Gen 3",
        "Serial Number": "LNV-TP-2023-014",
        "Penyerah": "Budi Santoso (IT)",
        "Penerima": "Rina Wijaya",
        "Divisi / Lokasi": "Keuangan (Gd. A, Lt. 3, Jakarta)",
        "Tanggal": "15 Jan 2024",
        "Status": "Verified BAST"
    },
    {
        "No. BAST": "BAST/IT-OPS/2024/03/088",
        "Nama Perangkat": "Apple MacBook Pro 14 M2 Pro",
        "Serial Number": "APP-MBP-2023-882",
        "Penyerah": "Rian Pratama (Design)",
        "Penerima": "Ahmad Fauzi",
        "Divisi / Lokasi": "Digital Marketing (Gd. B, Lt. 2, Jakarta)",
        "Tanggal": "10 Mar 2024",
        "Status": "Verified BAST"
    },
    {
        "No. BAST": "BAST/IT-OPS/2024/06/105",
        "Nama Perangkat": "Dell OptiPlex 7090 MT + Monitor",
        "Serial Number": "DLL-OPT-2022-301",
        "Penyerah": "Hendra Kurniawan (IT)",
        "Penerima": "Siti Rahma",
        "Divisi / Lokasi": "HRD (Gd. Utama, Lt. 1, Surabaya)",
        "Tanggal": "05 Jun 2024",
        "Status": "Verified BAST"
    }
]

import pandas as pd
df_bast = pd.DataFrame(data_rows)
st.dataframe(df_bast, use_container_width=True, hide_index=True)

