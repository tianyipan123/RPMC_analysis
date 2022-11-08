# RPMC Analysis Project

This project is created primarily for analyzing RPMC 
(Rotman Portfolio Management Competition) portfolios and relevant data analysis.

### Project Composition
- `holdings.py` keeps track of the current holdings in Google SpreadSheet
[portfolio](https://docs.google.com/spreadsheets/d/1hS4vtC7ekVef1fdf1KDb7DbemyOiqfgz3OZ62vxrTNM/edit#gid=0)
and possibly alarm the user of crucial fluctuations in the current
portfolio holdings.
- `stock_extraction.py` encapsulates the extraction of stock data from
yahoo finance, from intraday to yearly data.
- `technical_indicator.py` includes various common technical indicators in equity
market to facilitate data analysis and portfolio management.

### Dependency
- Python = 3.7
- yfinance = 0.1.62
- numpy = 1.12.6
- pandas = 1.3.5
- matplotlib = 3.5.1

**Note**: Higher versions of these packages might work well on this project, but is not guaranteed.
