'''
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
'''
import requests
from  pprint import pprint

# Last.fm API KEY

api_key = 'e0db9a39bfd86f85fd50b527c370cd56'

response = requests.get('http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&format=json&api_key=' + api_key)

if response.ok:

    with open('lastfm.topartists.json', 'w') as f:
        pprint(response.content.decode(encoding=response.encoding))
        f.writelines(response.content.decode(encoding=response.encoding))