# tests/test_client.py

import unittest

from models.client import Client


class TestClient(unittest.TestCase):
    def test_client_creation_success(self):
        client = Client(1, "Иван", 50000.0)

        self.assertEqual(client.name, "Иван")
        self.assertEqual(client.budget, 50000.0)

    def test_client_negative_budget(self):
        with self.assertRaises(ValueError):
            Client(2, "Должник", -1000.0)
