# test_services/test_search_service.py

import unittest

from models.property import Property
from services.search_service import SearchService


class TestSearchService(unittest.TestCase):
    def setUp(self):
        self.prop1 = Property(1, "Дешевая", 30000.0, 30.0)
        self.prop2 = Property(2, "Дорогая", 150000.0, 100.0)
        self.prop3 = Property(3, "Средняя", 70000.0, 60.0)

        self.prop1.sell()
        self.all_properties = [self.prop1, self.prop2, self.prop3]

    def test_find_properties_by_price(self):
        found = SearchService.find_properties(
            self.all_properties,
            max_price=100000.0,
        )

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].address, "Средняя")

    def test_find_properties_by_area(self):
        found = SearchService.find_properties(
            self.all_properties,
            min_area=80.0,
        )

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].address, "Дорогая")
