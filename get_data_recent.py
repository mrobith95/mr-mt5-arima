print('loading preparations...')
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import pytz
from datetime import datetime, timedelta

# --- FUNCTIONS ---
def isNaN(x):
    return x != x
# --- End of FUNCTIONS ---

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
## MT5 market watch timezone is GMT+3

## reading files
namafile = 'input-data.xlsx'
tabel_acc = pd.read_excel(namafile,'Login and Settings')
tabel_pair = pd.read_excel(namafile,'Pair Table')
print('preparation complete! Initialize and login to MT5...')
 
# connect to MetaTrader 5
account=tabel_acc['Acc. Number'][0]
if not mt5.initialize():
    print("mt5.initialize() failed, error code =",mt5.last_error())
    mt5.shutdown()
    quit()
 
### request connection status and parameters
##print(mt5.terminal_info())
##print(" ")
### get data on MetaTrader 5 version
##print(mt5.version())
##print(" ")

# now connect to trading account specifying the password and server
authorized=mt5.login(int(account),password=tabel_acc['Password'][0], server=tabel_acc['Server'][0])
if authorized:
    print("login successfull! Reading data available on MT5...")
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

## determine how many symbol/timeframe combo
n_pair = len(tabel_pair)

for k in range(n_pair): ## for each pair...
    simbol = tabel_pair['simbol'][k]  ## obtain symbol name
    ## choose timeframe
    if tabel_pair['timeframe'][k] == 'M1': ## adding timeframe
        waktuframe=mt5.TIMEFRAME_M1
    elif tabel_pair['timeframe'][k] == 'M5':
        waktuframe=mt5.TIMEFRAME_M5
    elif tabel_pair['timeframe'][k] == 'M15':
        waktuframe=mt5.TIMEFRAME_M15
    elif tabel_pair['timeframe'][k] == 'M30':
        waktuframe=mt5.TIMEFRAME_M30
    elif tabel_pair['timeframe'][k] == 'H1':
        waktuframe=mt5.TIMEFRAME_H1
    elif tabel_pair['timeframe'][k] == 'H4':
        waktuframe=mt5.TIMEFRAME_H4
    elif tabel_pair['timeframe'][k] == 'D1':
        waktuframe=mt5.TIMEFRAME_D1
    elif tabel_pair['timeframe'][k] == 'W1':
        waktuframe=mt5.TIMEFRAME_W1
    elif tabel_pair['timeframe'][k] == 'MN':
        waktuframe=mt5.TIMEFRAME_MN1
    else:
        print('Timeframe only receive standard MT5 timeframe. Timeframe settings become D1') 
        waktuframe=mt5.TIMEFRAME_D1

    # Now we ready to get new data

    ## if starting date is not specified...
    if isNaN(tabel_pair['starting date'][k]):
        ## Get data for ARIMA, just 40 latest candle
        eurgbp_rates = mt5.copy_rates_from_pos(simbol, waktuframe, 0, 40)
    else: ## otherwise
        ## check if date is valid, a.k.a 8 char long after become str
        start_date_str = str(int(tabel_pair['starting date'][k]))

        if len(start_date_str) == 8: ## if valid...
            ## extract date data
            start_date_year  = int(start_date_str[:4])
            start_date_month = int(start_date_str[4:6])
            start_date_day   = int(start_date_str[6:])

            ## add 1 month (31 days) if timeframe is MN
            if waktuframe==mt5.TIMEFRAME_MN1:
                diff_time = timedelta(days=31)
            ## add 1 week for W1
            elif waktuframe==mt5.TIMEFRAME_W1:
                diff_time = timedelta(weeks=1)
            else: ## add 1 day otherwise
                diff_time = timedelta(days=1)
            
            ## modify starting date
            start_date_entry = datetime(start_date_year, start_date_month, start_date_day,
                                        tzinfo = timezone)
            start_date_entry = start_date_entry + diff_time

            ## then take data
            eurgbp_rates = mt5.copy_rates_from(simbol, waktuframe, start_date_entry, 40)

        else: ## otherwise...
            print('Starting date invalid, must in yyyymmdd. Now taking recent data')
            eurgbp_rates = mt5.copy_rates_from_pos(simbol, waktuframe, 0, 40)

    ## the above rates give "untabulated" value, unsuitable to read. Use pandas for this purpose.
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(eurgbp_rates)

    # convert time in seconds into the datetime format
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    ##these line might be important in the future       
    #### remove real_volume since always zeros for forex(?)
    ##rates_frame.drop(columns=['real_volume'], inplace=True)
    ##
    #### also remove any na columns        
    ##rates_frame.dropna(inplace=True)
    ##print(rates_frame)

    # ## the rest of this code is simply for saving the csv
    ## save file into csv
    rates_frame.to_csv(tabel_pair['train data name'][k]+'.csv', index=False)

    # ## this part was used for auto-naming csv. Would be deleted in the future
    # ## prepare name of the symbol and timeframe 
    # namanya = simbol
    # if waktuframe == mt5.TIMEFRAME_M1:
    #     namanya = namanya+'_M1'
    # elif waktuframe == mt5.TIMEFRAME_M5:
    #     namanya = namanya+'_M5'
    # elif waktuframe == mt5.TIMEFRAME_M15:
    #     namanya = namanya+'_M15'
    # elif waktuframe == mt5.TIMEFRAME_M30:
    #     namanya = namanya+'_M30'
    # elif waktuframe == mt5.TIMEFRAME_H1:
    #     namanya = namanya+'_H1'
    # elif waktuframe == mt5.TIMEFRAME_H4:
    #     namanya = namanya+'_H4'
    # elif waktuframe == mt5.TIMEFRAME_D1:
    #     namanya = namanya+'_D1'
    # elif waktuframe == mt5.TIMEFRAME_W1:
    #     namanya = namanya+'_W1'
    # elif waktuframe == mt5.TIMEFRAME_MN1:
    #     namanya = namanya+'_MN1'
    # else:
    #     namanya = namanya+'_UNKNOWN'

    # ## prepare string for file name
    # tanggal = rates_frame['time'][40-1]
    # namadate = str(tanggal.year)
    # if len(str(tanggal.month)) < 2:
    #     namadate = namadate+'0'
    # namadate = namadate+str(tanggal.month)
    # if len(str(tanggal.day)) < 2:
    #     namadate = namadate+'0'
    # namadate = namadate+str(tanggal.day)
    # if len(str(tanggal.hour)) < 2:
    #     namadate = namadate+'0'
    # namadate = namadate+str(tanggal.hour)
    # if len(str(tanggal.minute)) < 2:
    #     namadate = namadate+'0'
    # namadate = namadate+str(tanggal.minute)

    print(f'saving {tabel_pair["train data name"][k]+".csv"} done') # printing

print('get recent data done')
print('')
