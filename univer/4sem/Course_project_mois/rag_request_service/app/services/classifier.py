from app.services.llm_classifier import classify_with_llm
from app.services.rule_classifier import classify_by_rules


async def classify_query(query: str) -> dict:
    try:
        query_type = await classify_with_llm(query)

        return {
            "type": query_type,
            "source": "llm",
            "llm_error": None,
        }

    except Exception as error:
        fallback_type = classify_by_rules(query)

        return {
            "type": fallback_type,
            "source": "rules",
            "llm_error": str(error),
        }