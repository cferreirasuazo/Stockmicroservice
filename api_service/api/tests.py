from django.test import TestCase
from api.stock_client import StockClient
from rest_framework.test import APITestCase
import json


class TestStockClient(TestCase):
    def test_stock_client(self):
        stock_code = 'aapl.us'
        test_client = StockClient()
        response = test_client.get(stock_code)
        self.assertEqual(response.get("name"), 'APPLE')

    def test_fail_stock_client(self):
        stock_code = 'meme.xxx'
        test_client = StockClient()
        self.assertRaises(ValueError, test_client.get, stock_code=stock_code)

    # def test_user_model_login(self):
    #     pass

# class TestSignUser(APITestCase):
#     def test_signup_user(self):
#         pass
    
#     def test_signin_user(self):
#         pass

#     def test_get_stock(self):
#         pass