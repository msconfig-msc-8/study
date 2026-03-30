import unittest

from models.agent import Agent
from models.client import Client
from models.deal import Deal
from models.document import Document
from models.property import Property


class TestDeal(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(1, "Смит", 5)
        self.client = Client(1, "Джон", 70000.0)
        self.property_obj = Property(1, "Улица", 50000.0, 45.0)
        self.document = Document(1, self.client, self.agent, self.property_obj)

    def test_complete_deal(self):
        deal = Deal(1, self.property_obj, self.client, self.agent, 50000.0)
        deal.complete(self.document)
        self.assertTrue(deal.is_completed)
        self.assertIs(deal.document, self.document)

    def test_negative_price_error(self):
        with self.assertRaises(ValueError):
            Deal(2, self.property_obj, self.client, self.agent, -100.0)
