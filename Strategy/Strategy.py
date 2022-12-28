from DataProcessor.DataLoader import DataLoader
import pandas as pd


class Strategy:
    """A template for trading strategies.

    === Attributes ===
    dataloader: A DataLoader that stores trade information
    money: the amount the strategy can use
    holding: store the calculated result by the Strategy
    """
    # Attribute Types
    dataloader: DataLoader
    money: int
    holding: pd.DataFrame

    def __init__(self, dc: DataLoader, money: int) -> None:
        """Initializer to Strategy.
        """
        self.dataloader = dc
        self.money = money
        self.holding = pd.DataFrame()

    def __str__(self) -> str:
        """String representation of Strategy.
        """
        raise NotImplementedError

    def develop_strategy(self) -> None:
        """The core function that generate the strategy and store calculated
        results in holding.
        """
        raise NotImplementedError
