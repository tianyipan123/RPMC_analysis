import pandas as pd
import numpy as np
from Toolbox import kpi, stock_extraction as se
from scipy.optimize import minimize, NonlinearConstraint, Bounds

import gc
import time
from contextlib import contextmanager
from tqdm import tqdm


class DataLoader:

    sptsx_df: pd.DataFrame
    spx_df: pd.DataFrame
    etf_df: pd.DataFrame
    industry_df: pd.DataFrame

    def __init__(self) -> None:
        self.sptsx_df = pd.DataFrame()
        self.spx_df = pd.DataFrame()
        self.etf_df = pd.DataFrame()
        self.industry_df = pd.DataFrame()

    def __str__(self) -> str:
        return "DataLoader is loading"

    def read_data(self) -> None:
        self._read_sptsx()
        self._read_spx()
        self._read_etf()

    def _read_sptsx(self) -> None:
        sptsx_df = pd.read_excel("tradable_list.xlsx", sheet_name="SPTSX")
        header = sptsx_df.iloc[0]
        sptsx_df = sptsx_df.iloc[1:]
        sptsx_df.columns = header
        sptsx_df["RPM Ticker"] = [ticker.split('-')[0] for ticker in
                                  sptsx_df["RPM Ticker"]]
        sptsx_df = sptsx_df.set_index("RPM Ticker")

        non_trackable = [
            "ABX", "ACO.X", "AD", "AFN", "ALA", "AP.UT", "APHA", "ARX",
            "ATD", "ATZ", "AX.UT", "BAM.A", "BBD.B", "BBU.UT", "BCB", "BEI.UT",
            "BEP.UT", "BIP.UT", "BPY.UT", "BTE", "BYD.UT", "CAR.UT", "CAS",
            "CCA",
            "CCL.B", "CFP", "CGX", "CHE.UT", "CHP.UT", "CHR", "CJT", "CNR",
            "CPX", "CRR.UT", "CSH.UT", "CSU", "CTC.A", "CU", "CUF.UT", "D.UT",
            "DGC", "DIR.UT", "DRG.UT", "DSG", "ECA", "ECN", "EFN", "EIF",
            "EMA", "EMP.A", "EQB", "EXE", "FCR", "FEC", "FFH", "FRU",
            "FTT", "GC", "GEI", "GIB.A", "GRT.UT", "GUD", "GWO", "HBC",
            "HCG", "HR.UT", "HSE", "IFC", "IFP", "IIP.UT", "IMG", "INE",
            "IPL", "IVN", "KL", "KMP.UT", "KXS", "LB", "LIF", "LNR",
            "LUN", "MFI", "MIC", "MRE", "MRU", "MTY", "MWC", "NFI",
            "NPI", "NVU.UT", "NWH.UT", "OGC", "ONEX", "OSB", "PVG", "PWF",
            "PXT", "QBR.B", "RCH", "RCI.B", "REI.UT", "RUS", "SIA", "SJR.B",
            "SMF", "SMU.UT", "SNC", "SRU.UT", "TCL.A", "TECK.B", "TIH", "TOU",
            "TOY", "TSGI", "WCP", "WDO", "WFT", "WJA", "WN", "WPK",
            "WSP", "WTE", "YRI",
            "MTL"  # this stock gives constnat stock price
        ]
        sptsx_df.drop(non_trackable, inplace=True)
        sptsx_df.drop(["Bloom.Berg Ticker"], inplace=True, axis=1)
        self.sptsx_df = sptsx_df

    def _read_spx(self) -> None:
        spx_df = pd.read_excel("tradable_list.xlsx", sheet_name="SPX")
        header = spx_df.iloc[0]
        spx_df = spx_df.iloc[1:]
        spx_df.columns = header
        spx_df["RPM-USTicker"] = [ticker.split('-')[0] for ticker in
                                  spx_df["RPM-USTicker"]]
        spx_df = spx_df.set_index("RPM-USTicker")

        non_trackable = [
            "ADS", "AGN", "ALXN", "ANTM", "BBT", "BF.B", "BHGE", "BLL",
            "BRK.B", "CBS", "CELG", "CERN", "COG", "CTL", "CXO", "DISCA",
            "DISCK", "ETFC", "FLIR", "HFC", "INFO", "JEC", "KSU",
            "LB", "MXIM", "MYL", "NBL", "PBCT", "RTN", "STI", "SYMC",
            "TIF", "UTX", "VAR", "VIAB", "WCG", "WLTW", "XEC", "XLNX",
            "T",  # T in yfinance seems to represent Telus rather than AT&T
            "NLSN", "TWTR", "CTXS"  # no lastest data available
        ]
        spx_df.drop(non_trackable, inplace=True)
        self.spx_df = spx_df

    def _read_etf(self) -> None:
        etf_df = pd.read_excel("tradable_list.xlsx", sheet_name="ETFs")
        header = etf_df.iloc[0]
        etf_df = etf_df.iloc[1:]
        etf_df.columns = header
        etf_df["RPM Ticker"] = [ticker.split('-')[0] for ticker in
                                etf_df["RPM Ticker"]]
        etf_df = etf_df.set_index("RPM Ticker")

        non_trackable = ["XCB", "XGB", "XSB", "IEMG.K", "XIC", "XIU"]
        etf_df.drop(non_trackable, inplace=True)
        self.etf_df = etf_df

    def count_industry(self) -> None:
        df1 = self.sptsx_df.groupby(["GICS Sector\n"]).count()
        df2 = self.spx_df.groupby("GICS Sector\n").count()
        self.industry_df = df1 + df2
