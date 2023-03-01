import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import funks
from random import randint
from config import bot

#выясняем сколько найдено страниц по запросу apple
def how_much_pages_store6(headers):
  url ='https://store6.ru/catalog'
  req = requests.get(url, headers=headers)
  soup = BeautifulSoup(req.text, 'lxml')
  n = soup.find_all(class_="pagination__link")[-1].get_text()
  n = int(n)
  #print(n)
  return n

#бежим по страницам и берем с них 
def pars_apple_store6(headers):
  
  with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""DROP TABLE store6""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store6 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
  i = 0       
  announce = False
  for page in range(1, how_much_pages_store6(headers)+1):
   # print('page', page)
    url = f'https://store6.ru/catalog?a%5BpriceMin%5D=150&a%5BpriceMax%5D=184880&s=-price&page={page}'
  
    req = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(req.text, 'lxml')
    all_items = soup.find_all(class_='product_item__content')
    for item in  all_items:
      try:
        name = item.find(class_="product_item__title product_item__title--watched").text
        price = item.find(class_="price__item").text
        price = price.replace(' ', '')
        price = price.replace('₽', '')
        url_for_record1 = item.find('a').get('href')
        url_for_record = 'https://store6.ru' + url_for_record1
        name_search = name.lower()
        name_search = f' {name_search} '
        aaa = name_search.replace('(', '')
        #неразрывный пробел на обычный
        name = name.replace(' ', ' ')
        aaa = aaa.replace(' ', ' ')
        aaa = aaa.replace(')','')
        aaa = aaa.replace(',','')
        aaa = aaa.replace('|',' ')
        aaa = aaa.replace('"', ' ')
        aaa = aaa.replace('-',' ')
        aaa = aaa.replace('/',' ')
        name_search = aaa.replace(';','')
        try:
              int(price)
        except Exception:
              price = price.replace('от', '')
              try:
                int(price)
              except Exception:
                print(price)
                continue
        #print(name, price, url_for_record)
        name_split = name_search.split(' ')
        if funks.parsed_items_control(price, name_split):
          with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""INSERT OR REPLACE INTO store6 (name, price, name_for_search, url) VALUES (?, ?, ?, ?)""", (name, price, name_search, url_for_record))
      except IndexError as e:
             print('store6', e)
      i+=1
    time.sleep(randint(3,7))
  if announce == True:
        bot.send_message(477612946, f'Проблемы при парсинге store6')
  return i
