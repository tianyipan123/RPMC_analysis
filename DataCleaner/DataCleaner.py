import pandas as pd
import numpy as np
from Toolbox import kpi, stock_extraction as se
from scipy.optimize import minimize, NonlinearConstraint, Bounds

import gc
import time
from contextlib import contextmanager
from tqdm import tqdm


class DataCleaner:

    def read_data(self) -> pd.DataFrame:
        pass

    def store_data(self) -> pd.DataFrame:
        pass
