from datetime import datetime
from POICrawler.place import Place
from POICrawler.foody_place import FoodyPlace


class Diner(FoodyPlace):

    def __init__(self, foody_id='', foody_rating='', name='', address='', phone='',
                 category=None, cuisine='', open_time=None, close_time=None,
                 price_min=None, price_max=None):
        super(Diner, self).__init__(foody_id, foody_rating,
                                    name, address, phone, category)
        self.cuisine = cuisine
        self.open_time = open_time
        self.close_time = close_time
        self.price_min = price_min
        self.price_max = price_max

    def get_cuisine(self):
        return self.cuisine

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
