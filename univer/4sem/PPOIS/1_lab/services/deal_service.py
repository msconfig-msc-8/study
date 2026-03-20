# services/deal_service.py

from models.client import Client
from models.agent import Agent
from models.property import Property
from models.document import Document
from services.document_service import DocumentService

class DealService:
    """
    Сервис для проведения сделок с недвижимостью.
    """

    @staticmethod
    def make_deal(deal_id: int, client: Client, agent: Agent, property_obj: Property) -> Document:
        """
        Проводит сделку: проверяет бюджет, списывает средства, продает объект и выдает документ.
        """
        # 1. Проверяем, не купил ли кто-то квартиру прямо перед нами
        if not property_obj.is_available:
            raise RuntimeError(f"Сделка отменена: Объект '{property_obj.address}' уже продан!")

        # 2. Проверяем, хватает ли у клиента денег (бюджет)
        if client.budget < property_obj.price:
            raise ValueError(f"Сделка отменена: У клиента {client.name} недостаточно средств! "
                             f"Нужно {property_obj.price}$, а есть только {client.budget}$.")

        # 3. Финансовая операция (списываем деньги)
        client.budget -= property_obj.price

        # 4. Фиксируем продажу объекта
        property_obj.sell()

        # 5. Оформление документации через другой сервис
        document = DocumentService.draft_document(deal_id, client, agent, property_obj)
        DocumentService.sign_document(document)

        # Возвращаем готовый и подписанный документ как результат успешной сделки
        return document