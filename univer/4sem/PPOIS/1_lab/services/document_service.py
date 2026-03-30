# services/document_service.py

from models.agent import Agent
from models.client import Client
from models.document import Document
from models.property import Property


class DocumentService:
    """
    Сервис для работы с документами (оформление и подписание).
    """

    @staticmethod
    def draft_document(
        doc_id: int,
        client: Client,
        agent: Agent,
        property_obj: Property,
    ) -> Document:
        """
        Создает черновик документа (договора купли-продажи).
        """
        return Document(doc_id, client, agent, property_obj)

    @staticmethod
    def sign_document(document: Document) -> None:
        """
        Подписывает переданный документ.
        """
        document.sign()
