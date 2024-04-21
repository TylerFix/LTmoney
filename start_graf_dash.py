import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import datetime
import sqlite3

# Создание приложения Dash
app = dash.Dash(__name__)

# Функция для получения данных из базы данных и обновления графика
def update_data_and_graph(interval):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()

    try:
        # Запрос данных из таблицы Price
        cursor.execute('SELECT * FROM Price')
        price_data = cursor.fetchall()

        # Разделение данных на списки для каждого столбца
        time_price = [row[4] for row in price_data]
        trakt_salt_price = [int(row[1]) for row in price_data]
        derzhprom_nikolskii_price = [int(row[2]) for row in price_data]
        dafi_uvileynii_price = [int(row[3]) for row in price_data]

        # Создание графика
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=time_price, y=trakt_salt_price, mode='lines', name='trakt_salt'))
        fig_price.add_trace(go.Scatter(x=time_price, y=derzhprom_nikolskii_price, mode='lines', name='derzhprom_nikolskii'))
        fig_price.add_trace(go.Scatter(x=time_price, y=dafi_uvileynii_price, mode='lines', name='dafi_uvileynii'))
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
    dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0)
])

# Определение функции обновления графика по интервалу
@app.callback(Output('price-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    return update_data_and_graph(n)

# Запуск приложения Dash
if __name__ == '__main__':
    app.run_server(debug=True)