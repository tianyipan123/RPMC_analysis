import pandas as pd
import numpy as np
import stock_extraction as se
import kpi
from scipy.optimize import minimize, LinearConstraint

#%% Data cleaning
# SPTSX
sptsx_df = pd.read_excel("tradable_list.xlsx", sheet_name="SPTSX")
header = sptsx_df.iloc[0]
sptsx_df = sptsx_df.iloc[1:]
sptsx_df.columns = header
sptsx_df["RPM Ticker"] = [ticker.split('-')[0] for ticker in sptsx_df["RPM Ticker"]]
sptsx_df = sptsx_df.set_index("RPM Ticker")

non_trackable = [
"ABX",	"ACO.X",	"AD",	"AFN",	"ALA",	"AP.UT",	"APHA",	"ARX",
"ATD",	"ATZ",	"AX.UT",	"BAM.A",	"BBD.B",	"BBU.UT",	"BCB",	"BEI.UT",
"BEP.UT",	"BIP.UT",	"BPY.UT",	"BTE",	"BYD.UT",	"CAR.UT", "CAS", "CCA",
"CCL.B",	"CFP",	"CGX",	"CHE.UT",	"CHP.UT",	"CHR",	"CJT",	"CNR",
"CPX",	"CRR.UT",	"CSH.UT",	"CSU",	"CTC.A",	"CU",	"CUF.UT", "D.UT",
"DGC",	"DIR.UT",	"DRG.UT",	"DSG",	"ECA",	"ECN",	"EFN", "EIF",
"EMA",	"EMP.A",	"EQB",	"EXE",	"FCR",	"FEC",	"FFH",	"FRU",
"FTT",	"GC",	"GEI",	"GIB.A",	"GRT.UT",	"GUD",	"GWO",	"HBC",
"HCG",	"HR.UT",	"HSE",	"IFC",	"IFP",	"IIP.UT",	"IMG",	"INE",
"IPL",	"IVN",	"KL",	"KMP.UT",	"KXS",	"LB",	"LIF",	"LNR",
"LUN",	"MFI",	"MIC",	"MRE",	"MRU",	"MTY",	"MWC",	"NFI",
"NPI",	"NVU.UT",	"NWH.UT",	"OGC",	"ONEX",	"OSB",	"PVG",	"PWF",
"PXT",	"QBR.B",	"RCH",	"RCI.B",	"REI.UT",	"RUS",	"SIA",	"SJR.B",
"SMF",	"SMU.UT",	"SNC",	"SRU.UT",	"TCL.A",	"TECK.B",	"TIH",	"TOU",
"TOY",	"TSGI",	"WCP",	"WDO",	"WFT",	"WJA",	"WN",	"WPK",
"WSP",	"WTE",	"YRI"]
sptsx_df.drop(non_trackable, inplace=True)
sptsx_list = list(sptsx_df.index)

# SPX
spx_df = pd.read_excel("tradable_list.xlsx", sheet_name="SPX")
header = spx_df.iloc[0]
spx_df = spx_df.iloc[1:]
spx_df.columns = header
spx_df["RPM-USTicker"] = [ticker.split('-')[0] for ticker in spx_df["RPM-USTicker"]]
spx_df = spx_df.set_index("RPM-USTicker")
spx_list = list(spx_df.index)

non_trackable = [
"ADS",	"AGN",	"ALXN",	"ANTM",	"BBT",	"BF.B",	"BHGE",	"BLL",
"BRK.B",	"CBS",	"CELG",	"CERN",	"COG",	"CTL",	"CXO",	"DISCA",
"DISCK",	"ETFC",  "FLIR",	"HFC",	"INFO",	"JEC",	"KSU",
"LB",	"MXIM",	"MYL",	"NBL",	"PBCT",	"RTN",	"STI",	"SYMC",
"TIF",	"UTX",	"VAR",	"VIAB",	"WCG",	"WLTW",	"XEC",	"XLNX",
"T" # T in yfinance seems to represent Telus rather than AT&T
]
spx_df.drop(non_trackable, inplace=True)

# ETF
etf_df = pd.read_excel("tradable_list.xlsx", sheet_name="ETFs")
header = etf_df.iloc[0]
etf_df = etf_df.iloc[1:]
etf_df.columns = header
etf_df["RPM Ticker"] = [ticker.split('-')[0] for ticker in etf_df["RPM Ticker"]]
etf_df = etf_df.set_index("RPM Ticker")

non_trackable = ["XCB", "XGB", "XSB", "IEMG.K", "XIC", "XIU"]
etf_df.drop(non_trackable, inplace=True)

