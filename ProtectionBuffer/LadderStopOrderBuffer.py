from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as PB
from Strategy.Strategy import Strategy
import pandas as pd
from Toolbox import stock_extraction as se
import numpy as np


class LadderStopOrderBuffer(PB):

    def __init__(self, strategy: Strategy, tolerance: float, layer: int, method: str) -> None:
        """Initializer to StopOrderBuffer.
        """
        PB.__init__(self, strategy, tolerance)
        self.layer = layer
        self.method = method

    def __str__(self) -> str:
        """String representation of StopOrderBuffer.
        """
        return f"Ladder Stop Order Buffer: layer = {self.layer}, " \
               f"method = {self.method}"

    def create_buffer(self) -> None:
        # TODO: change to switch case
        if self.method == "equal":
            self._equal_buffer()
        elif self.method == "geom":
            self._geometric_half_buffer()
        else:
            print("No such method; please use other available options.")

    def _equal_buffer(self) -> None:
        holding = self.strategy.holding
        buffer_list = []

        for ticker in holding["ticker"]:
            amount = holding.loc[ticker, "amount"]
            # if the holding is a buy signal, sign is 1
            amount, sign = round(abs(amount) / self.layer),\
                np.where(amount > 0, "Sell", "Buy")

            # build each layer
            for i in range(1, self.layer + 1):
                buffer_list.append(
                    self.__single_buffer(i, ticker, str(sign), amount,
                                         holding.loc[ticker, "location"])
                )
        self.buffer = pd.concat(buffer_list)

    def _geometric_half_buffer(self):
        holding = self.strategy.holding
        buffer_list = []

        for ticker in holding["ticker"]:
            amount = holding.loc[ticker, "amount"]
            # build each layer
            for i in range(1, self.layer + 1):
                amount, sign = round(abs(amount) / (2 ** i)), \
                    np.where(amount > 0, "Sell", "Buy")
                if i == self.layer:
                    amount = round(abs(amount) / (2 ** self.layer))
                # append result
                buffer_list.append(
                    self.__single_buffer(i, ticker, str(sign), amount,
                                         holding.loc[ticker, "location"])
                )
        # store result
        self.buffer = pd.concat(buffer_list)

    def __single_buffer(self, i: int, ticker: str, sign: str, amount: int,
                        location: str) -> pd.DataFrame:
        ratio = 1 - (self.tolerance * i / self.layer)
        price = se.get_current_price(ticker)
        return pd.DataFrame(
                {"Ticker": ticker + location,
                 "Buy/Sell": sign,
                 "Quantity": amount,
                 "Type": "STOP",
                 "Price": price * ratio
                 })
