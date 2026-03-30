# services/viewing_service.py

import datetime

from models.agent import Agent
from models.client import Client
from models.property import Property


class ViewingService:
    """
    Сервис для организации просмотров объектов недвижимости.
    """

    @staticmethod
    def arrange_viewing(
        client: Client,
        agent: Agent,
        property_obj: Property,
    ) -> str:
        """
        Организует просмотр объекта и возвращает отчет-строку.
        """
        if not property_obj.is_available:
            raise ValueError(
                f"Ошибка: Объект по адресу {property_obj.address} "
                "уже недоступен для просмотра!"
            )

        date_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        report = (
            f"[{date_now}] ПРОСМОТР:\n"
            f"Агент {agent.name} показывает объект "
            f"'{property_obj.address}' клиенту {client.name}."
        )
        return report
