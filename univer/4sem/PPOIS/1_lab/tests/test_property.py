# tests/test_property.py

import unittest

from models.property import Property


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.prop = Property(1, "ул. Тестовая, 1", 100000.0, 50.0)

    def test_property_initial_state(self):
        self.assertTrue(self.prop.is_available)

    def test_property_sell_success(self):
        self.prop.sell()
        self.assertFalse(self.prop.is_available)

    def test_property_sell_already_sold(self):
        self.prop.sell()

        with self.assertRaises(RuntimeError):
            self.prop.sell()
