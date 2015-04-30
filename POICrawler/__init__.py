from POICrawler.diners_crawler import DDAOCrawler


def main():
    ddao_crawler = DDAOCrawler()
    out = open('example_output.txt', 'w', encoding='utf-8')
    for diner in ddao_crawler.crawl():
        out.write(diner.get_name() + '\n' +
                  diner.get_address() + '\n' +
                  diner.get_phone() + '\n' +
                  diner.get_category() + '\n' +
                  diner.get_open_time() + '\n' +
                  diner.get_price_range() + '\n\n')
    out.close()
