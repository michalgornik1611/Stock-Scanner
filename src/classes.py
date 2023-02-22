import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import json
from urllib.request import urlopen
import yfinance as yf


class Stock:
    "Transform user's input into object of yfinance and enable to get the main info about company"
    def __init__(self, ticker):
        self.ticker = ticker

    def show_main_information (self):
        self.site = (f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}?modules=assetProfile')
        json_url = urlopen(self.site)
        self.data = json.loads(json_url.read())
        print (self.data['quoteSummary']['result'][0]['assetProfile']['longBusinessSummary'])

    def show_recommendations (self):
        self.site = (f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}?modules=recommendationTrend')
        json_url = urlopen(self.site)
        self.data = json.loads(json_url.read())
        reco = self.data['quoteSummary']['result'][0]['recommendationTrend']['trend'][0]
        print(f'Recommendations of {self.ticker.upper()} published last month: STRONG BUY - {reco["strongBuy"]}, BUY - {reco["buy"]}, HOLD - {reco["hold"]}, SELL - {reco["sell"]}, STRONG SELL - {reco["strongSell"]} ')


class Chart:
    "Enable to show a daily stock chart quotes, feature uses yfinance API"
    def __init__(self, ticker, type, period, interval, mav):
        self.ticker = yf.Ticker(ticker)
        self.type = type
        self.period = period
        self.interval = interval
        self.mav = mav


    def show_chart(self):
            frame = pd.DataFrame(self.ticker.history(period=self.period, interval=self.interval))
            mpf.plot(frame, type=f'{self.type}', volume=True, mav= self.mav, figsize=(15, 5)),


            plt.xlabel('Day')
            plt.ylabel("Price")
            plt.show()



def run_chart (ticker):
    type = str(input ("What type of chart do you want to see? (candle, line, renko, pnf)?"))
    period = str(input ("What period? (d, mo, y, ytd, max)"))
    interval = str(input ("What interval? (1h, 1d, 5d, 1wk, 1mo)"))
    mav = int(input ("Which moving average do you want to see? Write number."))

    user_stock = Chart (ticker, type, period, interval, mav)
    user_stock.show_chart()

def run_info ():
    ticker = input ("Write ticker of stock, that you want to scan:")
    user_stock = Stock (ticker)
    user_stock.show_main_information()
    user_stock.show_recommendations()
