import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json
from bs4 import BeautifulSoup
import re


class SjruSpider(scrapy.Spider):

    name = 'sjru'
    allowed_domains = ['russia.superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@href,'/vakansii/') and @target='_blank']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        salary_min_value = None
        salary_max_value = None
        salary_cur_value = None

        salary_value = response.xpath("//span[@class='_2Wp8I _3qB1R W89ts p-uEO']//text()").getall()
        url_value = response.url
        name_value = response.css('h1::text').get()
        _id_value = re.findall("-(\d+).html", response.url)[0]

        dom = BeautifulSoup(response.text, 'html.parser')
        s = dom.findAll('script', {'type': 'application/ld+json'})

        for i in s:
            j = json.loads(i.text)
            if j.get('@type') == 'JobPosting':

                if 'baseSalary' in j:
                    if 'value' in j['baseSalary']:
                        salary_min_value = j.get('baseSalary').get('value').get('minValue')
                        salary_max_value = j.get('baseSalary').get('value').get('maxValue')
                    salary_cur_value = j.get('baseSalary').get('currency')

                break

        yield JobparserItem(_id=_id_value, url=url_value, name=name_value, salary=salary_value,
                            salary_min=salary_min_value, salary_max=salary_max_value, salary_cur=salary_cur_value)