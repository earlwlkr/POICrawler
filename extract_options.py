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

    doc['price_max'] = list(diners_collection.aggregate([{
        "$group":
            {
                "_id": None,
                "value": {"$max": "$price_max"}
            }
    }]))[0]['value']
    doc['price_min'] = list(diners_collection.aggregate([{
        "$group":
            {
                "_id": None,
                "value": {"$min": "$price_min"}
            }
    }]))[0]['value']

    diner_options_collection.insert(doc)


if __name__ == '__main__':
    main()
