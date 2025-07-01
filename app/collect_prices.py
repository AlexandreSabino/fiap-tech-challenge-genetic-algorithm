from pandas import DataFrame
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

YEARS = 5

def collect_prices() -> DataFrame:
    end = date.today()
    start = end - relativedelta(years=YEARS)

    prices_usa = _load_prices_usa(start, end)
    prices_br_usd = _load_prices_br_in_usd(start, end)

    return pd.concat([prices_usa, prices_br_usd], axis=1, join='inner')

def _load_prices_br_in_usd(start, end) -> DataFrame:
    tickers_br = ['BOVA11.SA', 'SMAL11.SA', 'XFIX11.SA', 'IMAB11.SA']
    prices_br = yf.download(tickers_br, start=start, end=end, interval='1mo')['Close']
    prices_br = prices_br.dropna()
    usd_brl = yf.download("USDBRL=X", start=start, end=end, interval='1mo')['Close']
    prices_br_align, usd_brl_align = prices_br.align(usd_brl, join='inner', axis=0)
    prices_br_usd = prices_br_align.div(usd_brl_align['USDBRL=X'], axis=0)
    return prices_br_usd

def _load_prices_usa(start, end) -> DataFrame:
    tickers_usa = ['IVV', 'IAU', 'TLT', 'BIL', 'BTC-USD']
    prices_usa = yf.download(tickers_usa, start=start, end=end, interval='1mo')['Close']
    return prices_usa