from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as PB
from Strategy.Strategy import Strategy
import pandas as pd
import numpy as np
from Toolbox import stock_extraction as se


class FullStopOrderBuffer(PB):

    def __init__(self, strategy: Strategy, tolerance: float) -> None:
        """Initializer to StopOrderBuffer.
        """
        PB.__init__(self, strategy, tolerance)

    def __str__(self) -> str:
        """String representation of StopOrderBuffer.
        """
        return "Stop Order Buffer"

    def create_buffer(self) -> None:
        holding = self.strategy.holding
        buffer_list = []
        for ticker in holding["ticker"]:
            amount = holding.loc[ticker, "amount"]
            # if the holding is a buy signal, sign is 1
            amount, sign = abs(amount), amount > 0
            price = se.get_current_price(ticker)
            buffer_list.append(
                pd.DataFrame({"Ticker": ticker + holding.loc[ticker, "location"],
                              "Buy/Sell": np.where(sign, "Sell", "Buy"),
                              "Quantity": amount,
                              "Type": "STOP",
                              "Price": price * (1 - self.tolerance)
                              })
            )
        self.buffer = pd.concat(buffer_list)
