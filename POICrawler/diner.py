from POICrawler.place import Place


class Diner(Place):

    def __init__(self, name='', address='', phone='',
                 category='', open_time='', price_range=''):
        super(Diner, self).__init__(name, address, phone, category)
        self.open_time = open_time
        self.price_range = price_range

    def get_open_time(self):
        return self.open_time

    def get_price_range(self):
        return self.price_range
