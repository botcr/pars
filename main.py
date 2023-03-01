import requests
from bs4 import BeautifulSoup
import time
import sqlite3
from funks import time_check
import pars_store6
import pars_store1
import pars_store2
import cloudscraper
import ftplib
from config import *
from loguru import logger
import json
import pars_store4
import pars_store3
import pars_store5
import datetime
import base_work
import tables_create
import ftp_1c
import telebot
from telebot import types
import threading
from funks import get_current_msc_date
import os

headers = {
       'Accept': '*/*',
       'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"""
     }
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB", compression="zip")

#запускаем поток который отслеживает время и делает всякое про времени
time_check_args = (headers, logger)
time_check_thr = threading.Thread(target=time_check, args=time_check_args)
time_check_thr.start()


@bot.message_handler(content_types=['text', 'commands'])
def handler(message):
  global is_pars
  check = message.text.split(' ')
  with sqlite3.connect('pars.db') as data:
           curs = data.cursor()
           access = curs.execute("""SELECT access FROM users WHERE id = ?;""", (message.from_user.id,)).fetchone()
  if access != None:
    if access[0] == True:
      if message.text == 'store2' and is_pars == False:
        is_pars = True
        t3 = datetime.datetime.now()
        bot.send_message(message.from_user.id, f'Начал парсить, как закончу, отпишусь!')
        with open('logs.txt', 'a') as file:
          file.write(f"начал store2, {get_current_msc_date()}\n")
        pars_store2.pars_store2(headers)
        t4 = datetime.datetime.now()
        with open('logs.txt', 'a') as file:
          file.write(f"закончил store2 {t4-t3}, {get_current_msc_date()}\n")
        bot.send_message(message.from_user.id, f'парсинг store2 закончился, он занял {t4-t3}')
        is_pars = False
      elif message.text == 'store4' and is_pars == False:
        is_pars = True
        with open('logs.txt', 'a') as file:
          file.write(f"начал store4, {get_current_msc_date()}\n")
        t3 = datetime.datetime.now()
        bot.send_message(message.from_user.id, f'Начал парсить, как закончу, отпишусь!')
        pars_store4.pars_store4(headers)
        t4 = datetime.datetime.now()
        with open('logs.txt', 'a') as file:
          file.write(f"закончил store4 {t4-t3}, {get_current_msc_date()}\n")
        bot.send_message(message.from_user.id, f'парсинг store4 закончился, он занял {t4-t3}')
        is_pars = False
      elif message.text == 'store5' and is_pars == False:
        is_pars = True
        with open('logs.txt', 'a') as file:
          file.write(f"начал store5, {get_current_msc_date()}\n")
        t3 = datetime.datetime.now()
        bot.send_message(message.from_user.id, f'Начал парсить, как закончу, отпишусь!')
        pars_store5.pars_store5(headers)
        t4 = datetime.datetime.now()
        with open('logs.txt', 'a') as file:
          file.write(f"закончил store5 {t4-t3}, {get_current_msc_date()}\n")
        bot.send_message(message.from_user.id, f'парсинг store5 закончился, он занял {t4-t3}')
        is_pars = False
      elif message.text == 'clinic-mobile' and is_pars == False:
        is_pars = True
        with open('logs.txt', 'a') as file:
          file.write(f"начал clinic-mobile, {get_current_msc_date()}\n")
        t3 = datetime.datetime.now()
        bot.send_message(message.from_user.id, f'Начал парсить, как закончу, отпишусь!')
        pars_store3.pars_store3(headers)
        t4 = datetime.datetime.now()
        with open('logs.txt', 'a') as file:
          file.write(f"закончил clinic-mobile {t4-t3}, {get_current_msc_date()}\n")
        bot.send_message(message.from_user.id, f'парсинг clinic-mobile закончился, он занял {t4-t3}')
        is_pars = False
      elif message.text == 'store1' and is_pars == False:
        is_pars = True
        with open('logs.txt', 'a') as file:
          file.write(f"начал store1, {get_current_msc_date()}\n")
        t3 = datetime.datetime.now()
        bot.send_message(message.from_user.id, f'Начал парсить, как закончу, отпишусь!')
        pars_store1.pars_store1(headers)
        t4 = datetime.datetime.now()
        with open('logs.txt', 'a') as file:
          file.write(f"закончил store1 {t4-t3}, {get_current_msc_date()}\n")
        bot.send_message(message.from_user.id, f'парсинг store1 закончился, он занял {t4-t3}')
        is_pars = False
      elif message.text == 'store6' and is_pars == False:
        is_pars = True
        with open('logs.txt', 'a') as file:
          file.write(f"начал store6, {get_current_msc_date()}\n")
        t3 = datetime.datetime.now()
        bot.send_message(message.from_user.id, f'Начал парсить, как закончу, отпишусь!')
        pars_store6.pars_apple_store6(headers)
        t4 = datetime.datetime.now()
        with open('logs.txt', 'a') as file:
          file.write(f"закончил store6 {t4-t3}, {get_current_msc_date()}\n")
        bot.send_message(message.from_user.id, f'парсинг store6 закончился, он занял {t4-t3}')
        is_pars = False
      elif (message.text == 'store6' or message.text == 'store1' or message.text == 'clinic-mobile' or message.text == 'store5' or message.text == 'store4' or message.text == 'store2') and is_pars == True:
        bot.send_message(message.from_user.id, f'Прости, брат, я уже занят парсингом, попробуй позже')
      # если не парсинг то ищем товар
      elif message.text == '/all':
        print(1)
        what_to_do = '/all'
        base_work.send_to_telegram(bot, message, what_to_do)
      elif message.text == '/pars':
        pars_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        store2_but = types.KeyboardButton(text="store2")
        store3_but = types.KeyboardButton(text="clinic-mobile")
        store6_but = types.KeyboardButton(text="store6")
        store1_but = types.KeyboardButton(text="store1")
        store5_but = types.KeyboardButton(text="store5")
        store4_but = types.KeyboardButton(text="store4")
        pars_markup.add(store2_but, store3_but, store6_but, store1_but, store5_but, store4_but)
        bot.send_message(message.from_user.id, f'Меню', reply_markup=pars_markup)
      elif message.text == '/menus':
        menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        iPhone_but = types.KeyboardButton(text="📦 iPhone")
        Watch_but = types.KeyboardButton(text="📦 Watch")
        Mac_but = types.KeyboardButton(text="📦 Mac")
        iPad_but = types.KeyboardButton(text="📦 iPad")
        AirPods_but = types.KeyboardButton(text="📦 Pods")
        else_but = types.KeyboardButton(text="📦 Else")
        menu_markup.add(iPhone_but, Watch_but, Mac_but, iPad_but, AirPods_but, else_but)
        bot.send_message(message.from_user.id, f'Меню', reply_markup=menu_markup)
      elif message.text == '/menuse':
        menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        iPhone_with_empty_but = types.KeyboardButton(text="📦®️ iPhone")
        Watch_with_empty_but = types.KeyboardButton(text="📦®️ Watch")
        Mac_with_empty_but = types.KeyboardButton(text="📦®️ Mac")
        iPad_with_empty_but = types.KeyboardButton(text="📦®️ iPad")
        AirPods_with_empty_but = types.KeyboardButton(text="📦®️ Pods")
        else_with_empty_but = types.KeyboardButton(text="📦®️ Else")
        menu_markup.add(iPhone_with_empty_but, Watch_with_empty_but, Mac_with_empty_but, iPad_with_empty_but, AirPods_with_empty_but, else_with_empty_but)
        bot.send_message(message.from_user.id, f'Меню', reply_markup=menu_markup)
      elif message.text == '/menup':
        menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        iPhone_pars_but = types.KeyboardButton(text="💲 iPhone")
        Watch_pars_but = types.KeyboardButton(text="💲 Watch")
        Mac_pars_but = types.KeyboardButton(text="💲 Mac")
        iPad_pars_but = types.KeyboardButton(text="💲 iPad")
        AirPods_pars_but = types.KeyboardButton(text="💲 Pods")
        else_pars_but = types.KeyboardButton(text="💲 Else")
        menu_markup.add(iPhone_pars_but, Watch_pars_but, Mac_pars_but, iPad_pars_but, AirPods_pars_but, else_pars_but)
        bot.send_message(message.from_user.id, f'Меню', reply_markup=menu_markup)
      elif message.text[0] == '📦':
        base_work.send_to_telegram_not_pars(message)
      elif message.text[0] == '💲':
        what_to_do = 'category'
        base_work.send_to_telegram(bot, message, what_to_do)
      else:
        what_to_do = 'items_change_data'
        base_work.send_to_telegram(bot, message, what_to_do)
    else:
      pass_1(message)
  else:
    registration(message)
      
