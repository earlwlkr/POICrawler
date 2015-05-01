class Place(object):

    def __init__(self, name='', address=None, phone='', category=None):
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

    def get_category_string(self):
        if self.category == 3:
            return 'Nhà hàng'
        if self.category == 4:
            return 'Cà phê/Kem'
        if self.category == 5:
            return 'Quán ăn'
        return 'Undefined ' + str(self.category)
