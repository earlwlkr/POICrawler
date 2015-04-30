class Place(object):

    def __init__(self, name='', address='', phone='', category=''):
        self.name = name
        self.address = address
        self.phone = phone
        self.category = category

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_phone(self):
        return self.phone

    def get_category(self):
        return self.category