def registration(message):
    with sqlite3.connect('pars.db') as data:
           curs = data.cursor()
           curs.execute("""INSERT INTO users (id, first_name, username) VALUES (?, ?, ?)""",
                             (message.from_user.id, message.from_user.first_name, message.from_user.username,))
    handler(message)

def pass_1(message):
  msg = bot.send_message(message.from_user.id, 'Пожалуйста, введите пароль')
  bot.register_next_step_handler(msg, pass_record_2)

def pass_record_2(message):
  if (message.text).lower() == os.environ['password']:
    bot.send_message(message.from_user.id, 'Это верный пароль, приятного пользования. Чтобы использовать бота, воспользуйтесь кнопкой "меню" слева.')
    with sqlite3.connect('pars.db') as data:
        curs = data.cursor()
        curs.execute("""UPDATE users SET access = True WHERE id = ?""", (message.from_user.id,))
    handler(message)
  else:
    bot.send_message(message.from_user.id, 'Неверный пароль, попробуйте еще раз')
    handler(message)
    
@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_handler(callback):
  if 'change_data' in callback.data:
    info = callback.data.split(' ')
    msg = bot.send_message(callback.from_user.id, f'Введите полное наименование или url страницы на сайте {info[1]}\nИли введите слово \"удалить\" чтобы удалить текущее значение')
    args = (info[1], info[2])
    bot.register_next_step_handler(msg, change_comparison_data, args=args)
  elif 'yes_thats_true' in callback.data:
    info = callback.data.split(' ')
    args = (info[1], info[2], True)
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.id)
    
    bot.send_message(callback.from_user.id, f'Принято')
  elif 'no_thats_false' in callback.data:
    bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.id)

    
