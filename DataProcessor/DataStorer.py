import pandas as pd
import numpy as np
import pandas.io.excel


class DataStorer:

    writer: pd.io.excel.ExcelWriter

    def __init__(self, writer: pd.io.excel.ExcelWriter) -> None:
        self.holding_path = writer

    def __str__(self) -> str:
        return "DataStorer is storing"

    def store_buy(self, holding: pd.DataFrame) -> None:
        basket = pd.DataFrame(holding["ticker"] + "-" + holding["location"],
                              columns=["Ticker"])
        basket["Buy/Sell"] = np.where(holding["amount"] > 0, "Buy", "Sell")
        basket["Quantity"] = holding["amount"].abs()
        basket["Type"] = "MKT"
        basket.to_excel(self.writer, sheet_name="buy", index=False)
        self._store_allocation(basket, "buy")

    def store_hold(self, holding: pd.DataFrame) -> None:
        self._store_allocation(holding, "holding")
        self._store_online(holding)

    def _store_online(self, holding: pd.DataFrame) -> None:
        pass
        # TODO: Under construction

    def _store_allocation(self, allocation: pd.DataFrame, sheet) -> None:
        allocation.to_excel(self.writer, sheet_name=sheet, index=False)
        self.writer.save()

