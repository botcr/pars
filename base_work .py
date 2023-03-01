import json
import sqlite3
import telebot
from telebot import util, types
from config import base_names
from time import sleep
from config import bot
import funks
#сделать функцию которая будет доставать все из базы и формировать сообщение

def round_100(number_for_round):
  b = str(number_for_round)[-2:]
  if int(b) >= 50:
    v = 100
  elif int(b) < 50:
    v = 0
  return number_for_round-int(b)+v

def up_to_100(number_for_round):
  b = str(number_for_round)[-2:]
  if number_for_round > 0:
    v = 100
  else:
    v = 0
  return number_for_round-int(b)+v

def round_1000(number_for_round):
  b = str(number_for_round)[-2:]
  if int(b) >= 50:
    v = 100
  elif int(b) < 50:
    v = 0
  return float((number_for_round-int(b)+v)/1000)

def dot_in_price(price):
  price = str(price)
  if len(price) >= 7:
    price = price[:-6] + '.' + price[-6:-3] + '.' + price[-3:]
  elif len(price) >= 4:
    price = price[:-3] + '.' + price[-3:]
  return price

def take_category_from_json():
  pass

def send_to_telegram_not_pars(message):
    items = []
    with sqlite3.connect('pars.db', timeout=15000) as data:
          curs = data.cursor()
          if message.text == '📦®️ iPhone':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%iPhone%' ORDER BY groupid5;""")
          elif message.text == '📦®️ Watch':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%Watch%' ORDER BY full_name;""")
          elif message.text == '📦®️ Mac':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%MacBook%' ORDER BY full_name;""")
          elif message.text == '📦®️ iPad':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%iPad%' ORDER BY full_name;""")
          elif message.text == '📦®️ Pods':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%AirPods%' ORDER BY full_name;""")
          elif message.text == '📦®️ Else':
                curs.execute("""SELECT * FROM data_1c WHERE full_name NOT LIKE '%iPhone%' AND full_name NOT LIKE '%Watch%' AND full_name NOT LIKE '%iPad%' AND full_name NOT LIKE '%MacBook%' AND full_name NOT LIKE '%AirPods%' AND quantity != 0 ORDER BY full_name;""")
          elif message.text == '📦 iPhone':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%iPhone%' AND quantity != 0 ORDER BY groupid5;""")
          elif message.text == '📦 Watch':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%Watch%' AND quantity != 0 ORDER BY full_name;""")
          elif message.text == '📦 Mac':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%MacBook%' AND quantity != 0 ORDER BY full_name;""")
          elif message.text == '📦 iPad':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%iPad%' AND quantity != 0 ORDER BY full_name;""")
          elif message.text == '📦 Pods':
                curs.execute("""SELECT * FROM data_1c WHERE full_name LIKE '%AirPods%' AND quantity != 0 ORDER BY full_name;""")
          elif message.text == '📦 Else':
                curs.execute("""SELECT * FROM data_1c WHERE full_name NOT LIKE '%iPhone%' AND full_name NOT LIKE '%Watch%' AND full_name NOT LIKE '%iPad%' AND full_name NOT LIKE '%MacBook%' AND full_name NOT LIKE '%AirPods%' ORDER BY full_name;""")
          items1 = curs.fetchall()
    text = ''
    last_item_category = None
    print(items1)
    for items_1c in items1:
      if items_1c[6] != 0:
        quantity = '▪️'
      else:
        quantity = '🔻'
      #print(items_1c)
      if items_1c[2] != None:
          #делаем пробелы между категориями, если первое слово слишком общее, берем следующее слово
            if message.text == '📦 iPhone' or message.text == '📦®️ iPhone':
              item_category = items_1c[12]
            else:
              try:
                item_category = items_1c[2].split(' ')[1].lower()
              except IndexError:
                item_category = items_1c[2].lower()
              if item_category == 'apple' or item_category == 'ipad' or item_category == 'airpods' or item_category == 'macBook' or item_category == 'iphone':
                item_category = items_1c[2].split(' ')[2].lower()
            if last_item_category != item_category:
              text = text + '\n'
            item_text = f'{items_1c[2]}{quantity}{items_1c[6]}•>{round_1000(int(items_1c[3]))}\\{round_1000(int(items_1c[4]))}•*{round_1000(int(items_1c[5]))}*\n'
            last_item_category = item_category
            print(items_1c[2], last_item_category)
            #если краткого названия нет
      else:
            if message.text == '📦 iPhone' or message.text == '📦®️ iPhone':
              item_category = items_1c[12]
            else:
              item_category = items_1c[1].split(' ')[1].lower()
              if item_category == 'apple' or item_category == 'ipad' or item_category == 'airpods' or item_category == 'macBook':
                item_category = items_1c[2].split(' ')[2].lower()
            if last_item_category != item_category:
              text = text + '\n'
            item_text = f'{items_1c[1]}{quantity}{items_1c[6]}•>{round_1000(int(items_1c[3]))}\\{round_1000(int(items_1c[4]))}•*{round_1000(int(items_1c[5]))}*\n'
            last_item_category = item_category
            print(items_1c[1], last_item_category)
      text = text + item_text  
    text1 = util.smart_split(text, 4096)
    count = 0
    while count < 50:
      try:
        text = text1[count]
        bot.send_message(message.from_user.id, text, parse_mode='MARKDOWN')
        sleep(0.2)
      except IndexError:
        break
      count += 1

