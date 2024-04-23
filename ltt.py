from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
import datetime
from selenium.webdriver.chrome.options import Options

#  Адресса для просчета
streets_list_otkuda = ['Тракторобудівників проспект, 142/1','Ст. Метро "Держпром"','ТЦ "Дафі" (вхід ближче до Roshen)','Георгія Тарасенка (Плеханівська) вулиця, 43/1','Плиткова вулиця, 4']
streets_list_kuda = ['Салтівське шосе, 262А/5','ТРЦ "Нікольський"','Ювілейний (50-річчя ВЛКСМ) проспект, 34/1','Морозова вулиця, 20А/1','Луї Пастера вулиця, 234А/1']
count_streets = len(streets_list_otkuda)-1
print(count_streets)
value_list = [None,None,None,None,None]
value_prec = [None,None,None,None,None]
count_et = 0
basic_price = [80,54,77,84,56]
# DB
conn = sqlite3.connect('prices.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Price(
id INTEGER PRIMARY KEY,
trakt_salt INTEGER,
derzhprom_nikolskii INTEGER,
dafi_uvileynii INTEGER,
plechan_moroz INTEGER,
plitk_pastera INTEGER,
time TEXT)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Percent(
id INTEGER PRIMARY KEY,
trakt_salt INTEGER,
derzhprom_nikolskii INTEGER,
dafi_uvileynii INTEGER,
plechan_moroz INTEGER,
plitk_pastera INTEGER,
time TEXT)
''')

# Создание объекта опций для Chrome
chrome_options = Options()

# Установка опции headless в True
chrome_options.headless = True
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://ontaxi.com.ua/ru/kharkiv')
def calculation_price (streets_list_otkuda,streets_list_kuda,value_list,value_prec,count_et,basic_price,count_streets):
    while True:
        try:
            # Тело обновление сравнений
            element_otkuda = browser.find_element('xpath','//*[@id="inputplace0"]')
            element_otkuda.send_keys(streets_list_otkuda[count_et]) 
            sleep(2)
            element_otkuda.send_keys(Keys.ENTER) # костыль
            sleep(1)
            element_kuda = browser.find_element('xpath', '//*[@id="inputplace1"]')
            element_kuda.send_keys(streets_list_kuda[count_et])
            sleep(2)
            element_kuda.send_keys(Keys.ENTER)
            sleep(1)
            element_money = browser.find_element('xpath','//*[@id="orderForm"]/div[2]/div/div[1]/div[5]/div[2]/span/span[1]/span')
            print('Значение : ',element_money.text)
            value_list[count_et] = element_money.text
            l_adress_otkuda = len(streets_list_otkuda[count_et])
            l_adress_kuda = len(streets_list_kuda[count_et])

            for i in range(0,l_adress_otkuda):
                element_otkuda.send_keys(Keys.BACKSPACE)
            for i in range (0,l_adress_kuda):
                element_kuda.send_keys(Keys.BACKSPACE)
            # Конец тела сравнений
            # Калькулятор
            if count_et != count_streets : # костыль
                diff_price = int(value_list[count_et]) - basic_price[count_et]
                if diff_price != 0:
                    perc_value = int(value_list[count_et])*0.01
                    value_prec[count_et] = round(diff_price/perc_value)
                    print('Первая пара ',value_prec[count_et])
                else: 
                    value_prec[count_et] = 0
                count_et +=1
            
            elif count_et == count_streets:
                diff_price = int(value_list[count_et]) - basic_price[count_et]
                if diff_price != 0:
                    perc_value = int(value_list[count_et])*0.01
                    value_prec[count_et] = round(diff_price/perc_value)
                    print('Третья пара ',value_prec[count_et])
                else: 
                    value_prec[count_et] = 0
                now = datetime.datetime.now()
                formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
                print(formatted_time)
                # Запись в БД
                cursor.execute('INSERT INTO Price (trakt_salt, derzhprom_nikolskii, dafi_uvileynii, plechan_moroz, plitk_pastera, time) VALUES (?, ?, ?, ?, ?, ?)', (int(value_list[0]), int(value_list[1]),int(value_list[2]),int(value_list[3]),int(value_list[4]),str(formatted_time)))
                conn.commit()
                cursor.execute('INSERT INTO Percent (trakt_salt, derzhprom_nikolskii, dafi_uvileynii,plechan_moroz, plitk_pastera, time) VALUES (?, ?, ?, ?, ?, ?)', (int(value_prec[0]), int(value_prec[1]),int(value_prec[2]),int(value_prec[3]),int(value_prec[4]),str(formatted_time)))
                conn.commit()
                count_et = 0
            
        except Exception as e:
            print('Ошибка : ', e)
        

calculation_price(streets_list_otkuda,streets_list_kuda,value_list,value_prec,count_et,basic_price,count_streets)