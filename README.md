# mr-mt5-arima
A set of python script to forecast financial market data on your Metatrader5 (MT5) using ARIMA.

## Introduction
Accurate forecasting of financial markets is crucial for successful trading. This project aims to provide traders with a simple way to generate price forecasts directly from their MT5. ARIMA itself is a simple model to tune and fit, making it suitable in either in offline or online fitting scenario.

![predict-aarima-pics](https://github.com/user-attachments/assets/b3198cc3-5ce8-4f30-a62a-bd7c4e89fcc1)

## __Disclaimer__
⚠️
__The forecasts generated from this project are for informational purposes only and should not be considered financial advice.__
⚠️

## Features
* 2 ways to obtain/manage data: automated data retrieval from MT5 chart, or use bars data retrieved from MT5 History Center.
* Forecasts various financial instruments (Forex, Metals, Energies, Stocks) that available on your MT5.
* Automated ARIMA parameters tuning.
* Offline/Online ARIMA fitting.
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
* tabulate 0.9.0

Last 6 items are python packages, that could be installed using `pip install <package_name>==<version_number>`.

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
     * `simbol` are filled with the symbol/ticker name for financial instruments you want to forecast. Make sure they are exist on your MT5's Symbol list.
     * `timeframe` are filled with timeframe of the chart. Also determine the forecast frequency. Only accept `M1, M5, M15, M30, H1, H4, D1, W1, MN`.
     * `train data name` will become the file name of retrieved data, data used for training, and trained model. You can fill this later if you wish.

You can only fill 1 row of `Login and Settings` sheet, but you can write more than 1 row for `Pair Table` sheet when you need to forecast some instruments, for example.

![isi pair table](https://github.com/user-attachments/assets/b6fb5e54-5ebe-4827-9017-c4131ffe4cf9)

4. Open your MT5 desktop application, then open new charts for each pair of symbol/timeframe specified in `Pair Table` sheet. This is to make sure that your local MT5 is updated with recent data.

### Obtain financial data
There are 2 ways to obtain data for fitting models. Any data obtained would be saved in `training data` folder:

#### Retrieve directly from charts
1. Edit the `train data name` column on `Pair Table` sheet for each symbol/timeframe rows there. This column would serve as training data name.
2. Run `get_data_recent.py` to obtain financial data on your MT5, either by double-click the file or run it via your IDE (python's IDLE / VScode)

#### Using History Center
1. If you don't have a folder named `training data` in the same folder as this project, make it first.
2. Visit your MT5's History Center using View -> Symbols -> Bars.
3. Choose symbol, timeframe, starting date and ending date, then click `Request`. Make sure symbol and timeframe match symbol/timeframe on `Pair Table` sheet.
4. After data is fully dowloaded, click `Export Bars`.
5. Rename the filename if needed, then save it to the `training data` folder you just made at step 1.
6. Enter the name of downloaded file in `train data name` column, same row as matched symbol/timeframe, in `Pair Table` sheet.
7. Redo step 3 - 6 for other symbol/timeframe rows on `Pair Table` sheet.
8. Run `repair_history_data.py`, either by double-click the file or run it via your IDE (python's IDLE / VScode)

### ARIMA fitting
Run `train_new_model.py` to fit an ARIMA models for each symbol/timeframe pair specified in `Pair Table` sheet. Any data obtained would be saved in `arimas` folder.

### Use fitted models for forecasting
Run `core-arima-pretrain.py` to use your fitted models for forecasting. New forecast would appear in the terminal each time a new candle show up.

Here's how to read the output...

![predict-aarima-pics - Copy](https://github.com/user-attachments/assets/932ff264-3318-4c2b-911b-57048a533044)

* Time: The time as specified at time entry on _current_ (forming) candle.
* Symbol: Symbol/Ticker name
* Prev. Act. : Actual close price of previous candle.
* Error: Error in terms of point. Only appears on second or later prediction shown.
* [model_name] model: Rough description about fitted ARIMA model.
* Prediction table, consist of:
  * Candle time/index. Time/index of the forecasted value. First value is currently forming candle. 1 means candle after current candle, 2 means after that, etc.
  * Prediction: Close price prediction from ARIMA.
  * Lower Limit - Upper Limit: 95% Prediction Interval limit. More specifically, Limits are on 2.5% - 97.5% quantile.
* Elapsed time: Time spent on performing and show prediction.


### Online ARIMA fitting
You can also fit an ARIMA model each time a new candle show up by running `core-arima-online.py` instead. The way it's forecast shown is similar with `core-arima-pretrain.py`, but it is slower due to parameter tuning.

### Stopping the program
Click on your terminal (the same place where forecasts are shown) and press `Ctrl + C` on your keyboard.

### Logs and Archives ###
Each time you retrieve, repair, or fit an ARIMA model, you will also receive a copy of data/model for archiving. This archives are flagged by `_[recent date]` in their name. Note that `[recent date]` is taken from the date data of latest candle.

Model's performance log can be obtained from `logs` folder. Error on the log is the same as error shown on your terminal.

### Showing models' properties ###
Run `show_models.py` to get models' properties, as parameters, coefficients' p-values, etc. (NOTE: Only models trained on `train_new_model.py` would be checked)


