import pandas as pd
import numpy as np
import pandas.io.excel


class DataStorer:
    """Store calculated results.

    === Attributes ===
    writer: the Excel writer used to store results
    """
    # Attribute Types
    writer: pd.io.excel.ExcelWriter

    def __init__(self, writer: pd.io.excel.ExcelWriter) -> None:
        """Initializer to DataStorer.
        """
        self.writer = writer

    def __str__(self) -> str:
        """String representation of DataStorer.
        """
        return "Storing Data"

    def store_buy(self, holding: pd.DataFrame, buffer: pd.DataFrame) -> None:
        """Store holding by writer in Buying template format.
        """
        # Formulate Tradable basket in template
        basket = pd.DataFrame(holding["ticker"] + "-" + holding["location"],
                              columns=["Ticker"])
        basket["Buy/Sell"] = np.where(holding["amount"] > 0, "Buy", "Sell")
        basket["Quantity"] = holding["amount"].abs()
        basket["Type"] = "MKT"
        # store results
        self._store_allocation(basket, "buy")
        self._store_buffer(buffer)

    def store_hold(self, holding: pd.DataFrame) -> None:
        """Store holding by writer in more readable format.
        """
        self._store_allocation(holding, "holding")

    def _store_buffer(self, buffer: pd.DataFrame) -> None:
        # TODO: Must append to the excel
        buffer.to_excel(self.writer, sheet_name="buy", index=False)
        self.writer.save()

    def _store_allocation(self, allocation: pd.DataFrame, sheet) -> None:
        """A helper function for storage.
        """
        allocation.to_excel(self.writer, sheet_name=sheet, index=False)
        self.writer.save()

