import pandas as pd
import stock_extraction as se
import numpy as np


def cagr(DF: pd.DataFrame, spec: str = "Adj Close") -> (float, pd.DataFrame):
    """Compounded Annual Growth Return.
    """
    # Note: does not reflect risk
    df = DF.copy()
    df["return"] = df[spec].pct_change()
    n = len(df) / 252 # change the denominator if the time interval is not daily
    CAGR = (df[spec][-1] / df[spec][0]) ** (1/n) - 1
    return CAGR, df[["return"]]


def cagr_series(ds: pd.Series) -> float:
    n = len(ds) / 252
    return (ds.iloc[-1] / ds.iloc[0]) ** (1 / n) - 1


def volatility(DF: pd.DataFrame, spec: str = "Adj Close") -> float:
    """Measured by standard deviation.
    """
    # Note1: this value is annualized
    # Note2: assume normal distribution, which is not true
    # Note3: does not capture tail risk
    df = DF.copy()
    df["return"] = df[spec].pct_change()
    vol = df["return"].std() * np.sqrt(252)
    return vol


def volatility_series(ds: pd.Series) -> float:
    stock_return = ds.pct_change()
    vol = stock_return.std() * np.sqrt(252)
    return vol


def sharpe(DF: pd.DataFrame, spec: str = "Adj Close", rf: float = 0.04) -> float:
    """Sharpe Ratio.
    """
    # Note: >1: good, >2: very good, >3: excellent
    df = DF.copy()
    return (cagr(df, spec)[0] - rf) / volatility(df)


def sharpe_series(ds: pd.Series, rf: float = 0.04) -> float:
    return (cagr_series(ds) - rf) / volatility_series(ds)


def sortino(DF: pd.DataFrame, spec: str = "Adj Close", rf: float = 0.04) -> float:
    """Sortino Ratio.
    """
    # Note1: consider only harmful volatility
    # Note2: suitable for more sensitive investor
    df = DF.copy()
    df["return"] = df[spec].pct_change()
    neg_return = np.where(df["return"] > 0, 0, df["return"])
    neg_vol = pd.Series(neg_return[neg_return != 0]).std()
    return (cagr(df, spec)[0] - rf) / neg_vol


def sortino_series(ds: pd.Series, rf: float = 0.04) -> float:
    stock_return = ds.pct_change()
    neg_return = np.where(stock_return > 0, 0, stock_return)
    neg_vol = pd.Series(neg_return[neg_return != 0]).std()
    return neg_vol


def max_dd(DF: pd.DataFrame, spec: str = "Adj Close") -> float:
    """Maximum Drawdown.
    the largest percent drop in asset price.
    """
    # Note1: the peak has to come first and then the trough
    # Note2: good indicator for conservative investor
    df = DF.copy()
    df["cum_max"] = df[spec].cummax()
    return (1 - df[spec] / df["cum_max"]).max()


def max_dd_series(ds: pd.Series) -> float:
    cum_max = ds.cummax()
    return (1 - ds / cum_max).max()


def calmar(DF: pd.DataFrame, spec: str = "Adj Close") -> float:
    """Calmar Ratio. Measure of risk-adjusted return.
    """
    return cagr(DF, spec)[0] / max_dd(DF, spec)


def calmar_series(ds: pd.Series) -> float:
    return cagr_series(ds) / max_dd_series(ds)


if __name__ == "__main__":
    df, _ = se.get_daily_stock("AAPL", 200)
    print(cagr(df, "Adj Close")[0])
    print(volatility(df, "Adj Close"))
    print(sharpe(df, "Adj Close"))
    print(sortino(df, "Adj Close"))
    print(max_dd(df, "Adj Close"))
    print(calmar(df, "Adj Close"))
