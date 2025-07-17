from typing import Union
from fastapi.responses import JSONResponse
import json

from fastapi import FastAPI
from llm.lmModel import MyLLM
from vectorDB.vectorDB import MyVectorDB

myLLM = MyLLM()
myDB = MyVectorDB()
app = FastAPI()


@app.get("/")
def read_root():
    answer = myLLM.set_question("What is NCR Atleos")
    print(answer)
    return JSONResponse(
        content={"message": "Here is your response",
                 "DB":json.dumps(myDB.query("oranges")),
                 "LLM":json.dumps(myLLM.set_question("What is NCR Atleos"))
                 },
        headers={"X-Custom-Header": "json.dumps(answer)"}
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
