from datetime import datetime
from POICrawler.place import Place


class Diner(Place):

    def __init__(self, foody_id=None, name='', address='', phone='',
                 category=None, open_time=None, close_time=None,
                 price_min=None, price_max=None):
        super(Diner, self).__init__(name, address, phone, category)
        self.foody_id = foody_id
        self.open_time = open_time
        self.close_time = close_time
        self.price_min = price_min
        self.price_max = price_max

    def get_foody_id(self):
        return self.foody_id

    def get_open_time(self):
        return self.open_time

    def get_open_time_string(self):
        return datetime.strftime(self.open_time, '%H:%M')

    def get_close_time(self):
        return self.close_time

    def get_close_time_string(self):
        return datetime.strftime(self.close_time, '%H:%M')

    def get_price_min(self):
        return self.price_min

    def get_price_max(self):
        return self.price_max
