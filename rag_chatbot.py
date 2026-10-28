import os
import sys
import unicodedata
import chromadb
from groq import Groq

# Pastikan output terminal mendukung karakter UTF-8 / emoji di Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 1. Baca GROQ_API_KEY dari file .env
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY tidak ditemukan di file .env atau environment variables.")
    sys.exit(1)

# 2. Inisialisasi Klien ChromaDB & Groq
client_chroma = chromadb.PersistentClient(path="./chroma_db")
collection = client_chroma.get_or_create_collection(name="bast_mutasi")
groq_client = Groq(api_key=api_key)

def ask_asset_bot(user_question: str, n_results: int = 3) -> str:
    """
    Fungsi RAG:
    1. Retrieval: Cari n_results dokumen BAST kandidat teratas di ChromaDB.
    2. Augmentation & Generation: Berikan seluruh konteks ke model Groq untuk dijawab.
    """
    total_docs = collection.count()
    k = min(n_results, total_docs) if total_docs > 0 else 1

    results = collection.query(
        query_texts=[user_question],
        n_results=k
    )

    if not results["documents"] or len(results["documents"][0]) == 0:
        return "Data tidak ditemukan di catatan mutasi aset."

    # Gabungkan semua dokumen kandidat sebagai konteks
    context_blocks = []
    for i in range(len(results["ids"][0])):
        doc_id = results["ids"][0][i]
        doc_content = results["documents"][0][i]
        context_blocks.append(f"[File Dokumen: {doc_id}]\n{doc_content}")

    combined_context = "\n\n" + ("=" * 40) + "\n\n".join(context_blocks) + "\n\n" + ("=" * 40)

    # 2. PROMPT TEMPLATE
    system_instruction = (
        "Anda adalah Asisten AI Inventory Aset IT perusahaan.\n"
        "Tugas Anda adalah menjawab pertanyaan pengguna secara akurat HANYA berdasarkan "
        "koleksi dokumen Berita Acara Serah Terima (BAST) yang dilampirkan.\n\n"
        "Aturan Penulisan Jawaban:\n"
        "1. Jawab pertanyaan pengguna secara lugas dan faktual.\n"
        "2. Selalu sertakan rincian data mutasi aset berikut:\n"
        "   - Merk / Tipe Aset\n"
        "   - Serial Number (SN)\n"
        "   - Pihak Terkait (Penyerah & Penerima/Pemegang Terakhir)\n"
        "   - Tanggal Mutasi\n"
        "   - Lokasi / Unit Kerja Baru\n"
        "   - Dokumen Sumber (cantumkan persis nama filenya, misal bast_001.txt)\n"
        "3. Jika aset atau informasi yang ditanyakan tidak tercantum di dokumen BAST yang dilampirkan, "
        "jawab dengan tegas: 'Data tidak ditemukan di catatan mutasi aset.' Jangan berasumsi atau mengarang data."
    )

    user_prompt = f"""Koleksi Dokumen BAST yang Tersedia:
{combined_context}

Pertanyaan Pengguna: {user_question}
"""

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        model="openai/gpt-oss-20b",
        temperature=0.1
    )

    response_text = chat_completion.choices[0].message.content
    return unicodedata.normalize("NFKD", response_text)

def interactive_chat():
    print("=" * 60)
    print(" CHATBOT INVENTORY MUTASI ASET IT (RAG + GROQ)")
    print(" Ketik 'keluar' atau 'exit' untuk menutup sesi.")
    print("=" * 60)

    while True:
        try:
            query = input("\n[Anda]: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "keluar", "q"]:
                print("Terima kasih! Sampai jumpa.")
                break

            print("\n[AI Sedang Mencari Dokumen & Menjawab...]")
            response = ask_asset_bot(query)
            print(f"\n[Bot]:\n{response}\n")
            print("-" * 60)

        except (KeyboardInterrupt, EOFError):
            print("\nSesi diakhiri.")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        single_query = " ".join(sys.argv[1:])
        print(f"Pertanyaan: {single_query}\n")
        print(ask_asset_bot(single_query))
    else:
        interactive_chat()