def send_to_telegram(bot, message, what_to_do):
  with sqlite3.connect('pars.db', timeout=5000) as data:
    curs = data.cursor()
    if what_to_do == '/all':
      curs.execute("""SELECT * FROM comparison ORDER BY name_1c;""")
      items = curs.fetchall()
    elif what_to_do == 'items_change_data':
      text_for_search = f'%{message.text}%'
      curs.execute("""SELECT * FROM comparison WHERE name_1c LIKE ? or id == ?;""", (text_for_search, message.text))
      items = curs.fetchall()
      if items == None or len(items) == 0:
        curs.execute("""SELECT id FROM data_1c WHERE short_name LIKE ?;""", (text_for_search,))
        id_1c = curs.fetchone()
        curs.execute("""SELECT * FROM comparison WHERE id == ?;""", (id_1c[0],))
        items = curs.fetchall()
    elif what_to_do == 'category':
        items = []
        with sqlite3.connect('pars.db', timeout=15000) as data:
          curs = data.cursor()
          if message.text == '💲 iPhone':
                curs.execute("""SELECT id FROM data_1c WHERE full_name LIKE '%iPhone%' AND quantity > 0 ORDER BY groupid5;""")
          elif message.text == '💲 Watch':
                curs.execute("""SELECT id FROM data_1c WHERE full_name LIKE '%Watch%' AND quantity > 0 ORDER BY full_name;""")
          elif message.text == '💲 Mac':
                curs.execute("""SELECT id FROM data_1c WHERE full_name LIKE '%MacBook%' AND quantity > 0 ORDER BY full_name;""")
          elif message.text == '💲 iPad':
                curs.execute("""SELECT id FROM data_1c WHERE full_name LIKE '%iPad%' AND quantity > 0 ORDER BY full_name;""")
          elif message.text == '💲 Pods':
                curs.execute("""SELECT id FROM data_1c WHERE full_name LIKE '%AirPods%' AND quantity > 0 ORDER BY full_name;""")
          elif message.text == '💲 Else':
                curs.execute("""SELECT * FROM data_1c WHERE full_name NOT LIKE '%iPhone%' AND full_name NOT LIKE '%Watch%' AND full_name NOT LIKE '%iPad%' AND full_name NOT LIKE '%MacBook%' AND full_name NOT LIKE '%AirPods%' AND quantity > 0 ORDER BY full_name;""")
          items1 = curs.fetchall()
          for id in items1:
              with sqlite3.connect('pars.db', timeout=15000) as data:
                curs = data.cursor()
                curs.execute("""SELECT * FROM comparison WHERE id == ?;""", (id[0],))
                comparison = curs.fetchone()
              try:
                items.append(comparison)
              except IndexError:
                bot.send_message(477612946, f'парсинг store2 закончился, он занял {t4-t3}')
    #если что-то нашел
    if len(items) > 0:
      text = ''
      for item in items:
        if item[0] != None:
          curs.execute("""SELECT * FROM data_1c WHERE id == ?;""", (item[0],))
          items_1c = curs.fetchone()
        if items_1c != None:
          #выше ли розничная цена макс закупочной хоть на 1000
          price_difference = round_100(int(items_1c[5])) - up_to_100(int(items_1c[4]))
          if price_difference >= 1000:
            good_or_bad_price = '✅'
          elif price_difference < 1000:
            good_or_bad_price = '🆘'
          #если есть краткое название
          if items_1c[2] != None:
            item_text1 = f'*{items_1c[2]}* - {dot_in_price(up_to_100(int(items_1c[3])))}₽\\{dot_in_price(up_to_100(int(items_1c[4])))}₽ {good_or_bad_price} {items_1c[6]}шт\n📈 *{dot_in_price(round_100(int(items_1c[5])))}*'
            #если краткого названия нет
          else:
            item_text1 = f'*{items_1c[1]}* - {dot_in_price(int(up_to_100(int(items_1c[3]))))}₽|\\{dot_in_price(up_to_100(int(items_1c[4])))}₽ {good_or_bad_price} {items_1c[6]}шт\n📈 *{dot_in_price(round_100(int(items_1c[5])))}*'
          items_data = []
          for base_name in base_names:
            if base_name == 'store2':
              base_number = 2
            elif base_name == 'store1':
              base_number = 3
            elif base_name == 'store6':
              base_number = 4
            elif base_name == 'store4':
              base_number = 5
            elif base_name == 'store5':
              base_number = 6
            elif base_name == 'store3':
              base_number = 7
            if item[base_number] != None:
              w = """SELECT name, price, url FROM {table} WHERE name == ?;"""
              curs.execute(w.format(table=base_name), (item[base_number], ))
              item_info = curs.fetchone()
              if item_info != None:
                try:
                  item_list = [round_100(int(item_info[1])), base_name, item_info[0], item_info[2]]
                  items_data.append(item_list)
                except ValueError:
                  item_list = [0, base_name, item_info[0], item_info[2]]
                  items_data.append(item_list)
                #print(items_data)
                #item_text = item_text + f'[{base_name}]({item_info[2]}) {item_info[1]}\n{item_info[0]}\n'
              #else:
                # if item[base_number] != '0':
                #   print('не находит в базе ', item[base_number], base_name)
            # else:
            #   item_tupple = (None, None, None, None)
            #   items_data.append(item_tupple)
          item_text = ''
          items_data.sort()
          count_differents_of_prices = 0
          first_text_block = ''
          second_text_block = ''
          for item_data in items_data:
            #считаем на сколько в других машазинах цены выгоднее
            if round_100(int(items_1c[5])) > round_100(int(item_data[0])):
              count_differents_of_prices += 1
              if round_100(int(items_1c[5])) - round_100(int(item_data[0]))  >= 4000:
                count_differents_of_prices += 3
            first_text_block = first_text_block + f'[{item_data[1]}]({item_data[3]}) - {dot_in_price(round_100(int(item_data[0])))}₽\n'
            second_text_block = second_text_block + f'{item_data[2]}\n'
          if count_differents_of_prices > 0 and count_differents_of_prices < 4:
            exclamation_mark = f'❗️ {count_differents_of_prices}\n'
          elif count_differents_of_prices >= 4:
            exclamation_mark = f'❗️❗️ {count_differents_of_prices}\n'
          elif count_differents_of_prices == 0:
            exclamation_mark = '\n'
          item_text = item_text + exclamation_mark + first_text_block + second_text_block
          text = text + item_text1 + item_text + '\n'
          #делаем кнопки и посылаем каждый предмет отдельно
          if what_to_do == 'items_change_data':
            shops_markup = types.InlineKeyboardMarkup(row_width = 3)
            store2_but = types.InlineKeyboardButton(text='store2', callback_data=f'change_data store2 {item[0]}')
            store1_but = types.InlineKeyboardButton(text='store1', callback_data=f'change_data store1 {item[0]}')
            store6_but = types.InlineKeyboardButton(text='store6', callback_data=f'change_data store6 {item[0]}')
            store4_but = types.InlineKeyboardButton(text='store4', callback_data=f'change_data store4 {item[0]}')
            store5_but = types.InlineKeyboardButton(text='store5', callback_data=f'change_data store5 {item[0]}')
            store3_but = types.InlineKeyboardButton(text='clinic-mobile', callback_data=f'change_data store3 {item[0]}')
            shops_markup.add(store2_but, store1_but, store6_but, store4_but, store5_but, store3_but)
            bot.send_message(message.from_user.id, text, reply_markup=shops_markup, parse_mode='MARKDOWN', disable_web_page_preview=True)
          # если поиск был по всем то дробим на сообщения и кладем в 
      if what_to_do == '/all' or what_to_do == 'category':
        text1 = util.smart_split(text, 4096)
        count = 0
        while count < 50:
            try:
              text = text1[count]
              bot.send_message(message.from_user.id, text, parse_mode='MARKDOWN', disable_web_page_preview=True)
              sleep(0.2)
            except IndexError:
              break
            count += 1
    else:
      bot.send_message(message.from_user.id, 'Ничего не удалось найти, попробуйте еще раз изменив запрос')

