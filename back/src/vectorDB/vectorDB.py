import chromadb
import os
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

class MyVectorDB:

    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")

        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.base_url = os.getenv("CONFLUENCE_BASE_URL")

        if not self.username or not self.password or not self.base_url:
            raise RuntimeError("Missing required Confluence environment variables")

        self.fetch_and_import_pages(["718181419", "29520970"])

    def query(self, input_text):
        results = self.collection.query(
            query_texts=[input_text],  # Chroma will embed this for you
            n_results=1,  # how many results to return
        )
        return results
    
    def fetch_and_import_pages(self, page_ids: list[str]):
        documents = []
        ids = []
        metadatas = []

        for pid in page_ids:
            print(f"📄 Fetching Confluence page {pid} ...")
            page_text, page_url = self._fetch_confluence_page(pid)
            if page_text.strip():
                ids.append(pid)
                documents.append(page_text)
                metadatas.append({"url": page_url})

        if documents:
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas)
        else:
            print("⚠️ No valid pages fetched.")

    def _fetch_confluence_page(self, page_id: str) -> str:
        try:
            url = f"{self.base_url}/rest/api/content/{page_id}?expand=body.storage"
            resp = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            
            if resp.status_code != 200:
                print(f"⚠️ Failed to fetch page {page_id} -> {resp.status_code}")
                return ""
            
            data = resp.json()
            html_content = data.get("body", {}).get("storage", {}).get("value", "")
            soup = BeautifulSoup(html_content, "html.parser")
            page_text = soup.get_text(separator=".")

            webui_link = data.get("_links", {}).get("webui", "")
            page_url = f"{self.base_url}{webui_link}" if webui_link else ""

            return page_text, page_url
        
        except Exception as e:
            print(f"⚠️ Exception while fetching page {page_id}: {e}")
            return ""
        