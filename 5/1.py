# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re


def get_letters():
    options = webdriver.ChromeOptions()

    options.add_argument('headless')

    s = Service('./chromedriver')

    driver = webdriver.Chrome(service=s, options=options)

    driver.implicitly_wait(10)  # seconds

    print('Идем на https://mail.ru')

    driver.get('https://mail.ru')

    wait = WebDriverWait(driver, 30)

    print('Логинимся...')
    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="enter-mail-primary"]')))
    elem.send_keys(Keys.ENTER)

    popup = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'login')]")))

    driver.switch_to.frame(popup)

    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))

    elem.send_keys("study.ai_172@mail.ru")
    elem.send_keys(Keys.ENTER)

    driver.implicitly_wait(10)

    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))

    elem.send_keys("NextPassword172#")
    elem.send_keys(Keys.ENTER)

    driver.switch_to.default_content()

    refs = []

    print('Собираем ссылки', end='')
    while True:
        print('.', end='')
        elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class,"llc")]')))

        if len(refs) > 0 and len(elems) > 0:
            if refs[-1] == elems[-1].get_attribute("href"):
                break

        for i in elems:
            try:
                refs.append(i.get_attribute("href"))
            except:
                pass

        try:
            actions = ActionChains(driver)
            actions.move_to_element(elems[-1])
            actions.perform()
        except:
            pass

    print(f'\nЗакончили собирать ссылки! Собрано ссылок {len(refs)}')
    result = []

    print('Собираем содержимое писем', end='')

    for i in set(refs):

        print('.', end='')

        if i != None:
            letter = {}

            while True:
                try:
                    driver.get(i)
                    letter['ref'] = i

                    letter['id'] = re.findall("/0:(.*):0/", i)[0]

                    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="letter-contact"]')))
                    letter['from'] = elem.get_attribute('title')

                    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))
                    letter['subject'] = elem.text

                    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="letter__date"]')))
                    letter['date'] = elem.text

                    elem = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="letter-body__body-content"]')))
                    letter['text'] = elem.text

                    result.append(letter)

                    break

                except:
                    pass

    print(f'\nЗакончили собирать содержимое писем! Собрано писем {len(result)}')

    driver.quit()

    return result


def save_letters(letters_list):
    client = MongoClient('localhost', 27017)
    db = client['letters']
    letters = db.letters

    print('Сохраняем содержимое писем в БД', end='')
    for i in letters_list:
        if not letters.find_one({'id': i['id']}):
            print('.', end='')
            letters.insert_one(i)
    print('\nЗакончили сохранять содержимое писем в БД!')


letters = get_letters()

save_letters(letters)
