from POICrawler.diners_crawler import DDAOCrawler


def main():
    ddao_crawler = DDAOCrawler()
    diners = ddao_crawler.crawl()

    out = open('example_output.txt', 'w', encoding='utf-8')
    for diner in diners:
        out.write(diner.get_name() + '\n' +
                  diner.get_address() + '\n' +
                  diner.get_phone() + '\n' +
                  diner.get_category() + '\n' +
                  diner.get_open_time() + '\n' +
                  diner.get_price_range() + '\n\n')
    out.close()
