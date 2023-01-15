import time
import pandas as pd
from contextlib import contextmanager

from DataProcessor.DataLoader import DataLoader
from DataProcessor.DataStorer import DataStorer
from Strategy.SharpeMaxStrategy import SharpeMaxStrategy
from ProtectionBuffer.FullStopOrderBuffer import FullStopOrderBuffer
from ProtectionBuffer.LadderStopOrderBuffer import LadderStopOrderBuffer
from Visualizer.Visualizer import Visualizer


@contextmanager
def timer(name: str) -> None:
    """This function is used for display time taken."""
    s = time.time()
    yield
    elapsed = time.time() - s
    print(f"[{name}] takes {elapsed: .3f} seconds")


#%% Preparation
money = 700000
dataloader = DataLoader()

with timer(str(dataloader)):
    dataloader.read_data()
    dataloader.count_industry()

#%% Develop Strategy
strategy = SharpeMaxStrategy(dataloader, money, 100, 100, 20)
with timer(str(strategy)):
    strategy.develop_strategy()

#%% Add Buffer
buffer = FullStopOrderBuffer(strategy, 0.05)
# buffer = LadderStopOrderBuffer(strategy, 0.1, 4, "geom")
with timer(str(buffer)):
    buffer.create_buffer()
    buffer.remove_zero_buffer()

#%% Store result
holding_path = "holding.xlsx"
writer = pd.ExcelWriter(holding_path)
data_storer = DataStorer(writer)
with timer(str(data_storer)):
    data_storer.store_buy(strategy.holding, buffer.buffer)
    data_storer.store_hold(strategy.holding)

#%% Visualize Result
url = "https://docs.google.com/spreadsheets/d/1hS4vtC7ekVef1fdf1KDb7DbemyOiqfgz3OZ62vxrTNM/edit#gid=0"
url = url.replace('/edit#gid=', '/export?format=csv&gid=')
visualizer = Visualizer(url)
with timer(str(visualizer)):
    visualizer.fetch_holding()
    visualizer.summarize_kpi()
    visualizer.visualize()
    visualizer.document()
