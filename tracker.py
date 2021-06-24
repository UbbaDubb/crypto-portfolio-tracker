#!/usr/bin/python

import pandas as pd
from datetime import datetime
import crypto_portfolio_kit as ek

#Reading in your trade history and changing dates to YYYY-MM-DD
trades = pd.read_csv('trade-history.csv', header=0, index_col=0, parse_dates=False, na_values=-99.99)


#Builds a dataframe of all the assets in the portfolio, with the amount, market price and value of each.
# Value and market price are in desired currency, in this example I have used GBP.
# Note: Defining the exchange of where each asset is held is not necessary, as the default exchange provides
# a better current price inline with the exchange online, than when defining the exchange.
curr='GBP'
s=sorted(set(trades['To'].to_list()))
df=pd.DataFrame(list(s))
del df[0]
df['Asset']=pd.DataFrame(list(s))
df['Amount'] = list(map(lambda x: ek.crypto_amount(trades, x), df['Asset']))
df['Market Price']=list(map(lambda x: ek.get_current_price(x, curr), df['Asset']))
df['Value'] =list(map(lambda x: ek.crypto_value(trades, x, curr), df['Asset']))
print("Profit/Loss is ", df[ 'Value'].sum(), curr ,"as of", datetime.now())
print(df)
