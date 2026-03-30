import unittest

from models.agent import Agent
from models.client import Client
from models.property import Property
from services.viewing_service import ViewingService


class TestViewingService(unittest.TestCase):
    def test_arrange_viewing_sold_property(self):
        client = Client(1, "Покупатель", 10000.0)
        agent = Agent(1, "Агент", 2)
        prop = Property(1, "Квартира", 50000.0, 40.0)

        prop.sell()

        with self.assertRaises(ValueError):
            ViewingService.arrange_viewing(client, agent, prop)
