from POICrawler.diners_crawler import FoodyVNCrawler

def main():
    LIMIT = 2

    diners_crawler = FoodyVNCrawler()
    diners_crawler.crawl()
    out = open('example_output.txt', 'w', encoding='utf-8')
    count = 0
    for diner in diners_crawler.crawl():
        count += 1
        out.write('STT: {}'.format(count) + '\n')
        out.write('Tên: ' + diner.get_name() + '\n' +
                  'Địa chỉ: ' + str(diner.get_address()) + '\n' +
                  'SĐT: ' + diner.get_phone() + '\n' +
                  'Danh mục: ' + diner.get_category_string() + '\n' +
                  'Giờ mở cửa: ' + diner.get_open_time_string() + ' - ' +
                  diner.get_close_time_string() + '\n' +
                  'Khoảng giá: ' + str(diner.get_price_min()) + ' - ' +
                  str(diner.get_price_max()) + '\n\n')

        print('{} diners collected.'.format(count))
        if count >= LIMIT:
            break
    out.close()


if __name__ == '__main__':
    main()
