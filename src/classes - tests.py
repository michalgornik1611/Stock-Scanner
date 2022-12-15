import yfinance

from classes import Stock
import unittest


class TestStock (unittest.TestCase):
    "Test from class Stock"



    def right_display_of_information(self):
        stock = Stock('aapl')
        assertEqual(stock.show_main_information(),yf.Ticker('aapl').info['longBusinessSummary'])





if __name__ == '__main__':
    unittest.main()

