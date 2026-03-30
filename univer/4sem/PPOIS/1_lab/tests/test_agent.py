import unittest

from models.agent import Agent
from models.client import Client


class TestAgent(unittest.TestCase):
    def test_assign_client(self):
        agent = Agent(1, "Смит", 5)
        client = Client(1, "Нео", 10000.0)

        agent.assign_client(client)

        self.assertEqual(len(agent.clients), 1)
        self.assertEqual(agent.clients[0].name, "Нео")
