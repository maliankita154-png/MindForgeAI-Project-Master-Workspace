import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from app import create_app


class AetheraAppTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_public_pages_render(self):
        for route in ["/", "/dashboard", "/rainfall", "/demand", "/reservoir", "/digital-twin", "/sustainability", "/about"]:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, route)
            self.assertIn(b"AETHERA", response.data, route)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_overview_reads_the_csv_practice_dataset(self):
        response = self.client.get("/api/overview")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data_label"], "Synthetic CSV practice data")
        self.assertGreater(response.json["rainfall"], 0)

    def test_digital_twin_returns_bounded_values(self):
        response = self.client.post("/api/twin/simulate", json={"drought": 90, "growth": 40, "conservation": 30})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(0 <= response.json["availability"] <= 100)
        self.assertTrue(0 <= response.json["resilience"] <= 100)
