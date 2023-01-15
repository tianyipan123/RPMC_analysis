from Strategy.Strategy import Strategy
import pandas as pd


class ProtectionBuffer:
    """A template for Buffer

    === Attributes ===
    strategy: A strategy that holds the calculated strategy holding
    buffer: store the buffer
    tolerance: percentage of tolerated loss
    """
    # Attribute Types
    strategy: Strategy
    buffer: pd.DataFrame
    tolerance: float

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
        """Create buffer to the strategy and store in buffer.
        """
        raise NotImplementedError

    def remove_zero_buffer(self) -> None:
        """Remove all non-zero entries in self.buffer.
        """
        self.buffer = self.buffer[self.buffer["Quantity"] != 0]
