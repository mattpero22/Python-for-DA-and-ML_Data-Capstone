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

# get stock data using REST request and Tiingo's endpoint and return a dataframe
def get_tiingo_stock_data (ticker):
        request_url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate=2006-1-1&endDate=2016-1-1&token={TIINGO_API}"
        headers = {
            'Content-Type': 'application/json'
        }
        requestResponse = requests.get(request_url, headers=headers)
        return requestResponse.json()

# work in tandem with get_tiingo_stock_data to dump the json response into a local file
def scrape_stock_data(tickers):
    for ticker in tickers:
        json_data = get_tiingo_stock_data(ticker)
        with open(f"{ticker}_data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)


# go through directory of json files and aggregate the data into a MultiIndex dataframe
def aggregate_bank_data(tickers):
    dataframes = [pd.read_json(f"./stock_data/{ticker}_data.json") for ticker in tickers]
    df = pd.concat(dataframes, axis=1, keys=STOCK_TICKERS)
    return df

# get the max close amount for each company given from the dataset
def get_max_close(data, tickers):
    arr  = [(float(data.xs(f"{ticker}", axis=1)["close"].max()), f"{ticker}") for ticker in tickers]
    return arr


def main():
    bank_data = aggregate_bank_data(STOCK_TICKERS)
    bank_data.columns.names = ['Bank Ticker','Stock Info']
    arr_closes = get_max_close(bank_data, STOCK_TICKERS)
    print(bank_data.head())
    print(bank_data.xs(key='close',axis=1,level='Stock Info').max())

if __name__ == '__main__':
    main()