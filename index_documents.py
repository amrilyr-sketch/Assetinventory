import os
import chromadb

def run_indexing():
    # 1. Tentukan folder database lokal dan folder sumber dokumen
    db_path = "./chroma_db"
    data_dir = "./data"

    print("Memulai proses indexing...")
    
    # 2. Inisialisasi ChromaDB dengan penyimpanan lokal permanen
    client = chromadb.PersistentClient(path=db_path)
    
    # Buat atau ambil koleksi 'bast_mutasi'
    # ChromaDB otomatis menggunakan model embedding lokal bawaan (all-MiniLM-L6-v2)
    collection = client.get_or_create_collection(name="bast_mutasi")

    # 3. Baca semua file .txt di folder data
    if not os.path.exists(data_dir):
        print(f"Folder '{data_dir}' tidak ditemukan!")
        return

    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    
    documents = []
    ids = []
    metadatas = []

    for filename in files:
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append(content)
            ids.append(filename)
            metadatas.append({"source": filename})
            print(f"  - Membaca file: {filename}")

    # 4. Simpan dokumen ke ChromaDB (upsert: perbarui jika sudah ada, tambahkan jika baru)
    if documents:
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"\nBerhasil mengindeks {len(documents)} dokumen BAST ke dalam ChromaDB!")
        print(f"Total data tersimpan di koleksi: {collection.count()} item.")
    else:
        print("Tidak ada dokumen .txt untuk diindeks.")

if __name__ == "__main__":
    run_indexing()

