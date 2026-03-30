from models.agent import Agent
from models.client import Client
from models.deal import Deal
from models.property import Property
from services.document_service import DocumentService


class DealService:
    """
    Сервис для проведения сделок с недвижимостью.
    """

    @staticmethod
    def make_deal(
        deal_id: int,
        client: Client,
        agent: Agent,
        property_obj: Property,
    ) -> Deal:
        """
        Проводит сделку: проверяет бюджет, продает объект,
        оформляет документ и возвращает завершенную сделку.
        """
        if not property_obj.is_available:
            raise RuntimeError(
                f"Сделка отменггена : Объект '{property_obj.address}' уже продан!"
            )

        if client.budget < property_obj.price:
            raise ValueError(
                f"Сделка отменена: У клиента {client.name} "
                f"недостаточно средств! Нужно {property_obj.price}$, "
                f"а есть только {client.budget}$."
            )

        client.budget -= property_obj.price
        property_obj.sell()

        deal = Deal(deal_id, property_obj, client, agent, property_obj.price)
        document = DocumentService.draft_document(
            deal_id,
            client,
            agent,
            property_obj,
        )
        DocumentService.sign_document(document)
        deal.complete(document)
        return deal
