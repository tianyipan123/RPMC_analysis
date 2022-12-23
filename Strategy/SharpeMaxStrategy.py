from Strategy import Strategy
from DataProcessor.DataLoader import DataLoader
import pandas as pd
import numpy as np
from Toolbox import stock_extraction as se
from Toolbox import kpi
from scipy.optimize import minimize, NonlinearConstraint, Bounds
from typing import Dict, List

import gc
from tqdm import tqdm


def _sharpe_portfolio(stock_prices: pd.DataFrame, weight: list) -> float:
    """Weight the stock price in the dataframe and get sharpe ratio.

    Precondition: len(stock_price.columns) == len(weight)
    """
    time_series = stock_prices.dot(weight)
    time_series = pd.Series(time_series)
    assert isinstance(time_series, pd.Series)
    return kpi.sharpe_series(time_series)


def _optimize_weight(stock_prices: pd.DataFrame, outlay: float) -> np.array:
    """Produce the optimal amount of stocks given stock price and outlay
     using scipy.optimize.
    """
    ticker_num = len(stock_prices.columns)
    w0 = np.ones(ticker_num) / ticker_num

    b = Bounds(lb=0, ub=1)
    cons = NonlinearConstraint(fun=(lambda x: np.sum(x)), lb=1, ub=1)

    res = minimize(lambda w: -1 * _sharpe_portfolio(stock_prices, w), w0,
                   bounds=b, constraints=cons)
    # 1 additional iteration
    res = minimize(lambda w: -1 * _sharpe_portfolio(stock_prices, w), res.x,
                   bounds=b, constraints=cons)
    w = res.x
    basket = stock_prices.iloc[-1].dot(w)
    quantity = (outlay / basket * w).round()
    print(_sharpe_portfolio(stock_prices, quantity))
    return quantity


class SharpeMaxStrategy(Strategy):

    sharpe_mean: pd.DataFrame
    target: Dict[str, List[str]]
    industry_list: List[str]
    industry_allocation: pd.DataFrame
    stock_num: int

    def __init__(self, dc: DataLoader, money: int, stock_num: int) -> None:
        Strategy.__init__(self, dc, money)
        self.sharpe_mean = pd.DataFrame()
        self.target = {}
        self.industry_list = list(dc.industry_df.index)
        self.industry_allocation = pd.DataFrame()
        self.stock_num = stock_num

    def __str__(self) -> str:
        return "Strategy: Maximize Sharpe Ratio"

    def develop_strategy(self) -> None:
        self._select_possible_stocks()
        self._decide_industry_allocation()
        self._impose_quota()
        self._decide_stock_quantity()

    def _select_possible_stocks(self) -> None:
        stock_df = pd.concat([self.dataloader.sptsx_df, self.dataloader.spx_df])
        stock_df = stock_df.reset_index()
        sharpe_dict = {}
        target = {}

        for ind in tqdm(self.industry_list):
            tickers_list = list(
                stock_df["index"][stock_df["GICS Sector\n"] == ind])
            pos = []
            target_list = []
            for ticker in tickers_list:
                stock_price, _ = se.get_daily_stock(ticker, 100)
                sharpe = kpi.sharpe(stock_price)
                if kpi.volatility(stock_price) == 0:
                    print(ticker)
                if sharpe > 0:
                    pos.append(sharpe)
                    target_list.append(ticker)
            # rank stocks based on Sharpe Ratio
            target_list = np.array(target_list)
            target_list = target_list[np.argsort(pos)[::-1]]
            mean = np.mean(pos)
            sharpe_dict[ind] = mean
            target[ind] = target_list
        gc.collect()  # remove stock_price garbage

        # save results
        sharpe_mean = pd.DataFrame.from_dict(sharpe_dict, orient="index")
        self.sharpe_mean = sharpe_mean
        self.target = target

    def _decide_industry_allocation(self) -> None:
        allocation = (self.stock_num * self.sharpe_mean / np.sum(
            self.sharpe_mean.values)).round().astype(int)
        if allocation[0]["Telecommunication Services"] > 4:
            available = allocation[0]["Telecommunication Services"] - 4
            r = np.random.randint(0, 11, available)
            for i in r:
                allocation.iloc[i] += 1
            allocation[0]["Telecommunication Services"] = 4
        allocation.columns = ["allocation"]
        self.dataloader.industry_df = pd.concat(
            [self.dataloader.industry_df, allocation], axis=1)

    def _impose_quota(self) -> None:
        # Prologue
        allocation = self.industry_allocation
        target = self.target
        industry_df = self.dataloader.industry_df
        # Body
        for i in range(11):
            ind = self.industry_list[i]
            quota = allocation.loc[ind, "allocation"]
            ticker_list = self.target[ind]
            if quota > len(ticker_list):
                allocation.loc[ind] = quota
            else:
                target[ind] = ticker_list[:quota]
        industry_df["money"] = self.money * industry_df["allocation"] / np.sum(
            industry_df["allocation"])
        # Epilogue
        self.dataloader.industry_df = industry_df
        self.target = target
        self.industry_allocation = allocation

    def _decide_stock_quantity(self) -> None:
        holding = []
        for ind in tqdm(self.industry_list):
            print("current industry is " + ind)
            tickers = self.target[ind]
            stock_prices = se.get_tickers_spec(tickers, "Adj Close", 21)
            weight = _optimize_weight(
                stock_prices, self.dataloader.industry_df["money"][ind])
            holding.append(pd.Series(weight, index=tickers, dtype=int))
            gc.collect()

        # reformat the result
        holding = pd.concat(holding)
        holding = pd.DataFrame(holding[holding != 0])
        holding = holding.reset_index()
        # update location
        location = []
        for i in range(len(holding.index)):
            ticker = holding.iloc[i]["index"]
            if ticker in list(self.dataloader.sptsx_df.index):
                location.append("CA")
            elif ticker in list(self.dataloader.spx_df.index):
                location.append("US")
            else:
                location.append(np.nan)
        holding["location"] = location
        holding = holding.rename(columns={0: "amount", "index": "ticker"})
        self.holding = holding
