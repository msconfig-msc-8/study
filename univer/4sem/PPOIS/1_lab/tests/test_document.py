import unittest

from models.agent import Agent
from models.client import Client
from models.document import Document
from models.property import Property


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.client = Client(1, "Клиент", 100000.0)
        self.agent = Agent(1, "Агент", 5)
        self.property_obj = Property(1, "Улица", 50000.0, 40.0)

    def test_sign_document(self):
        doc = Document(1, self.client, self.agent, self.property_obj)

        self.assertFalse(doc.is_signed)

        doc.sign()
        self.assertTrue(doc.is_signed)

    def test_sign_already_signed(self):
        doc = Document(1, self.client, self.agent, self.property_obj)
        doc.sign()

        with self.assertRaises(RuntimeError):
            doc.sign()
