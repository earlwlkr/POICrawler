import os
import re
import json
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

from POICrawler.cinema import Cinema
from POICrawler.requester import Requester
from POICrawler.address import Address


class CinemaCrawler(object):

    price_re = re.compile('\d+\.\d+đ')

    def __init__(self):
        self.session = Requester()

    # Chuyển giờ thành datetime (ví dụ 08:00 AM, 8am, ...)
    def parse_time(self, string):
        time = None
        try:
            time = datetime.strptime(string, '%I:%M %p')
        except ValueError:
            try:
                time = datetime.strptime(string, '%I%p')
            except ValueError:
                try:
                    time = datetime.strptime(string, '%I:%M%p')
                except ValueError:
                    time = datetime.strptime(string, '%I:%M')
        return time

    def extract_item_info(self, item):
        foody_id = item['Id']
        print('Getting cinema id ' + str(foody_id))
        name = item['Name']
        address = Address(
            item['Address'], item['District'], item['City'])

        phone_response = self.session.get(
            'http://www.foody.vn/Restaurant/GetPhoneByResId', params={'resId': foody_id})
        phone_json = json.loads(phone_response.text)
        phone = phone_json['phone']

        category = 'Rạp chiếu phim'

        trademark = ''
        if '-' in name:
            trademark = name.split('-')[0].strip()

        link = 'http://www.foody.vn' + item['DetailUrl']
        rating = item['AvgRating']

        return Cinema(foody_id, rating, trademark, name, address, phone, category)

    def crawl(self):

        data = {
            'append': 'true',
            'c': '13'
        }
        headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = 'http://www.foody.vn/ho-chi-minh/dia-diem'

        response = self.session.get(url, headers=headers, params=data)
        if response.status_code != 200:
            return

        items = json.loads(response.text)['restaurants']

        for item in items:
            for sub_item in item['SubItems']:
                yield self.extract_item_info(sub_item)
            yield self.extract_item_info(item)

