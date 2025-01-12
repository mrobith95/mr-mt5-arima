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

## Requirement
You need the following to run these codes:
* Spreadsheet Editor (like Excel)
* Python 3.8.10

## Installation and Usage
Follow this steps to use this project:
1. Download the entire project as ZIP. Click on Green `Code` button -> Download as ZIP.
2. Extract the downloaded ZIP.
3. Edit `input-data.xlsx` data with the following:
   * test
4. Open your MT5 desktop application, then open new charts for each pair of symbol/timeframe specified in `Pair Table` sheet. This is to make sure that your local MT5 is updated with recent data.

### Obtain financial data
There are 2 ways to obtain data for `train_new_model.py`:

#### using `get_data_recent.py`
1. Edit the `train data name` column on `Pair Table` sheet for each symbol/timeframe rows there. This column would serve as model name.
2. Just run `get_data_recent.py` to obtain financial data on your MT5, either by double-click the file or run it via your IDE (python's IDLE / VScode)

#### using `repair_history_data.py`
1. Visit your MT5's History Center using View -> Symbols -> Bars.
2. Choose symbol, timeframe, starting date and ending date, then click `Request`. Make sure symbol and timeframe match symbol/timeframe on `Pair Table` sheet.
3. After data is fully dowloaded, click `Export Bars`.
4. Rename the filename if needed, then save it to the same folder as this project's folder.
5. Enter the name of downloaded file in `train data name` column, same row as matched symbol/timeframe, in `Pair Table` sheet.
6. Redo step 2 - 5 for other symbol/timeframe rows on `Pair Table` sheet.
7. Run `repair_history_data.py`, either by double-click the file or run it via your IDE (python's IDLE / VScode)

## Disclaimer
The forecast generated from this project are for informational purposes only and should not be considered financial advice.


