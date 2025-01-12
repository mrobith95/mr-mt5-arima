# mr-mt5-arima
A set of python script to forecast financial market data on your Metatrader5 using ARIMA.

## Introduction
Accurate forecasting of financial markets is crucial for successful trading. This project aims to provide traders with an easily implementable solution for generating price forecasts directly from their MT5 environment. ARIMA itself is a simple model to tune and fit, making it suitable in either in offline or online fitting scenario.

## Features
* 2 ways to obtain/manage data: automated data retrieval from MT5 chart, or use bars data retrieved from MT5 History Center.
* Forecasts various financial instruments (Forex, Metals, Energies, Stocks).
* Automated ARIMA parameters tuning.
* Offline or Online ARIMA fitting.
* Online monitoring and forecast: Forecast would be performed each time a new candle is detected.
* Intraday forecast (up to 1 minute forecast) available (workload dependant).
* Performance log.

## How it Works
* Instrument to be forecast and MT5 login data is obtained from `input-data.xlsx`.
* `get_data_recent.py` then retrieve financial data directly from MT5 chart.
  * or you can repair data downloaded from MT5's History Center instead, using `repair_history_data.py`.
* ARIMA model then trained on downloaded financial data using `train_new_model.py`.
* Use the trained model for forecasting online by running `core-arima-pretrain.py`

If you prefer an always up-to-date model, you can instead train a new ARIMA model each time a candle is finished using `core-arima-online.py`

## Installation and Usage
Follow this steps to use this project:
1. test
2. test2

## Disclaimer
The forecast generated from this project are for informational purposes only and should not be considered financial advice.


