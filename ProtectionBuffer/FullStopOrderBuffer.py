from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as PB
from Strategy.Strategy import Strategy
import pandas as pd
import numpy as np
from Toolbox import stock_extraction as se
from tqdm import tqdm


class FullStopOrderBuffer(PB):
    """A ProtectionBuffer that full insures the holding
    """

    def __init__(self, strategy: Strategy, tolerance: float) -> None:
        """Initializer to StopOrderBuffer.
        """
        PB.__init__(self, strategy, tolerance)

    def __str__(self) -> str:
        """String representation of StopOrderBuffer.
        """
        return "Stop Order Buffer"

    def create_buffer(self) -> None:
        """Inherited method from ProtectionBuffer.
        """
        holding = self.strategy.holding
        holding = holding.set_index("ticker")
        buffer_list = []

        for ticker in tqdm(holding.index):
            amount = holding.loc[ticker, "amount"]
            # if the holding is a buy signal, sign is 1
            amount, sign = abs(amount), amount > 0
            price = se.get_current_price(ticker)
            ticker_name = ticker + "-" + holding.loc[ticker, "location"]
            buffer_list.append(
                pd.DataFrame({"Ticker": [ticker_name],
                              "Buy/Sell": np.where(sign, "Sell", "Buy"),
                              "Quantity": [amount],
                              "Type": ["STOP"],
                              "Price": [price * (1 - self.tolerance)]
                              })
            )
        self.buffer = pd.concat(buffer_list)
