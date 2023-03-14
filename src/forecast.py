
import urllib
import urllib.parse
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt

class Forecast:
        """Feature help to get average dynamics of growth of different positions in Financial Statements.
        It also can predict values of finance positions in 2023 based on counted dynamics."""
        def __init__(self, ticker):
                self.ticker = ticker


        def count_dynamics(self):

                response = urllib.request.urlopen(
                        f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}?modules=incomeStatementHistory')
                content = response.read()
                data = json.loads(content.decode('utf8'))
                financial_results = ["totalRevenue", "costOfRevenue", "grossProfit", "ebit", "netIncome"]
                years = [0,1,2,3]

                for _ in financial_results:
                        results = []
                        for year in years:
                                results.append(data['quoteSummary']['result'][0]['incomeStatementHistory']['incomeStatementHistory'][year][_]['raw'])
                        x = int (results[0])
                        y = int (results[1])
                        z = ((x / y) - 1) * 100
                        print(f'Last year dynamics of {_} equals {round (z,2)}%')

        def predictions(self):
                response = urllib.request.urlopen(
                        f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}?modules=incomeStatementHistory')
                content = response.read()
                data = json.loads(content.decode('utf8'))
                financial_results = ["totalRevenue", "costOfRevenue", "grossProfit", "ebit", "netIncome"]
                years = [0, 1, 2, 3]

                for _ in financial_results:
                        results = []
                        for year in years:
                                results.append(data['quoteSummary']['result'][0]['incomeStatementHistory']['incomeStatementHistory'][year][_]['raw'])
                                global results_reverse
                                results_reverse = results[::-1]
                        yearss = []
                        valuess =[]


                        for i in enumerate(results_reverse, start = 2019):
                                yearss.append (i[0])
                                valuess.append(i[1])
                        dyn = valuess[-1] * (1 + ((valuess[-1]/valuess[-2] - 1)))
                        yearss.append (2023)
                        valuess.append (dyn)


                        x_axis = yearss
                        y_axis = valuess
                        plt.bar(x_axis, y_axis)
                        plt.title(f"{_} of {self.ticker.upper()}")
                        plt.xlabel ("Year")
                        plt.ylabel ("USD")
                        plt.show()

def run_forecast(ticker):
        user_stock = Forecast (ticker)
        user_stock.count_dynamics()
        user_stock.predictions()