def check_info_find_same_items():
  with open("file.json", "r") as file:
    data_1c = json.load(file)
  for json_file in data_1c:  
    with sqlite3.connect('pars.db', timeout=15000) as data:
      curs = data.cursor()
      #в начале механизм проверки есть ли уже закрепленные за id название в компарайзон
      curs.execute("""SELECT * FROM comparison WHERE id == ?;""", (json_file['identifier'],))
      comparison = curs.fetchone()
      #если записи вообще не нашлось то пишем
      if comparison == None or comparison[0] == None:
        curs.execute("""INSERT INTO comparison (id, name_1c) VALUES (?, ?)""", (json_file['identifier'], json_file['fullname']))
        comparison = [None, None, None, None, None, None, None, None]
      #print(json_file['identifier'])
      bn = 2
      for base_name in base_names:
        #в начале механизм проверки есть ли уже закрепленные за id названия из магазинов которые сейчас актуальны
        w = """SELECT price FROM {table} WHERE name == ?;"""              
        curs.execute(w.format(table=base_name), (comparison[bn],))
        item0 = curs.fetchall()
        if comparison[bn] != '0' and comparison[bn] != 0 and (comparison[bn] == None or len(item0) == 0):
          #print(comparison[bn])
          #пробуем найти по модели
          if json_file['model'] != "":
            #print(json_file['model'])
            model = f'''%{json_file['model']}%'''
            model = model.lower()
            w = """SELECT * FROM {table} WHERE name_for_search LIKE ?;"""              
            curs.execute(w.format(table=base_name), (model,))
            item0 = curs.fetchall()
            if len(item0) == 1:
              item1 = item0[0]
              column_name = 'name_' + base_name
              a = """UPDATE comparison SET {column} = ? WHERE id = ?"""
              curs.execute(a.format(column=column_name), (str(item1[0]), str(json_file['identifier'])))
              continue
            
          
          #если нет, то пробуем найти сходства
          search_query3 = json_file['fullname']
          search_query2 = search_query3.lower()
          search_query1 = search_query2.split()
          search_query = []
          search_query0 = '%'
          i = 0
          last_results = None
          while i < len(search_query1):
            if search_query1[i] != 'смартфон' and search_query1[i] != 'клавиатура' and search_query1[i] != 'наушники' and search_query1[i] != 'часы' and search_query1[i] != 'телефон' and search_query1[i] != 'apple' and search_query1[i] != 'умная' and search_query1[i] != 'колонка':
              search_query.append(f'% {search_query1[i]} %')
              search_query0 = search_query0 + ' ' + search_query1[i] + '%'
              #поиск по словам
              w = """SELECT * FROM {table} WHERE name_for_search LIKE ?;"""              
              curs.execute(w.format(table=base_name), (search_query0,))
              item0 = curs.fetchall()
              #print(item0)
              # if len(search_query) == 1:
              #     w = """SELECT * FROM {table} WHERE name_for_search LIKE ?;"""              
              #     curs.execute(w.format(table=base_name) (search_query[0],))
              if len(search_query) >= 2:
                  w = funks.select_request(search_query, base_name)
                  curs.execute(w, search_query)
              item = curs.fetchall()
              column_name = 'name_' + base_name
              if len(item0) == 1:
                item1 = item0[0]
                #print(item1, json_file['identifier'])
                a = """UPDATE comparison SET {column} = ? WHERE id = ?"""
                curs.execute(a.format(column=column_name), (item1[0], json_file['identifier']))
                continue
              if len(item) > 1:
                last_results = item
                #print(len(item))
              elif len(item) == 1:
                item1 = item[0]
                #print(item1, json_file['identifier'])
                a = """UPDATE comparison SET {column} = ? WHERE id = ?"""
                curs.execute(a.format(column=column_name), (str(item1[0]), str(json_file['identifier'])))
              search_query0 = search_query0[:-1]
              #ищем из всех вариантов наиболее подходящий
              # if json_file['identifier'] == '5f343672-1c52-11ed-8c49-48f17f95d0fc':
              #   print(item, item0, search_query, base_name)
              try:
                iiii = i + 1
                search_query1[iiii]
              except IndexError:
                if last_results != None:
                  #print(base_name, len(last_results))
                  final_result_index = []
                  for last_result2 in last_results:
                    ii = 0
                    last_result1 = last_result2[0].lower().split()
                    last_result = []
                    while ii < len(last_result1):
                      if last_result1[ii] != 'смартфон' and last_result1[ii] != 'клавиатура' and last_result1[ii] != 'наушники' and last_result1[ii] != 'часы' and last_result1[ii] != 'телефон' and last_result1[ii] != 'apple' and last_result1[ii] != 'умная' and last_result1[ii] != 'колонка':
                        last_result.append(last_result1[ii])
                      ii+=1
                    n = 0
                    for word in search_query1:
                      if word in last_result:
                        n+=1
                    price_difference = json_file['retailprice'] - last_result2[2]
                    final_result_index.append([n, abs(price_difference)])
                    #ищем у кого большее число совпадений, если одинаково то останется то что раньше      
                    
                    max_number = [0, final_result_index[0][0], final_result_index[0][1]]
                    count_number = -1
                    for nn in final_result_index:
                      count_number+=1
                      #если совпадений больше то записывается где больше совпадений
                      if nn[0] > max_number[1]:
                        max_number = [count_number, nn[0], nn[1]]
                      #если совпадений одинаково, то записывается где ближе цена
                      elif nn[0] == max_number[1] and max_number[2] > nn[1]:
                        max_number = [count_number, nn[0], nn[1]]
                  item_that_we_need = last_results[max_number[0]]
                  a = """UPDATE comparison SET {column} = ? WHERE id = ?"""
                  curs.execute(a.format(column=column_name), (str(item_that_we_need[0]), str(json_file['identifier'])))
                  print(final_result_index, max_number, search_query2, '|||', item_that_we_need[0])
                  # if json_file['identifier'] == '5f343672-1c52-11ed-8c49-48f17f95d0fc':
                  #   print(base_name, final_result_index, search_query2, '|||', item_that_we_need[0])
                    #pass
            i+=1
            #print(i)
        bn+=1
  print('закончил соотнесение базы')



