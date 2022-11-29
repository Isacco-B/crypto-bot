import requests
import json
import time
from datetime import datetime


class Bot():
    def __init__(self,params):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.params = params 
        self.headers = {
            'Accepts' : 'application/json',
            'X-CMC_PRO_API_KEY' : '86c54475-e065-4001-8f36-6aa8f6ec8f18'
        }

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']

while(True):
    
    name_json_file = datetime.now().strftime("%d_%m_%Y - %H:%M:%S")
    currency_data = Bot(params={'start': '1','limit': '100','convert': 'USD'}).fetchCurrenciesData()
    best_10_currency = Bot(params={'start': '1','limit': '10','convert': 'USD','sort': 'percent_change_24h'}).fetchCurrenciesData()
    worst_10_currency = Bot(params={'start': '1','limit': '10','convert': 'USD','sort': 'percent_change_24h','sort_dir': 'asc'}).fetchCurrenciesData()
    first_20_currency = Bot(params={'start': '1','limit': '20','convert': 'USD'}).fetchCurrenciesData()


# Calcola la criptovaluta con il volume maggiore (in $) delle ultime 24 ore
    def currencyVolume(currencies):
        higher_currency_vol = None
        for currency in currencies:
            if not higher_currency_vol or currency['quote']['USD']['volume_24h'] > higher_currency_vol['quote']['USD']['volume_24h']:
                higher_currency_vol = currency
        return higher_currency_vol

# Calcola le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)
    def bestWorstCurrency(currencies):
        i = 1
        best_worst_currency = []
        for currency in currencies:
            d = {
                f'{i}' : currency
            }
            i += 1
            best_worst_currency.append(d)
        return best_worst_currency

# Calcola la quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute*
# La quantita di denaro necessaria per acquistare una unita di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
    def currencyPrice(currencies,volume=0):
        price = 0
        if volume > 0:
            for currency in currencies:
                if currency['quote']['USD']['volume_24h'] > 76000000:
                    price += currency['quote']['USD']['price']
            return price
        else:
            for currency in currencies:
                price += currency['quote']['USD']['price']
            return price

# Calcola la percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna
# delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata)
    def earningPercentage(currencies):
        buy_price = 0
        for currency in currencies:
            buy_price += currency['quote']['USD']['price'] * 100 / (100 + currency['quote']['USD']['percent_change_24h'])
        sell_price = currencyPrice(first_20_currency)
        percentuale = round((sell_price - buy_price) / buy_price * 100, 2)
        return percentuale


    track_1 = currencyVolume(currency_data)
    track_2 = bestWorstCurrency(best_10_currency)
    track_3 = bestWorstCurrency(worst_10_currency)
    track_4 = currencyPrice(first_20_currency)
    track_5 = currencyPrice(currency_data,volume=76000000)
    track_6 = earningPercentage(first_20_currency)

    file_json = [{

        "La criptovaluta con il volume maggiore (in $) delle ultime 24 ore" : track_1,
        "Le migliori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)" : track_2,
        "Le peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)" : track_3,
        "La quantita di denaro necessaria per acquistare una unita di ciascuna delle prime 20 criptovalute" : track_4,
        "La quantita di denaro necessaria per acquistare una unita di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$" : track_5,
        "La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unita di ciascuna delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata)" : track_6
    }]

    with open(f'{name_json_file}.json', 'w') as f:
        print("The json file is created")
        json.dump(file_json, f, indent= 4)
    
    hours = 24
    seconds = hours * 60 * 60
    time.sleep(seconds)