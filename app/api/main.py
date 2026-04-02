from fastapi import FastAPI
from pydantic import BaseModel
import os

from app.main import run_pipeline

app = FastAPI()

# 🚀 Health check
@app.get("/")
def home():
    return {"status": "Artemis running 🚀"}


# 🚀 GET endpoint (simple testing)
@app.get("/query")
def query_get(q: str):
    return run_pipeline(q)


# 🚀 POST endpoint (production usage)
class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query_post(request: QueryRequest):
    return run_pipeline(request.query)