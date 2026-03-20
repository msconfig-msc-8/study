# services/viewing_service.py

import datetime
from models.property import Property
from models.client import Client
from models.agent import Agent

class ViewingService:
    """
    Сервис для организации просмотров объектов недвижимости.
    """

    @staticmethod
    def arrange_viewing(client: Client, agent: Agent, property_obj: Property) -> str:
        """
        Организует просмотр объекта и возвращает отчет-строку.
        """
        # Снова защищаем систему от ошибок логики (исключения)
        if not property_obj.is_available:
            raise ValueError(f"Ошибка: Объект по адресу {property_obj.address} уже недоступен для просмотра!")

        # Получаем текущее время для отчета
        date_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
        # Формируем красивый отчет о просмотре
        report = (f"[{date_now}] ПРОСМОТР:\n"
                  f"Агент {agent.name} показывает объект '{property_obj.address}' "
                  f"клиенту {client.name}.")
        
        return report