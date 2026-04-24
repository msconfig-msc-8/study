# tests/test_str_methods.py

import unittest

from models.agent import Agent
from models.client import Client
from models.deal import Deal
from models.document import Document
from models.market import Market
from models.property import Property


class TestStrMethods(unittest.TestCase):
    """Тесты для методов __str__ всех моделей."""

    def test_client_str(self) -> None:
        client = Client(1, "Иван", 50000.0)
        result = str(client)
        self.assertIn("Иван", result)
        self.assertIn("50000.0", result)

    def test_agent_str(self) -> None:
        agent = Agent(1, "Мария", 10)
        result = str(agent)
        self.assertIn("Мария", result)
        self.assertIn("10", result)

    def test_property_str_available(self) -> None:
        prop = Property(1, "ул. Пушкина, 5", 80000.0, 55.0)
        result = str(prop)
        self.assertIn("Доступен", result)
        self.assertIn("ул. Пушкина, 5", result)
        self.assertIn("55.0", result)

    def test_property_str_sold(self) -> None:
        prop = Property(1, "ул. Ленина, 1", 60000.0, 30.0)
        prop.sell()
        result = str(prop)
        self.assertIn("Продан", result)

    def test_market_str_stable(self) -> None:
        market = Market("Минск", 1.0)
        result = str(market)
        self.assertIn("Стабилен", result)

    def test_market_str_growing(self) -> None:
        market = Market("Минск", 1.2)
        result = str(market)
        self.assertIn("Растет", result)

    def test_market_str_falling(self) -> None:
        market = Market("Минск", 0.8)
        result = str(market)
        self.assertIn("Падает", result)

    def test_document_str(self) -> None:
        client = Client(1, "Пётр", 100000.0)
        agent = Agent(1, "Иван", 5)
        prop = Property(1, "ул. Садовая, 10", 70000.0, 60.0)
        doc = Document(1, client, agent, prop)
        result = str(doc)
        self.assertIn("Черновик", result)
        self.assertIn("Пётр", result)
        self.assertIn("Иван", result)

    def test_document_str_signed(self) -> None:
        client = Client(1, "Пётр", 100000.0)
        agent = Agent(1, "Иван", 5)
        prop = Property(1, "ул. Садовая, 10", 70000.0, 60.0)
        doc = Document(1, client, agent, prop)
        doc.sign()
        result = str(doc)
        self.assertIn("Подписан", result)

    def test_deal_str_in_progress(self) -> None:
        client = Client(1, "Анна", 200000.0)
        agent = Agent(1, "Олег", 3)
        prop = Property(1, "Невский, 1", 100000.0, 90.0)
        deal = Deal(1, prop, client, agent, 100000.0)
        result = str(deal)
        self.assertIn("В процессе", result)
        self.assertIn("Анна", result)

    def test_deal_str_completed(self) -> None:
        client = Client(1, "Анна", 200000.0)
        agent = Agent(1, "Олег", 3)
        prop = Property(1, "Невский, 1", 100000.0, 90.0)
        deal = Deal(1, prop, client, agent, 100000.0)
        doc = Document(1, client, agent, prop)
        deal.complete(doc)
        result = str(deal)
        self.assertIn("Завершена", result)
