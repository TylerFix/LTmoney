from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
import datetime
from selenium.webdriver.chrome.options import Options
import threading
import subprocess
import webbrowser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Эксперимент с импортом

from dash import *
from dash import dcc, html, callback_context
import plotly.graph_objects as go
from dash.dependencies import Input, Output



# Инициализация
# Адреса для OnTaxi
streets_list_otkuda = [['Тракторобудівників проспект, 142/1','Ст. Метро "Держпром"','ТЦ "Дафі" (вхід ближче до Roshen)','Георгія Тарасенка (Плеханівська) вулиця, 43/1','Плиткова вулиця, 4'],
                       ['Героїв Крут (12 Квітня) вулиця, 3','Авраменка вулиця, 1','Балка Поповка вулиця, 21','Рубана вулиця, 20','Тенісна вулиця, 20'],
                       ['Європейська (Миронова) вулиця, 8А','Запорізьке шосе, 72','Набережна Перемоги вулиця, 134','Переволочанський (Новочеркаський) провулок, 5','Зоряна вулиця, 4'],
                       ['Французька (Комінтернівська) вулиця, 7','Індустріальний мікрорайон, 68','Проскурівська вулиця, 31А','Турнірна вулиця, 10','Старотернівська (Глазунова) вулиця, 106'],
                       ['І. Мазепи (Мануїльського) вулиця, 164','Новогоголівська вулиця, 42/1','Корольова вулиця, 101','Покровська (Щорса) вулиця, 142','Князькова вулиця, 39А']]
streets_list_kuda = [['Салтівське шосе, 262А/5','ТРЦ "Нікольський"','Ювілейний (50-річчя ВЛКСМ) проспект, 34/1','Морозова вулиця, 20А/1','Луї Пастера вулиця, 234А/1'],
                     ['Перемоги вулиця, 87В','Аптечна вулиця, 3','Дальня вулиця, 41/2','Будівельників бульвар, 1','Теплична вулиця, 1'],
                     ['Макарова вулиця, 1А','Запорізьке шосе, 27Б','Набережна Перемоги вулиця, 2Г','Слобожанський (Газети "Правда") проспект, 5А','Славни вулиця, 1'],
                     ['Автомеханічна (Кисловодська) вулиця, 1','Сонячний мікрорайон, 3','Говерлівська (Самойлова) вулиця, 82','Груднева вулиця, 1','Центральна вулиця, 1А'],
                     ['Пункт Незламності (Епіцентр)','Хінчанський проїзд, 1/67','Комунальний провулок, 1','Пункт Незламності (Нова пошта №27)','Є. Коновальця (Якубовського) вулиця, 7А']]


streets_list_otkuda_opti = [['Госпром (Майдан Свободы 5/1)','Тракторобудівників просп., 134','Трц Дафи ул. Героев Труда 9','Планерна вул., 2','Масивна вул., 2'],
                            [' Атб (Патриотическая 52а)','Дружний проїзд, 12','Хортицьке шосе, 34','Полякова ул. 21','Хортицкая ул. (Разумовка пос.) 20'],
                            [' Пригородная ул., 27','С Делви (Паникахи ул. 48)','Днепр -Главный ','Херсонская ул. 46','Овражная ул. 49'],
                            [' Ярослава Мудрого (Брозовського Отто) вул., 55','Нарвська вул., 8','Дубки (Косарева) вул., 193','Сергія Колачевського (23-го Лютого) вул., 66','Танкістів вул., 40'],
                            ['Селецкая ул. 10',' 3-Й Чудновский пер. 4','Каракульная ул. 27','Украинки Леси ул. 40','Вокзальная ул. 3']]
