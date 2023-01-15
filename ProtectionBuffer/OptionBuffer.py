from ProtectionBuffer.ProtectionBuffer import ProtectionBuffer as PB
import pandas as pd
from Strategy.Strategy import Strategy


class OptionBuffer(PB):

    def __init__(self, strategy: Strategy, tolerance: float) -> None:
        """Initializer to OptionBuffer.
        """
        PB.__init__(self, strategy, tolerance)

    def __str__(self) -> str:
        """String representation of OptionBuffer.
        """
        return "Option Buffer"

    def create_buffer(self) -> None:
        pass
