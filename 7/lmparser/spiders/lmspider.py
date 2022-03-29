import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmspiderSpider(scrapy.Spider):
    name = 'lmspider'
    allowed_domains = ['www.olx.kz']
    start_urls = ['https://www.olx.kz/elektronika/audiotehnika/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//table[@summary='Объявление']//a[@data-cy='listing-ad-title']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):

        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//div[@data-testid='ad-price-container']/h3/text()[1]")
        loader.add_xpath("description", "//div[@data-cy='ad_description']/div/text()")
        loader.add_xpath("photos", "//div[@data-cy='adPhotos-swiperSlide']//img/@data-src|//div[@data-cy='adPhotos-swiperSlide']//img/@src")

        yield loader.load_item()