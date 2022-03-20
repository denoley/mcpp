# import salary as salary
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json
from bs4 import BeautifulSoup


class HhruSpider(scrapy.Spider):

    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://izhevsk.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=python',
        'https://izhevsk.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        _id_value = None
        salary_min_value = None
        salary_max_value = None
        salary_cur_value = None

        salary_value = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url_value = response.url
        name_value = response.css('h1::text').get()

        dom = BeautifulSoup(response.text, 'html.parser')
        s = dom.find('script', {'type': 'application/ld+json'})
        j = json.loads(s.text)

        if 'baseSalary' in j:
            if 'value' in j['baseSalary']:
                salary_min_value = j.get('baseSalary').get('value').get('minValue')
                salary_max_value = j.get('baseSalary').get('value').get('maxValue')
            salary_cur_value = j.get('baseSalary').get('currency')
        _id_value = j.get('identifier').get('value')

        yield JobparserItem(_id=_id_value, url=url_value, name=name_value, salary=salary_value,
                            salary_min=salary_min_value, salary_max=salary_max_value, salary_cur=salary_cur_value)
