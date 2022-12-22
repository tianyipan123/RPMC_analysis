from ProtectionBuffer import ProtectionBuffer
import pandas as pd


class OptionBuffer(ProtectionBuffer):

    def __init__(self):
        ProtectionBuffer.__init__(self)

    def __str__(self):
        return "This is Option Buffer"

    def create_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
