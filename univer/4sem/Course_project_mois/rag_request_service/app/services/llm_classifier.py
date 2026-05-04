import json
import re

import httpx

from app.core.config import settings
from app.core.constants import ALLOWED_QUERY_TYPES


SYSTEM_PROMPT = """
Ты являешься классификатором пользовательских запросов для справочной RAG-системы
по технологиям искусственного интеллекта.

Твоя задача — определить тип запроса пользователя.

Допустимые типы:
- definition — если пользователь просит объяснить термин, понятие, метод, архитектуру или инструмент;
- comparison — если пользователь просит сравнить две или более технологии, модели, методы или инструменты;
- recommendation — если пользователь просит подобрать, посоветовать или выбрать технологию, модель, метод или инструмент.

Верни только один JSON-объект без markdown, без пояснений и без комментариев.

Строго такой формат:
{"type": "definition"}

Ключ type обязательно должен быть в двойных кавычках.
Значение type обязательно должно быть одним из:
definition, comparison, recommendation.
"""


def _parse_llm_response(content: str) -> str:
    content = content.strip()

    # Убираем markdown-обёртку, если модель вдруг вернула ```json ... ```
    content = content.replace("```json", "").replace("```", "").strip()

    # 1. Пытаемся распарсить нормальный JSON
    try:
        data = json.loads(content)
        query_type = data.get("type")

        if query_type in ALLOWED_QUERY_TYPES:
            return query_type

    except json.JSONDecodeError:
        pass

    # 2. Пытаемся найти "type": "..."
    match = re.search(
        r'"type"\s*:\s*"(definition|comparison|recommendation)"',
        content,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).lower()

    # 3. Пытаемся найти type: "..." без кавычек у ключа
    match = re.search(
        r'type\s*:\s*"(definition|comparison|recommendation)"',
        content,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).lower()

    # 4. Последний вариант: ищем просто одно из допустимых слов
    match = re.search(
        r"\b(definition|comparison|recommendation)\b",
        content,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).lower()

    raise ValueError(f"Не удалось извлечь тип запроса из ответа LLM: {content}")


async def classify_with_llm(query: str) -> str:
    if not settings.use_llm:
        raise RuntimeError("LLM-классификация отключена.")

    provider = settings.llm_provider.lower().strip()

    if provider == "deepseek":
        return await _classify_with_deepseek(query)

    if provider == "local":
        return await _classify_with_local_model(query)

    raise RuntimeError(f"Неизвестный LLM-провайдер: {settings.llm_provider}")


async def _classify_with_deepseek(query: str) -> str:
    if not settings.deepseek_api_key:
        raise RuntimeError("DeepSeek API key не указан в .env.")

    url = f"{settings.deepseek_base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.deepseek_model,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        "response_format": {
            "type": "json_object",
        },
        "max_tokens": 50,
        "temperature": 0,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
        response = await client.post(url, headers=headers, json=payload)

    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    return _parse_llm_response(content)


async def _classify_with_local_model(query: str) -> str:
    """
    Заготовка для будущей локальной модели.
    Потом здесь можно будет подключить Ollama, llama.cpp
    или локальную модель через transformers.
    """
    raise NotImplementedError("Локальная LLM пока не подключена.")