from pymongo import MongoClient


def main():
    client = MongoClient()
    db = client.cityhotspots
    db.drop_collection('dineroptions')
    diners_collection = db.diners

    doc = {}
    diner_options_collection = db.dineroptions
    doc['categories'] = diners_collection.distinct('category')
    doc['categories'].insert(0, 'Tất cả')
    doc['cuisines'] = diners_collection.distinct('cuisine')
    doc['cuisines'].insert(0, 'Tất cả')
    doc['districts'] = diners_collection.distinct('address.district')
    doc['districts'].insert(0, 'Tất cả')

    doc['price_max'] = diners_collection.find_one(sort=[("price_max", -1)])['price_max']
    doc['price_min'] = diners_collection.find_one(sort=[("price_min", 1)])['price_min']

    diner_options_collection.insert(doc)


if __name__ == '__main__':
    main()
