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
def how_much_pages_store3(headers, url):
  final_url = f'https://cmstore.ru/catalog/{url}'
  req = requests.get(final_url, headers=headers, proxies=proxies, verify=False)
  soup = BeautifulSoup(req.text, 'lxml')
  try:
    n2 = soup.find(class_="paggination x12")
    print(n2)
    n = n2.find_all("p")[-1].get_text()
    print(n)
    n = int(n)
  except (IndexError, AttributeError):  
    n=1
  return n
  
#бежим по страницам и берем с них 
def pars_store3(headers):
  
  with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""DROP TABLE store3""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store3 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
  urls_for_pars = ('naushniki_i_kolonki/naushniki/apple_airpods/', 'umnye_chasy_i_fitnes_braslety/umnye_chasy/apple/' , 'smartfony/apple/', 'noutbuki_i_planshety/monobloki_apple/', 'noutbuki_i_planshety/planshety_apple/', 'noutbuki_i_planshety/noutbuki_apple/', 'aksessuary/aksessuary_dlya_televizora/', 'naushniki_i_kolonki/naushniki/nakladnye_i_polnorazmernye_naushniki/apple/')
            
  i = 0
  announce = False
  items_wrong = ''
  for url in urls_for_pars:
    is_break = False
    first_item = None
    p=1
    for page in range(1, 1000):
      #url_for_request = f'https://cmstore.ru/catalog/{url}?PAGEN_1={page}'
     # print(url_for_request)
      req = requests.get("https://utp.sberbank-ast.ru/Bankruptcy/NBT/BidView/11/0/0/20610402", headers=headers, proxies=proxies)
      soup = BeautifulSoup(req.text, 'lxml')
      fh = open('myweb.html', 'w')
      fh.write(req.text)
      fh.close()
      # print(1)
     
    
      #prices = soup.find_all(class_="newPrice")
        #print(is_next_page, p)
      items = soup.find_all(class_="item x3 lg4 md3 xmd4 sm6")
      items1 = soup.find_all(class_="item md4 sm6")
      if items == []:
        items = items1
      print(items, items1)
      #print(items)
      for item in items:
          try:
            name = item.find(class_='hideFixBlock').text
            #print(name)
            url_for_record = item.find('a').get('href')
            price = item.find(class_="newPrice").text
            url_for_record =  'https://cmstore.ru' + url_for_record
            name = name.replace(' ', ' ')
            name = name.replace('\n', ' ')
            name_search = name.lower()
            name_search = f' {name_search} '
            aaa = name_search.replace('(', '')
            #неразрывный пробел на обычный
            aaa = aaa.replace(' ', ' ')
            aaa = aaa.replace(')','')
            aaa = aaa.replace(',','')
            aaa = aaa.replace('/',' ')
            aaa = aaa.replace('|',' ')
            aaa = aaa.replace('-',' ')
            name_search = aaa.replace(';','')
            price = price.replace(' ', '')
            price = price.replace(' ', '')
            price = price.replace('₽', '')
            price = price.replace('.00', '')
            price = price.replace(',', '')
            try:
              int(price)
            except Exception:
              price = price.replace('от', '')
              try:
                int(price)
              except Exception:
                print("error", price)
                continue
            #записываем 1 товар и сверяем с ним все остальные
            if first_item == None:
              first_item = name
            else:
              if first_item == name:
                is_break = True
                break
            print(name, price, url_for_record)
            name_split = name_search.split(' ')
            if funks.parsed_items_control(price, name_split):
              print('ye')
              with sqlite3.connect('pars.db', timeout=15000) as data:
                    curs = data.cursor() 
                    curs.execute("""INSERT OR REPLACE INTO store3 (name, name_for_search, price, url) VALUES (?, ?, ?, ?)""", (name, name_search, price, url_for_record))  
          except IndexError as e:
             print('clinic-mobile', e)
          i+=1
          if is_break:
            break
          
      p+=1
     
      time.sleep(randint(2,6))
  print(i)
  return i
