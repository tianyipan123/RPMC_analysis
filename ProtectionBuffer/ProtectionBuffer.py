import pandas as pd


class ProtectionBuffer:

    def __init__(self):
        pass

    def __str__(self):
        raise NotImplementedError

    def create_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
