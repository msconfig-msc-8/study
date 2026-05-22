import tempfile
import unittest
from pathlib import Path

from models.agency import Agency
from models.agent import Agent
from models.client import Client
from models.market import Market
from models.property import Property
from services.deal_service import DealService
from storage.json_storage import backup_data_file, load_agency, save_agency


class TestJsonStorage(unittest.TestCase):
    def test_save_and_load_agency_state(self):
        agency = Agency("Test Agency", Market("Минск", 1.15))
        agency.add_agent(Agent(1, "Agent One", 3))
        agency.add_client(Client(1, "Client One", 100000.0))
        agency.add_property(Property(1, "Test address", 40000.0, 45.0))

        deal = DealService.make_deal(
            1,
            agency.get_client_by_id(1),
            agency.get_agent_by_id(1),
            agency.get_property_by_id(1),
        )
        agency.add_deal(deal)
        agency.add_document(deal.document)

        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "data.json"
            save_agency(agency, data_file)
            loaded_agency = load_agency(data_file)

        self.assertEqual(loaded_agency.name, "Test Agency")
        self.assertEqual(loaded_agency.market.trend_multiplier, 1.15)
        self.assertEqual(loaded_agency.clients[0].budget, 60000.0)
        self.assertFalse(loaded_agency.properties[0].is_available)
        self.assertEqual(len(loaded_agency.deals), 1)
        self.assertTrue(loaded_agency.deals[0].is_completed)
        self.assertIsNotNone(loaded_agency.deals[0].document)
        self.assertEqual(loaded_agency.deals[0].client.name, "Client One")
        self.assertEqual(loaded_agency.deals[0].agent.name, "Agent One")
        self.assertEqual(
            loaded_agency.deals[0].property_obj.address,
            "Test address",
        )

    def test_backup_data_file_moves_broken_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "data.json"
            data_file.write_text("{broken json", encoding="utf-8")

            backup_file = backup_data_file(data_file)

            self.assertFalse(data_file.exists())
            self.assertTrue(backup_file.exists())
            self.assertIn("data_broken_", backup_file.name)
            self.assertEqual(
                backup_file.read_text(encoding="utf-8"),
                "{broken json",
            )


if __name__ == "__main__":
    unittest.main()
