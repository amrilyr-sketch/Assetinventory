import sys
import chromadb

def search_bast(query_text, n_results=1):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="bast_mutasi")

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    # Gunakan query dari argumen terminal atau default nomor seri ThinkPad
    query = sys.argv[1] if len(sys.argv) > 1 else "LNV-TP-2023-014"
    
    print(f"Mencari di ChromaDB dengan kata kunci: '{query}'")
    print("=" * 50)
    
    res = search_bast(query, n_results=1)
    
    if res["documents"] and len(res["documents"][0]) > 0:
        doc_id = res["ids"][0][0]
        distance = res["distances"][0][0]
        content = res["documents"][0][0]
        
        print(f"Dokumen Ditemukan: {doc_id}")
        print(f"Jarak Kemiripan (Distance): {distance:.4f} (semakin kecil semakin mirip)")
        print("-" * 50)
        print(content)
        print("=" * 50)
    else:
        print("Dokumen tidak ditemukan.")

