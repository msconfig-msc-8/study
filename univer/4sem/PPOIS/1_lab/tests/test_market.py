import unittest

from models.market import Market


class TestMarket(unittest.TestCase):
    def test_update_trend_success(self):
        market = Market("Москва", 1.0)
        market.update_trend(1.2)  # Цены выросли на 20%
        self.assertEqual(market.trend_multiplier, 1.2)

    def test_negative_trend_error(self):
        market = Market("Москва", 1.0)
        with self.assertRaises(ValueError):
            market.update_trend(-0.5)
