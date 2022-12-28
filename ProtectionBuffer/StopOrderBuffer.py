from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as PB
import pandas as pd


class StopOrderBuffer(PB):

    def __init__(self) -> None:
        """Initializer to StopOrderBuffer.
        """
        PB.__init__(self)

    def __str__(self) -> str:
        """String representation of StopOrderBuffer.
        """
        return "This is Stop Order Buffer"

    def create_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
