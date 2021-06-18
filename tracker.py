#!/usr/bin/python

import pandas as pd
import requests
from datetime import datetime

trades = pd.read_csv('trade-history.csv', header=0, index_col=0, parse_dates=False, na_values=-99.99)
#Reading in your trade history and changing dates to YYYY-MM-DD


# Calculates how much of each asset we have left after all the trades.
def crypto_amount(from_sym='', end_date='', start_date=trades.index.min(), account=''):
    df = trades
    if end_date:
        df = trades.loc[start_date:end_date]
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
                  'tsyms': to_sym }
    
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()[to_sym]
    
    return data

#Using the crypto_amount and get_current price functions, it calculates the value of the crypto asset in desired currency
def crypto_value(from_sym='BTC', to_sym='USD', exchange='', account=''):
    url = 'https://min-api.cryptocompare.com/data/price'    
    
    deps = trades.loc[trades['To']==from_sym]
    wdrwls = trades.loc[trades['From']==from_sym]
    
    parameters = {'fsym': from_sym,
                  'tsyms': to_sym }
    if account:
        deps = deps.loc[deps['Account']==account]
        wdrwls = wdrwls.loc[wdrwls['Account']==account]
        
    if exchange:
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()[to_sym]
    amount= (deps['Amount'].sum())-(wdrwls['Paid'].sum())
    return data*amount  

#Builds a dataframe of all the assets in the portfolio, with the amount, market price and value of each.
# Value and market price are in desired currency, in this example I have used GBP.
# Note: Defining the exchange of where each asset is held is not necessary, as the default exchange provides
# a better current price inline with the exchange online, than when defining the exchange.
s=sorted(set(trades['To'].to_list()))
df=pd.DataFrame(list(s))
del df[0]
df['Asset']=pd.DataFrame(list(s))
df['Amount'] = list(map(lambda x: crypto_amount(x), df['Asset']))
df['Market Price']=list(map(lambda x: get_current_price(x, 'GBP'), df['Asset']))
df['GBP Value'] =list(map(lambda x: crypto_value(x, 'GBP'), df['Asset']))
print("Profit/Loss is £", df['GBP Value'].sum(), "as of", datetime.now())
print(df)
