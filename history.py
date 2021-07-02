#!/usr/bin/python

import crypto_portfolio_kit as ck
import pandas as pd

trades = pd.read_csv('trade-history.csv', header=0, index_col=0, na_values=-99.99)

# %%time
accounts = sorted(set(trades['Account'].to_list()))

d = {}
for name in accounts:
        d[name] = ck.portfolio(trades, account=name, exchange=name)

for name in accounts:
    d[name] = d[name].fillna(0)

fp = sum(d.values())
#Converts the portfolio history to desired currency, however it can be left in USDT if desired.
fp = ck.convert(fp, 'USDT', 'GBP')

print(fp)
fp.to_csv("portfolio-history.csv")


