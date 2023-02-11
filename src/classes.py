import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd


class Stock:
    "Transform user's input into object of yfinance and enable to get the main info about company"
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

    def show_main_information (self):
        print (self.ticker.info['longBusinessSummary'])

    def analyst_informations (self):
        print (self.ticker.get_recommendations()[:5])

class Chart(Stock):
    "Enable to show a daily stock chart quotes"

    def __init__(self, ticker, type, period, interval, mav):
        super().__init__(ticker)
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

def run_info (ticker):
    user_stock = Stock(ticker)
    user_stock.show_main_information()
    print ("Latest recommendations:")
    user_stock.analyst_informations()


