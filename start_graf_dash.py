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
        # Запрос данных из таблицы Price за указанный временной интервал HA
        cursor.execute('SELECT * FROM PriceHark WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data = cursor.fetchall()

        # Разделение данных на списки для каждого столбца
        time_price = [row[12] for row in price_data]
        sum_ontaxi_ha = [row[11] for row in price_data]
        trakt_salt_price = [row[1] for row in price_data]
        derzhprom_nikolskii_price = [row[2] for row in price_data]
        dafi_uvileynii_price = [row[3] for row in price_data]
        plechan_moroz_price = [row[4] for row in price_data]
        plitk_pastera_price = [row[5] for row in price_data]
        dif_ontaxi_ha_1 = [row[6] for row in price_data]
        dif_ontaxi_ha_2 = [row[7] for row in price_data]
        dif_ontaxi_ha_3 = [row[8] for row in price_data]
        dif_ontaxi_ha_4 = [row[9] for row in price_data]
        dif_ontaxi_ha_5 = [row[10] for row in price_data]
        #plechan_moroz, plitk_pastera,80,54,77

        
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=time_price, y=trakt_salt_price, mode='lines', name=f'Тракторобудівників проспект, 142/1-Салтівське шосе, 262А/5, Б :80, ТТ:{trakt_salt_price[-1]} , %:({dif_ontaxi_ha_1[-1]})'))
        fig_price.add_trace(go.Scatter(x=time_price, y=derzhprom_nikolskii_price, mode='lines', name=f'Ст. Метро "Держпром"-ТРЦ "Нікольський",Б:54,ТТ:{derzhprom_nikolskii_price[-1]} грн, %:({dif_ontaxi_ha_2[-1]})'))
        fig_price.add_trace(go.Scatter(x=time_price, y=dafi_uvileynii_price, mode='lines', name=f'ТЦ "Дафі" (вхід ближче до Roshen)-Ювілейний (50-річчя ВЛКСМ) проспект, 34/1,Б:77,ТТ:{dafi_uvileynii_price[-1]} грн, %:({dif_ontaxi_ha_3[-1]})'))
        fig_price.add_trace(go.Scatter(x=time_price, y=plechan_moroz_price, mode='lines', name=f'Георгія Тарасенка (Плеханівська) вулиця, 43/1-Морозова вулиця, 20А/1,Б:84,ТТ:{plechan_moroz_price[-1]} грн,%:({dif_ontaxi_ha_4[-1]})'))
        fig_price.add_trace(go.Scatter(x=time_price, y=plitk_pastera_price, mode='lines', name=f'Плиткова вулиця, 4-Луї Пастера вулиця, 234А/1,Б:56,ТТ:{plitk_pastera_price[-1]} грн ({dif_ontaxi_ha_5[-1]})'))
        fig_price.add_trace(go.Scatter(x=time_price, y=sum_ontaxi_ha, mode='lines', name=f'Средний процент на город ({sum_ontaxi_ha[-1]})'))
        fig_price.update_layout(title='Цены OnTaxi Харьков', xaxis_title='Время', yaxis_title='Цена')
        # HA Opti
        cursor.execute('SELECT * FROM PriceHarkivOpti WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_opti_ha = cursor.fetchall()

        time_price_opti_ha = [row[11] for row in price_data_opti_ha]
        adress_1_ha = [row[1] for row in price_data_opti_ha]
        adress_2_ha = [row[2] for row in price_data_opti_ha]
        adress_3_ha = [row[3] for row in price_data_opti_ha]
        adress_4_ha = [row[4] for row in price_data_opti_ha]
        adress_5_ha = [row[5] for row in price_data_opti_ha]
           
        fig_price_opti_ha = go.Figure()
        fig_price_opti_ha .add_trace(go.Scatter(x=time_price_opti_ha, y=adress_1_ha, mode='lines', name='Госпром (Майдан Свободы 5/1) - Тц Никольский (Пушкинская ул. 2)'))
        fig_price_opti_ha .add_trace(go.Scatter(x=time_price_opti_ha, y=adress_2_ha, mode='lines', name='Тракторобудівників просп., 134 - Салтівське шосе, 24'))
        fig_price_opti_ha .add_trace(go.Scatter(x=time_price_opti_ha, y=adress_3_ha, mode='lines', name='Трц Дафи ул. Героев Труда 9 - Тюрінська (Якіра) вул., 2'))
        fig_price_opti_ha .add_trace(go.Scatter(x=time_price_opti_ha, y=adress_4_ha, mode='lines', name='Планерна вул., 2 - Біологічна вул., 9'))
        fig_price_opti_ha .add_trace(go.Scatter(x=time_price_opti_ha, y=adress_5_ha, mode='lines', name='Масивна вул., 2 - Соснова вул., 7'))
        fig_price_opti_ha .update_layout(title='Цены Opti Харьков', xaxis_title='Время', yaxis_title='Цена')

        # ZAp
        cursor.execute('SELECT * FROM PriceZap WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_zap = cursor.fetchall()

        
        time_price_zap = [row[12] for row in price_data_zap]
        sum_ontaxi_zap = [row[11] for row in price_data_zap]
        krut_perem_price = [row[1] for row in price_data_zap]
        avram_aptech_price = [row[2] for row in price_data_zap]
        popovka_daln_price = [row[3] for row in price_data_zap]
        ruban_budiv_price = [row[4] for row in price_data_zap]
        tenis_tepli_price = [row[5] for row in price_data_zap]
        dif_ontaxi_zap_1 = [row[6] for row in price_data_zap]
        dif_ontaxi_zap_2 = [row[7] for row in price_data_zap]
        dif_ontaxi_zap_3 = [row[8] for row in price_data_zap]
        dif_ontaxi_zap_4 = [row[9] for row in price_data_zap]
        dif_ontaxi_zap_5 = [row[10] for row in price_data_zap]

       
        fig_price_zap = go.Figure()
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=krut_perem_price, mode='lines', name=f'Героїв Крут (12 Квітня) вулиця, 3 - Перемоги вулиця, 87В / 77 грн ({dif_ontaxi_zap_1[-1]})'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=avram_aptech_price, mode='lines', name=f'Авраменка вулиця, 1 - Аптечна вулиця, 3 / 75 грн ({dif_ontaxi_zap_2[-1]})'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=popovka_daln_price, mode='lines', name=f'Балка Поповка вулиця, 21 - Дальня вулиця, 41/2 / 95 грн ({dif_ontaxi_zap_3[-1]})'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=ruban_budiv_price, mode='lines', name=f'Рубана вулиця, 20 - Будівельників бульвар, 1 / 59 грн ({dif_ontaxi_zap_4[-1]})'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=tenis_tepli_price, mode='lines', name=f'Тенісна вулиця, 20 - Теплична вулиця, 1 / 77 грн({dif_ontaxi_zap_5[-1]})'))
        fig_price_zap.add_trace(go.Scatter(x=time_price_zap, y=sum_ontaxi_zap, mode='lines', name=f'Средний процент город({sum_ontaxi_zap[-1]})'))
        fig_price_zap.update_layout(title='Цены OnTaxi Запорожье', xaxis_title='Время', yaxis_title='Цена')

        # Dnepr
        cursor.execute('SELECT * FROM PriceDnepr WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_dnepr = cursor.fetchall()

        
        time_price_dnepr = [row[12] for row in price_data_dnepr]
        sum_ontaxi_dnepr = [row[11] for row in price_data_dnepr]
        mironova_makar_price = [row[1] for row in price_data_dnepr]
        zapor_zapor_price = [row[2] for row in price_data_dnepr]
        peremog_peremog_price = [row[3] for row in price_data_dnepr]
        novoch_pravdi_price = [row[4] for row in price_data_dnepr]
        zoryana_zlavni_price = [row[5] for row in price_data_dnepr]
        dif_ontaxi_dp_1 = [row[6] for row in price_data_dnepr]
        dif_ontaxi_dp_2 = [row[7] for row in price_data_dnepr]
        dif_ontaxi_dp_3 = [row[8] for row in price_data_dnepr]
        dif_ontaxi_dp_4 = [row[9] for row in price_data_dnepr]
        dif_ontaxi_dp_5 = [row[10] for row in price_data_dnepr]
      

       
        fig_price_dnepr = go.Figure()
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=mironova_makar_price, mode='lines', name=f'Європейська (Миронова) вулиця, 8А - Макарова вулиця, 1А / 114 грн ({dif_ontaxi_dp_1[-1]})'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=zapor_zapor_price, mode='lines', name=f'Запорізьке шосе, 72 - Запорізьке шосе, 27Б / 74 грн ({dif_ontaxi_dp_2[-1]})'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=peremog_peremog_price, mode='lines', name=f'Набережна Перемоги вулиця, 134 - Набережна Перемоги вулиця, 2Г / 113 грн ({dif_ontaxi_dp_3[-1]})'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=novoch_pravdi_price, mode='lines', name=f'Переволочанський (Новочеркаський) провулок, 5 - Слобожанський (Газети "Правда") проспект, 5А / 117 грн ({dif_ontaxi_dp_4[-1]})'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=zoryana_zlavni_price, mode='lines', name=f'Зоряна вулиця, 4 - Славни вулиця, 1 / 66 грн ({dif_ontaxi_dp_5[-1]})'))
        fig_price_dnepr.add_trace(go.Scatter(x=time_price_dnepr, y=sum_ontaxi_dnepr, mode='lines', name=f'Средний процент город ({sum_ontaxi_dnepr[-1]})'))
        fig_price_dnepr.update_layout(title='Цены OnTaxi Днепр', xaxis_title='Время', yaxis_title='Цена')

        #KR

        cursor.execute('SELECT * FROM PriceKR WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_kr = cursor.fetchall()

        
        time_price_kr = [row[12] for row in price_data_kr]
        sum_ontaxi_kr = [row[11] for row in price_data_kr]
        franc_avto_price = [row[1] for row in price_data_kr]
        indus_sonyach_price = [row[2] for row in price_data_kr]
        prosk_goverl_price = [row[3] for row in price_data_kr]
        turn_grud_price = [row[4] for row in price_data_kr]
        glazunov_centr_price = [row[5] for row in price_data_kr]
        dif_ontaxi_kr_1 = [row[6] for row in price_data_kr]
        dif_ontaxi_kr_2 = [row[7] for row in price_data_kr]
        dif_ontaxi_kr_3 = [row[8] for row in price_data_kr]
        dif_ontaxi_kr_4 = [row[9] for row in price_data_kr]
        dif_ontaxi_kr_5 = [row[10] for row in price_data_kr]

       
        fig_price_kr = go.Figure()
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=franc_avto_price, mode='lines', name=f'Французька (Комінтернівська) вулиця, 7 -> Автомеханічна (Кисловодська) вулиця, 1 (60) ({dif_ontaxi_kr_1[-1]})'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=indus_sonyach_price, mode='lines', name=f'Індустріальний мікрорайон, 68 -> Сонячний мікрорайон, 3 (64) ({dif_ontaxi_kr_2[-1]})'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=prosk_goverl_price, mode='lines', name=f'Проскурівська вулиця, 31А -> Говерлівська (Самойлова) вулиця, 82 (79) ({dif_ontaxi_kr_3[-1]})'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=turn_grud_price, mode='lines', name=f'Турнірна вулиця, 10 -> Груднева вулиця, 1 (55) ({dif_ontaxi_kr_4[-1]})'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=glazunov_centr_price, mode='lines', name=f'Старотернівська (Глазунова) вулиця, 106 -> Центральна вулиця, 1А (79) ({dif_ontaxi_kr_5[-1]})'))
        fig_price_kr.add_trace(go.Scatter(x=time_price_kr, y=sum_ontaxi_kr, mode='lines', name=f'Средний процент на город ({sum_ontaxi_kr[-1]})'))
        fig_price_kr.update_layout(title='Цены OnTaxi Кривой Рог', xaxis_title='Время', yaxis_title='Цена')
    
        # Zt

        cursor.execute('SELECT * FROM PriceZhitom WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_zt = cursor.fetchall()

        
        time_price_zt = [row[12] for row in price_data_zt]
        sum_ontaxi_zt = [row[11] for row in price_data_zt]
        mazep_epic_price = [row[1] for row in price_data_zt]
        novog_hinch_price = [row[2] for row in price_data_zt]
        korol_komun_price = [row[3] for row in price_data_zt]
        shors_novaposh_price = [row[4] for row in price_data_zt]
        knyas_koval_price = [row[5] for row in price_data_zt]
        dif_ontaxi_zt_1 = [row[6] for row in price_data_zt]
        dif_ontaxi_zt_2 = [row[7] for row in price_data_zt]
        dif_ontaxi_zt_3 = [row[8] for row in price_data_zt]
        dif_ontaxi_zt_4 = [row[9] for row in price_data_zt]
        dif_ontaxi_zt_5 = [row[10] for row in price_data_zt]
      

       
        fig_price_zt = go.Figure()
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=mazep_epic_price, mode='lines', name=f'І. Мазепи (Мануїльського) вулиця, 164 -> Пункт Незламності (Епіцентр) (59) ({dif_ontaxi_zt_1[-1]})'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=novog_hinch_price, mode='lines', name=f'Новогоголівська вулиця, 42/1 -> Хінчанський проїзд, 1/67 (70) ({dif_ontaxi_zt_2[-1]})'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=korol_komun_price, mode='lines', name=f'Корольова вулиця, 101 -> Комунальний провулок, 1 (54) ({dif_ontaxi_zt_3[-1]})'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=shors_novaposh_price, mode='lines', name=f'Покровська (Щорса) вулиця, 142 -> Пункт Незламності (Нова пошта №27) (72) ({dif_ontaxi_zt_4[-1]})'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=knyas_koval_price, mode='lines', name=f'Князькова вулиця, 39А -> Є. Коновальця (Якубовського) вулиця, 7А (90) ({dif_ontaxi_zt_5[-1]})'))
        fig_price_zt.add_trace(go.Scatter(x=time_price_zt, y=sum_ontaxi_zt, mode='lines', name=f'Средний процент город({sum_ontaxi_zt[-1]})'))
        fig_price_zt.update_layout(title='Цены OnTaxi Житомир', xaxis_title='Время', yaxis_title='Цена')
        # Zap Opti

        cursor.execute('SELECT * FROM PriceZapOpti WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_opti_zap = cursor.fetchall()

        
        time_price_opti_zap = [row[11] for row in price_data_opti_zap]
        adress_1_zap = [row[1] for row in price_data_opti_zap]
        adress_2_zap = [row[2] for row in price_data_opti_zap]
        adress_3_zap = [row[3] for row in price_data_opti_zap]
        adress_4_zap = [row[4] for row in price_data_opti_zap]
        adress_5_zap = [row[5] for row in price_data_opti_zap]
      

       
        fig_price_opti_zap = go.Figure()
        fig_price_opti_zap.add_trace(go.Scatter(x=time_price_opti_zap, y=adress_1_zap, mode='lines', name='Атб (Патриотическая 52а) -Броньова вул., 16'))
        fig_price_opti_zap.add_trace(go.Scatter(x=time_price_opti_zap, y=adress_2_zap, mode='lines', name='Дружний проїзд, 12 - Перемоги вул., 63'))
        fig_price_opti_zap.add_trace(go.Scatter(x=time_price_opti_zap, y=adress_3_zap, mode='lines', name='Хортицьке шосе, 34 - Сорочинская ул. (Новгородская ул.) 11'))
        fig_price_opti_zap.add_trace(go.Scatter(x=time_price_opti_zap, y=adress_4_zap, mode='lines', name='Полякова ул. 21 - Карпенко-Карого ул. 40'))
        fig_price_opti_zap.add_trace(go.Scatter(x=time_price_opti_zap, y=adress_5_zap, mode='lines', name='Хортицкая ул. (Разумовка пос.) 20 - Кооперативная ул. (Разумовка) 11'))
        fig_price_opti_zap.update_layout(title='Цены Opti Запорожье', xaxis_title='Время', yaxis_title='Цена')

        # Opti Dnepr

        cursor.execute('SELECT * FROM PriceDneprOpti WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_opti_dnepr = cursor.fetchall()

        
        time_price_opti_dnepr = [row[11] for row in price_data_opti_dnepr]
        adress_1_dp = [row[1] for row in price_data_opti_dnepr]
        adress_2_dp = [row[2] for row in price_data_opti_dnepr]
        adress_3_dp = [row[3] for row in price_data_opti_dnepr]
        adress_4_dp = [row[4] for row in price_data_opti_dnepr]
        adress_5_dp = [row[5] for row in price_data_opti_dnepr]
      

       
        fig_price_opti_dnepr = go.Figure()
        fig_price_opti_dnepr.add_trace(go.Scatter(x=time_price_opti_dnepr, y=adress_1_dp, mode='lines', name='Пригородная ул., 27 - Каруны ул. 8'))
        fig_price_opti_dnepr.add_trace(go.Scatter(x=time_price_opti_dnepr, y=adress_2_dp, mode='lines', name='С Делви (Паникахи ул. 48) - Тополиная ул. (Тополь) 41'))
        fig_price_opti_dnepr.add_trace(go.Scatter(x=time_price_opti_dnepr, y=adress_3_dp, mode='lines', name='Днепр -Главный - Боброва ул. (Майдан Озёрный) 12'))
        fig_price_opti_dnepr.add_trace(go.Scatter(x=time_price_opti_dnepr, y=adress_4_dp, mode='lines', name='Херсонская ул. 46 - Русановская ул. 121'))
        fig_price_opti_dnepr.add_trace(go.Scatter(x=time_price_opti_dnepr, y=adress_5_dp, mode='lines', name='Овражная ул. 49 - Переяславская ул. 21'))
        fig_price_opti_dnepr.update_layout(title='Цены Opti Днепр', xaxis_title='Время', yaxis_title='Цена')
        # Opti KR

        cursor.execute('SELECT * FROM PriceKROpti WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_opti_kr = cursor.fetchall()

        
        time_price_opti_kr = [row[11] for row in price_data_opti_kr]
        adress_1_kr = [row[1] for row in price_data_opti_kr]
        adress_2_kr = [row[2] for row in price_data_opti_kr]
        adress_3_kr = [row[3] for row in price_data_opti_kr]
        adress_4_kr = [row[4] for row in price_data_opti_kr]
        adress_5_kr = [row[5] for row in price_data_opti_kr]
      

       
        fig_price_opti_kr = go.Figure()
        fig_price_opti_kr.add_trace(go.Scatter(x=time_price_opti_kr, y=adress_1_kr, mode='lines', name='Ярослава Мудрого (Брозовського Отто) вул., 55 - Героїв АТО (Димитрова) вул., 27'))
        fig_price_opti_kr.add_trace(go.Scatter(x=time_price_opti_kr, y=adress_2_kr, mode='lines', name='Нарвська вул., 8 - Коцюбинського вул., 9'))
        fig_price_opti_kr.add_trace(go.Scatter(x=time_price_opti_kr, y=adress_3_kr, mode='lines', name=' Дубки (Косарева) вул., 193 - Тесленка вул., 24'))
        fig_price_opti_kr.add_trace(go.Scatter(x=time_price_opti_kr, y=adress_4_kr, mode='lines', name='Сергія Колачевського (23-го Лютого) вул., 66 - Тимирязева ул. 26'))
        fig_price_opti_kr.add_trace(go.Scatter(x=time_price_opti_kr, y=adress_5_kr, mode='lines', name='Танкістів вул., 40 - Беринга вул., 7'))
        fig_price_opti_kr.update_layout(title='Цены Opti Кривой Рог', xaxis_title='Время', yaxis_title='Цена')

        # Opti Zt

        cursor.execute('SELECT * FROM PriceZhitomOpti WHERE time BETWEEN ? AND ?', (start_time, end_time))
        price_data_opti_zt = cursor.fetchall()

        
        time_price_opti_zt = [row[11] for row in price_data_opti_zt]
        adress_1_zt = [row[1] for row in price_data_opti_zt]
        adress_2_zt = [row[2] for row in price_data_opti_zt]
        adress_3_zt = [row[3] for row in price_data_opti_zt]
        adress_4_zt = [row[4] for row in price_data_opti_zt]
        adress_5_zt = [row[5] for row in price_data_opti_zt]
      

       
        fig_price_opti_zt = go.Figure()
        fig_price_opti_zt.add_trace(go.Scatter(x=time_price_opti_zt, y=adress_1_zt, mode='lines', name='Селецкая ул. 10 - Королева ул. 51'))
        fig_price_opti_zt.add_trace(go.Scatter(x=time_price_opti_zt, y=adress_2_zt, mode='lines', name='3-Й Чудновский пер. 4 - Гагарина ул. 6'))
        fig_price_opti_zt.add_trace(go.Scatter(x=time_price_opti_zt, y=adress_3_zt, mode='lines', name='Каракульная ул. 27 - Друкарский ( Колхозный 2-Й) пер. 36'))
        fig_price_opti_zt.add_trace(go.Scatter(x=time_price_opti_zt, y=adress_4_zt, mode='lines', name='Украинки Леси ул. 40 - Тена Бориса ул. 123'))
        fig_price_opti_zt.add_trace(go.Scatter(x=time_price_opti_zt, y=adress_5_zt, mode='lines', name='Вокзальная ул. 3 - Космонавтов ул. 4'))
        fig_price_opti_zt.update_layout(title='Цены Opti Житомир', xaxis_title='Время', yaxis_title='Цена')
        
        
        return fig_price, fig_price_zap, fig_price_dnepr, fig_price_kr, fig_price_zt,fig_price_opti_ha, fig_price_opti_zap, fig_price_opti_dnepr, fig_price_opti_kr, fig_price_opti_zt


    except Exception as e:
        print("Ошибка при обновлении графика:", e)
        return None
    finally:
        # Закрытие соединения с базой данных
        conn.close()

# Определение макета веб-приложения
app.layout = html.Div(children=[
    dcc.Graph(id='price-graph-hark'),
    dcc.Graph(id='price-graph-zap'),
    dcc.Graph(id='price-graph-dnepr'),
    dcc.Graph(id='price-graph-kr'),
    dcc.Graph(id='price-graph-zt'),
    dcc.Graph(id='price-graph-opti-ha'),
    dcc.Graph(id='price-graph-opti-zap'),
    dcc.Graph(id='price-graph-opti-dnepr'),
    dcc.Graph(id='price-graph-opti-kr'),
    dcc.Graph(id='price-graph-opti-zt'),
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
@app.callback(Output('price-graph-hark', 'figure'),Output('price-graph-zap','figure'),Output('price-graph-dnepr','figure'),Output('price-graph-kr','figure'),Output('price-graph-zt','figure'),Output('price-graph-opti-ha','figure'),Output('price-graph-opti-zap','figure'),Output('price-graph-opti-dnepr','figure'),Output('price-graph-opti-kr','figure'),Output('price-graph-opti-zt','figure'),
              Input('date-picker-range', 'start_date'),
               Input('date-picker-range', 'end_date'),
               Input('auto-update-checklist', 'value'),
               Input('interval-component', 'n_intervals'))
def update_graph(start_date, end_date, auto_update_value, n_intervals):
    if 'enabled' in auto_update_value:
        return update_data_and_graph(start_date, end_date)
    else:
        return dash.no_update

# Запуск приложения Dash
if __name__ == '__main__':
    app.run_server()
    #app.run_server(debug=True)