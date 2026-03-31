from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.coordinator_agent import run_agents
from app.vectorstore.faiss_store import VectorStore
from app.services.embedding_service import embed_text
from app.services.reranker import rerank
from app.agents.query_rewriter import rewrite_query
import os

PORT = int(os.environ.get("PORT", 10000))

app = FastAPI()

vectorstore = VectorStore()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query_endpoint(request: QueryRequest):
    user_query = request.query

    # rewrite
    rewritten_query = rewrite_query(user_query)

    # run multi-agent system
    answer = run_agents(
        rewritten_query,
        vectorstore,
        embed_text,
        rerank
    )

    return {
        "query": user_query,
        "rewritten_query": rewritten_query,
        "answer": answer
    }
