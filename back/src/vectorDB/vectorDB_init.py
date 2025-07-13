import chromadb

chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection(name="my_collection")
collection.add(
    ids=["id1", "id2"],
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ]
)
print(chroma_client.heartbeat())

results = collection.query(
    query_texts=["orange"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)