def change_comparison_data(message, args):
  base = args[0]
  item_1c_id = args[1]
  with sqlite3.connect('pars.db', timeout=15000) as data:
    curs = data.cursor()
    if message.text != 'удалить':
      text_for_search = f'%{message.text}%'
      text_for_search = text_for_search.lower()
      aaa = text_for_search.replace('(', '')
      aaa = aaa.replace(')','')
      aaa = aaa.replace(',','')
      aaa = aaa.replace(' ', ' ')
      aaa = aaa.replace('/',' ')
      text_for_search = aaa.replace(';','')
      w = """SELECT name, price, url FROM {table} WHERE name == ? OR name_for_search LIKE ? OR url LIKE ? OR url == ?;"""
      curs.execute(w.format(table=base), (message.text, text_for_search, text_for_search, message.text))
      item_info = curs.fetchone()
      if item_info != None:
        text = f'[{item_info[0]}]({item_info[2]})\nЦена {item_info[1]}\nЗаписан в базу, если это не тот товар, повторите процедуру введя название или ссылку иначе'
        column_name = 'name_' + base
        a = """UPDATE comparison SET {column} = ? WHERE id = ?"""
        curs.execute(a.format(column=column_name), (item_info[0], item_1c_id))
        bot.send_message(message.from_user.id, text, parse_mode='Markdown') 
      elif item_info == None:
        bot.send_message(message.from_user.id, 'Простите, ничего не найдено')
    else:
      column_name = 'name_' + base
      a = """UPDATE comparison SET {column} = '0' WHERE id = ?"""
      curs.execute(a.format(column=column_name), (item_1c_id,))
      bot.send_message(message.from_user.id, 'Значение успешно удалено')
    
    
bot.infinity_polling()
   