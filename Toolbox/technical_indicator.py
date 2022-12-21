import pandas as pd
import stock_extraction as se
import numpy as np
import matplotlib.pyplot as plt


def macd(DF: pd.DataFrame, spec: str = "Adj Close", a: int = 12, b: int = 26,
         c: int = 9) -> pd.DataFrame:
    """Momentum indicator.
    """
    # Note1: many false positives during sideways market
    # Note2: this indicator is lagging, so should not be used for prediction
    # Note3: macd cut from above: bearish, cut from below: bullish.
    df = DF.copy()
    df["ma_fast"] = df[spec].ewm(span=a, min_periods=a).mean()
    df["ma_slow"] = df[spec].ewm(span=b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
    return df.loc[:, ["macd", "signal"]]


def atr(DF: pd.DataFrame, n: int = 14) -> pd.DataFrame:
    """Average True Range reflects the volatility of the asset price.
    """
    # Note1: H-high, L-low, PC-previous close.
    # Note2: Has to pass a complete data frame.
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = df["High"] - df["Adj Close"].shift(1)
    df["H-PC"] = df["H-PC"].abs()
    df["L-PC"] = df["Low"] - df["Adj Close"].shift(1)
    df["L-PC"] = df["L-PC"].abs()
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(span=n, min_periods=n).mean()
    # com instead of span is closer to Yahoo Finance
    return df[["ATR"]]


def bollinger_bands(DF: pd.DataFrame, spec: str = "Adj Close", n: int = 14)\
        -> pd.DataFrame:
    """volatility indicator.
    """
    # Note: if price close to upper band, over-buy occurs, vice versa.
    df = DF.copy()
    df["MB"] = df[spec].rolling(n).mean()
    df["UB"] = df["MB"] + 2 * df[spec].rolling(n).std(ddof=0)
    df["LB"] = df["MB"] - 2 * df[spec].rolling(n).std(ddof=0)
    df["BB_Width"] = df["UB"] - df["LB"]
    return df[["MB", "UB", "LB", "BB_Width"]]


def rsi(DF: pd.DataFrame, spec: str = "Adj Close", n: int = 14) -> pd.DataFrame:
    """Momentum indicator.
    """
    # Note: rsi: 0 ~ 100: > 70: overbought, <30: oversold
    df = DF.copy()
    df["change"] = df[spec] - df[spec].shift(1)
    df["gain"] = np.where(df["change"] >= 0, df["change"], 0)
    df["loss"] = np.where(df["change"] < 0, -1 * df["change"], 0)
    df["avg_gain"] = df["gain"].ewm(alpha=1 / n, min_periods=n).mean()
    df["avg_loss"] = df["loss"].ewm(alpha=1 / n, min_periods=n).mean()
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - 100 / (1 + df["rs"])
    return df[["rsi"]]


def adx(DF: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Trend strength indicator.
    """
    # Note1: no implication in direction
    # Note2: 0-25: absent or weak trend, 25-50: strong trend,
    # 50-75: very strong trend, 75-100: extremely strong trend
    df = DF.copy()
    df["ATR"] = atr(df, n)
    df["upmove"] = df["High"] - df["High"].shift(1)
    df["downmove"] = df["Low"] - df["Low"].shift(1)
    df["+dm"] = np.where((df["upmove"] > df["downmove"]) & (df["upmove"] > 0), df["upmove"], 0)
    df["-dm"] = np.where((df["downmove"] > df["upmove"]) & (df["downmove"] > 0), df["downmove"], 0)
    df["+di"] = 100 * (df["+dm"] / df["ATR"]).ewm(span=n, min_periods=n).mean()
    # com = n will close to Yahoo Finance
    df["-di"] = 100 * (df["-dm"] / df["ATR"]).ewm(span=n, min_periods=n).mean()
    df["ADX"] = 100 * abs((df["+di"] - df["-di"]) / (df["+di"] + df["-di"])).ewm(span=n, min_periods=n).mean()
    return df[["ADX"]]


if __name__ == "__main__":
    df, _ = se.get_daily_stock("AAPL", 200)
    sig_macd = macd(df, "Adj Close")
    sig_atr = atr(df)
    sig_bb = bollinger_bands(df, "Adj Close")
    sig_rsi = rsi(df, "Adj Close")
    sig_adx = adx(df)
    df_list = [df["Adj Close"], sig_macd, sig_atr, sig_bb, sig_rsi, sig_adx]
    df_title = ["price", "macd", "atr", "bollinger bands", "rsi", "adx"]
    plt.figure(figsize=(10, 20))
    for i in range(1, 7):
        plt.subplot(6, 1, i)
        plt.plot(df_list[i - 1])
        plt.title(df_title[i - 1], fontsize=30)
        plt.xticks([])
    plt.show()
