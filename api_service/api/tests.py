from cgi import print_exception
from unittest import skipIf
from django.test import TestCase, Client
from api.stock_client import StockClient
from rest_framework.test import APITestCase
import json
from django.urls import reverse
from django.conf import settings
import requests

client = Client()
stock_url = settings.STOCK_SERVICE_URL + '/stocks?code=ACEVW.US'
is_stock_service_down = True
is_skipif_message = "STOCK SERVICE DOWN"
try:
    request = requests.get(stock_url)
    is_stock_service_down = False
    if request.status_code != 200:
        is_stock_service_down = True
except:
    pass


class TestStockClient(TestCase):
    @skipIf(condition=is_stock_service_down, reason=is_skipif_message)
    def test_stock_client(self):
        stock_code = 'aapl.us'
        test_client = StockClient()
        response = test_client.get(stock_code)
        self.assertEqual(response.get("name"), 'APPLE')

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_fail_stock_client(self):
        stock_code = 'meme.xxx'
        test_client = StockClient()
        self.assertRaises(ValueError, test_client.get, stock_code=stock_code)


class UnauthenticatedAccess(APITestCase):
    @skipIf(is_stock_service_down, is_skipif_message)
    def test_request_stock(self):
        url_stock = reverse("stock")
        response = self.client.get(url_stock)
        self.assertEqual(response.status_code, 403)

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_request_history(self):
        url_history = reverse("history")
        response = self.client.get(url_history)
        self.assertEqual(response.status_code, 403)

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_request_stats(self):
        url_stats = reverse("stats")
        response = self.client.get(url_stats)
        self.assertEqual(response.status_code, 403)


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

        self.new_super_user = {
            "email": "taskmaster@mail.com",
            "password": "meganfox",
            "password2": "meganfox",
            "first_name": "Michael",
            "last_name": "Bay",
            "username": "taskmaster@mail.com",
            "is_staff": True,
            "is_superuser": True
        }

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_signin_user(self):
        url = reverse("signin-user")
        response = self.client.post(url, self.new_user, format='json')
        self.assertEqual(response.status_code, 201)

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_signup_user(self):
        url = reverse("signin-user")
        signup = self.client.post(url, self.new_user, format='json')
        signup_response = json.loads(signup.content)
        is_authenticated = self.client.login(username=self.user_login.get(
            "email"), password=self.user_login.get("password"))
        self.assertEqual(signup_response.get("email"),
                         self.user_login.get("email"))
        self.assertTrue(is_authenticated)

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_stock(self):
        url_signin = reverse("signin-user")
        url_stock = reverse("stock") + '?q=ACAX.US'

        signup = self.client.post(url_signin, self.new_user, format='json')
        signup_response = json.loads(signup.content)
        is_authenticated = self.client.login(username=self.user_login.get(
            "email"), password=self.user_login.get("password"))
        stock_response = self.client.get(url_stock)
        stock = json.loads(stock_response.content)
        self.assertEqual(stock_response.status_code, 200)
        self.assertEqual(stock.get("symbol"), 'ACAX.US')

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_history(self):
        url_history = reverse("history")
        url_signin = reverse("signin-user")
        url_stock = reverse("stock") + '?q={stock_code}'
        stock_codes = ["ACEVW.US", 'ACER.US', 'DUK_A.US', 'HYMCL.US', 'LZB.US']
        signup = self.client.post(url_signin, self.new_user, format='json')
        signup_response = json.loads(signup.content)
        is_authenticated = self.client.login(username=self.user_login.get(
            "email"), password=self.user_login.get("password"))

        for stock_code in stock_codes:
            url_stock = reverse("stock") + '?q={stock_code}'
            url = url_stock.replace("{stock_code}", stock_code)
            self.client.get(url)

        history_response = self.client.get(url_history)
        self.assertEqual(history_response.status_code, 200)

    @skipIf(is_stock_service_down, is_skipif_message)
    def test_stats(self):
        url_stats = reverse("stats")
        url_signin = reverse("signin-user")
        url_stock = reverse("stock") + '?q={stock_code}'
        stock_codes = ["ACEVW.US", "ACEVW.US", "ACEVW.US", 'HYMCL.US', 'DUK_A.US',
                       'DUK_A.US', 'HYMCL.US', 'HYMCL.US', 'NFLX.US', 'LZB.US', 'LZB.US',
                       'NFLX.US', 'DUK_A.US', 'DUK_A.US', 'HYMCL.US', 'NFLX.US',
                       'ACER.US', 'ACER.US', 'ACER.US', 'DUK_A.US', 'LZB.US', 'LZB.US',
                       'NFLX.US', 'HYMCL.US', 'HYMCL.US', 'HYMCL.US', 'HYMCL.US', 'LZB.US',
                       'LZB.US', 'LZB.US', 'NFLX.US', 'NFLX.US', 'LZB.US', 'LZB.US', 'NFLX.US']
        signup = self.client.post(url_signin, self.new_super_user, format='json')
        signup_response = json.loads(signup.content)
        is_authenticated = self.client.login(username=self.new_super_user.get(
            "username"), password=self.new_super_user.get("password"))

        for stock_code in stock_codes:
            url_stock = reverse("stock") + '?q={stock_code}'
            url = url_stock.replace("{stock_code}", stock_code)
            self.client.get(url)

        stats_response = self.client.get(url_stats)
        self.assertEqual(stats_response.status_code, 200)