streets_list_kuda_opti = [['Тц Никольский (Пушкинская ул. 2)','Салтівське шосе, 24','Тюрінська (Якіра) вул., 2','Біологічна вул., 9','Соснова вул., 7'],
                          ['Броньова вул., 16','Перемоги вул., 63','Новгородська вул., 11',' Карпенко-Карого ул. 40','Кооперативная ул. (Разумовка) 11'],
                          ['Каруны ул. 8','Тополиная ул. (Тополь) 41','Боброва ул. (Майдан Озёрный) 12','Русановская ул. 121','Переяславская ул. 21'],
                          ['Героїв АТО (Димитрова) вул., 27','Коцюбинського вул., 9','Тесленка вул., 24','Тимирязева ул. 26','Беринга вул., 7'],
                          ['Королева ул. 51','Гагарина ул. 6','Друкарский ( Колхозный 2-Й) пер. 36','Тена Бориса ул. 123','Космонавтов ул. 4']]
web_list = ['https://ontaxi.com.ua/ru/kharkiv','https://ontaxi.com.ua/ru/zaporizhzhya','https://ontaxi.com.ua/ru/dnipro','https://ontaxi.com.ua/ru/kryvyi-rih','https://ontaxi.com.ua/ru/zhytomyr']
web_list_opti = ['https://opti.global/ru/checkout_ru-kharkiv','https://opti.global/ru/checkout_ru-zaporizhzhya','https://opti.global/ru/checkout_ru-dnipro','https://opti.global/ru/checkout_ru-kriviyrig','https://opti.global/ru/checkout_ru-zhitomir']

# счетчик сайтов
count_streets = len(streets_list_otkuda)-1
count_streets_opti = len(streets_list_otkuda_opti)-1
cities_count = len(web_list)-1
cities_count_opti = len(web_list_opti)-1
print(f'Улиц для расчета - {count_streets}')
print(f'Городов для расчета - {cities_count}')
value_prec = [None,None,None,None,None] # HARKIV
count_et = 0
count_et_opti = 0
basic_price = [80,54,77,84,56] # HARKIV
basic_price_cities = [50,55,60,50,45] # Базовые цены по городам, для устранения артефактов на графике
db_save_list = ['PriceHark','PriceZap','PriceDnepr','PriceKR','PriceZhitom']
db_save_list_opti = ['PriceHarkivOpti','PriceZapOpti','PriceDneprOpti','PriceKROpti','PriceZhitomOpti']
db_conn = [None,None,None,None,None]
db_cur = [None,None,None,None,None]

db_conn_opti = [None,None,None,None,None]
db_cur_opti = [None,None,None,None,None]
url = 'http://127.0.0.1:8050/'

