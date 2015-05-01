import os
import re
import json
from bs4 import BeautifulSoup

from POICrawler.diner import Diner
from POICrawler.requester import Requester


class DinerCrawler(object):

    def __init__(self):
        self.session = Requester()

    # Subclasses must implement this method,
    # return list of Diners
    def crawl(self):
        raise NotImplementedError


class FoodyVNCrawler(DinerCrawler):

    def __init__(self):
        super(FoodyVNCrawler, self).__init__()

    def get_sub_category(self, id):
        if id == 1:
            return 'Nhà hàng'
        if id == 2:
            return 'Cà phê/Kem'
        if id == 3:
            return 'Quán ăn'
        return 'Không tìm thấy ' + str(id)

    def crawl(self):

        data = {
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

            restaurants = json.loads(response.text)['restaurants']

            for restaurant in restaurants:
                name = restaurant['Name']
                address = restaurant['Address'] + ' ' +\
                    restaurant['District'] + ' ' + restaurant['City']
                phone = restaurant['Phone']
                category = self.get_sub_category(restaurant['MainCategoryId'])

                link = 'http://www.foody.vn' + restaurant['DetailUrl']
                print('Requesting page {}'.format(link))
                response = self.session.get(link)
                soup = BeautifulSoup(response.text)
                try:
                    open_time = soup.find('span', attrs={'itemprop': 'opens'}).text + \
                        ' - ' + \
                        soup.find('span', attrs={'itemprop': 'closes'}).text

                    price_range = soup.find(
                        'span', attrs={'itemprop': 'priceRange'}).find('span').text

                except AttributeError:
                    print('Error with ' + link)
                    continue

                yield Diner(name, address, phone,
                            category, open_time, price_range)

            data['page'] += 1


# class DDAOCrawler(DinerCrawler):

#     def __init__(self):
#         super(DDAOCrawler, self).__init__()

#     # Returns all Diners from URL response.
#     # It gets link from the 'desc' div,
#     # goes to link and get diner's details.
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

#     # Returns a Diner from the details page.
#     def get_diner_details(self, details_response):
#         soup = BeautifulSoup(details_response.text)

#         name = soup.find('h1', class_='place-detail-title').string

#         description = soup.find('div', class_='desc')

#         anchor = description.find('a', class_='place-category')
#         category = anchor.string

#         # Has to call next_sibling 2 times because:
#         # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling
#         anchor = anchor.next_sibling.next_sibling
#         address = anchor.span.next.string.strip()

#         anchor = anchor.next_sibling.next_sibling
#         phone = anchor.span.next.string.strip()

#         anchor = description.find('div', class_='block')
#         open_time = anchor.find('ul', class_='bullet').li.string

#         # Skip phần comment (<!-- /.block -->)
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
