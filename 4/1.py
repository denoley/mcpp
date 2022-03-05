# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника; +
# наименование новости;+
# ссылку на новость; +
# дата публикации. +
# Сложить собранные новости в БД
# Минимум один сайт, максимум - все три

import requests
from lxml import html
from pymongo import MongoClient


def read_lenta_news():
    '''
    Чтение новостей из Ленты
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Safari/537.35'}

    response = requests.get('https://lenta.ru/', headers=headers)

    dom = html.fromstring(response.text)
    items = dom.xpath("//a[contains(@class,'_topnews')]")

    items_list = []
    for item in items:
        item_info = {}

        item_info['source'] = 'lenta'
        item_info['title'] = item.xpath(".//span/text()|.//h3/text()")[0]
        item_info['ref'] = 'lenta.ru' + item.xpath(".//@href")[0]
        item_info['time'] = item.xpath(".//time/text()")[0]

        items_list.append(item_info)

    return items_list


def read_yandex_news():
    '''
    Чтение новостей из Ленты
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Safari/537.35'}

    response = requests.get('https://yandex.ru/news/', headers=headers)

    dom = html.fromstring(response.text)
    items = dom.xpath("//div[contains(@class,'news-top-flexible-stories')]/div")

    items_list = []
    for item in items:
        item_info = {}

        item_info['source'] = 'yandex'
        item_info['title'] = item.xpath(".//div[contains(@class,'card__annotation')]/text()")[0]
        item_info['ref'] = item.xpath(".//h2/a/@href")[0]
        item_info['time'] = item.xpath(".//span[contains(@class,'time')]/text()")[0]

        items_list.append(item_info)

    return items_list


def save_news(news):
    '''
    Сохраняем новости
    :param news: словарь с новостями
    :return:
    '''
    client = MongoClient('localhost', 27017)
    db = client['news']
    news_collection = db.news

    for i in news:
        if not news_collection.find_one({'title': i['title']}):
            news_collection.insert_one(i)
            print('Запсь', i['title'], 'добавлена в БД')


save_news(read_lenta_news())

save_news(read_yandex_news())
