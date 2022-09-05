from cgi import print_exception
from django.test import TestCase
from api.stock_client import StockClient
from rest_framework.test import APITestCase
import json
from django.urls import reverse


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



# class UnAuthenticatedAccess(APITestCase):
#     def setUp(self):
#         self.url_stock = reverse("stock")
#         self.url_history = reverse("history")
#         self.url_stats = reverse("reverse")

#     def test_request_(self):
#         response = self.client.get()
#         self.assertEqual(response.status_code,403) 
#     def test_request_(self):
#         response = self.client.get()
#         self.assertEqual(response.status_code,403)     
#     def test_request_(self):
#         response = self.client.get()
#         self.assertEqual(response.status_code,403)     
#     def test_request_(self):
#         response = self.client.get()
#         self.assertEqual(response.status_code,403) 




class TestUser(APITestCase):
    def setUp(self):
        self.new_user = {
            "email": "michael@mail.com",
            "password": "meganfox",
            "password2": "meganfox",
            "first_name": "Michael",
            "last_name": "Bay",
            "username": "michael@mail.com"
        }
        self.user_login = {
            "email": "michael@mail.com",
            "password": "meganfox"
        }

    def test_signin_user(self):
        url = reverse("signin-user")
        response = self.client.post(url, self.new_user, format='json')
        self.assertEqual(response.status_code, 201)

    def test_signup_user(self):
        url = reverse("signin-user")
        signup = self.client.post(url, self.new_user, format='json')
        signup_response = json.loads(signup.content)
        is_authenticated = self.client.login(username=self.user_login.get(
            "email"), password=self.user_login.get("password"))
        self.assertEqual(signup_response.get("email"),
                         self.user_login.get("email"))
        self.assertTrue(is_authenticated)

    def test_stock(self):
        url_signin = reverse("signin-user")
        url_stock = reverse("stock") + '?q=ACAX.US'
        
        signup = self.client.post(url_signin, self.new_user, format='json')
        signup_response =  json.loads(signup.content)
        is_authenticated = self.client.login(username=self.user_login.get(
            "email"), password=self.user_login.get("password"))
        stock_response = self.client.get(url_stock)
        stock = json.loads(stock_response.content)
        self.assertEqual(stock_response.status_code, 200)
        self.assertEqual(stock.get("symbol"), 'ACAX.US')

    def test_history(self):
        url_history = reverse("history")
        url_signin = reverse("signin-user")
        url_stock = reverse("stock") + '?q={stock_code}'
        stock_codes = ["ACEVW.US", 'ACER.US', 'DUK_A.US', 'HYMCL.US', 'LZB.US' ]
        signup = self.client.post(url_signin, self.new_user, format='json')
        signup_response =  json.loads(signup.content)
        is_authenticated = self.client.login(username=self.user_login.get(
            "email"), password=self.user_login.get("password"))
        
        for stock_code in stock_codes:
            url_stock = reverse("stock") + '?q={stock_code}'
            url = url_stock.replace("{stock_code}", stock_code )
            self.client.get(url)

        history_response = self.client.get(url_history)
        self.assertEqual(history_response.status_code, 200)

#     def test_stats(self):
#         url = reverse("stats")

