# Cryptocurrency Portfolio Tracker in Python

> #### Disclaimer!
>
> This is not financial advice and shouldn't be taken as such.
> I am not a professional adviser and this is solely for educational purposes
> or for those who already invest in the highly volatile cryptocurrencies
> at their own risk, and wish to utilise to keep track of their trades.
> In addition, the trades in the Trade_history.csv file are not real and were
> generated purely for the educational purpose of this code. For those
> interested in using this, be aware of the limitations highlighted at the end.

## Requirements

- python 3
- pandas
- numpy

## Running 

```console
$ python ./tracker.py
$ python ./history.py
```

## Motivation

For many people who invest in cryptocurrencies and other assets classes, tracking those investments
across multiple accounts can be difficult and time consuming. Therefore this code has been
created to calculate the current
profit/loss based on the  crypto assets one holds, across all accounts. Through very
simple functions, it then calculates the £GBP value of each crypto asset, though
of course this can be changed to different currencies. This all involves calling
the cryptocompare.com API.

## Limitations

- The current price is not 100% correct and does hold a very small
  uncertainty
- The more trades are made, the more uncertainty there will be for the
  calculations for the amount of each asset that is currently owned
- The trades have to be monitored in a similar fashion to the example
  [`trade-history.csv`](trade-history.csv) file provided, with the:`'Date',
  'Account','From','To','Amount','Paid'` columns compulsory for the
  code to function.

I hope you find this useful and informative, yet again I would like to
highlight that this is not financial advice and that the trades in the
[`trade-history.csv`](trade-history.csv) file were purely examples.
I myself used this code to keep track of my investments across two
accounts and it turned out to be very accurate and in line with the values
displayed in the two exchanges. Therefore, for personal use, one only has 
to match the trade history file with their trades. 
