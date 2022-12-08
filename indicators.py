import asyncio
import aiohttp
import pandas as pd
import json
import statistics
from urllib.request import urlopen


companies_SP = pd.read_csv(
        'https://gist.githubusercontent.com/ZeccaLehn/f6a2613b24c393821f81c0c1d23d4192/raw/fe4638cc5561b9b261225fd8d2a9463a04e77d19/SP500.csv')
tickers_SP = companies_SP["Symbol"]

class DefiningSector:

    """Get info about sector of  stock"""

    def __init__(self, ticker):
        self.ticker = ticker

    @staticmethod
    def arrangement_of_group(ticker):
        if ticker.upper() in companies_SP.values:
            sector = (companies_SP.loc[companies_SP['Symbol'] == ticker.upper()])['Sector'].iloc[0]
            groups = companies_SP.groupby(by='Sector').get_group(sector)["Symbol"]
            print(f"Sector of {ticker.upper()} is {sector}")
            return groups

        else:
            print('Ticker is not in our list.')

class Analysis:

    """Compare stock to companies from sector based on specialized indicators."""

    def __init__(self, ticker):
        self.ticker = ticker


    async def download_site(session, url):
        async with session.get(url) as response:
            return await response.text()


    async def download_all_sites(sites):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(Analysis.download_site(session=session, url=url))
                tasks.append(task)
            return await asyncio.gather(*tasks, return_exceptions=True)


    def generate_urls(ticker_names: list[str]) -> list[str]:
        modules = ['financialData', 'defaultKeyStatistics']
        list1 = []

        for module in modules:

            for w in ticker_names:

                list1.append(f'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{w}?modules={module}')

        return list1



    def post_process_result(result, i):
        modules = ['financialData', 'defaultKeyStatistics']
        list1 = []

        for module in modules:
            try:
                return result['quoteSummary']['result'][0][module][i]['raw']
            except:
                pass


    def processing_stock(ticker, i):
        modules = ['financialData', 'defaultKeyStatistics']

        for module in modules:
            try:
                site = f'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{ticker}?modules={module}'
                json_url = urlopen(site)
                data = json.loads(json_url.read())
                return (data['quoteSummary']['result'][0][module][i]['raw'])
            except:
                pass

    def research(ticker, results):
        profitability = ["ebitdaMargins",
                         "profitMargins",
                         "grossMargins",
                         "operatingMargins",
                         "returnOnAssets",
                         "returnOnEquity"]

        liquidity = ["currentRatio",
                     "quickRatio"]

        debt = ["debtToEquity"]

        market_value =  ["enterpriseToEbitda",
                         "trailingEps",
                         "pegRatio",
                         "forwardPE",
                         "priceToBook",
                         "enterpriseToRevenue"]
        type_of_ratios = [profitability, liquidity, debt, market_value]



        for kind_of_ratio in type_of_ratios:
            our_rating = 0
            for ratio in kind_of_ratio:

                our_stock = Analysis.processing_stock(ticker, ratio)
                x = []
                for result in results:
                    try:
                        x.append(float(Analysis.post_process_result(json.loads(result), ratio)))
                    except:
                        pass
                print(f"Value of {ratio} of your stock is {our_stock:.2f} (median for companies from sector: {statistics.median(x):.2f})")
                decreasing_values_better = ["debtToEquity",
                         "enterpriseToEbitda",
                         "trailingEps",
                         "pegRatio",
                         "forwardPE",
                         "priceToBook",
                         "enterpriseToRevenue"]

                if ratio not in decreasing_values_better and float(our_stock) > float(statistics.median(x)):
                    our_rating += 1
                elif ratio in decreasing_values_better and float(our_stock) < float(statistics.median(x)):
                    our_rating += 1
                else:
                    our_rating -= 1

            if our_rating > 0:
                print(f"Based on above indicators, stock is undervalued, our rating equals: {our_rating}\n")
            elif our_rating < 0:
                print (f"Based on above indicators, stock is overvalued, our rating equals: {our_rating}\n")
            else:
                print ("Indicators do not show difference between stock and other companies from sector.\n")


def main (ticker):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    companies_from_sector = DefiningSector.arrangement_of_group(ticker)
    urls = Analysis.generate_urls(companies_from_sector)
    results = asyncio.run(Analysis.download_all_sites(urls))
    Analysis.research(ticker, results)

if __name__ == "__main__":
    main(input("Type ticker of stock:"))

