from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as PB
import pandas as pd


class OptionBuffer(PB):

    def __init__(self) -> None:
        """Initializer to OptionBuffer.
        """
        PB.__init__(self)

    def __str__(self) -> str:
        """String representation of OptionBuffer.
        """
        return "This is Option Buffer"

    def create_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
