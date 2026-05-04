import re

from app.core.constants import (
    QUERY_TYPE_DEFINITION,
    QUERY_TYPE_COMPARISON,
    QUERY_TYPE_RECOMMENDATION,
)


def classify_by_rules(query: str) -> str:
    text = query.lower().strip()

    comparison_patterns = [
        r"чем\s+.*отличается",
        r"чем\s+.*отличаются",
        r"сравни",
        r"сравнение",
        r"разница",
        r"отличие",
        r"\bvs\b",
        r"\bversus\b",
    ]

    recommendation_patterns = [
        r"что\s+.*выбрать",
        r"какой\s+.*выбрать",
        r"какую\s+.*выбрать",
        r"какие\s+.*выбрать",
        r"что\s+.*лучше\s+использовать",
        r"что\s+.*лучше\s+применить",
        r"какой\s+.*лучше",
        r"посоветуй",
        r"рекомендуй",
        r"рекомендация",
        r"подбери",
        r"выбрать\s+для",
    ]

    definition_patterns = [
        r"что\s+такое",
        r"объясни",
        r"дай\s+определение",
        r"определение",
        r"что\s+означает",
        r"расскажи\s+про",
    ]

    if any(re.search(pattern, text) for pattern in comparison_patterns):
        return QUERY_TYPE_COMPARISON

    if any(re.search(pattern, text) for pattern in recommendation_patterns):
        return QUERY_TYPE_RECOMMENDATION

    if any(re.search(pattern, text) for pattern in definition_patterns):
        return QUERY_TYPE_DEFINITION

    return QUERY_TYPE_DEFINITION