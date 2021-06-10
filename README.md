<h1>Cryptocurrency Portfolio Tracker in Python</h1>

Disclaimer!
<br>This is not financial advice and shouldn't be taken as such. I am not a professional adviser and this is solely for educational purposes or for those who already invest in the highly volatile cryptocurrencies at their own risk, and wish to utilise to keep track of their trades. In addition, the trades in the Trade_history.csv file are not real and were generated purely for the educational purpose of this code. For those interested in using this, be aware of the limitations highlighted at the end.

After investing some of my money in cryptocurrencies before properly researching crypto exchanges, I came upon the problem that I did not wish to cash in on the assets I was already holding, in order to put the money in a better suited crypto exchange for me. However, if I were to keep the cryptocurrency assets in the old exchanges and keep investing in the new and more tailed for me exchanges, I would then have to flip through different apps to calculate the performance of my overall crypto portfolio.

Thus I decided to write this very short code, which calculates my current profit/loss based on the assets I hold, across all accounts. The code is very short and only requires a csv spreadsheet file, which it reads to calculate the amount of each asset still owned up-to-date. Through very simple functions, it then calculates the £GBP value of each asset, though of course this can be changed to different currencies. This involves using the cryptocompare library to call the cryptocompare.com API.

Limitations
- The current price is not 100% correct and does hold a very small uncertainty
- The more trades are made, the more uncertainty there will be as the calculations for the amount of each asset that is currently owned
- The trades have to be monitored in a similar fashion to the example Trade_history.csv file provided, with the: 'Account','From','To','Amount','Paid' columns compulsory for the code to function.

I hope you find this useful and informative, yet again I would like to highlight that this is not financial advice and that the trades in the Trade_history.csv file were purely examples. I myself used this code to keep track of my investments across two accounts and it turned out to be very accurate compared to the values displayed in the two exchanges.

