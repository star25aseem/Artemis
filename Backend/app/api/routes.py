from fastapi import APIRouter
from app.services.rag_pipeline import process_query

router = APIRouter()

@router.post("/query")
async def query_papers(query: str):
    result = await process_query(query)
    return {"response": result}
