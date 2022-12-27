import pandas as pd


class ProtectionBuffer:

    def __init__(self) -> None:
        """Initializer to ProtectionBuffer.
        """
        pass

    def __str__(self) -> str:
        """String representation of ProtectionBuffer.
        """
        raise NotImplementedError

    def create_buffer(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
