import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

companies_SP = pd.read_csv(
        'https://gist.githubusercontent.com/ZeccaLehn/f6a2613b24c393821f81c0c1d23d4192/raw/fe4638cc5561b9b261225fd8d2a9463a04e77d19/SP500.csv')
tickers_SP = companies_SP["Symbol"]

def count_dynamics():
        stock = yf.Ticker('aapl')
        x = stock.get_financials()
        financial_results = ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Ebit", "Net Income"]

        for result in financial_results:
                list_of_averages =[]
                values = []
                for _ in range (3):
                        percent = (int(x.loc[result].iloc[_]) / int(x.loc[result].iloc[_ + 1]) - 1)
                        values.append(percent)
                        dynamic = ((percent * 100))
                        print (f"Growth dynamic of {result} in {str(x.columns[_])[:4]} was {dynamic:.2f}%")
                average = (sum(values)/len(values))
                print(average)
                list_of_averages.append(average)
                return list_of_averages



def predictions():
        for
        count_dynamics()

predictions()


