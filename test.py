import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Аутентификация
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)
#new_sheet = client.create('price_ha')
# Открываем нужную таблицу
new_sheet = client.open('price_ha').sheet1

# Добавляем данные
data = [['Имя', 'Возраст', 'Город'],
        ['Валерое', 25, 'кр'],
        ['Алинка', 30, 'Днепр']]
new_sheet.insert_rows(data, row=1)

# Читаем данные из таблицы
values = new_sheet.get_all_values()
print(values)

spreadsheet_url = new_sheet.url
print("Ссылка на вашу таблицу:", spreadsheet_url)

