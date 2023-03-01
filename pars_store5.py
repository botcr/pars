import requests
import json
import time
import sqlite3
import funks
from random import randint
import re
import fake_useragent
from config import bot

#city 4 == Владивосток
proxies = {
 ''
 }



  
#бежим по страницам и берем с них 
def pars_store5(headers):
  
  with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""DROP TABLE store5""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store5 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
  i = 0
  announce = False
  is_next_page = True
    # p=1
  offset = 0
  while is_next_page == True:
      
      url_for_request = f'https://store5.ru/api/v1/products/?limit=960&offset={offset}&ordering=-has_ordering_priority,-ordering_is_available_in_city,-ordering_weight,-ordering_is_available,price'
      req = requests.get(url_for_request, headers=headers, proxies=proxies)
      items_data = req.json()
      if items_data.get('next') == None:
        is_next_page = False
      #print(items_data.get('next'))
      items = items_data.get('results')
      # try:  
      #   n = soup.find_all(class_="page-numbers")[-1].get_text()
      # except IndexError:  
      #   is_next_page = False
      # if '→' not in n:
      #   is_next_page = False
      
      
        #print(items)
      for item in items:
        try:
          name = item.get('name')
          url_for_record1 = item.get('id')
          url_for_record = 'https://store5.ru/product/' + str(url_for_record1)
          name_search = name.lower()
          name_search = f' {name_search} '
          aaa = name_search.replace('(', '')
          aaa = aaa.replace(')','')
          #неразрывный пробел на обычный
          name = name.replace(' ', ' ')
          aaa = aaa.replace(' ', ' ')
          aaa = aaa.replace(',','')
          aaa = aaa.replace('|',' ')
          aaa = aaa.replace('"', ' ')
          aaa = aaa.replace('/',' ')
          aaa = aaa.replace('-',' ')
          name_search = aaa.replace(';','')
          prices = item.get('prices')
          price = str(prices[0].get('price'))
          price = price.replace(' ', '')
          price = price.replace('.0', '')
          try:
              int(price)
          except Exception:
              price = price.replace('от', '')
              try:
                int(price)
              except Exception:
                print(price)
                continue
          # price = price.replace(',', '')
          #print(name, price, url_for_record)
          name_split = name_search.split(' ')
          if funks.parsed_items_control(price, name_split):
            if ('клавиатура' not in name_split and int(price) <= 32000) or int(price) > 32000:
               # print(name, price, url_for_record)
                with sqlite3.connect('pars.db', timeout=15000) as data:
                  curs = data.cursor()
                  curs.execute("""INSERT OR REPLACE INTO store5 (name, name_for_search, price, url) VALUES (?, ?, ?, ?)""", (name, name_search, int(price), url_for_record))
                
        except IndexError as e:
             print('store5', e)    
        i+=1
      offset+=960
          
      time.sleep(randint(2,6))
  print(i)
  return i
