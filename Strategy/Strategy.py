from DataProcessor.DataLoader import DataLoader
import pandas as pd


class Strategy:

    dataloader: DataLoader
    money: int
    holding: pd.DataFrame

    def __init__(self, dc: DataLoader, money: int) -> None:
        self.dataloader = dc
        self.money = money
        self.holding = pd.DataFrame()

    def __str__(self) -> str:
        raise NotImplementedError

    def develop_strategy(self) -> None:
        raise NotImplementedError
