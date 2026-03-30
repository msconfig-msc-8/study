import unittest

from models.market import Market
from models.property import Property
from services.valuation_service import ValuationService


class TestValuationService(unittest.TestCase):
    def test_estimate_market_value_with_market_object(self):
        property_obj = Property(1, "Улица", 100000.0, 50.0)
        market = Market("Минск", 1.15)

        estimated_value = ValuationService.estimate_market_value(
            property_obj,
            market,
        )

        self.assertEqual(estimated_value, 115000.0)
