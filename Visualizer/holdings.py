import pandas as pd
from Toolbox import kpi, stock_extraction as se
import matplotlib.pyplot as plt
from datetime import date
pd.options.mode.chained_assignment = None

#%% Fetch holdings
url = "https://docs.google.com/spreadsheets/d/1hS4vtC7ekVef1fdf1KDb7DbemyOiqfgz3OZ62vxrTNM/edit#gid=0"
url = url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url)
header = df.iloc[0]
df = df[1:]
df.columns = header
df["amount"] = df["amount"].astype(int)

#%% Compute portfolio valuation trend
tickers = list(df["ticker"])
stock_prices = se.get_tickers_spec(tickers, "Adj Close", 50)
weight = df[["amount"]]
weight.index = stock_prices.columns
weight["amount"] = weight["amount"].astype(float)
portfolio = stock_prices.dot(weight)

#%% Visualization and Saving Results
portfolio_holding = portfolio[-5:]
cagr = kpi.cagr(portfolio, "amount")[0]
sharpe = kpi.sharpe(portfolio, "amount")
sortino = kpi.sortino(portfolio, "amount")
max_dd = kpi.max_dd(portfolio, "amount")
calmar = kpi.calmar(portfolio, "amount")

kpi_df = pd.DataFrame([cagr, sharpe, sortino, max_dd, calmar],
                      columns=["KPI"], index=["cagr", "Sharpe Ratio",
                                            "Sortino Ratio", "Maximum Drawdown",
                                            "Calmar Ratio"])

print("cagr = " + str(cagr))
print("sharpe ratio = " + str(sharpe))
print("sortino ratio = " + str(sortino))
print("maximum drawdown = " + str(max_dd))
print("calmar ratio = " + str(calmar))

fig = plt.figure()
plt.plot(portfolio)
fig.autofmt_xdate()
prediction_path = "../prediction/"
title = str(date.today())
plt.savefig(prediction_path + title)
plt.show()

writer = pd.ExcelWriter(f"prediction/{title}.xlsx")
df.to_excel(writer, sheet_name="holding")
kpi_df.to_excel(writer, sheet_name="kpi")
writer.save()

