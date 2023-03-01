import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import funks
from random import randint
import re
import fake_useragent
from config import bot



#выясняем сколько найдено страниц по запросу apple
def how_much_pages_store2(headers):

  url ='https://store2.ru/catalog/apple?page=1'
  req = requests.get(url, headers=headers)
  soup = BeautifulSoup(req.text, 'lxml')
  n = soup.find_all(class_="prod-pagination__item")[-1].get_text()
  n = int(n)
  #print(n)
  return n

#бежим по страницам и берем с них 
def pars_store2(headers):

  # удаляем таблицу и создаем заново
  with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""DROP TABLE store2""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store2 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")

  i = 0   
  announce = False
  for page in range(1, how_much_pages_store2(headers)+1):
    #print('page', page)
    url = f'https://store2.ru/catalog/apple?page={page}&sort=price_desc'
  
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    all_items = soup.find_all(class_='catalog-card')
    for item in  all_items:
      try:
        name = item.find(class_="catalog-card__title").text
        url_for_record1 = item.find('a').get('href')
        url_for_record = 'https://store2.ru' + url_for_record1
        name_search = name.lower()
        name_search = f' {name_search} '
        #неразрывный пробел на обычный
        name = name.replace(' ', ' ')
        aaa = name_search.replace(' ', ' ')
        aaa = aaa.replace('(', '')
        aaa = aaa.replace(')','')
        aaa = aaa.replace(',','')
        aaa = aaa.replace('"', ' ')
        aaa = aaa.replace('/',' ')
        aaa = aaa.replace('-',' ')
        aaa = aaa.replace('|',' ')
        name_search = aaa.replace(';','')
        price = item.find('b', class_="cart-modal-count").text
        price = price.replace(' ', '')
        price = price.replace('₽', '')
        try:
          int(price)
        except Exception:
          price = price.replace('от', '')
          try:
            int(price)
          except Exception:
            continue
        #print(name, price, url_for_record)
        #print(price)
        name_split = name_search.split(' ')
        if funks.parsed_items_control(price, name_split):
          print(1)
          with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""INSERT OR REPLACE INTO store2 (name, name_for_search, price, url) VALUES (?, ?, ?, ?)""", (name, name_search, price, url_for_record))
      except IndexError as e:
            print('store2', e)
      i+=1
    time.sleep(randint(2,3))
  if announce == True:
        bot.send_message(477612946, f'Проблемы при парсинге biggek')
  return i
  
# не работает, сначала открывает главную страницу
# def pars_store2_to_find_item(search_query, useragent):
#   headers = {
#        'Accept': '*/*',
#        'User-Agent': f'{useragent.random}'
#   }
#   proxies = {
#   ''
#   }
#   query = search_query.split(' ')
#   i = 1
#   search_query = query[0]
#   while i < len(query):
#     query[i] = f'%20{query[i]}'
#     search_query = search_query + query[i]
#     i += 1
  
#   url = f'https://store2.ru/?digiSearch=true&term={search_query}&params=%7Csort%3DDEFAULT'
#   req = requests.get(url, headers=headers, proxies=proxies, timeout=(10, 27))
#   fh = open('myweb.html', 'w')
#   fh.write(req.text)
#   fh.close()
#   soup = BeautifulSoup(req.text, 'lxml')
#   all_items = soup.find_all(class_='digi-product__meta')
#   print(all_items)
#   name = all_items[0].find(class_="digi-product__label").text
#   price = soup.find('b', class_="digi-product__price").text
#   price = price.replace(' ', '')
#   price = price.replace('₽', '')
#   return name, price
