from Strategy.Strategy import Strategy as Stt
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
    """Return Sharpe ratio from weighing the stock_prices by weight.

    Precondition: len(stock_price.columns) == len(weight)
    """
    # calculate weighted price
    time_series = stock_prices.dot(weight)
    time_series = pd.Series(time_series)
    assert isinstance(time_series, pd.Series)
    # return Sharpe ratio
    return kpi.sharpe_series(time_series)


def _optimize_weight(stock_prices: pd.DataFrame, outlay: float) -> np.array:
    """Return the optimal amount of stocks that can product maximal Sharpe ratio
     with stock_prices and outlay.
    """
    # Initialization of weight
    ticker_num = len(stock_prices.columns)
    w0 = np.ones(ticker_num) / ticker_num
    # Add conditions of weight
    b = Bounds(lb=0, ub=1)
    cons = NonlinearConstraint(fun=(lambda x: np.sum(x)), lb=1, ub=1)
    # maximize Sharpe ratio
    res = minimize(lambda w: -1 * _sharpe_portfolio(stock_prices, w), w0,
                   bounds=b, constraints=cons)
    # 1 additional iteration for more accuracy
    res = minimize(lambda w: -1 * _sharpe_portfolio(stock_prices, w), res.x,
                   bounds=b, constraints=cons)
    w = res.x
    # display and return results
    basket = stock_prices.iloc[-1].dot(w)
    quantity = (outlay / basket * w).round()
    print(_sharpe_portfolio(stock_prices, quantity))
    return quantity


class SharpeMaxStrategy(Stt):
    """ A Strategy that maximizes the Sharpe ratio.

    === Attributes ===
    sharpe_mean: stores the average Sharpe ratio in each industry
    target: stores tickers that has positive Sharpe ratio in each industry
    industry_list: a list of all industries
    stock_num: number of potential stocks chosen
    selection_filter: number of days used for stock data
                      in initial stock selection
    optimization_filter: number of days for stock data used
                         in weight optimization
    """
    # Attribute Types
    sharpe_mean: pd.DataFrame
    target: Dict[str, List[str]]
    industry_list: List[str]
    stock_num: int
    selection_filter: int
    optimization_filter: int

    def __init__(self, dc: DataLoader, money: int, stock_num: int,
                 selection_filter: int, optimization_filter: int) -> None:
        """Initializer to SharpeMaxStrategy.
        """
        Stt.__init__(self, dc, money)
        self.sharpe_mean = pd.DataFrame()
        self.target = {}
        self.industry_list = list(dc.industry_df.index)
        self.stock_num = stock_num
        self.selection_filter = selection_filter
        self.optimization_filter = optimization_filter

    def __str__(self) -> str:
        """String representation of SharpeMaxStrategy.
        """
        return "Strategy: Maximize Sharpe Ratio"

    def develop_strategy(self) -> None:
        """Inherited method from Strategy.
        """
        self._select_possible_stocks()
        self._decide_industry_allocation()
        self._impose_quota()
        self._decide_stock_quantity()

    def _select_possible_stocks(self) -> None:
        """Select stocks with positive Sharpe ratio in self.selection_filter
        days and store the results in sharpe_mean and target.
        """
        # setup
        stock_df = pd.concat([self.dataloader.sptsx_df, self.dataloader.spx_df])
        stock_df = stock_df.reset_index()
        sharpe_dict = {}
        target = {}
        sel_filter = self.selection_filter

        # store ticker with positive Sharpe ratio
        for ind in tqdm(self.industry_list):
            tickers_list = list(
                stock_df["index"][stock_df["GICS Sector\n"] == ind]
            )
            pos = []
            target_list = []
            for ticker in tickers_list:
                stock_price, success = se.get_daily_stock(ticker, sel_filter)
                sharpe = kpi.sharpe(stock_price)
                if kpi.volatility(stock_price) == 0:
                    print(ticker)
                if sharpe > 0 and success:
                    pos.append(sharpe)
                    target_list.append(ticker)
            # rank stocks by Sharpe Ratio
            target_list = np.array(target_list)
            target_list = target_list[np.argsort(pos)[::-1]]
            mean = np.mean(pos)
            sharpe_dict[ind] = mean
            target[ind] = target_list
        # remove stock_price garbage
        gc.collect()

        # save results
        sharpe_mean = pd.DataFrame.from_dict(sharpe_dict, orient="index")
        self.sharpe_mean = sharpe_mean
        self.target = target

    def _decide_industry_allocation(self) -> None:
        """Decide industry allocation for the number of stocks by their average
        performance in Sharpe ratio.
        """
        allocation = (self.stock_num * self.sharpe_mean / np.sum(
            self.sharpe_mean.values)).round().astype(int)
        # edge case because Telecommunication Services industry
        # have much fewer stocks
        if allocation[0]["Telecommunication Services"] > 4:
            available = allocation[0]["Telecommunication Services"] - 4
            # randomly assign the exceeded availability to other industry
            r = np.random.randint(0, 11, available)
            for i in r:
                allocation.iloc[i] += 1
            allocation[0]["Telecommunication Services"] = 4
        allocation.columns = ["allocation"]
        # save results
        self.dataloader.industry_df = pd.concat(
            [self.dataloader.industry_df, allocation], axis=1)

    def _impose_quota(self) -> None:
        """Impose quota from _industry_allocation() and change target to
        only include targeted stocks.
        """
        # setup
        target = self.target
        industry_df = self.dataloader.industry_df
        # Body: impose quota
        for i in range(11):
            ind = self.industry_list[i]
            quota = industry_df.loc[ind, "allocation"]
            ticker_list = self.target[ind]
            if quota > len(ticker_list):
                industry_df.loc[ind, "allocation"] = quota
            else:
                target[ind] = ticker_list[:quota]
        industry_df["money"] = self.money * industry_df["allocation"] / np.sum(
            industry_df["allocation"])
        # save results
        self.dataloader.industry_df = industry_df
        self.target = target

    def _decide_stock_quantity(self) -> None:
        # setup
        holding = []
        opt_filter = self.optimization_filter
        # optimize the weight of stocks inside each industry
        for ind in tqdm(self.industry_list):
            print("current industry is " + ind)
            tickers = self.target[ind]
            stock_prices = se.get_tickers_spec(tickers, "Adj Close",
                                               self.selection_filter // 2)
            stock_prices = stock_prices[-self.optimization_filter:]
            weight = _optimize_weight(
                stock_prices, self.dataloader.industry_df["money"][ind])
            holding.append(pd.Series(weight, index=tickers, dtype=int))
            gc.collect()

        # reformat the result
        holding = pd.concat(holding)
        holding = pd.DataFrame(holding[holding != 0])
        holding = holding.reset_index()

        # update location for selected tickers
        location = []
        for i in range(len(holding.index)):
            ticker = holding.iloc[i]["index"]
            if ticker in list(self.dataloader.sptsx_df.index):
                location.append("CA")
            elif ticker in list(self.dataloader.spx_df.index):
                location.append("US")
            else:
                location.append(np.nan)
        # save results
        holding["location"] = location
        holding = holding.rename(columns={0: "amount", "index": "ticker"})
        self.holding = holding
