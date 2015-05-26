from datetime import datetime
from POICrawler.place import Place
from POICrawler.foody_place import FoodyPlace


class Cinema(FoodyPlace):

    def __init__(self, foody_id='', foody_rating='', trademark='',
                 name='', address=None, phone='',
                 category=None):
        super(Cinema, self).__init__(foody_id, foody_rating,
                                     name, address, phone, category)
        self.trademark = trademark

    def get_trademark(self):
        return self.trademark
