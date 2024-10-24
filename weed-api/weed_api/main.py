# fastapi_project/main.py
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Do you wanna cook?"}

def start():
    uvicorn.run("weed_api.main:app", host="0.0.0.0", port=8000, reload=True)