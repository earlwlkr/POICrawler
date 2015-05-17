from pymongo import MongoClient


def main():
    client = MongoClient()
    db = client.cityhotspots
    db.drop_collection('dineroptions')
    diners_collection = db.diners

    doc = {}
    diner_options_collection = db.dineroptions
    doc['categories'] = diners_collection.distinct('category')
    doc['cuisines'] = diners_collection.distinct('cuisine')
    doc['districts'] = diners_collection.distinct('address.district')
    diner_options_collection.insert(doc)


if __name__ == '__main__':
    main()
