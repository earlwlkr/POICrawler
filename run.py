from pymongo import MongoClient
from POICrawler.diners_crawler import FoodyVNCrawler
from POICrawler.cinemas_crawler import CinemaCrawler
from POICrawler.diner import Diner


def encode_diner(diner):
    address = diner.get_address()
    return {
        "_type": "diner",
        "foody_id": diner.get_foody_id(),
        "rating": diner.get_foody_rating(),
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


def encode_cinema(cinema):
    address = cinema.get_address()
    return {
        "_type": "cinema",
        "foody_id": cinema.get_foody_id(),
        "rating": cinema.get_foody_rating(),
        "name": cinema.get_name(),
        "address": {
            "street_address": address.get_street_address(),
            "district": address.get_district(),
            "city": address.get_city(),
            "country": address.get_country()
        },
        "category": cinema.get_category(),
        "phone": cinema.get_phone(),
        "trademark": cinema.get_trademark()
    }


def main():
    DINERS_LIMIT = 28000
    crawl_diners(DINERS_LIMIT)
    crawl_cinemas


def crawl_diners(limit):
    client = MongoClient()
    db = client.cityhotspots
    db.drop_collection('diners')
    diners_collection = db.diners

    diners_crawler = FoodyVNCrawler()
    count = 0

    for diner in diners_crawler.crawl():
        count += 1

        obj = encode_diner(diner)
        diners_collection.replace_one(
            {'foody_id': diner.get_foody_id()}, obj, upsert=True)

        print('{} diners collected.'.format(count))
        if count >= limit:
            break


def crawl_cinemas():
    client = MongoClient()
    db = client.cityhotspots
    db.drop_collection('cinemas')
    cinemas_collection = db.cinemas

    cinemas_crawler = CinemaCrawler()
    for cinema in cinemas_crawler.crawl():
        obj = encode_cinema(cinema)
        cinemas_collection.replace_one(
            {'foody_id': cinema.get_foody_id()}, obj, upsert=True)


if __name__ == '__main__':
    main()
