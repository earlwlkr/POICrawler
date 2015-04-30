# -*- coding: utf-8 -*-
# Python code to parse news content from VnExpress RSS Feeds.
import os
import re
import traceback
from bs4 import BeautifulSoup   # external lib
import requests                 # external lib


session = requests.Session()


class Place:

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


# Lấy các thông tin:
#   - Tên
#   - Địa chỉ
#   - SDT
#   - Loại (nhà hàng, quán ăn, kem/cafe)
#   - Giờ mở cửa
#   - Giá (min, max)
def get_diner_places():
    word_re = re.compile('(\w+)', flags=re.UNICODE)
    parsed_links = []

    main_url = 'http://diadiemanuong.com/tp-ho-chi-minh/3/'
    response = session.get(main_url)
    response.encoding = 'utf-8'

    main_soup = BeautifulSoup(response.text)

    out = open('out.txt', 'w', encoding='utf-8')

    data = {
        'ajax': 1,
        'offset': 20,
        'areaid': 3,
        'areaseo': 'tp-ho-chi-minh'
    }

    next_page = session.post(
        'http://diadiemanuong.com/location/ajaxLoadMore/', data=data)
    next_page.encoding = 'utf-8'
    out.write(next_page.text)

    for item in main_soup.find_all('div', class_='desc'):
        if item.h2 is None:
            continue

        anchor = item.h2.a

        name = anchor.string
        link = anchor['href']

        details_page = session.get(link)
        details_page.encoding = 'utf-8'

        soup = BeautifulSoup(details_page.text)
        description = soup.find('div', class_='desc')

        anchor = description.find('a', class_='place-category')
        category = anchor.string

        # Phải gọi next_sibling 2 lần vì:
        # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling
        anchor = anchor.next_sibling.next_sibling
        address = anchor.span.next.string.strip()

        anchor = anchor.next_sibling.next_sibling
        phone = anchor.span.next.string.strip()

        anchor = description.find('div', class_='block')
        open_time = anchor.find('ul', class_='bullet').li.string

        # Skip phần comment (<!-- /.block -->)
        anchor = anchor.next_sibling.next_sibling.next_sibling
        price_range = anchor.find('strong').string

        diner = Diner(name, address, phone,
                      category, open_time, price_range)

        out.write(diner.get_name() + '\n' +
                  diner.get_address() + '\n' +
                  diner.get_phone() + '\n' +
                  diner.get_category() + '\n' +
                  diner.get_open_time() + '\n' +
                  diner.get_price_range() + '\n\n')

        

    out.close()
    print('Parsed a total of {0} articles.'.format(len(parsed_links)))

if __name__ == '__main__':
    get_diner_places()
