from __future__ import annotations

import datetime

from models.agent import Agent
from models.client import Client
from models.document import Document
from models.property import Property


class Deal:
    """
    Класс, представляющий сделку с недвижимостью.
    """

    def __init__(
        self,
        deal_id: int,
        property_obj: Property,
        client: Client,
        agent: Agent,
        final_price: float,
    ):
        self.deal_id = deal_id
        self.property_obj = property_obj
        self.client = client
        self.agent = agent

        if final_price <= 0:
            raise ValueError("Сумма сделки должна быть положительной!")
        self.final_price = final_price

        self.created_at = datetime.datetime.now()
        self.completed_at: datetime.datetime | None = None
        self.document: Document | None = None
        self.is_completed = False

    def complete(self, document: Document) -> None:
        """
        Завершает сделку и привязывает оформленный документ.
        """
        if self.is_completed:
            raise RuntimeError("Сделка уже была завершена ранее!")

        self.document = document
        self.completed_at = datetime.datetime.now()
        self.is_completed = True

    def __str__(self) -> str:
        status = "Завершена" if self.is_completed else "В процессе"
        return (
            f"Сделка №{self.deal_id} [{status}] | "
            f"Клиент: {self.client.name} | Агент: {self.agent.name} | "
            f"Объект: {self.property_obj.address} | Сумма: {self.final_price}$"
        )
