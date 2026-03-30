from __future__ import annotations

import datetime

from models.agent import Agent
from models.client import Client
from models.property import Property


class Document:
    """
    Класс, представляющий договор по сделке с недвижимостью.
    """

    def __init__(
        self,
        document_id: int,
        client: Client,
        agent: Agent,
        property_obj: Property,
    ):
        self.document_id = document_id
        self.client = client
        self.agent = agent
        self.property_obj = property_obj
        self.created_at = datetime.datetime.now()
        self.is_signed = False

    def sign(self) -> None:
        """
        Подписывает документ.
        """
        if self.is_signed:
            raise RuntimeError(f"Документ №{self.document_id} уже подписан!")

        self.is_signed = True

    def __str__(self) -> str:
        status = "Подписан" if self.is_signed else "Черновик"
        date_str = self.created_at.strftime("%d-%m-%Y")
        return (
            f"Документ №{self.document_id} [{status}] от {date_str} | "
            f"Клиент: {self.client.name} | Агент: {self.agent.name} | "
            f"Объект: {self.property_obj.address}"
        )
