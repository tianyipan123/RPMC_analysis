import pandas as pd
from Toolbox import kpi, stock_extraction as se
import matplotlib.pyplot as plt
from datetime import date
pd.options.mode.chained_assignment = None


class Visualizer:

    url: str
    holding: pd.DataFrame
    kpi_df: pd.DataFrame
    portfolio: pd.DataFrame

    def __init__(self, url: str):
        self.url = url
        self.holding = pd.DataFrame()
        self.kpi_df = pd.DataFrame()
        self.portfolio = pd.DataFrame()

    def fetch_holding(self) -> None:
        df = pd.read_csv(self.url)
        header = df.iloc[0]
        df = df[1:]
        df.columns = header
        df["amount"] = df["amount"].astype(int)

    def summarize_kpi(self) -> None:
        tickers = list(self.holding["ticker"])
        stock_prices = se.get_tickers_spec(tickers, "Adj Close", 50)
        weight = self.holding[["amount"]]
        weight.index = stock_prices.columns
        weight["amount"] = weight["amount"].astype(float)
        # Calculate KPI
        portfolio = stock_prices.dot(weight)
        cagr = kpi.cagr(portfolio, "amount")[0]
        sharpe = kpi.sharpe(portfolio, "amount")
        sortino = kpi.sortino(portfolio, "amount")
        max_dd = kpi.max_dd(portfolio, "amount")
        calmar = kpi.calmar(portfolio, "amount")

        kpi_df = pd.DataFrame([cagr, sharpe, sortino, max_dd, calmar],
                              columns=["KPI"], index=["cagr", "Sharpe Ratio",
                                                      "Sortino Ratio",
                                                      "Maximum Drawdown",
                                                      "Calmar Ratio"])
        print("cagr = " + str(cagr))
        print("sharpe ratio = " + str(sharpe))
        print("sortino ratio = " + str(sortino))
        print("maximum drawdown = " + str(max_dd))
        print("calmar ratio = " + str(calmar))

    def visualize(self) -> None:
        fig = plt.figure()
        plt.plot(self.portfolio)
        fig.autofmt_xdate()
        prediction_path = "../prediction/"
        title = str(date.today())
        plt.savefig(prediction_path + title)
        plt.show()

    def document(self) -> None:
        title = str(date.today())
        writer = pd.ExcelWriter(f"prediction/{title}.xlsx")
        self.holding.to_excel(writer, sheet_name="holding")
        self.kpi_df.to_excel(writer, sheet_name="kpi")
        writer.save()
