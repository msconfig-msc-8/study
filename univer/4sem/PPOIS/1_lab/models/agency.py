from __future__ import annotations

from models.agent import Agent
from models.client import Client
from models.deal import Deal
from models.document import Document
from models.market import Market
from models.property import Property


class Agency:
    """
    Класс, представляющий агентство недвижимости.
    Хранит основные сущности и текущее состояние рынка.
    """

    def __init__(self, name: str, market: Market):
        self.name = name
        self.market = market
        self.agents: list[Agent] = []
        self.clients: list[Client] = []
        self.properties: list[Property] = []
        self.documents: list[Document] = []
        self.deals: list[Deal] = []

    def add_agent(self, agent: Agent) -> None:
        self.agents.append(agent)

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def add_property(self, property_obj: Property) -> None:
        self.properties.append(property_obj)

    def add_document(self, document: Document) -> None:
        self.documents.append(document)

    def add_deal(self, deal: Deal) -> None:
        self.deals.append(deal)

    def get_agent_by_id(self, agent_id: int) -> Agent:
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        raise ValueError(f"Агент с id={agent_id} не найден.")

    def get_client_by_id(self, client_id: int) -> Client:
        for client in self.clients:
            if client.client_id == client_id:
                return client
        raise ValueError(f"Клиент с id={client_id} не найден.")

    def get_property_by_id(self, property_id: int) -> Property:
        for property_obj in self.properties:
            if property_obj.property_id == property_id:
                return property_obj
        raise ValueError(
            f"Объект недвижимости с id={property_id} не найден."
        )

    def __str__(self) -> str:
        return (
            f"Агентство '{self.name}' | Агентов: {len(self.agents)} | "
            f"Клиентов: {len(self.clients)} | "
            f"Объектов: {len(self.properties)} | "
            f"Сделок: {len(self.deals)} | Документов: {len(self.documents)}"
        )
