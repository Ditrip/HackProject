from typing import Union
from fastapi.responses import JSONResponse
import json
from fastapi import FastAPI
from llm.lmModel import MyLLM
from vectorDB.vectorDB import MyVectorDB
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

myLLM = MyLLM()
myDB = MyVectorDB()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints --
@app.get("/")
def read_root():
    return JSONResponse(
        content={"message": "Here is your response"},
        headers={"X-Custom-Header": "json.dumps(answer)"}
    )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class InputModel(BaseModel):
    prompt: str

@app.post("/process-user-prompt")
def process_user_prompt(prompt: InputModel):
    result = myDB.query(prompt.prompt)
    docs = result.get("documents", [])
    flattened_docs = docs[0] if docs else []
    ids = result.get("ids", [])
    page_id = ids[0][0] if ids else None
    answer = myLLM.answer_from_context(flattened_docs, prompt.prompt)
    metas = result.get("metadatas", [])
    page_url = metas[0][0].get("url") if metas and metas[0] else None

    if page_url:
        final_text = f"{answer}\n\nSource URL: {page_url}"
    else:
        final_text = answer
    
    return final_text

   
