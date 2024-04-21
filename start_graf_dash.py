import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import datetime
import sqlite3

# Создание приложения Dash
app = dash.Dash(__name__)

# Функция для получения данных из базы данных и обновления графика
def update_data_and_graph(start_time, end_time):

    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()

    try:
        # Запрос данных из таблицы Price за указанный временной интервал
        cursor.execute('SELECT * FROM Price WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data = cursor.fetchall()

        # Разделение данных на списки для каждого столбца
        time_price = [row[6] for row in price_data]
        trakt_salt_price = [int(row[1]) for row in price_data]
        derzhprom_nikolskii_price = [int(row[2]) for row in price_data]
        dafi_uvileynii_price = [int(row[3]) for row in price_data]
        plechan_moroz_price = [row[4] for row in price_data]
        plitk_pastera_price = [row[5] for row in price_data]
        #plechan_moroz, plitk_pastera,80,54,77

        # Создание графика
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=time_price, y=trakt_salt_price, mode='lines', name='Тракторобудівників проспект, 142/1 - Салтівське шосе, 262А/5, 80 грн'))
        fig_price.add_trace(go.Scatter(x=time_price, y=derzhprom_nikolskii_price, mode='lines', name='Ст. Метро "Держпром" - ТРЦ "Нікольський", 54 грн'))
        fig_price.add_trace(go.Scatter(x=time_price, y=dafi_uvileynii_price, mode='lines', name='ТЦ "Дафі" (вхід ближче до Roshen) - Ювілейний (50-річчя ВЛКСМ) проспект, 34/1, 77 грн'))
        fig_price.add_trace(go.Scatter(x=time_price, y=plechan_moroz_price, mode='lines', name='Георгія Тарасенка (Плеханівська) вулиця, 43/1 - Морозова вулиця, 20А/1, 84 грн'))
        fig_price.add_trace(go.Scatter(x=time_price, y=plitk_pastera_price, mode='lines', name='Плиткова вулиця, 4 - Луї Пастера вулиця, 234А/1, 56 грн'))
        fig_price.update_layout(title='Цены OnTaxi Харьков', xaxis_title='Время', yaxis_title='Цена')

        return fig_price
    except Exception as e:
        print("Ошибка при обновлении графика:", e)
        return None
    finally:
        # Закрытие соединения с базой данных
        conn.close()

# Определение макета веб-приложения
app.layout = html.Div(children=[
    dcc.Graph(id='price-graph'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=datetime.datetime.now() - datetime.timedelta(days=1),
        end_date=datetime.datetime.now()
    ),
    html.Label('Автоматическое обновление данных:'),
    dcc.Checklist(
        id='auto-update-checklist',
        options=[{'label': 'Включено', 'value': 'enabled'}],
        value=[]
    ),
    dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0)
])

# Определение функции обновления графика по интервалу и при включении чек-бокса
@app.callback(Output('price-graph', 'figure'),
              [Input('date-picker-range', 'start_date'),
               Input('date-picker-range', 'end_date'),
               Input('auto-update-checklist', 'value'),
               Input('interval-component', 'n_intervals')])
def update_graph(start_date, end_date, auto_update_value, n_intervals):
    if 'enabled' in auto_update_value:
        return update_data_and_graph(start_date, end_date)
    else:
        return dash.no_update

# Запуск приложения Dash
if __name__ == '__main__':
    app.run_server(debug=True)