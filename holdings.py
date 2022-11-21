import pandas as pd
import stock_extraction as se
import matplotlib.pyplot as plt
import kpi

#%% Fetch holdings
url = "https://docs.google.com/spreadsheets/d/1hS4vtC7ekVef1fdf1KDb7DbemyOiqfgz3OZ62vxrTNM/edit#gid=0"
url = url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url)
header = df.iloc[0]
df = df[1:]
df.columns = header

#%% Compute portfolio valuation trend
tickers = list(df["ticker"])
stock_prices = se.get_tickers_spec(tickers, "Adj Close", 99)
weight = df[["amount"]]
weight.index = stock_prices.columns
weight["amount"] = weight["amount"].astype(float)
portfolio = stock_prices.dot(weight)

#%% Visualization
cagr = kpi.cagr(portfolio, "amount")[0]
sharpe = kpi.sharpe(portfolio, "amount")
sortino = kpi.sortino(portfolio, "amount")
max_dd = kpi.max_dd(portfolio, "amount")
calmar = kpi.calmar(portfolio, "amount")

print("cagr = " + str(cagr))
print("sharpe ratio = " + str(sharpe))
print("sortino ratio = " + str(sortino))
print("maximum drawdown = " + str(max_dd))
print("calmar ratio = " + str(calmar))

plt.figure()
plt.plot(portfolio)
plt.show()
