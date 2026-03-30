# test_services/test_deal_service.py

import unittest

from models.agent import Agent
from models.client import Client
from models.property import Property
from services.deal_service import DealService


class TestDealService(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(1, "Агент Смит", 10)
        self.rich_client = Client(1, "Богач", 100000.0)
        self.poor_client = Client(2, "Бедняк", 10000.0)
        self.property = Property(1, "Вилла", 50000.0, 100.0)

    def test_make_deal_success(self):
        deal = DealService.make_deal(
            1,
            self.rich_client,
            self.agent,
            self.property,
        )

        self.assertEqual(self.rich_client.budget, 50000.0)
        self.assertFalse(self.property.is_available)
        self.assertTrue(deal.is_completed)
        self.assertEqual(deal.client.name, "Богач")
        self.assertIsNotNone(deal.document)
        self.assertTrue(deal.document.is_signed)

    def test_make_deal_not_enough_money(self):
        with self.assertRaises(ValueError):
            DealService.make_deal(
                2,
                self.poor_client,
                self.agent,
                self.property,
            )

    def test_make_deal_already_sold(self):
        DealService.make_deal(3, self.rich_client, self.agent, self.property)

        with self.assertRaises(RuntimeError):
            DealService.make_deal(
                4,
                self.poor_client,
                self.agent,
                self.property,
            )
