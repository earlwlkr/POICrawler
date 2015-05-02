from pymongo import MongoClient


def main():
    client = MongoClient()
    db = client.cityhotspots
    diners_collection = db.diners

    out = open('STATS.md', 'w', encoding='utf-8')
    cuisines = []
    diners_per_district = {}

    for diner in diners_collection.find():
        if diner['cuisine'] not in cuisines:
            cuisines.append(diner['cuisine'])

        district = diner['address']['district']
        diners_per_district[
            district] = diners_per_district.get(district, 0) + 1

    out.write('## Các nền ẩm thực\n')
    for cuisine in cuisines:
        out.write(cuisine + '\n')
    out.write('\n')

    out.write('## Số quán ăn mỗi quận\n')
    for item in diners_per_district.items():
        out.write(item[0] + ': ' + str(item[1]) + '\n')

    out.close()


if __name__ == '__main__':
    main()
