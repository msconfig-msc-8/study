# tests/test_agency.py

import unittest

from models.agency import Agency
from models.agent import Agent
from models.client import Client
from models.deal import Deal
from models.document import Document
from models.market import Market
from models.property import Property


class TestAgency(unittest.TestCase):
    def setUp(self) -> None:
        self.market = Market("Тестовый рынок", 1.0)
        self.agency = Agency("Тестовое агентство", self.market)
        self.agent = Agent(1, "Иван", 5)
        self.client = Client(1, "Пётр", 100000.0)
        self.prop = Property(1, "ул. Тестовая, 1", 50000.0, 40.0)

    def test_add_agent(self) -> None:
        self.agency.add_agent(self.agent)
        self.assertEqual(len(self.agency.agents), 1)
        self.assertEqual(self.agency.agents[0].name, "Иван")

    def test_add_client(self) -> None:
        self.agency.add_client(self.client)
        self.assertEqual(len(self.agency.clients), 1)
        self.assertEqual(self.agency.clients[0].name, "Пётр")

    def test_add_property(self) -> None:
        self.agency.add_property(self.prop)
        self.assertEqual(len(self.agency.properties), 1)

    def test_add_document(self) -> None:
        doc = Document(1, self.client, self.agent, self.prop)
        self.agency.add_document(doc)
        self.assertEqual(len(self.agency.documents), 1)

    def test_add_deal(self) -> None:
        deal = Deal(1, self.prop, self.client, self.agent, 50000.0)
        self.agency.add_deal(deal)
        self.assertEqual(len(self.agency.deals), 1)

    def test_get_agent_by_id_success(self) -> None:
        self.agency.add_agent(self.agent)
        found = self.agency.get_agent_by_id(1)
        self.assertEqual(found.name, "Иван")

    def test_get_agent_by_id_not_found(self) -> None:
        with self.assertRaises(ValueError):
            self.agency.get_agent_by_id(999)

    def test_get_client_by_id_success(self) -> None:
        self.agency.add_client(self.client)
        found = self.agency.get_client_by_id(1)
        self.assertEqual(found.name, "Пётр")

    def test_get_client_by_id_not_found(self) -> None:
        with self.assertRaises(ValueError):
            self.agency.get_client_by_id(999)

    def test_get_property_by_id_success(self) -> None:
        self.agency.add_property(self.prop)
        found = self.agency.get_property_by_id(1)
        self.assertEqual(found.address, "ул. Тестовая, 1")

    def test_get_property_by_id_not_found(self) -> None:
        with self.assertRaises(ValueError):
            self.agency.get_property_by_id(999)

    def test_str(self) -> None:
        result = str(self.agency)
        self.assertIn("Тестовое агентство", result)
        self.assertIn("Агентов: 0", result)
