from django.test import TestCase
from stocks.stock_client import StooqClient
from rest_framework.test import APITestCase
import json
# Create your tests here.

class TestStockService(TestCase):
    def setUp(self):
        self.stock_client = StooqClient()

    def test_stock_service(self):
        stock_code = 'ACAX.US'
        response = self.stock_client.get_stock(stock_code)
        self.assertEqual(response["name"], "ALSET CAPITAL ACQUISITION")

    def test_raise_exception(self):
        invalid_stock_code = "DALL.E"
        self.assertRaises(ValueError, self.stock_client.get_stock, stock_code=invalid_stock_code)

class TestStockAPI(APITestCase):
    def test_request_stock(self):
        url = "/stocks?code=ACAX.US"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fail_request_stock(self):
        invalid_stock_code_url = "/stocks?code=DALL.E"
        response = self.client.get(invalid_stock_code_url)
        self.assertEqual(response.status_code, 500)

    def test_request_stock_body(self):
        url = "/stocks?code=ACAX.US"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data.get("name"), "ALSET CAPITAL ACQUISITION")



