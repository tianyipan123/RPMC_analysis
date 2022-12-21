import pandas as pd


class Strategy:

    def __init__(self):
        pass

    def __str__(self):
        raise NotImplementedError

    def develop_strategy(self) -> pd.DataFrame:
        raise NotImplementedError
