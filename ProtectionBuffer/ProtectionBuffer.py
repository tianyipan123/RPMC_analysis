from Strategy.Strategy import Strategy
import pandas as pd


class ProtectionBuffer:

    def __init__(self, strategy: Strategy, tolerance: float) -> None:
        """Initializer to ProtectionBuffer.
        """
        self.strategy = strategy
        # TODO: might not need to specify the column
        self.buffer = pd.DataFrame(columns=["Ticker", "Buy/Sell", "Quantity",
                                            "Type", "Price"])
        self.tolerance = tolerance

    def __str__(self) -> str:
        """String representation of ProtectionBuffer.
        """
        raise NotImplementedError

    def create_buffer(self) -> None:
        raise NotImplementedError
