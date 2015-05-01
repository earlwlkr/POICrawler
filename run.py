from pymongo import MongoClient
from POICrawler.diners_crawler import FoodyVNCrawler
from POICrawler.diner import Diner


def encode_diner(diner):
    address = diner.get_address()
    return {
        "_type": "diner",
        "foody_id": diner.get_foody_id(),
        "name": diner.get_name(),
        "address": {
            "street_address": address.get_street_address(),
            "district": address.get_district(),
            "city": address.get_city(),
            "country": address.get_country()
        },
        "phone": diner.get_phone(),
        "open_time": diner.get_open_time(),
        "close_time": diner.get_close_time(),
        "price_min": diner.get_price_min(),
        "price_max": diner.get_price_max()
    }


def main():
    LIMIT = 1000

    client = MongoClient()
    db = client.cityhotspots

    diners_collection = db.diners

    diners_crawler = FoodyVNCrawler()
    diners_crawler.crawl()
    out = open('example_output.txt', 'w', encoding='utf-8')
    count = 0

    for diner in diners_crawler.crawl():
        count += 1
        out.write('STT: {}'.format(count) + '\n')
        out.write('Foody ID: ' + str(diner.get_foody_id()) + '\n' +
                  'Tên: ' + diner.get_name() + '\n' +
                  'Địa chỉ: ' + str(diner.get_address()) + '\n' +
                  'SĐT: ' + diner.get_phone() + '\n' +
                  'Danh mục: ' + diner.get_category_string() + '\n' +
                  'Giờ mở cửa: ' + diner.get_open_time_string() + ' - ' +
                  diner.get_close_time_string() + '\n' +
                  'Khoảng giá: ' + str(diner.get_price_min()) + ' - ' +
                  str(diner.get_price_max()) + '\n\n')

        diners_collection.insert(encode_diner(diner))

        print('{} diners collected.'.format(count))
        if count >= LIMIT:
            break
    out.close()


if __name__ == '__main__':
    main()
