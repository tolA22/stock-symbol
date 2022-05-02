from random import random
import requests
from multiprocessing.pool import ThreadPool
from settings import FINNHUB_API_KEY, FINNHUB_BASE_URL
import csv

HEADER = ['stock_symbol', 'percentage_change',
          'current_price', 'last_close_price']


def main():
    pool = ThreadPool(6)
    results = []
    #APPLE, AMAZON, NETFLIX, FACEBOOK, GOOGLE
    symbolList = ["AAPL", "AMZN", "NFLX", "MSFT", "FB", "GOOGL"]
    for symbol in symbolList:
        results.append(pool.apply_async(fetchQuotes(symbol)))
    pool.close()
    pool.join()
    results = [r.get() for r in results]
    most_volatile_stock = None
    current = 0
    symbol = symbolList[current]
    for i in range(0, len(results)):
        stock = results[i]
        percentChange = abs(stock["dp"])
        if((percentChange) > current):
            current = (percentChange)
            most_volatile_stock = stock
            symbol = symbolList[i]

    generateCSV(symbol, most_volatile_stock)
    print(most_volatile_stock, "Most volatile stock")


def fetchQuotes(symbol):
    try:
        url = "{}quote?symbol={}&token={}".format(
            FINNHUB_BASE_URL, symbol, FINNHUB_API_KEY)
        response = requests.get(url)
        return response.json
    except Exception as e:
        return None


def generateCSV(symbol, data):
    data = [symbol, data["dp"], data["c"], data["pc"]]
    path = 'stock-symbol{}.csv'.format(int(random()))
    print(path)
    with open(path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(HEADER)
        # write the data
        writer.writerow(data)


main()
