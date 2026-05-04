from app.core.constants import (
    QUERY_TYPE_DEFINITION,
    QUERY_TYPE_COMPARISON,
    QUERY_TYPE_RECOMMENDATION,
)


async def route_query(query: str, query_type: str) -> dict:
    """
    Маршрутизирует запрос в нужный сценарий обработки.

    Пока здесь используются заглушки.
    Позже вместо них будет вызов backend / LangChain / Neo4j.
    """

    if query_type == QUERY_TYPE_DEFINITION:
        return {
            "scenario": "definition_scenario",
            "answer": "Запрос направлен в сценарий получения определения."
        }

    if query_type == QUERY_TYPE_COMPARISON:
        return {
            "scenario": "comparison_scenario",
            "answer": "Запрос направлен в сценарий сравнения объектов."
        }

    if query_type == QUERY_TYPE_RECOMMENDATION:
        return {
            "scenario": "recommendation_scenario",
            "answer": "Запрос направлен в сценарий формирования рекомендации."
        }

    return {
        "scenario": "unknown_scenario",
        "answer": "Не удалось определить сценарий обработки запроса."
    }