import re
from fastapi import HTTPException


def preprocess_query(query: str) -> str:
    if query is None:
        raise HTTPException(
            status_code=400,
            detail="Запрос не должен быть пустым."
        )

    normalized_query = query.strip()
    normalized_query = re.sub(r"\s+", " ", normalized_query)

    if not normalized_query:
        raise HTTPException(
            status_code=400,
            detail="Запрос не должен быть пустым."
        )

    return normalized_query