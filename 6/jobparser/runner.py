from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_process = CrawlerProcess(settings=crawler_settings)

    crawler_process.crawl(SjruSpider)
    crawler_process.crawl(HhruSpider)
    crawler_process.start()

'''
{'_id': 51241188,
 'name': 'Преподаватель по программированию для детей (Python)',
 'salary': ['от ', '30\xa0000', ' до ', '75\xa0000', ' ', 'руб.', ' на руки'],
 'salary_cur': 'RUR',
 'salary_max': 75000,
 'salary_min': 30000,
 'url': 'https://izhevsk.hh.ru/vacancy/51241188?from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=python'}
 {'_id': '42195294',
 'name': 'Разработчик на Python',
 'salary': ['от', '\xa0', '150\xa0000\xa0руб.'],
 'salary_cur': 'RUB',
 'salary_max': 450000,
 'salary_min': 150000,
 'url': 'https://russia.superjob.ru/vakansii/razrabotchik-na-python-42195294.html'}
'''
