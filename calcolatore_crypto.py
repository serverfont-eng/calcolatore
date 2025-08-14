
import streamlit as st
import requests
from datetime import datetime

# Funzione per ottenere l'ID della crypto su CoinGecko a partire dal simbolo
def get_coin_id(symbol):
    url = "https://api.coingecko.com/api/v3/coins/list"
    coins = requests.get(url).json()
    for coin in coins:
        if coin['symbol'].lower() == symbol.lower():
            return coin['id']
    return None

# Funzione per ottenere il prezzo storico di una crypto in USD
def get_historical_price(coin_id, date):
    formatted_date = date.strftime('%d-%m-%Y')
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={formatted_date}"
    data = requests.get(url).json()
    try:
        return data['market_data']['current_price']['usd']
    except KeyError:
        return None

# Funzione per ottenere il prezzo attuale di una crypto
def get_current_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    data = requests.get(url).json()
    return data[coin_id]['usd']

# UI dell'app
st.set_page_config(page_title="Calcolatore Guadagni Crypto", page_icon="💰")
st.title("💰 Calcolatore Guadagni Crypto")
st.write("Inserisci i dettagli del tuo investimento per scoprire quanto varrebbe oggi.")

symbol = st.text_input("Simbolo della crypto (es. BTC, ETH, TROLL)").strip()
investment = st.number_input("Importo investito in USD", min_value=1.0, value=100.0)
date = st.date_input("Data di acquisto", value=datetime(2024, 1, 1))

if st.button("Calcola"):
    coin_id = get_coin_id(symbol)
    if not coin_id:
        st.error("Crypto non trovata. Controlla il simbolo.")
    else:
        historical_price = get_historical_price(coin_id, date)
        current_price = get_current_price(coin_id)

        if historical_price and current_price:
            quantity = investment / historical_price
            current_value = quantity * current_price
            profit_percent = ((current_value - investment) / investment) * 100

            st.success(f"💹 Valore attuale: ${current_value:,.2f}")
            st.info(f"📈 Guadagno/Perdita: {profit_percent:.2f}%")
            st.write(f"Prezzo di acquisto: ${historical_price:,.8f} USD")
            st.write(f"Prezzo attuale: ${current_price:,.8f} USD")
        else:
            st.error("Impossibile ottenere i dati per la data selezionata.")
