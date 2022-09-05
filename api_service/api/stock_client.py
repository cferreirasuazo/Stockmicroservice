from django.conf import settings
import requests
class StockClient():
    def __init__(self):
        self.stock_url = settings.STOCK_SERVICE_URL +'/stocks?code={stock_code}'

    def get(self, stock_code):
        url = self.stock_url.replace('{stock_code}', stock_code)
        response = requests.get(url)

        if response.status_code == 500:
            raise ValueError(f"Invalid Stock Code: {stock_code}")
        return response.json()
        