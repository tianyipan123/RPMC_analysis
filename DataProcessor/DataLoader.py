import pandas as pd


class DataLoader:
    """Load trade data and perform elementary processes for further
    investigation in data.

    === Attributes ===
    sptsx_df: tradable tickers with sector information in SPTSX
    spx_df: tradable tickers with sector information in SPX
    etf_df: tradable tickers for ETFs with sector information
    industry_df: industry statistic for tickers in SPTSX and SPX
    tradable_path: file path for tradable stock information
    """
    # Attribute Types
    sptsx_df: pd.DataFrame
    spx_df: pd.DataFrame
    etf_df: pd.DataFrame
    industry_df: pd.DataFrame
    tradable_path: str

    def __init__(self) -> None:
        """Initializer to DataLoader.
        """
        self.sptsx_df = pd.DataFrame()
        self.spx_df = pd.DataFrame()
        self.etf_df = pd.DataFrame()
        self.industry_df = pd.DataFrame()
        self.tradable_path = "DataProcessor/tradable_list.xlsx"

    def __str__(self) -> str:
        """String representation of DataLoader.
        """
        return "Loading Data"

    def read_data(self) -> None:
        """Read SPTSX, SPX, and ETF information from tradable_path.
        """
        self._read_sptsx()
        self._read_spx()
        self._read_etf()

    def _read_sptsx(self) -> None:
        """Read SPTSX data from tradable_path and store results in sptsx_df.
        """
        # setup
        sptsx_df = pd.read_excel(self.tradable_path, sheet_name="SPTSX")
        header = sptsx_df.iloc[0]
        sptsx_df = sptsx_df.iloc[1:]
        sptsx_df.columns = header
        sptsx_df["RPM Ticker"] = [ticker.split('-')[0] for ticker in
                                  sptsx_df["RPM Ticker"]]
        sptsx_df = sptsx_df.set_index("RPM Ticker")

        # remove non_trackable tickers
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
            "MTL",  # this stock gives constant stock price
            "IAG" # point to another not listed stock
        ]
        sptsx_df.drop(non_trackable, inplace=True)
        # drop unused information
        sptsx_df.drop(["Bloom.Berg Ticker"], inplace=True, axis=1)
        self.sptsx_df = sptsx_df

    def _read_spx(self) -> None:
        """Read SPX data from tradable_path and store results in spx_df.
        """
        # setup
        spx_df = pd.read_excel(self.tradable_path, sheet_name="SPX")
        header = spx_df.iloc[0]
        spx_df = spx_df.iloc[1:]
        spx_df.columns = header
        spx_df["RPM-USTicker"] = [ticker.split('-')[0] for ticker in
                                  spx_df["RPM-USTicker"]]
        spx_df = spx_df.set_index("RPM-USTicker")

        # remove non_trackable tickers
        non_trackable = [
            "ADS", "AGN", "ALXN", "ANTM", "BBT", "BF.B", "BHGE", "BLL",
            "BRK.B", "CBS", "CELG", "CERN", "COG", "CTL", "CXO", "DISCA",
            "DISCK", "ETFC", "FLIR", "HFC", "INFO", "JEC", "KSU",
            "LB", "MXIM", "MYL", "NBL", "PBCT", "RTN", "STI", "SYMC",
            "TIF", "UTX", "VAR", "VIAB", "WCG", "WLTW", "XEC", "XLNX",
            "T",  # T in yfinance seems to represent Telus rather than AT&T
            "NLSN", "TWTR", "CTXS",  # no lastest data available
        ]
        spx_df.drop(non_trackable, inplace=True)

        # remove unused information
        spx_df.drop(["Bloom.B-USerg Ticker"], inplace=True, axis=1)
        self.spx_df = spx_df

    def _read_etf(self) -> None:
        """Read ETF data from tradable_path and store results in etf_df.
        """
        # setup
        etf_df = pd.read_excel(self.tradable_path, sheet_name="ETFs")
        header = etf_df.iloc[0]
        etf_df = etf_df.iloc[1:]
        etf_df.columns = header
        etf_df["RPM Ticker"] = [ticker.split('-')[0] for ticker in
                                etf_df["RPM Ticker"]]
        etf_df = etf_df.set_index("RPM Ticker")

        # remove non_trackable information
        non_trackable = ["XCB", "XGB", "XSB", "IEMG.K", "XIC", "XIU"]
        etf_df.drop(non_trackable, inplace=True)
        # save result
        self.etf_df = etf_df

    def count_industry(self) -> None:
        """Count how many stocks are in each industry and store the results
        in industry_df.
        """
        # group stocks by industry types
        df1 = self.sptsx_df.groupby(["GICS Sector\n"]).count()
        df2 = self.spx_df.groupby("GICS Sector\n").count()
        # save results
        self.industry_df = df1 + df2
