from POICrawler.place import Place


class FoodyPlace(Place):

    def __init__(self, foody_id='', foody_rating='',
                 name='', address=None, phone='', category=None):
        super(FoodyPlace, self).__init__(name, address, phone, category)
        self.foody_id = foody_id
        self.foody_rating = foody_rating

    def get_foody_id(self):
        return self.foody_id

    def get_foody_rating(self):
        return self.foody_rating
