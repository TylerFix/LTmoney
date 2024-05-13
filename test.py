import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Аутентификация
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Создание новой таблицы
new_sheet = client.create('price_ha')

# Запись данных в таблицу
sheet = client.open('PriceLT').sheet1
data = [['Имя', 'Возраст', 'Город'],
        ['Анна', 25, 'Москва'],
        ['Иван', 30, 'Санкт-Петербург']]
sheet.insert_rows(data, row=1)

# Чтение данных из таблицы
values = sheet.get_all_values()
print(values)