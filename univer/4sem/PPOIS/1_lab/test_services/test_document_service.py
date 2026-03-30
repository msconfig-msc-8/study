import unittest

from models.agent import Agent
from models.client import Client
from models.property import Property
from services.document_service import DocumentService


class TestDocumentService(unittest.TestCase):
    def test_draft_and_sign(self):
        client = Client(1, "Джон", 50000.0)
        agent = Agent(1, "Смит", 5)
        prop = Property(1, "Улица", 20000.0, 30.0)

        doc = DocumentService.draft_document(1, client, agent, prop)
        self.assertFalse(doc.is_signed)

        DocumentService.sign_document(doc)
        self.assertTrue(doc.is_signed)
