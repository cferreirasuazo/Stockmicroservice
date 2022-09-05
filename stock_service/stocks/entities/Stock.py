import datetime
class Stock():
    def __init__(self, symbol, date, time, open, high, low, close, volume, name):
        self.symbol = symbol
        self.date = date
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.name = name

        self.date_format = '%Y-%m-%d %H:%M:%S'

    def parsed_date(self):
        datetime_str = self.date + " " + self.time
        date_time_object = datetime.datetime.strptime(
            datetime_str, self.date_format)
        return date_time_object

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "name": self.name
        }
