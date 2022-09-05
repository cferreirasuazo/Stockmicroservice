import requests
import csv
from contextlib import closing


#TODO formatear data aqui

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

    def get_stock(self, stock_code):
        url = self.get_stock_url(stock_code)
        response = []
        stock = {}
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                response.append(row)
            values = response[1]
            
            if 'N/D' in values:
                raise ValueError(f'Invalide Stock Code {stock_code}')

            for x, z in enumerate(values):
                stock[self.stock_keys[x].lower()] = z
        return stock
