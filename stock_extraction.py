import datetime
import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Dict


def get_intra_stock(ticker: str, days: int) -> (pd.DataFrame, bool):
    """Get intraday data with 5 minutes as interval.
    Return the dataframe and whether if it contains NaN.
    """
    end_time = datetime.datetime.today()
    start_time = end_time - datetime.timedelta(days)
    df = yf.download(ticker, start=start_time, end=end_time, interval="5m", progress=False)
    if df.notnull().all().all():
        return df, True
    return df.dropna(), False


def get_daily_stock(ticker: str, days: int) -> (pd.DataFrame, bool):
    """Get daily data.
    Return the dataframe and whether if it contains NaN.
    """
    end_time = datetime.datetime.today()
    start_time = end_time - datetime.timedelta(days)
    df = yf.download(ticker, start=start_time, end=end_time, interval="1d", progress=False)
    if df.notnull().all().all():
        return df, True
    return df.dropna(), False


def get_monthly_stock(ticker: str, months: int) -> (pd.DataFrame, bool):
    """Get monthly data with 1 day as interval.
    Count 1 month = 30 days.
    Return the dataframe and whether if it contains NaN.
    """
    end_time = datetime.datetime.today()
    start_time = end_time - datetime.timedelta(months * 30)
    df = yf.download(ticker, start=start_time, end=end_time, interval="1d", progress=False)
    if df.notnull().all().all():
        return df, True
    return df.dropna(), False


def get_year_stock(ticker: str, year: int) -> (pd.DataFrame, bool):
    """Get yearly data with 1 day as interval.
    Count 1 year = 365 days.
    Return the dataframe and whether if it contains NaN.
    """
    # note that sometimes yfinance will return weird datetime, so dropna()
    # will not loss information at all
    end_time = datetime.datetime.today()
    start_time = end_time - datetime.timedelta(year * 365)
    df = yf.download(ticker, start=start_time, end=end_time, interval="1mo", progress=False)
    if df.notnull().all().all():
        return df, True
    return df.dropna(), False


def get_tickers_all(ticker_list: List[str], days: int) -> \
        (Dict[str, pd.DataFrame], bool):
    """Get daily data for each valid ticker in ticker_list.
    Return the dataframe and whether if it contains NaN.
    """
    data_dict = {}
    success = []
    for ticker in ticker_list:
        data_dict[ticker], s = get_daily_stock(ticker, days)
        success.append(s)
    return data_dict, np.all(success)


def get_tickers_spec(ticker_list: List[str], spec_type: str, days: int) -> \
        pd.DataFrame:
    """Get daily data for each valid ticker in ticker_list with spec.
    Return the dataframe and whether if it contains NaN.

    Pre-condition: spec_type in ["Open"]
    """
    # Note that if Chinese stocks are involved there will be NaN appear because
    # of different timezones. Hence, I dropna() to remove such irregularity.
    # One has to check the shape of the DataFrame received before usage.
    valid_list = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    if spec_type not in valid_list:
        print("Enter valid Type")
        return pd.DataFrame()
    data_list = []
    success_ticker = []
    for ticker in ticker_list:
        df, s = get_daily_stock(ticker, days)
        if s:
            data_list.append(df[spec_type])
            success_ticker.append(ticker)
    total_df = pd.concat(data_list, axis=1)
    total_df = total_df.dropna()
    total_df.columns = success_ticker
    return total_df


if __name__ == "__main__":
    symbol = "AAPL"
    df1, _ = get_intra_stock(symbol, 5)
    df2, _ = get_daily_stock(symbol, 100)
    df3, _ = get_monthly_stock(symbol, 4)
    df4, _ = get_year_stock(symbol, 2)
    symbols = ["AAPL", "META", "0700.HK"]
    df5, _ = get_tickers_all(symbols, 100)
    df6 = get_tickers_spec(symbols, "Adj Close", 20)
