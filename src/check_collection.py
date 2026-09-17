import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collections = client.list_collections()

print("Total collections found:", len(collections))
for c in collections:
    print("Collection name:", c.name)