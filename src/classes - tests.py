import yfinance

from classes import Stock
import unittest


class TestStock (unittest.TestCase):
    """Tests for class Stock"""

    def right_display_of_information(self):
        stock = Stock('aapl')
        expression = yf.Ticker('aapl').info['longBusinessSummary']
        self.assertEqual(stock.show_main_information(),expression)

    def right_display_of_recommendation(self):
        stock = Stock('aapl')
        expression = yf.Ticker('aapl').get_recommendations()[:5]
        self.assertEqual(stock.analyst_informations(),expression)


class TestChart(unittest.TestCase):
    """Tests for class Chart"""

    def right_display_of_chart(self, type, period, interval, mav):
        self.ticker = 'aapl'
        self.type = 'line'
        self.period = '1y'
        self.interval = '1d'
        self.mav = 3
        chart = Chart(self.ticker,self.type, self.period, self.interval, self.mav)

        self.assertEqual(chart, )


if __name__ == '__main__':
    unittest.main()

