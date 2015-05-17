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

    doc['max_price'] = list(diners_collection.aggregate([{
        "$group":
            {
                "_id": None,
                "max": {"$max": "$price_max"}
            }
    }]))[0]['max']
    doc['min_price'] = list(diners_collection.aggregate([{
        "$group":
            {
                "_id": None,
                "min": {"$min": "$price_min"}
            }
    }]))[0]['min']
    
    diner_options_collection.insert(doc)


if __name__ == '__main__':
    main()
