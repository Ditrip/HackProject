import chromadb

class MyVectorDB:

    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
        self.collection.add(
            ids=["id1", "id2"],
            documents=[
                "This is a document about pineapple",
                "This is a document about oranges",
            ],
        )

    def query(self, input_text):
        results = self.collection.query(
            query_texts=[input_text],  # Chroma will embed this for you
            n_results=2,  # how many results to return
        )
        return results

