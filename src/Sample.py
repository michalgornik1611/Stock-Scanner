import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from src.classes import Stock

class Predictions(Stock):
        def __init__(self, ticker):
                super().__init__(ticker)
                self.ticker = ticker
        def count_dynamics(self):

                x = self.ticker.get_financials()
                financial_results = ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Ebit", "Net Income"]
                list_of_averages = []
                for result in financial_results:

                        values = []
                        for _ in range (3):
                                percent = (int(x.loc[result].iloc[_]) / int(x.loc[result].iloc[_ + 1]) - 1)
                                values.append(percent)
                                dynamic = ((percent * 100))
                                # print (f"Growth dynamic of {result} in {str(x.columns[_])[:4]} was {dynamic:.2f}%")
                        average = (sum(values)/len(values))
                        list_of_averages.append(average)

                return list_of_averages



        def predictions(self):
                x = self.ticker.get_financials()
                financial_results = ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Ebit", "Net Income"]
                y = Predictions.count_dynamics(self.ticker)
                w = list(zip(financial_results, y))

                for result, dynamic in w:
                        var1 = x.loc[result]
                        var2 = var1.values.tolist()[::-1]
                        var3 = var2[-1] * (1 + dynamic)
                        var2.append(round(var3,1))
                        print (var2)
                        years = []
                        values = []
                        for _ in enumerate(var2, start = 2019):
                                years.append(_[0])
                                values.append(_[1])

                        x_axis = years
                        y_axis = values
                        plt.bar(x_axis, y_axis)
                        plt.title(f"{result}")
                        plt.xlabel ("Year")
                        plt.ylabel ("USD")
                        plt.show()





x = Predictions('xrx')
x.predictions()


