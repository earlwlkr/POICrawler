from POICrawler.diners_crawler import FoodyVNCrawler

def main():
    LIMIT = 500

    diners_crawler = FoodyVNCrawler()
    diners_crawler.crawl()
    out = open('example_output.txt', 'w', encoding='utf-8')
    count = 0
    for diner in diners_crawler.crawl():
        out.write(diner.get_name() + '\n' +
                  diner.get_address() + '\n' +
                  diner.get_phone() + '\n' +
                  diner.get_category() + '\n' +
                  diner.get_open_time() + '\n' +
                  diner.get_price_range() + '\n\n')
        count += 1
        print('{} diners collected.'.format(count))
        if count >= LIMIT:
            break
    out.close()


if __name__ == '__main__':
    main()
