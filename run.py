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
        "category": diner.get_category(),
        "phone": diner.get_phone(),
        "cuisine": diner.get_cuisine(),
        "open_time": diner.get_open_time(),
        "close_time": diner.get_close_time(),
        "price_min": diner.get_price_min(),
        "price_max": diner.get_price_max()
    }


def main():
    LIMIT = 3000
    SAVE_TO_DATABASE = True

    if SAVE_TO_DATABASE:
        client = MongoClient()
        db = client.cityhotspots
        db.drop_collection('diners')
        diners_collection = db.diners

    diners_crawler = FoodyVNCrawler()
    out = open('example_output.txt', 'w', encoding='utf-8')
    count = 0

    for diner in diners_crawler.crawl():
        count += 1
        out.write('STT: {}'.format(count) + '\n' +
                  'Foody ID: ' + str(diner.get_foody_id()) + '\n' +
                  'Tên: ' + diner.get_name() + '\n' +
                  'Địa chỉ: ' + str(diner.get_address()) + '\n' +
                  'SĐT: ' + diner.get_phone() + '\n' +
                  'Danh mục: ' + diner.get_category() + '\n' +
                  'Nền ẩm thực: ' + diner.get_cuisine() + '\n' +
                  'Giờ mở cửa: ' + diner.get_open_time_string() + ' - ' +
                  diner.get_close_time_string() + '\n' +
                  'Khoảng giá: ' + str(diner.get_price_min()) + ' - ' +
                  str(diner.get_price_max()) + '\n\n')

        if SAVE_TO_DATABASE:
            diners_collection.insert(encode_diner(diner))

        print('{} diners collected.'.format(count))
        if count >= LIMIT:
            break
    out.close()

if __name__ == '__main__':
    main()
