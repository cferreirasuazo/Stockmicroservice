import requests
import csv
from contextlib import closing
from .entities.Stock import Stock

# TODO formatear data aqui


class StooqClient():
    def __init__(self):
        self.stooq_url = "http://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv​"
        self.stock_keys = {
            0: "Symbol",
            1: "Date",
            2: "Time",
            3: "Open",
            4: "High",
            5: "Low",
            6: "Close",
            7: "Volume",
            8: "Name"
        }

    def get_stock_url(self, stock_code):
        stock_url = self.stooq_url.replace("{stock_code}", stock_code)
        return stock_url

    def get_stock_from_csv(self, url):
        response = []
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                response.append(row)

        return response[1]

    def format_stock(self, values):
        stock_values = {}
        for x, z in enumerate(values):
            stock_values[self.stock_keys[x].lower()] = z

        stock = Stock(symbol=stock_values.get("symbol"),
                      date=stock_values.get("date"),
                      time=stock_values.get("time"),
                      open=stock_values.get("open"),
                      high=stock_values.get("high"),
                      low=stock_values.get("low"),
                      close=stock_values.get("close"),
                      volume=stock_values.get("volume"),
                      name=stock_values.get("name"))

        return stock.to_dict()

    def get_stock(self, stock_code):
        url = self.get_stock_url(stock_code)
        values = self.get_stock_from_csv(url)
        if 'N/D' in values:
            raise ValueError(f'Invalide Stock Code: {stock_code}')

        stock = self.format_stock(values)
        return stock
