import pandas as pd
import numpy as np
import requests
from datetime import datetime


# Calculates how much of each asset we have left after all the trades.
def crypto_amount(df, from_sym='', end_date='', start_date='', account=''):
    start_date = df.index.min()
    if end_date:
        df = df.loc[start_date:end_date]
    deps = df.loc[df['To'] == from_sym]
    wdrwls = df.loc[df['From'] == from_sym]
    if account:
        deps = deps.loc[deps['Account'] == account]
        wdrwls = wdrwls.loc[wdrwls['Account'] == account]

    amount = (deps['Amount'].sum()) - (wdrwls['Paid'].sum())
    return amount


# Pulls the current price as a float in desired currency, using the cryptocompare api.
# https://tcoil.info/how-to-get-price-data-for-bitcoin-and-cryptocurrencies-with-python-json-restful-api/
def get_current_price(from_sym='BTC', to_sym='USD', exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price'

    parameters = {'fsym': from_sym,
                  'tsyms': to_sym}

    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange

    # response comes as json
    response = requests.get(url, params=parameters)
    data = response.json()[to_sym]

    return data


# Using the crypto_amount and get_current price functions, it calculates the value of the crypto asset in desired currency
def crypto_value(df, from_sym='BTC', to_sym='USD', exchange='', account=''):
    url = 'https://min-api.cryptocompare.com/data/price'

    deps = df.loc[df['To'] == from_sym]
    wdrwls = df.loc[df['From'] == from_sym]

    parameters = {'fsym': from_sym,
                  'tsyms': to_sym}
    if account:
        deps = deps.loc[deps['Account'] == account]
        wdrwls = wdrwls.loc[wdrwls['Account'] == account]

    if exchange:
        parameters['e'] = exchange

    # response comes as json
    response = requests.get(url, params=parameters)
    data = response.json()[to_sym]
    amount = (deps['Amount'].sum()) - (wdrwls['Paid'].sum())
    return data * amount


# Using the cryptocompare API, it pulls the historical data, in particular the closing price
def get_hist_close(from_sym='BTC', to_sym='USDT', timeframe='day', limit=2000, aggregation=1, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/v2/histo'
    baseurl = url + timeframe

    parameters = {'fsym': from_sym,
                  'tsym': to_sym,
                  'limit': limit,
                  'aggregate': aggregation}
    if exchange:
        parameters['e'] = exchange

    # response comes as json
    response = requests.get(baseurl, params=parameters)

    json = response.json()

    if json['Response'] == 'Error':
        return get_hist_close(from_sym, to_sym, timeframe, limit, aggregation)

    data = json['Data']['Data']

    # data from json is in array of dictionaries
    df = pd.DataFrame.from_dict(data)

    # time is stored as an epoch, we need normal dates
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df = pd.DataFrame(df['close'])

    return df


# Using most of the previous functions, it calculates a historical porotfolio for a desired account and exchange in USDT.
def portfolio(th, account='', exchange='', timeframe='day'):
    #global USDT
    assets = sorted(set(th['To'].to_list()))
    start_dt = th.index.min()
    end_dt = datetime.today().strftime('%Y-%m-%d')

    if account:
        th = th.loc[th['Account'] == account]
    tl = pd.date_range(start_dt, end_dt).strftime("%Y-%m-%d")  # Defines the date range

    # Creates a dataframe of the different amounts held over the date range
    holdings = pd.DataFrame(np.zeros((len(tl), len(assets))))
    holdings = holdings.set_index(tl)
    holdings.columns = assets

    for asset in assets:
        holdings[asset] = list(map(lambda x: crypto_amount(th, asset, x), holdings.index))
    if 'USDT' in holdings.columns:
        USDT = holdings['USDT']
        del holdings['USDT']
    assets = sorted(set(th['To'].to_list()))
    if 'USDT' in assets:
        assets.remove('USDT')
    holdings.fillna(0)

    # Creates a dataframe for the historical prices of the assets
    prices_hist = pd.DataFrame(np.zeros((len(tl), len(assets))))
    prices_hist = prices_hist.set_index(tl)
    prices_hist.columns = assets
    for asset in assets:
        prices_hist[asset] = list((get_hist_close(asset, limit=(len(tl) - 1), exchange=exchange, timeframe=timeframe)['close']))
    # Creates a final dataframe, which is the product of the two previous ones.
    portfolio_hist = prices_hist * holdings
    if 'USDT' in assets:
        portfolio_hist['USDT'] = USDT
    invested = portfolio_hist['GBP']
    del portfolio_hist['GBP']
    portfolio_hist = portfolio_hist.reindex(sorted(portfolio_hist.columns), axis=1)
    portfolio_hist['Total'] = portfolio_hist.sum(axis=1)
    portfolio_hist['Invested'] = invested
    portfolio_hist.fillna(0)
    return portfolio_hist


def convert(pt, from_sym='USDT', to_sym='', exchange=''):
    z = get_hist_close(from_sym, to_sym, limit=len(pt) - 1).to_numpy()
    df = pt.multiply(z, axis='rows')
    return df
