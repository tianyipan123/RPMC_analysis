from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as pb
import pandas as pd


class OptionBuffer(pb):

    def __init__(self):
        pb.__init__(self)

    def __str__(self):
        return "This is Option Buffer"

    def create_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
