import datetime as dt
import os
import requests
import json

import numpy as np
import pandas as pd
import dotenv as env





env.load_dotenv()
TIINGO_API = os.getenv("TIINGO_API_KEY")

# bank of america, citigroup, goldman sachs, jpmorgan chase, morgan stanley, wells fargo
STOCK_TICKERS = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

# get stock data using pandas datareader and return a dataframe
def get_tiingo_stock_data (ticker):
        request_url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate=2006-1-1&endDate=2016-1-1&token={TIINGO_API}"
        headers = {
            'Content-Type': 'application/json'
        }
        requestResponse = requests.get(request_url, headers=headers)
        return requestResponse.json()

def scrape_stock_data(tickers):
    for ticker in tickers:
        json_data = get_tiingo_stock_data(ticker)
        with open(f"{ticker}_data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)







def main():
    print(get_tiingo_stock_data('INTC'))

if __name__ == '__main__':
    main()