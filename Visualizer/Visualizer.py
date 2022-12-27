import pandas as pd
from Toolbox import kpi
from Toolbox import stock_extraction as se
import matplotlib.pyplot as plt
from datetime import date
pd.options.mode.chained_assignment = None


class Visualizer:
    """Visualize result for current holding.

    === Attributes
    url: Google Spreadsheet link for current holding amount
    holding: current holding
    kpi_df: store KPI's for holding
    portfolio: balance with current holding in time series
    """
    # Attribute Types
    url: str
    holding: pd.DataFrame
    kpi_df: pd.DataFrame
    portfolio: pd.DataFrame

    def __init__(self, url: str) -> None:
        """Initializer to Visualizer.
        """
        self.url = url
        self.holding = pd.DataFrame()
        self.kpi_df = pd.DataFrame()
        self.portfolio = pd.DataFrame()

    def __str__(self) -> str:
        """String representation of Visualizer.
        """
        return "Visualizer is working"

    def fetch_holding(self) -> None:
        """Fetch the holding from self.url and store results in holding.
        """
        holding = pd.read_csv(self.url)
        header = holding.iloc[0]
        holding = holding[1:]
        holding.columns = header
        holding["amount"] = holding["amount"].astype(int)
        self.holding = holding

    def summarize_kpi(self) -> None:
        """Calculate KPI and store in kpi_df.
        """
        # setup
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
        # print result to console
        print("cagr = " + str(cagr))
        print("sharpe ratio = " + str(sharpe))
        print("sortino ratio = " + str(sortino))
        print("maximum drawdown = " + str(max_dd))
        print("calmar ratio = " + str(calmar))
        # save results
        self.kpi_df = pd.DataFrame([cagr, sharpe, sortino, max_dd, calmar],
                                   columns=["KPI"],
                                   index=["cagr", "Sharpe Ratio",
                                          "Sortino Ratio",
                                          "Maximum Drawdown",
                                          "Calmar Ratio"])
        self.portfolio = portfolio

    def visualize(self) -> None:
        """Plot the portfolio time series and save it in /prediction/.
        """
        # plot
        fig = plt.figure()
        plt.plot(self.portfolio)
        fig.autofmt_xdate()
        # save plot
        prediction_path = "/prediction/"
        title = str(date.today())
        plt.savefig(prediction_path + title)
        plt.show()

    def document(self) -> None:
        """Document holding and KPI in /prediction/.
        """
        title = str(date.today())
        writer = pd.ExcelWriter(f"prediction/{title}.xlsx")
        self.holding.to_excel(writer, sheet_name="holding")
        self.kpi_df.to_excel(writer, sheet_name="kpi")
        writer.save()
