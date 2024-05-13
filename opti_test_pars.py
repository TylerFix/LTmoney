import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import datetime
import sqlite3

# Создание приложения Dash
app = dash.Dash(__name__)

# Функция для получения данных из базы данных и обновления графика
def update_data_and_graph(start_time, end_time):

    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()

    try:
        # Запрос данных из таблицы Price за указанный временной интервал HA
        cursor.execute('SELECT * FROM PriceHark WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data = cursor.fetchall()

        # Разделение данных на списки для каждого столбца
        time_price = [row[11] for row in price_data]
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
        # ZAp
        cursor.execute('SELECT * FROM PriceZap WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_zap = cursor.fetchall()

        
        time_price_zap = [row[11] for row in price_data_zap]
        krut_perem_price = [int(row[1]) for row in price_data_zap]
        avram_aptech_price = [int(row[2]) for row in price_data_zap]
        popovka_daln_price = [int(row[3]) for row in price_data_zap]
        ruban_budiv_price = [row[4] for row in price_data_zap]
        tenis_tepli_price = [row[5] for row in price_data_zap]
      

       
        fig_price_zap = go.Figure()
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=krut_perem_price, mode='lines', name='Героїв Крут (12 Квітня) вулиця, 3 - Перемоги вулиця, 87В / 77 грн'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=avram_aptech_price, mode='lines', name='Авраменка вулиця, 1 - Аптечна вулиця, 3 / 75 грн'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=popovka_daln_price, mode='lines', name='Балка Поповка вулиця, 21 - Дальня вулиця, 41/2 / 95 грн'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=ruban_budiv_price, mode='lines', name='Рубана вулиця, 20 - Будівельників бульвар, 1 / 59 грн'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=tenis_tepli_price, mode='lines', name='Тенісна вулиця, 20 - Теплична вулиця, 1 / 77 грн'))
        fig_price_zap.update_layout(title='Цены OnTaxi Запорожье', xaxis_title='Время', yaxis_title='Цена')

        # Dnepr
        cursor.execute('SELECT * FROM PriceDnepr WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_dnepr = cursor.fetchall()

        
        time_price_dnepr = [row[11] for row in price_data_dnepr]
        mironova_makar_price = [int(row[1]) for row in price_data_dnepr]
        zapor_zapor_price = [int(row[2]) for row in price_data_dnepr]
        peremog_peremog_price = [int(row[3]) for row in price_data_dnepr]
        novoch_pravdi_price = [row[4] for row in price_data_dnepr]
        zoryana_zlavni_price = [row[5] for row in price_data_dnepr]
      

       
        fig_price_dnepr = go.Figure()
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=mironova_makar_price, mode='lines', name='Європейська (Миронова) вулиця, 8А - Макарова вулиця, 1А / 114 грн'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=zapor_zapor_price, mode='lines', name='Запорізьке шосе, 72 - Запорізьке шосе, 27Б / 74 грн'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=peremog_peremog_price, mode='lines', name='Набережна Перемоги вулиця, 134 - Набережна Перемоги вулиця, 2Г / 113 грн'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=novoch_pravdi_price, mode='lines', name='Переволочанський (Новочеркаський) провулок, 5 - Слобожанський (Газети "Правда") проспект, 5А / 117 грн'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=zoryana_zlavni_price, mode='lines', name='Зоряна вулиця, 4 - Славни вулиця, 1 / 66 грн'))
        fig_price_dnepr.update_layout(title='Цены OnTaxi Днепр', xaxis_title='Время', yaxis_title='Цена')

        #KR

        cursor.execute('SELECT * FROM PriceKR WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_kr = cursor.fetchall()

        
        time_price_kr = [row[11] for row in price_data_kr]
        franc_avto_price = [int(row[1]) for row in price_data_kr]
        indus_sonyach_price = [int(row[2]) for row in price_data_kr]
        prosk_goverl_price = [int(row[3]) for row in price_data_kr]
        turn_grud_price = [row[4] for row in price_data_kr]
        glazunov_centr_price = [row[5] for row in price_data_kr]
      

       
        fig_price_kr = go.Figure()
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=franc_avto_price, mode='lines', name='Французька (Комінтернівська) вулиця, 7 -> Автомеханічна (Кисловодська) вулиця, 1 (60)'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=indus_sonyach_price, mode='lines', name='Індустріальний мікрорайон, 68 -> Сонячний мікрорайон, 3 (64)'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=prosk_goverl_price, mode='lines', name='Проскурівська вулиця, 31А -> Говерлівська (Самойлова) вулиця, 82 (79)'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=turn_grud_price, mode='lines', name='Турнірна вулиця, 10 -> Груднева вулиця, 1 (55)'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=glazunov_centr_price, mode='lines', name='Старотернівська (Глазунова) вулиця, 106 -> Центральна вулиця, 1А (79)'))
        fig_price_kr.update_layout(title='Цены OnTaxi Кривой Рог', xaxis_title='Время', yaxis_title='Цена')
    
        # Zt

        cursor.execute('SELECT * FROM PriceZhitom WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_zt = cursor.fetchall()

        
        time_price_zt = [row[11] for row in price_data_zt]
        mazep_epic_price = [int(row[1]) for row in price_data_zt]
        novog_hinch_price = [int(row[2]) for row in price_data_zt]
        korol_komun_price = [int(row[3]) for row in price_data_zt]
        shors_novaposh_price = [row[4] for row in price_data_zt]
        knyas_koval_price = [row[5] for row in price_data_zt]
      

       
        fig_price_zt = go.Figure()
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=mazep_epic_price, mode='lines', name='І. Мазепи (Мануїльського) вулиця, 164 -> Пункт Незламності (Епіцентр) (59)'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=novog_hinch_price, mode='lines', name='Новогоголівська вулиця, 42/1 -> Хінчанський проїзд, 1/67 (70)'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=korol_komun_price, mode='lines', name='Корольова вулиця, 101 -> Комунальний провулок, 1 (54)'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=shors_novaposh_price, mode='lines', name='Покровська (Щорса) вулиця, 142 -> Пункт Незламності (Нова пошта №27) (72)'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=knyas_koval_price, mode='lines', name='Князькова вулиця, 39А -> Є. Коновальця (Якубовського) вулиця, 7А (90)'))
        fig_price_zt.update_layout(title='Цены OnTaxi Житомир', xaxis_title='Время', yaxis_title='Цена')
        

        return fig_price, fig_price_zap, fig_price_dnepr, fig_price_kr, fig_price_zt
    except Exception as e:
        print("Ошибка при обновлении графика:", e)
        return None
    finally:
        # Закрытие соединения с базой данных
        conn.close()

# Определение макета веб-приложения
app.layout = html.Div([
    html.Button('OnTaxi', id='btn-1', n_clicks=0),
    html.Button('Opti', id='btn-2', n_clicks=0),
    html.Div(id='page-content')
])

# Обработчик событий для переключения между страницами
@app.callback(
    Output('page-content', 'children'),
    [Input('btn-1', 'n_clicks'),
     Input('btn-2', 'n_clicks')]
)
def display_page(btn_1_clicks, btn_2_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-1' in changed_id:
        return html.Div([
            html.H1('Это страница 1'),
            dcc.Graph(id='price-graph-hark'),
            dcc.Graph(id='price-graph-zap'),
            dcc.Graph(id='price-graph-dnepr'),
            dcc.Graph(id='price-graph-kr'),
            dcc.Graph(id='price-graph-zt')
        ])
    elif 'btn-2' in changed_id:
        return html.Div([
            html.H1('Это страница 2'),
            dcc.Graph(id='price-graph')
        ])
    else:
        return html.Div([
            html.H1('Это страница 1'),
            dcc.Graph(id='price-graph')
        ])

# Запуск приложения Dash
if __name__ == '__main__':
    app.run_server(debug=True)