# RPMC Analysis Project

This project is created primarily for analyzing RPMC 
(Rotman Portfolio Management Competition) portfolios and relevant data analysis.

### Project Composition

- `main.py` can be used to run the program and generate the latest result.
- `DataProcessor` directory stores class needed for data access and storage.
In the directory, `DataLoader.py` preprocess the data in `tradable_list.xlsx` and
help further investigation. `DataStorer.py` stores the results from investigation.
- `ProtectionBuffer` directory attempts to add protection to the strategy. In the
directory, `ProtectionBuffer` provides the interface of such buffer, while
`StopOrderBuffer.py` and `OptionBuffer.py` implements various financial
instruments to achieve the goal (currently under construction).
- `Strategy` directory stores the quantitative strategies towards stock trading.
In the directory, `Strategy.py` provides the interface of such strategy, and
`SharpeMaxStrategy.py` implements such framework and develop the stock
allocation by maximizing the Sharpe ratio.
- `Toolbox` directory stores various tools in analyzing stocks. `kpi.py` develop
various KPI for stocks time series; `stock_extraction.py` is a wrapper class for
`yfinance`, which provides more specific and easy-to-access tools to extract
stock information; `technical_indictor.py` implements common technical indictors
used in technical analysis.
- `Visualizer` directory only contains `Visualizer.py`, which is used to display
current holding trends and keep such record in `prediction` directory.
- `prediction` directory is used solely for keeping record of weekly performance.
- `holding.xlsx` is stores template for the software to trade stocks in basket, 
and stores more visual-friendly way of seeing the holding for the week. To see
the latest holding, please click [here](https://docs.google.com/spreadsheets/d/1hS4vtC7ekVef1fdf1KDb7DbemyOiqfgz3OZ62vxrTNM/edit#gid=0).

> Sample uses of these functions are given in `__main__` of each file.

### Dependency
- Python = 3.7
- yfinance = 0.1.62
- numpy = 1.12.6
- pandas = 1.3.5
- matplotlib = 3.5.1

**Note**: Higher versions of these packages might work well on this project, but are not guaranteed.
