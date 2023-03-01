import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import funks
from random import randint
import datetime
from config import bot

#выясняем сколько найдено страниц по запросу apple
def how_much_pages_store1(headers):
  url ='https://store1.ru/catalog/'
  req = requests.get(url, headers=headers)
  soup = BeautifulSoup(req.text, 'lxml')
  n2 = soup.find_all(class_="pagination")[-1].get_text()
  n1 = n2.split('\n')
  n = int(n1[8])
  #print(n)
  return n
  
#бежим по страницам и берем с них 
def pars_store1(headers):
  
  with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""DROP TABLE store1""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store1 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
  i = 0   
  announce = False
  items_wrong = ''
  for page in range(1, how_much_pages_store1(headers)+1):
    #print('page', page)
    url = f'https://store1.ru/catalog/?sort=price&PAGEN_1={page}'
  
    req = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(req.text, 'lxml')
    all_items = soup.find_all(class_='catalog-item-choices__item')
    for item in  all_items:
      try:
        name = item.find('h4', class_="product__title").text
        price = item.find('div', class_="product__price").text
        price = price.replace(' ', '')
        price = price.replace('руб.', '')
        name_search = name.lower()
        name_search = f' {name_search} '
        aaa = name_search.replace('(', '')
        #неразрывный пробел на обычный
        name = name.replace(' ', ' ')
        aaa = aaa.replace(' ', ' ')
        aaa = aaa.replace(')','')
        aaa = aaa.replace(',',' ')
        aaa = aaa.replace('|',' ')
        aaa = aaa.replace('/',' ')
        aaa = aaa.replace('-',' ')
        aaa = aaa.replace('"', ' ')
        name_search = aaa.replace(';','')
        url_for_record1 = item.find('a').get('href')
        url_for_record = 'https://store1.ru' + url_for_record1
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
        if funks.parsed_items_control(price, name_split) and 'клавиатура' not in name_split:
          
          with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""INSERT OR REPLACE INTO store1 (name, price, name_for_search, url) VALUES (?, ?, ?, ?)""", (name, price, name_search, url_for_record))
      except IndexError as e:
             print('store1', e)
      i+=1
    print(i)
    time.sleep(randint(2,3))
  if announce == True:
        bot.send_message(477612946, f'Проблемы при парсинге store1')
        print(items_wrong)
  return i
