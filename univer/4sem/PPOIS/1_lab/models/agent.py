from __future__ import annotations

from models.client import Client


class Agent:
    """
    Класс, представляющий агента по недвижимости.
    """

    def __init__(self, agent_id: int, name: str, experience_years: int):
        self.agent_id = agent_id
        self.name = name
        self.experience_years = experience_years
        self.clients: list[Client] = []

    def assign_client(self, client: Client) -> None:
        """
        Метод для прикрепления клиента к агенту.
        """
        self.clients.append(client)

    def __str__(self) -> str:
        return (
            f"Агент #{self.agent_id}: {self.name} "
            f"(Опыт: {self.experience_years} лет)"
        )
