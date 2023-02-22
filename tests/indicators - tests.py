import asyncio
from typing import Optional
import aiohttp
import pandas as pd
import json
import statistics
from urllib.request import urlopen


companies_SP: pd.DataFrame = pd.read_csv(
        'https://gist.githubusercontent.com/ZeccaLehn/f6a2613b24c393821f81c0c1d23d4192/raw/fe4638cc5561b9b261225fd8d2a9463a04e77d19/SP500.csv')
tickers_SP: pd.Series = companies_SP["Symbol"]

class SectorDataBuilder:
    """Get info about sector of  stock"""

    @staticmethod
    def _get_ticker_sector(ticker: str) -> Optional[str]:
        if ticker.upper() in companies_SP.values:
            sector: str = (companies_SP.loc[companies_SP['Symbol'] == ticker.upper()])['Sector'].iloc[0]
            print(f"Sector of {ticker.upper()} is {sector}")
            return sector
        else:
            print('Ticker is not in our list.')

    @staticmethod
    def _build_series_by_sector(sector: str) -> Optional[pd.Series]:
        try:
            groups: pd.Series = companies_SP.groupby(by='Sector').get_group(sector)["Symbol"]
            return groups
        except KeyError:
            print("No such sector in our list")
            return

    def build(self, ticker: str) -> Optional[pd.Series]:
        sector: str = self._get_ticker_sector(ticker)
        if sector:
            return self._build_series_by_sector(sector)
        else:
            return None

    @staticmethod
    def arrangement_of_group(ticker):
        if ticker.upper() in companies_SP.values:
            sector = (companies_SP.loc[companies_SP['Symbol'] == ticker.upper()])['Sector'].iloc[0]
            groups = companies_SP.groupby(by='Sector').get_group(sector)["Symbol"]
            print(f"Sector of {ticker.upper()} is {sector}")
            return groups

        else:
            print('Ticker is not in our list.')



class AsyncDataDownloader:
    """Compare stock to companies from sector based on specialized indicators."""

    def __init__(self, ticker_names: list[str]):
        self.ticker_names = ticker_names

    @staticmethod
    async def download_site(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def download_all_sites(self, sites):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(self.download_site(session=session, url=url))
                tasks.append(task)
            return await asyncio.gather(*tasks, return_exceptions=True)

    def _generate_urls(self) -> list[str]:
        modules = ['financialData', 'defaultKeyStatistics']
        list_ = []
        for module in modules:
            for w in self.ticker_names:
                list_.append(f'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{w}?modules={module}')
        return list_

    def download(self):
        sites: list[str] = self._generate_urls()
        return asyncio.run(self.download_all_sites(sites))


class ReportBuilder:
    """Compare stock to companies from sector based on specialized indicators."""
    def __init__(self):
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
        self.types_of_ratios = [profitability, liquidity, debt, market_value]
        self.decreasing_values_better = \
            ["debtToEquity",
             "enterpriseToEbitda",
             "trailingEps",
             "pegRatio",
             "forwardPE",
             "priceToBook",
             "enterpriseToRevenue"]

    @staticmethod
    def _post_process_result(result, ratio):
        modules = ['financialData', 'defaultKeyStatistics']
        for module in modules:
            try:
                return result['quoteSummary']['result'][0][module][ratio]['raw']
            except KeyError:
                continue

    @staticmethod
    def _processing_stock(ticker, ratio):
        modules = ['financialData', 'defaultKeyStatistics']
        for module in modules:
            try:
                site = f'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{ticker}?modules={module}'
                json_url = urlopen(site)
                data = json.loads(json_url.read())
                return data['quoteSummary']['result'][0][module][ratio]['raw']
            except KeyError:
                continue

    def build(self, ticker: str, results):
        for type_of_ratios in self.types_of_ratios:
            our_rating = 0
            for ratio in type_of_ratios:
                our_stock = self._processing_stock(ticker, ratio)
                x = []
                for result in results:
                    try:
                        x.append(float(self._post_process_result(json.loads(result), ratio)))
                    except:
                        pass
                print(f"Value of {ratio} of your stock is {our_stock:.2f} (median for companies from sector: {statistics.median(x):.2f})")

                if ratio not in self.decreasing_values_better and float(our_stock) > float(statistics.median(x)):
                    our_rating += 1
                elif ratio in self.decreasing_values_better and float(our_stock) < float(statistics.median(x)):
                    our_rating += 1
                else:
                    our_rating -= 1

            if our_rating > 0:
                print(f"Based on above indicators, stock is undervalued, our rating equals: {our_rating}\n")
            elif our_rating < 0:
                print (f"Based on above indicators, stock is overvalued, our rating equals: {our_rating}\n")
            else:
                print ("Indicators do not show difference between stock and other companies from sector.\n")





def run (ticker: str):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    companies_from_sector = SectorDataBuilder().build(ticker)
    if companies_from_sector is None:
        print("No companies from sector found.")
        return
    else:
        data = AsyncDataDownloader(companies_from_sector.tolist()).download()
        report_builder = ReportBuilder()
        report_builder.build(ticker, data)




def test_get_ticker_sector():
    assert SectorDataBuilder()._get_ticker_sector('Non existing ticker') is None
    assert isinstance(SectorDataBuilder()._get_ticker_sector('AAPL'), str)


def test_build_series_by_sector():
    assert SectorDataBuilder()._build_series_by_sector('Non existing sector') is None
    assert isinstance(SectorDataBuilder()._build_series_by_sector('Information Technology'), pd.Series)


def test_build():
    assert SectorDataBuilder().build('Non existing ticker') is None
    assert isinstance(SectorDataBuilder().build('AAPL'), pd.Series)

def test_arrangement_of_group():
    assert SectorDataBuilder().arrangement_of_group('Non existing ticker') is None
    assert isinstance(SectorDataBuilder().arrangement_of_group('AAPL'), pd.Series)

def test():
    assert AsyncDataDownloader.download_site('Non existing list') is None
    assert isinstance(AsyncDataDownloader.__init__(), list)



if __name__ == '__main__':
    test_get_ticker_sector()
    test_build_series_by_sector()
    test_build()
    test_arrangement_of_group()
