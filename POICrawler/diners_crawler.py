import os
import re
import json
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

from POICrawler.diner import Diner
from POICrawler.requester import Requester
from POICrawler.address import Address


class DinerCrawler(object):

    def __init__(self):
        self.session = Requester()

    # Subclasses must implement this method,
    # return list of Diners
    def crawl(self):
        raise NotImplementedError


class FoodyVNCrawler(DinerCrawler):

    price_re = re.compile('\d+\.\d+đ')

    def __init__(self):
        super(FoodyVNCrawler, self).__init__()

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

    def parse_price(self, string):
        min_price = None
        max_price = None

        for match in self.price_re.findall(string):
            match = match.replace('.', '').replace('đ', '')

            if min_price is None:
                min_price = int(match)
            elif max_price is None:
                max_price = int(match)
            else:
                break
        return min_price, max_price

    def extract_item_info(self, item):
        foody_id = item['Id']
        name = item['Name']
        address = Address(
            item['Address'], item['District'], item['City'])

        phone_response = self.session.get(
            'http://www.foody.vn/Restaurant/GetPhoneByResId', params={'resId': foody_id})
        phone_json = json.loads(phone_response.text)
        phone = phone_json['phone']

        rating = item['AvgRating']

        try:
            cuisine = item['Cuisines'][0]['Name']
        except IndexError:
            cuisine = 'Việt Nam'

        link = 'http://www.foody.vn' + item['DetailUrl']
        print('Requesting page {}'.format(link))
        response = self.session.get(link)
        soup = BeautifulSoup(response.text)

        try:
            category = soup.find(
                'div', class_='category-items').a['title']
            open_time = self.parse_time(
                soup.find('span', attrs={'itemprop': 'opens'}).text)
            close_time = self.parse_time(
                soup.find('span', attrs={'itemprop': 'closes'}).text)

            if close_time <= open_time:
                close_time += timedelta(days=1)

            min_price, max_price = self.parse_price(soup.find(
                'span', attrs={'itemprop': 'priceRange'}).find('span').text)

        except (AttributeError, ValueError):
            print('Error with ' + link)
            return None

        return Diner(foody_id, rating, name, address, phone,
                     category, cuisine, open_time, close_time, min_price, max_price)

    def crawl(self):

        data = {
            'append': 'true',
            'c': '1,2,3,4,6,11,12,39',
            'page': 1
        }
        headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = 'http://www.foody.vn/ho-chi-minh/dia-diem'

        while True:
            response = self.session.get(url, headers=headers, params=data)
            if response.status_code != 200:
                return

            items = json.loads(response.text)['searchItems']

            for item in items:
                for sub_item in item['SubItems']:
                    extracted_info = self.extract_item_info(sub_item)
                    if extracted_info is None:
                        continue
                    yield extracted_info
                extracted_main_info = self.extract_item_info(item)
                if extracted_main_info is None:
                    continue
                yield extracted_main_info
            data['page'] += 1


# class DDAOCrawler(DinerCrawler):

#     def __init__(self):
#         super(DDAOCrawler, self).__init__()

# Returns all Diners from URL response.
# It gets link from the 'desc' div,
# goes to link and get diner's details.
#     def extract_page_data(self, response):
#         main_soup = BeautifulSoup(response.text)
#         diners = []

#         for item in main_soup.find_all('div', class_='desc'):
#             if item.h2 is None:
#                 continue

#             anchor = item.h2.a
#             link = anchor['href']

#             details_response = self.session.get(link)
#             yield self.get_diner_details(details_response)

# Returns a Diner from the details page.
#     def get_diner_details(self, details_response):
#         soup = BeautifulSoup(details_response.text)

#         name = soup.find('h1', class_='place-detail-title').string

#         description = soup.find('div', class_='desc')

#         anchor = description.find('a', class_='place-category')
#         category = anchor.string

# Has to call next_sibling 2 times because:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling
#         anchor = anchor.next_sibling.next_sibling
#         address = anchor.span.next.string.strip()

#         anchor = anchor.next_sibling.next_sibling
#         phone = anchor.span.next.string.strip()

#         anchor = description.find('div', class_='block')
#         open_time = anchor.find('ul', class_='bullet').li.string

# Skip phần comment (<!-- /.block -->)
#         anchor = anchor.next_sibling.next_sibling.next_sibling
#         price_range = anchor.find('strong').string

#         return Diner(name, address, phone,
#                      category, open_time, price_range)

#     def crawl(self):
#         data = {
#             'ajax': 1,
#             'offset': 0,
#             'areaid': 3,
#             'areaseo': 'tp-ho-chi-minh'
#         }

#         offset = 0

#         while True:
#             response = self.session.post(
#                 'http://diadiemanuong.com/location/ajaxLoadMore/', data=data)

#             if response.status_code != 200:
#                 return

#             for diner in self.extract_page_data(response):
#                 yield diner

#             offset += 10
#             data['offset'] = offset
