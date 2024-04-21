import sqlite3
import plotly.graph_objects as go

# Подключение к базе данных SQLite
conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

# Запрос данных из таблицы Price
cursor.execute('SELECT * FROM Price')
price_data = cursor.fetchall()

# Запрос данных из таблицы Percent
cursor.execute('SELECT * FROM Percent')
percent_data = cursor.fetchall()

# Разделение данных на списки для каждого столбца
time_price = [row[4] for row in price_data]
trakt_salt_price = [int(row[1]) for row in price_data]
derzhprom_nikolskii_price = [int(row[2]) for row in price_data]
dafi_uvileynii_price = [int(row[3]) for row in price_data]

time_percent = [row[4] for row in percent_data]
trakt_salt_percent = [int(row[1]) for row in percent_data]
derzhprom_nikolskii_percent = [int(row[2]) for row in percent_data]
dafi_uvileynii_percent = [int(row[3]) for row in percent_data]

# Создание графиков
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=time_price, y=trakt_salt_price, mode='lines', name='Тракторобудівників проспект, 142/1 - Салтівське шосе, 262А/5'))
fig_price.add_trace(go.Scatter(x=time_price, y=derzhprom_nikolskii_price, mode='lines', name='Ст. Метро "Держпром" - ТРЦ "Нікольський"'))
fig_price.add_trace(go.Scatter(x=time_price, y=dafi_uvileynii_price, mode='lines', name='ТЦ "Дафі" (вхід ближче до Roshen) - Ювілейний (50-річчя ВЛКСМ) проспект, 34/1'))
fig_price.update_layout(title='Цены на такси', xaxis_title='Время', yaxis_title='Цена')

fig_percent = go.Figure()
fig_percent.add_trace(go.Scatter(x=time_percent, y=trakt_salt_percent, mode='lines', name='Тракторобудівників проспект, 142/1 - Салтівське шосе, 262А/5'))
fig_percent.add_trace(go.Scatter(x=time_percent, y=derzhprom_nikolskii_percent, mode='lines', name='Ст. Метро "Держпром" - ТРЦ "Нікольський"'))
fig_percent.add_trace(go.Scatter(x=time_percent, y=dafi_uvileynii_percent, mode='lines', name='ТЦ "Дафі" (вхід ближче до Roshen) - Ювілейний (50-річчя ВЛКСМ) проспект, 34/1'))
fig_percent.update_layout(title='Проценты', xaxis_title='Время', yaxis_title='Процент')

# Отображение графиков
fig_price.show()
fig_percent.show()