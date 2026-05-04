from fastapi import APIRouter
from pydantic import BaseModel

from app.services.preprocessing import preprocess_query
from app.services.classifier import classify_query
from app.services.request_router import route_query

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "RAG request service is running",
    }


@router.post("/api/query")
async def process_query(request: QueryRequest):
    normalized_query = preprocess_query(request.query)

    classification_result = await classify_query(normalized_query)

    routing_result = await route_query(
        query=normalized_query,
        query_type=classification_result["type"],
    )

    response = {
        "status": "success",
        "original_query": request.query,
        "normalized_query": normalized_query,
        "type": classification_result["type"],
        "classification_source": classification_result["source"],
        "scenario": routing_result["scenario"],
        "answer": routing_result["answer"],
        "message": f"Запрос классифицирован как: {classification_result['type']}",
    }

    if classification_result["source"] == "rules":
        response["llm_error"] = classification_result["llm_error"]

    return response