#%% Industries Count
sptsx_df.drop(["Bloom.Berg Ticker"], inplace=True, axis=1)
# industries = sptsx_df["GICS Sector\n"].unique()
df1 = sptsx_df.groupby(["GICS Sector\n"]).count()
spx_df.drop(["Bloom.B-USerg Ticker"], inplace=True, axis=1)
df2 = spx_df.groupby("GICS Sector\n").count()

industry_df = df1 + df2
industry_list = list(industry_df.index)

#%% Divide proportion
stock_num = 100
stock_df = pd.concat([sptsx_df, spx_df])
stock_df = stock_df.reset_index()
sharpe_dict = {}
target = {}
for ind in industry_df.index:
    ticker_list = list(stock_df["index"][stock_df["GICS Sector\n"] == ind])
    pos = []
    target_list = []
    for ticker in ticker_list:
        stock_price, _ = se.get_daily_stock(ticker, 200)
        sharpe = 0
        try:
            sharpe = kpi.sharpe(stock_price)
        except Exception:
            print(ticker)
        if sharpe > 0:
            pos.append(sharpe)
            target_list.append(ticker)
    # rank stocks based on Sharpe Ratio
    target_list = np.array(target_list)
    target_list = target_list[np.argsort(pos)[::-1]]
    sharpe_dict[ind] = np.mean(pos)
    target[ind] = target_list
# allocate
sharpe_mean = pd.DataFrame.from_dict(sharpe_dict, orient="index")
allocation = (stock_num * sharpe_mean / np.sum(sharpe_mean.values)).round().astype(int)
if allocation[0]["Telecommunication Services"] > 4:
    available = allocation[0]["Telecommunication Services"] - 4
    r = np.random.randint(0, 11, available)
    for i in r:
        allocation.iloc[i] += 1
    allocation[0]["Telecommunication Services"] = 4
allocation.columns = ["allocation"]
industry_df = pd.concat([industry_df, allocation], axis=1)

#%% Select stocks
money = 1000000
for i in range(11):
    ind = industry_list[i]
    quota = allocation.loc[ind, "allocation"]
    ticker_list = target[ind]
    if quota > len(ticker_list):
        allocation.loc[ind] = quota
    else:
        target[ind] = ticker_list[:quota]
industry_df["money"] = money * industry_df["allocation"] / np.sum(industry_df["allocation"])

#%% Optimize Weight
# stock_price = se.get_tickers_spec(list(stock_df.index), "Adj Close", 200)


def sharpe_portfolio(weight: list) -> float:
    """Weight the stock price in the dataframe and get sharpe ratio.

    Precondition: len(stock_price.columns) == len(weight)
    """
    time_series = stock_prices.dot(weight)
    time_series = pd.Series(time_series)
    assert isinstance(time_series, pd.Series)
    return kpi.sharpe_series(time_series)


def optimize_weight(stock_prices: pd.DataFrame, outlay: float) -> np.array:
    """Produce the optimal amount of stocks given stock price and outlay
     using scipy.optimize.
    """
    ticker_num = len(stock_prices.columns)
    w0 = np.ones(ticker_num) / ticker_num

    cons = (
        {"type": "eq",
         "fun": lambda x: np.sum(x) - 1,
         "jac": lambda x: np.ones(len(x))},
        LinearConstraint(np.identity(len(w0)), lb=0, ub=1)
    )

    res = minimize(lambda w: -1 * sharpe_portfolio(w), w0, constraints=cons)
    # 1 iteration
    res = minimize(lambda w: -1 * sharpe_portfolio(w), res.x, constraints=cons)
    w = res.x
    basket = stock_prices.iloc[-1].dot(w)
    quantity = (outlay / basket * w).round()
    print(sharpe_portfolio(quantity))
    return quantity


holding = []
for i in range(11):
    ind = industry_list[i]
    tickers = target[ind]
    stock_prices = se.get_tickers_spec(tickers, "Adj Close", 100)
    weight = optimize_weight(stock_prices, industry_df["money"][ind])
    holding.append(pd.Series(weight, index=tickers, dtype=int))
holding = pd.concat(holding)
holding = pd.DataFrame(holding[holding != 0])
holding = holding.reset_index()
location = []
for i in range(len(holding.index)):
    ticker = holding.iloc[i]["index"]
    if ticker in sptsx_list:
        location.append("CA")
    elif ticker in spx_list:
        location.append("US")
    else:
        location.append(np.nan)
holding["location"] = location
holding.to_excel("temp.xlsx")