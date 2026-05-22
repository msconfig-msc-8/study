from app.services.llm_classifier import classify_with_llm
from app.services.rule_classifier import classify_by_rules


async def classify_query(query: str) -> dict:
    llm_error = None

    # Пробуем LLM два раза, потому что API иногда может вернуть неполный JSON
    for _ in range(2):
        try:
            query_type = await classify_with_llm(query)

            return {
                "type": query_type,
                "source": "llm",
                "llm_error": None,
            }

        except Exception as error:
            llm_error = str(error)

    # Если LLM оба раза не сработала — используем резервные правила
    fallback_type = classify_by_rules(query)

    return {
        "type": fallback_type,
        "source": "rules",
        "llm_error": llm_error,
    }