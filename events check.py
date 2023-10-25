from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timezone, date, timedelta
import locale



tele_auth_token = "6763894837:AAFFj52q-g-arFORD7zoJTnUM3PZDhiq2TU" # Authentication token provided by Telegram bot
tel_group_id = "eventi_fuorigrotta" # Telegram group name
#data:
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
data_corrente = date.today()
data_corrent_plus_1 = data_corrente + timedelta(days=1)
nome_mese_abbreviato = data_corrente.strftime('%b')
date_plus_one = '2023-10-23'
giorno = data_corrente.day
ora_desiderata = 8  # Esempio: 13 rappresenta le 13:00 (1:00 PM)
#links:
basket_napoli_page_link = 'https://napolibasket.it/calendario-2023-24/'
calcio_napoli_page_link = 'https://sscnapoli.it/calendario/'
eventi_mostra_napoli_page_link = 'https://www.mostradoltremare.it/events/oggi/?tribe-bar-date='



def basket_search():
    source = requests.get(basket_napoli_page_link, timeout=20).text
    soup = BeautifulSoup(source, 'lxml')
    calendar = soup.find('tbody')
    lega = 'Basket'
    for link in calendar.find_all('tr'):
        match_date = link.find('td', class_='data-date').text.split(' ', 1)[0]
        match_data_ora = link.find('date').text
        match_casa = link.find('td', class_='data-home has-logo has-logo').text
        match_fuori_casa = link.find('td', class_='data-away has-logo has-logo').text
        if link is not None:
            if (match_date == data_corrente or match_date == data_corrent_plus_1) and match_casa == 'GeVi Napoli Basket ': 
                send_msg_on_telegram(lega, match_data_ora, (match_casa + ' - ' + match_fuori_casa), basket_napoli_page_link)
            else: 
                print(lega, match_data_ora, (match_casa + ' - ' + match_fuori_casa), 'non ricorre tra oggi e domani')
        else: 
            print('Nessun evento ' + lega + ' rilevato')

def calcio_search():
    source = requests.get(calcio_napoli_page_link, timeout=20).text
    soup = BeautifulSoup(source, 'lxml')
    calendar = soup.find('div', class_='partite-olimpia')
    lega_1 = 'Calcio Serie A'
    lega_2 = 'Calcio Champions League'
    for link in calendar.find_all('div', class_='schedule-single d-flex flex-wrap flex-lg-nowrap position-relative mb-3 mb-md-2 scheduled championship-1 place-home'):
        match_giorno = link.find('p', class_='number-stagione heading xl bold').text
        match_mese = link.find('p', class_= 'text body m').text
        match_ora = link.find('p', class_= 'time body l semibold').text
        match_date = match_giorno + ' ' + match_mese + ' ' + match_ora
        match_casa = link.find('p', class_='team-name heading l bold clr-blueDark me-3').text
        match_fuori_casa = link.find('p', class_='team-name heading l bold clr-blueDark ms-3').text
        if link is not None:
            if str(match_giorno + match_mese)==(str(giorno) + nome_mese_abbreviato) or str(match_giorno + match_mese)==(str(giorno + 1) + nome_mese_abbreviato) :
                send_msg_on_telegram(lega_1, (match_giorno + ' ' + match_mese), (match_casa + ' - ' + match_fuori_casa), calcio_napoli_page_link)
            else: 
                print(lega_1, (match_giorno + ' ' + match_mese), (match_casa + ' - ' + match_fuori_casa), 'non ricorre tra oggi e domani')
        else: 
            print('Nessun evento ' + lega_1 + ' rilevato')

    for link in calendar.find_all('div', class_='schedule-single d-flex flex-wrap flex-lg-nowrap position-relative mb-3 mb-md-2 scheduled championship-4 place-home'):
        match_giorno = link.find('p', class_='number-stagione heading xl bold').text
        match_mese = link.find('p', class_= 'text body m').text
        match_ora = link.find('p', class_= 'time body l semibold').text
        match_date = match_giorno + ' ' + match_mese + ' ' + match_ora
        match_casa = link.find('p', class_='team-name heading l bold clr-blueDark me-3').text
        match_fuori_casa = link.find('p', class_='team-name heading l bold clr-blueDark ms-3').text
        if link is not None:
            if str(match_giorno + match_mese)==(str(giorno) + nome_mese_abbreviato) or str(match_giorno + match_mese)==(str(giorno + 1) + nome_mese_abbreviato):
                send_msg_on_telegram(lega_2, (match_giorno + ' ' + match_mese), (match_casa + ' - ' + match_fuori_casa), calcio_napoli_page_link)
            else:
                print(lega_2, (match_giorno + ' ' + match_mese), (match_casa + ' - ' + match_fuori_casa), 'non ricorre tra oggi e domani')
        else: 
            print('Nessun evento ' + lega_2 + ' rilevato')


def mostra_search():
    link_filter = eventi_mostra_napoli_page_link + str(data_corrente)
    source = requests.get(link_filter, timeout=20).text
    soup = BeautifulSoup(source, 'lxml')
    lega = 'Mosta Oltremare'
    
    calendar = soup.find('div', class_='tribe-events-day')
    for link in calendar.find_all('div', class_='type-tribe_events'):
        evento = link.find('a', class_='url').text.strip()
        start_date = link.find('span', class_='tribe-event-date-start').text
        end_date = link.find('span', class_='tribe-event-date-end').text
        data_evento = start_date + ' - ' + end_date
        send_msg_on_telegram(lega, data_evento, evento, link_filter)


def send_msg_on_telegram(lega, data, evento, info):

    msg = (lega + ': ' + data + ', ' + evento + '. Info:' + info)
    telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id=@{tel_group_id}&text={msg}"
    tel_resp = requests.get(telegram_api_url)
    if tel_resp.status_code == 200:
        print ("Notification for " +  msg + "has been sent on Telegram")
    else:
        print ("Could not send Message: status "+str(tel_resp))

basket_search()
calcio_search()
mostra_search()

