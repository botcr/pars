import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import funks
from random import randint
import re
import fake_useragent
from config import bot

proxies = {
 ''
 }

#выясняем сколько найдено страниц по запросу apple
# def how_much_pages_store4(headers, url):

#   req = requests.get(url, headers=headers, proxies=proxies, verify=False)
#   soup = BeautifulSoup(req.text, 'lxml')
#   n = soup.find_all(class_="pagination")#[-2].get_text()
#   #n = list(n)
#   print(n)
#   return n
#бежим по страницам и берем с них 
def pars_store4(headers):
  
  with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""DROP TABLE store4""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store4 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
  urls_for_pars = ('telefony_apple/', 'apple_watch_/', 'planshety_apple/', 'apple_imac/', 'apple_macbook/', 'naushniki_apple_/', 'portativnaya_akustika_apple/', 'aksessuary_dlya_apple/')
            
  i = 0
  announce = False
  for url in urls_for_pars:
    next_page = True
    p = 1
    while next_page == True:
      i_on_p = 0
      url_for_request = f'https://store4.net/{url}?pagesize=72%3FPAGEN_1%3D2&PAGEN_1={p}'
      #print('page', p, url_for_request)
      req = requests.get(url_for_request, headers=headers, proxies=proxies, verify=False)
      soup = BeautifulSoup(req.text, 'lxml')
      #is_next_page = soup.find(class_="total_num_product")
      #print('is_next_page', is_next_page)
      #if is_next_page == None:
        
      all_items = soup.find_all(class_='bp_text')
      for item in  all_items:
        try:
          name = item.find(class_="bp_text_info bp_width_fix").text
          url_for_record1 = item.find(class_="bp_text_info bp_width_fix").find('a').get('href')
          url_for_record = f'https://store4.net{url_for_record1}'
          name = name[38:]
          #неразрывный пробел на обычный
          name = name.replace(' ', ' ')
          name = name.replace('\n', '')
          name_search = name.lower()
          name_search = f' {name_search} '
          aaa = name_search.replace('(', '')
          aaa = aaa.replace(' ', ' ')
          aaa = aaa.replace(')','')
          aaa = aaa.replace(',','')
          aaa = aaa.replace('/',' ')
          aaa = aaa.replace('|',' ')
          aaa = aaa.replace('"', ' ')
          aaa = aaa.replace('-',' ')
          name_search = aaa.replace(';','')
          price = item.find(class_="bp_text_price bp_width_fix").text
          price = price.replace(' ', '')
          price = price.replace('—', '')
          try:
              int(price)
          except Exception:
              price = price.replace('от', '')
              try:
                int(price)
              except Exception:
                print(price)
                continue
          print(name, price, url_for_record)
          name_split = name_search.split(' ')
          if funks.parsed_items_control(price, name_split):
            with sqlite3.connect('pars.db', timeout=15000) as data:
              curs = data.cursor() 
              curs.execute("""INSERT OR REPLACE INTO store4 (name, name_for_search, price, url) VALUES (?, ?, ?, ?)""", (name, name_search, price, url_for_record))  
        except IndexError as e:
             print('store_77', e)
        i_on_p+=1
        i+=1
      print(i_on_p, p)
      if i_on_p < 72 or p > 7:
        next_page = False
      p+=1
      time.sleep(randint(2,4))
  if announce == True:
        bot.send_message(477612946, f'Проблемы при парсинге store4')
  return i
