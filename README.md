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
* pandas 1.4.2
* numpy 1.22.3
* MetaTrader 5.0.37
* pytz 2023.3.post1
* statsmodels 0.13.2

Last 5 items are python packages, that could be installed using `pip`

## Installation and Usage
This part would be separated by into sub-sections.

### Preparation
1. Download the entire project as ZIP. Click on Green `Code` button -> Download as ZIP.
2. Extract the downloaded ZIP.
3. Edit the following sheets on `input-data.xlsx`:
   * `Login and Settings` sheet with account informations:
     * `Acc. Number` with your Account Number.
     * `Password` with that account's password.
     * `Server` with the server assigned for that account.
   * `Pair Table` sheet with financial instrument information that you want to forecast:
     * `simbol` are filled with the symbol name for financial instruments you want to forecast.
     * `timeframe` are filled with timeframe of the chart. Also determine the forecast frequency. Only accept `M1, M5, M15, M30, H1, H4, D1, W1, MN`.
     * (optional) `starting date` are filled with the _ending_ date when retrieve data using `get_data_recent.py`. When it is empty, it is using the most recent data available on your MT5.

You can only fill 1 row of `Login and Settings` sheet, but you can write more tahn 1 row for `Pair Table` sheet when you need to forecast some instruments, for example.

4. Open your MT5 desktop application, then open new charts for each pair of symbol/timeframe specified in `Pair Table` sheet. This is to make sure that your local MT5 is updated with recent data.

### Obtain financial data
There are 2 ways to obtain data for `train_new_model.py`:

#### using `get_data_recent.py`
1. Edit the `train data name` column on `Pair Table` sheet for each symbol/timeframe rows there. This column would serve as training data name.
2. Just run `get_data_recent.py` to obtain financial data on your MT5, either by double-click the file or run it via your IDE (python's IDLE / VScode)

#### using `repair_history_data.py`
1. Visit your MT5's History Center using View -> Symbols -> Bars.
2. Choose symbol, timeframe, starting date and ending date, then click `Request`. Make sure symbol and timeframe match symbol/timeframe on `Pair Table` sheet.
3. After data is fully dowloaded, click `Export Bars`.
4. Rename the filename if needed, then save it to the same folder as this project's folder.
5. Enter the name of downloaded file in `train data name` column, same row as matched symbol/timeframe, in `Pair Table` sheet.
6. Redo step 2 - 5 for other symbol/timeframe rows on `Pair Table` sheet.
7. Run `repair_history_data.py`, either by double-click the file or run it via your IDE (python's IDLE / VScode)

### ARIMA fitting using `train_new_model.py`
Just run `train_new_model.py` to fit an ARIMA models for each symbol/timeframe pair specified in `Pair Table` sheet. You would receive 2 copies of `.pkl` file containing fitted ARIMA model for each symbol/timeframe pairs, 1 for forecasting and 1 for your archive.

### Use fitted models for forecasting
Run `core-arima-pretrain.py` to use your fitted models for forecasting. New forecast would appear in the terminal each time a new candle show up.

Here's how to read the output...

### Online ARIMA fitting
You can also fit an ARIMA model each time a new candle show up by running `core-arima-pretrain.py` instead. The way it's forecast shown is similar with `core-arima-pretrain.py`, but it is slower due to parameter tuning.

## Disclaimer
The forecast generated from this project are for informational purposes only and should not be considered financial advice.


