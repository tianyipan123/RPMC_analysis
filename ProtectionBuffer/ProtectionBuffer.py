from Strategy.Strategy import Strategy
import pandas as pd


class ProtectionBuffer:

    def __init__(self, strategy: Strategy, tolerance: float) -> None:
        """Initializer to ProtectionBuffer.
        """
        self.strategy = strategy
        self.buffer = pd.DataFrame()
        self.tolerance = tolerance

    def __str__(self) -> str:
        """String representation of ProtectionBuffer.
        """
        raise NotImplementedError

    def create_buffer(self) -> None:
        raise NotImplementedError

    def remove_zero_buffer(self) -> None:
        self.buffer = self.buffer[self.buffer["Quantity"] != 0]
