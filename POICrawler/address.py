class Address(object):

    def __init__(self, street_address, district, city):
        self.street_address = street_address
        self.district = district
        self.city = city
        self.country = "Vietnam"

    def get_street_address(self):
        return self.street_address

    def get_district(self):
        return self.district

    def get_city(self):
        return self.city

    def get_country(self):
        return self.country

    def __str__(self):
        return self.street_address + ' ' + self.district + ', ' + self.city
