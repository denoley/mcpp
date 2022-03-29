from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lmparser import settings
from lmparser.spiders.lmspider import LmspiderSpider



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmspiderSpider)

    process.start()

'''
{'description': ['Продам оригинальные наушники на айфон, качают хорошо не '
                 'порваные, целые. Торга нет цена окончательная! Новые стоят '
                 '10к. Играют как эирподсы оригинальные наушники от айфона'],
 'name': 'Наушники Apple оригинал не дорого',
 'photos': ['https://frankfurt.apollo.olxcdn.com:443/v1/files/6rqbw0yybah21-KZ/image;s=1062x1416',
            'https://frankfurt.apollo.olxcdn.com:443/v1/files/90f41zmk39mk2-KZ/image;s=1416x1062'],
 'price': 5000,
 'url': 'https://www.olx.kz/d/obyavlenie/naushniki-apple-original-ne-dorogo-IDm5hEG.html'}
'''