# Testing google table
# DB
# DB OnTaxi (тестовый вариант)
conn = sqlite3.connect('prices.db',check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceHark(
id INTEGER PRIMARY KEY,
trakt_salt INTEGER,
derzhprom_nikolskii INTEGER,
dafi_uvileynii INTEGER,
plechan_moroz INTEGER,
plitk_pastera INTEGER,
dif_trakt_salt INTEGER,
dif_derzhprom_nikolskii INTEGER,
dif_dafi_uvileynii INTEGER,
dif_plechan_moroz INTEGER,
dif_plitk_pastera INTEGER,
summary_ontaxi_ha INTEGER,
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
cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceZap(
id INTEGER PRIMARY KEY,
krut_perem INTEGER,
avram_aptech INTEGER,
popovka_daln INTEGER,
ruban_budiv INTEGER,
tenis_tepli INTEGER,
dif_krut_perem INTEGER,
dif_avram_aptech INTEGER,
dif_popovka_daln INTEGER,
dif_ruban_budiv INTEGER,
dif_tenis_tepli INTEGER,
summary_ontaxi_zp INTEGER,
time TEXT)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceDnepr(
id INTEGER PRIMARY KEY,
mironova_makar INTEGER,
zapor_zapor INTEGER,
peremog_peremog INTEGER,
novoch_pravdi INTEGER,
zoryana_zlavni INTEGER,
dif_mironova_makar INTEGER,
dif_zapor_zapor INTEGER,
dif_peremog_peremog INTEGER,
dif_novoch_pravdi INTEGER,
dif_zoryana_zlavni INTEGER,
summary_ontaxi_dp INTEGER,
time TEXT)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceKR(
id INTEGER PRIMARY KEY,
franc_avto INTEGER,
indus_sonyach INTEGER,
prosk_goverl INTEGER,
turn_grud INTEGER,
glazunov_centr INTEGER,
dif_franc_avto INTEGER,
dif_indus_sonyach INTEGER,
dif_prosk_goverl INTEGER,
dif_turn_grud INTEGER,
dif_glazunov_centr INTEGER,
summary_ontaxi_kr INTEGER,
time TEXT)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceZhitom(
id INTEGER PRIMARY KEY,
mazep_epic INTEGER,
novog_hinch INTEGER,
korol_komun INTEGER,
shors_novaposh INTEGER,
knyas_koval INTEGER,
dif_mazep_epic INTEGER,
dif_novog_hinch INTEGER,
dif_korol_komun INTEGER,
dif_chors_novaposh INTEGER,
dif_knyas_koval INTEGER,
summary_ontaxi_zt INTEGER,
time TEXT)
''')

# DB Opti (тестовый вариант)
cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceHarkivOpti(
id INTEGER PRIMARY KEY,
adress_1 INTEGER,
adress_2 INTEGER,
adress_3 INTEGER,
adress_4 INTEGER,
adress_5 INTEGER,
dif_adress_1 INTEGER,
dif_adress_2 INTEGER,
dif_adress_3 INTEGER,
dif_adress_4 INTEGER,
dif_adress_5 INTEGER,
time TEXT)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceZapOpti(
id INTEGER PRIMARY KEY,
adress_1 INTEGER,
adress_2 INTEGER,
adress_3 INTEGER,
adress_4 INTEGER,
adress_5 INTEGER,
dif_adress_1 INTEGER,
dif_adress_2 INTEGER,
dif_adress_3 INTEGER,
dif_adress_4 INTEGER,
dif_adress_5 INTEGER,
time TEXT)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceDneprOpti(
id INTEGER PRIMARY KEY,
adress_1 INTEGER,
adress_2 INTEGER,
adress_3 INTEGER,
adress_4 INTEGER,
adress_5 INTEGER,
dif_adress_1 INTEGER,
dif_adress_2 INTEGER,
dif_adress_3 INTEGER,
dif_adress_4 INTEGER,
dif_adress_5 INTEGER,
time TEXT)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceKROpti(
id INTEGER PRIMARY KEY,
adress_1 INTEGER,
adress_2 INTEGER,
adress_3 INTEGER,
adress_4 INTEGER,
adress_5 INTEGER,
dif_adress_1 INTEGER,
dif_adress_2 INTEGER,
dif_adress_3 INTEGER,
dif_adress_4 INTEGER,
dif_adress_5 INTEGER,
time TEXT)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS PriceZhitomOpti(
id INTEGER PRIMARY KEY,
adress_1 INTEGER,
adress_2 INTEGER,
adress_3 INTEGER,
adress_4 INTEGER,
adress_5 INTEGER,
dif_adress_1 INTEGER,
dif_adress_2 INTEGER,
dif_adress_3 INTEGER,
dif_adress_4 INTEGER,
dif_adress_5 INTEGER,
time TEXT)
''')
# Конец DB


# Создание объекта опций для Chrome
chrome_options = Options()
# Функция парсинга
def calculation_price_ontaxi(streets_list_otkuda,streets_list_kuda,value_prec,count_et,basic_price,count_streets,web_list,db_count,db_conn,db_cur,basic_price_cities,db_save_cities):
    chrome_options.headless = True
    #browser = webdriver.Chrome(options=chrome_options)
    print('Счетчик базы данных',db_count)
    db_conn[db_count] = sqlite3.connect('prices.db', check_same_thread=False)
    db_cur[db_count] = db_conn[db_count].cursor()
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(web_list[db_count])
    value_list = [0,0,0,0,0]
    value_dif = [0,0,0,0,0]
    basic_lt = [[79,52,79,88,52],
                [67,66,77,49,71],
                [106,63,101,102,73],
                [53,61,70,61,52],
                [65,70,65,85,75]]
    while True:
        try:
            # Тело обновление сравнений
            element_otkuda = browser.find_element('xpath','//*[@id="inputplace0"]')
            element_otkuda.send_keys(streets_list_otkuda[db_count][count_et]) 
            sleep(2)
            element_otkuda.send_keys(Keys.ENTER) 
            sleep(1)
            element_kuda = browser.find_element('xpath', '//*[@id="inputplace1"]')
            element_kuda.send_keys(streets_list_kuda[db_count][count_et])
            sleep(2)
            element_kuda.send_keys(Keys.ENTER)
            sleep(1)
            element_money = browser.find_element('xpath','//*[@id="orderForm"]/div[2]/div/div[1]/div[5]/div[2]/span/span[1]/span')
            print(f'Значение адреса {count_et+1} {db_save_cities[db_count]} : ',element_money.text)
            if int(element_money.text) > basic_price_cities[db_count]:
                value_list[count_et] = int(element_money.text)
                # Цена разницы базового ЛТ к Ontaxi
                value_dif[count_et] = ((value_list[count_et]-basic_lt[db_count][count_et])/basic_lt[db_count][count_et])*100
            l_adress_otkuda = len(streets_list_otkuda[db_count][count_et])
            l_adress_kuda = len(streets_list_kuda[db_count][count_et])

            for i in range(0,l_adress_otkuda):
                element_otkuda.send_keys(Keys.BACKSPACE)
            for i in range (0,l_adress_kuda):
                element_kuda.send_keys(Keys.BACKSPACE)
            # Конец тела сравнений
            # Калькулятор
            if count_et != count_streets : #
                diff_price = int(value_list[count_et]) - basic_price[count_et]
                if diff_price != 0:
                    perc_value = int(value_list[count_et])*0.01
                    if perc_value != 0:
                        value_prec[count_et] = round(diff_price/perc_value)
                    else: 
                        value_prec[count_et] = 0
                else: 
                    value_prec[count_et] = 0
                count_et +=1            
            elif count_et == count_streets:
                diff_price = int(value_list[count_et]) - basic_price[count_et]
                if diff_price != 0:
                    perc_value = int(value_list[count_et])*0.01
                    value_prec[count_et] = round(diff_price/perc_value)
                else: 
                    value_prec[count_et] = 0
                now = datetime.datetime.now()
                formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
                print(formatted_time)
                # Среднее по городам
                value_sum = sum(value_dif)/len(value_dif)
                # Запись в БД
                db_cur[db_count].execute(f'INSERT INTO {db_save_list[db_count]} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (int(value_list[0]), int(value_list[1]),int(value_list[2]),int(value_list[3]),int(value_list[4]),int(value_dif[0]),int(value_dif[1]),int(value_dif[2]),int(value_dif[3]),int(value_dif[4]),int(value_sum),str(formatted_time)))
                db_conn[db_count].commit()
                #cursor.execute('INSERT INTO Percent (trakt_salt, derzhprom_nikolskii, dafi_uvileynii,plechan_moroz, plitk_pastera, time) VALUES (?, ?, ?, ?, ?, ?)', (int(value_prec[0]), int(value_prec[1]),int(value_prec[2]),int(value_prec[3]),int(value_prec[4]),str(formatted_time)))
                #conn.commit()
                count_et = 0
            
        except Exception as e:
            print('Ошибка парсера : ', e)
            
# Парсер opti
def calculation_price_opti (db_count,web_list_opti,count_et_opti,db_conn_opti,db_cur_opti,streets_list_otkuda_opti,streets_list_kuda_opti):
    chrome_options = Options()
    chrome_options.headless = True
    db_conn_opti[db_count] = sqlite3.connect('prices.db', check_same_thread=False)
    db_cur_opti[db_count] = db_conn_opti[db_count].cursor()
    #browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(web_list_opti[db_count])
    value_list = [None,None,None,None,None]
    while True:
        element_otkuda = browser.find_element('xpath','/html/body/div[1]/main/div[2]/div/form/div/div[1]/div/div[1]/div[1]/div[1]/input')
        element_otkuda.send_keys(streets_list_otkuda_opti[db_count][count_et_opti]) 
        sleep(3)
        element_otkuda_spis = browser.find_element('xpath','//*[@id="autocomplete-list"]/div/strong')
        element_otkuda_spis.click()
        sleep(3)
        element_kuda = browser.find_element('xpath', '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div/div[1]/div[1]/div[2]/input')
        element_kuda.send_keys(streets_list_kuda_opti[db_count][count_et_opti])
        sleep(3)
        element_kuda_spis = browser.find_element('xpath','//*[@id="autocomplete-list"]/div/strong')
        element_kuda_spis.click()
        sleep(3)
        element_money = browser.find_element('xpath','/html/body/div[1]/main/div[2]/div/form/div/div[2]/div/div/div[1]/span[1]')
        print (element_money.text)
        if element_money.text:
            value_list[count_et_opti] = int(element_money.text)
        else:
            value_list[count_et_opti] = 0
        l_adress_otkuda = len(streets_list_otkuda_opti[db_count][count_et_opti])
        l_adress_kuda = len(streets_list_kuda_opti[db_count][count_et_opti])
        for i in range(0,l_adress_otkuda):
            element_otkuda.send_keys(Keys.BACKSPACE)
        for i in range (0,l_adress_kuda):
            element_kuda.send_keys(Keys.BACKSPACE)

        # Калькулятор
        if count_et_opti != count_streets_opti : #
            diff_price = int(value_list[count_et_opti]) - basic_price[count_et_opti]
            if diff_price != 0:
                perc_value = int(value_list[count_et_opti])*0.01
                value_prec[count_et_opti] = round(diff_price/perc_value)
            else: 
                value_prec[count_et_opti] = 0
            count_et_opti +=1            
        elif count_et_opti == count_streets_opti:
            diff_price = int(value_list[count_et_opti]) - basic_price[count_et_opti]
            if diff_price != 0:
                perc_value = int(value_list[count_et_opti])*0.01
                value_prec[count_et_opti] = round(diff_price/perc_value)
            else: 
                value_prec[count_et_opti] = 0
            now = datetime.datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            print(formatted_time)
            # Запись в БД
            db_cur_opti[db_count].execute(f'INSERT INTO {db_save_list_opti[db_count]} VALUES (NULL, ?, ?, ?, ?, ?, 0, 0, 0, 0 , 0, ?)', (int(value_list[0]), int(value_list[1]),int(value_list[2]),int(value_list[3]),int(value_list[4]),str(formatted_time)))
            db_conn_opti[db_count].commit()
            count_et_opti = 0

# Старт новых потоков        
threads = []

for i in range(cities_count+1):
    print(f'Открываю потоки попытка {i}')
    try:
        thread = threading.Thread(target=calculation_price_ontaxi, args=(streets_list_otkuda,streets_list_kuda,value_prec,count_et,basic_price,count_streets,web_list,i,db_conn,db_cur,basic_price_cities,db_save_list))
        thread.start()
        threads.append(thread)
        print (f'Поток {i+1} запущен с городом {web_list[i]}')
        sleep (5)
    except Exception as c:
        #print('Не запустил поток. Ошибка : ', c)
        print('Ошибка')

#for a in range(cities_count_opti+1):
#    print(f'Открываю потоки opti попытка {a}')
#    try:
#        thread = threading.Thread(target=calculation_price_opti, args=(a,web_list_opti,count_et_opti,db_conn_opti,db_cur_opti,streets_list_otkuda_opti,streets_list_kuda_opti))
#        thread.start()
#        threads.append(thread)
#        print (f'Поток {a+1} запущен с городом {web_list_opti[a]}')
#        sleep (5)
#    except Exception as c:
        #print('Не запустил поток. Ошибка : ', c)
#        print('Ошибка')

webbrowser.open(url)
print('Открыл адресс - ', url)
subprocess.run(['python','start_graf_dash.py'])