print('loading preparations...')
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import sys
import csv
import os
import pytz
from train_new_model_np import train_model
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.iolib.smpickle import load_pickle
import warnings ## NOTE: This is for suppress WARNING!
from timeit import default_timer as def_timer
from tabulate import tabulate

## To check: arima models trained from here should
## make arimas-online folder and several model with
## time flag

##==========CLASSES===========

## Classes here

##==========END OF CLASSES===========

##==========FUNCTIONS===========

## rounding function for rounding
def repair_number(number, poin, digit, tipe):
    aja = 0
    if tipe == 'floor':
        aja = np.round(np.floor(number/poin)*poin, decimals=digit)
    if tipe == 'ceil':
        aja = np.round(np.ceil(number/poin)*poin, decimals=digit)
    if tipe == 'round':
        aja = np.round(number, decimals=digit)
    
    return aja

## rounding, but for list
def repair_number_mat(matrik, poin, digit, tipe):
    aja = ''
    panjang = len(matrik)
    for a in range(panjang):
        tulis = repair_number(matrik[a], poin, digit, tipe)
        if a == 0:
            aja = aja + str(tulis)
        else:
            aja = aja + ' - ' + str(tulis)
            
    return aja

## for printing on tabulate
def repair_number_tab(matrik, poin, digit, tipe):
    ini_list = []
    panjang = len(matrik)
    for a in range(panjang):
        tulis = repair_number(matrik[a], poin, digit, tipe)
        ini_list.append(tulis)

    return ini_list

## rounding + display for error
def repair_error(number, poin):
    return str(int(np.round(number/poin)))+" point(s)"

## check a model if it is exist
## if not exist, do train
## if exist, do test
def check_file_and_operate(file_path, symbol_name, timeframe):
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
##        # Perform operations on the existing file
##        with open(file_path, 'r') as file:
##            content = file.read()
##            print(f"File contents: {content}")
##        # You can add more operations here
##    else:
##        ## : This part might be not working properly
##        ##     : DO NOT ACCESS THIS PART
##        ## train a new model if it is not exist
##        ## if it is weekend by metatrader, then use latest bar
##        ## otherwise, find latest saturday
##        print(f"The file '{file_path}' does not exist.")
##        # Perform operations for non-existent file
##        sekarang = datetime.now(tz=pytz.timezone("Etc/UTC"))
##        if ~(sekarang.weekday() == 5 or (sekarang.weekday() == 6 and sekarang.hour < 21)):
##            mulaidat = find_previous_saturday(sekarang)
##            mulaidat = datetime(mulaidat.year, mulaidat.month, mulaidat.day, tzinfo=timezone)
####            print(mulaidat)
##            # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
##            rates = mt5.copy_rates_from(symbol_name, timeframe, mulaidat, 1201)
##        else:
##            rates = mt5.copy_rates_from_pos(symbol_name, timeframe, 0, 1201)
##
##        # create DataFrame out of the obtained data
##        rates_frame = pd.DataFrame(rates)
##        # convert time in seconds into the datetime format
##        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
##                                   
####        # display data
####        print("\nDisplay dataframe with data")
####        print(rates_frame)
##
##        ## saving rates_frame as csv
##        ttterbaru = rates_frame['time'][10-1]
##        namanya = symbol_name + str(ttterbaru.year)
##        if len(str(ttterbaru.month)) < 2:
##            namanya = namanya + '0'
##        namanya = namanya + str(ttterbaru.month)
##        if len(str(ttterbaru.day)) < 2:
##            namanya = namanya + '0'
##        namanya = namanya + str(ttterbaru.day)
##        if len(str(ttterbaru.hour)) < 2:
##            namanya = namanya + '0'
##        namanya = namanya + str(ttterbaru.hour)
##        if len(str(ttterbaru.minute)) < 2:
##            namanya = namanya + '0'
##        namanya = namanya + str(ttterbaru.minute)
##        namanya = namanya + '.csv'
##        
##        rates_frame.to_csv(namanya)
##        ## NOTE: ini masih ada "kolom indexing" nya
##
##        ## train model
##        train_model(rates_frame, file_path)
##
####        return rates_frame
##
##        ## NEXT: buat function untuk training. sementara tidak ada tuningnya dlu
##            
####        with open(file_path, 'w') as file:
####            file.write("This is a new file.")
####        print(f"Created a new file: '{file_path}'")

def find_previous_saturday(tanggal):
    # change Timestamp to str
    tanggal_tahun = str(tanggal.year)
    tanggal_bulan = str(tanggal.month)
    if len(tanggal_bulan) < 2:
        tanggal_bulan = '0'+tanggal_bulan
    tanggal_hari  = str(tanggal.day)
    if len(tanggal_hari) < 2:
        tanggal_hari = '0'+tanggal_hari
    tanggal_str   = tanggal_tahun+tanggal_bulan+tanggal_hari 
    
    # Convert the input string to a datetime object
    given_date = datetime.strptime(tanggal_str, "%Y%m%d")
    
    # Calculate the number of days to subtract to get to the previous Saturday
    days_to_subtract = (given_date.weekday() + 2) % 7
    
    # If the given date is a Saturday, we want the previous Saturday
    if days_to_subtract == 0:
        days_to_subtract = 7
    
    # Subtract the calculated number of days
    previous_saturday = given_date - timedelta(days=days_to_subtract)
    
    return previous_saturday

##def train_model(datanya, file_path):
##    ndata = len(datanya)
##    open_np   = datanya['open'].to_numpy()
##    high_np   = datanya['high'].to_numpy()
##    low_np    = datanya['low'].to_numpy()
##    close_np  = datanya['close'].to_numpy()
##    ## data yang lain: time, tick_volume, spread, real_volume
##
##    ## diffing
##    dopen_np = open_np[1:] - open_np[:-1]
##    dhigh_np = high_np[1:] - high_np[:-1]
##    dlow_np = low_np[1:] - low_np[:-1]
##    dclose_np = close_np[1:] - close_np[:-1]
##
##    ## input 12 bars, output 6 bars
##    nrow = ndata - 18
##    Xall = np.zeros((nrow, 12, 1))
##    Yall = np.zeros((nrow,  6, 1)) ## close only
##
##    for i in range(nrow):
##        for j in range(12): ## 12 inputs
##            Xall[i,j,0] = dclose_np[i+j]
##
##        for j in range(6): ## 6 outputs
##            Yall[i,j,0] = dclose_np[i+j+12]
##
##    ## plan B
##    model = pelatih(Xall, Yall)
##    model.save_weights('weights/'+file_path+'/'+file_path)
##
##    ## saving model for record
##    tanggal = datanya['time'][ndata-1]
##    # make new file name
##    tanggal_tahun = str(tanggal.year)
##    tanggal_bulan = str(tanggal.month)
##    if len(tanggal_bulan) < 2:
##        tanggal_bulan = '0'+tanggal_bulan
##    tanggal_hari  = str(tanggal.day)
##    if len(tanggal_hari) < 2:
##        tanggal_hari = '0'+tanggal_hari
##    tanggal_jam   = str(tanggal.hour)
##    if len(tanggal_jam) < 2:
##        tanggal_jam = '0'+tanggal_jam
##    tanggal_menit   = str(tanggal.minute)
##    if len(tanggal_menit) < 2:
##        tanggal_menit = '0'+tanggal_menit
##    tanggal_str   = file_path+tanggal_tahun+tanggal_bulan+tanggal_hari+tanggal_jam+tanggal_menit 
##
##    model.save_weights('weights/'+file_path+'/'+tanggal_str)

##==========END OF FUNCTIONS===========

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
## MT5 market watch timezone is GMT+3

## reading symbols and timeframes to be predicted
namafile = 'input-data.xlsx'
tabel_acc = pd.read_excel(namafile,'Login and Settings')
tabel_pair = pd.read_excel(namafile,'Pair Table')
 
# connect to MetaTrader 5
account=tabel_acc['Acc. Number'][0]
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
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
    print("login successfull!")
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

## determine how many symbol/timeframe pairs
n_pair = len(tabel_pair)

# determine sets
simbolset = tabel_pair['simbol'] ## symbol name
simbolset = simbolset.to_numpy() ## not sure why i convert to numpy.
poinset = [] ## point for each symbol
digitset = [] ## digit for each symbol
waktuframeset = [] ## timeframe used for code's timer
waktuframetemp = tabel_pair['timeframe'] ##timeframe from .xlsx file
namanyaset = tabel_pair["train data name"] ## model name, following inputs on 'train data name' column on 'Pair Table' sheet
for k in range(0,n_pair):
    infosimbol = mt5.symbol_info(simbolset[k]) ## read symbol info
    poinset.append(np.float_power(10,-1*infosimbol.digits)) ## adding point
    digitset.append(infosimbol.digits) ## adding digit
    if waktuframetemp[k] == 'M1': ## adding timeframe
        waktuframeset.append(mt5.TIMEFRAME_M1)  
    elif waktuframetemp[k] == 'M5':
        waktuframeset.append(mt5.TIMEFRAME_M5)
    elif waktuframetemp[k] == 'M15':
        waktuframeset.append(mt5.TIMEFRAME_M15)
    elif waktuframetemp[k] == 'M30':
        waktuframeset.append(mt5.TIMEFRAME_M30)
    elif waktuframetemp[k] == 'H1':
        waktuframeset.append(mt5.TIMEFRAME_H1)
    elif waktuframetemp[k] == 'H4':
        waktuframeset.append(mt5.TIMEFRAME_H4)
    elif waktuframetemp[k] == 'D1':
        waktuframeset.append(mt5.TIMEFRAME_D1)
    elif waktuframetemp[k] == 'W1':
        waktuframeset.append(mt5.TIMEFRAME_W1)
    elif waktuframetemp[k] == 'MN':
        waktuframeset.append(mt5.TIMEFRAME_MN)
    else:
        print('Timeframe only receive standard MT5 timeframe. Timeframe settings become MN') 
        waktuframeset.append(mt5.TIMEFRAME_MN)

##ambildata = 1000 ## number of candles to consider. Might useful later
saatini = [] ## time of latest candle
namanama = [] ## name of records
namamodel = [] ## name of models
##datas = [] ## data for recording model performance

## numpy arrays for memory
pred = np.zeros((n_pair, 5))
lowerl = np.zeros((n_pair, 5))
upperl = np.zeros((n_pair, 5))
galat = np.zeros((n_pair))

## determine the date this code was run, also for naming performance records
now = datetime.now()
dt_string = now.strftime("%Y%m%d%H%M%S")

## check if logs folder exist, then make it if it is not
if not os.path.isdir('logs'):
    os.makedirs('logs')

warnings.filterwarnings('ignore') ## NOTE: This will suppress ANY WARNING!

for k in range(0,n_pair):
    simbol = simbolset[k] #get symbol
    waktuframe = waktuframeset[k] ## get timeframe
    infosimbol = mt5.symbol_info(simbol) ## read symbol's info
    poin = np.float_power(10,-1*infosimbol.digits) ## get numbers behind decimal

## get recent finished candle, and save it's time
    timer_rates = mt5.copy_rates_from_pos(simbol, waktuframe, 0, 2) 
    timer_frame = pd.DataFrame(timer_rates)
    timer_frame['time']=pd.to_datetime(timer_frame['time'], unit='s')
    saatini.append(timer_frame["time"][1])
    
    namanama.append(namanyaset[k]+'_record_'+dt_string+'.csv') ## performance record file name
    namamodel.append(namanyaset[k]) ## model name 
    
##  write csv of record
##    datas.append([])
##    datas[k].append(["Timestamp", "prediction", "close"])
    with open('logs/'+namanama[k], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Prediction", "Actual", "2.5% Quant", "97.5% Quant",
                         "Prediction 2", "Prediction 3", "Prediction 4", "Prediction 5",
                         "2.5% Quant 2", "2.5% Quant 3", "2.5% Quant 4", "2.5% Quant 5",
                         "97.5% Quant 2", "97.5% Quant 3", "97.5% Quant 4", "97.5% Quant 5"])

##  as far as I remember, this is for pretrain model. Would be leave like that for now
    file_path = namamodel[k]
    check_file_and_operate(file_path, simbol, waktuframe)

print("Ready to Predict!") ## no hello :(

while True: ## need better command than while maybe
    for k in range(0,n_pair): # for each pair/timeframe combo
        
        ## prepare data
        simbol = simbolset[k] #get symbol
        infosimbol = mt5.symbol_info(simbol) ## read symbol's info
        poin = np.float_power(10,-1*infosimbol.digits) ## get numbers behind decimal
        waktuframe = waktuframeset[k] ## get timeframe
        file_path = namamodel[k] ## get model name
        
        ## get candles, for timer
        timer_rates  = mt5.copy_rates_from_pos(simbol, waktuframe, 0, 2)
        timer_frame = pd.DataFrame(timer_rates)
        timer_frame['time']=pd.to_datetime(timer_frame['time'], unit='s')
        
        ## check if new candle just finished
        if timer_frame.iloc[-1]["time"] != saatini[k]:
            saatini[k] = timer_frame.iloc[-1]["time"] # renew timer
            prevtime = timer_frame.iloc[-2]["time"] # time to be logged
            print("================================")
            print("Time       :", saatini[k])

            ## Get data for ARIMA, just 40 latest candle
            eurgbp_rates = mt5.copy_rates_from_pos(simbol, waktuframe, 0, 40)

            ## the above rates give "untabulated" value, unsuitable to read. Use pandas for this purpose.
            # create DataFrame out of the obtained data
            rates_frame = pd.DataFrame(eurgbp_rates)

            # convert time in seconds into the datetime format
            rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

            ## logging training data
            ## prepare string for file name
            tanggal = rates_frame['time'][40-1]
            namadate = str(tanggal.year)
            if len(str(tanggal.month)) < 2:
                namadate = namadate+'0'
            namadate = namadate+str(tanggal.month)
            if len(str(tanggal.day)) < 2:
                namadate = namadate+'0'
            namadate = namadate+str(tanggal.day)
            if len(str(tanggal.hour)) < 2:
                namadate = namadate+'0'
            namadate = namadate+str(tanggal.hour)
            if len(str(tanggal.minute)) < 2:
                namadate = namadate+'0'
            namadate = namadate+str(tanggal.minute)
            rates_frame.to_csv('training data/'+file_path+'_'+namadate+'.csv', index=False)
                         
            ##  ##these line might be important in the future       
            #### remove real_volume since always zeros for forex(?)
            ##rates_frame.drop(columns=['real_volume'], inplace=True)
            ##
            #### also remove any na columns        
            ##rates_frame.dropna(inplace=True)
            ##print(rates_frame)

            # make numpy array since the model was train on numpy
            open_np   = rates_frame['open'].to_numpy()
            high_np   = rates_frame['high'].to_numpy()
            low_np    = rates_frame['low'].to_numpy()
            close_np  = rates_frame['close'].to_numpy()
            dclose_np = close_np[1:] - close_np[:-1]
            
            adadata = open_np.shape[0] # number of data

            print("Symbol     :", simbol)
            ## if a prediction was performed, do comparison with actual and log it
            ## NOTE: error computation only on the most recent data
            if pred[k,0] > 0:
                galat[k] = np.abs(pred[k,0] - close_np[39])
##                datas[k].append([saatini[k], pred[k,0], close_np[39]])
                t1 = repair_number(pred[k,0], poinset[k], digitset[k], "round")
                t2 = repair_number(close_np[38], poinset[k], digitset[k], "round")
                t3 = repair_number(lowerl[k,0], poinset[k], digitset[k], "ceil")
                t4 = repair_number(upperl[k,0], poinset[k], digitset[k], "floor")
                t12 = repair_number(pred[k,1], poinset[k], digitset[k], "round")
                t13 = repair_number(pred[k,2], poinset[k], digitset[k], "round")
                t14 = repair_number(pred[k,3], poinset[k], digitset[k], "round")
                t15 = repair_number(pred[k,4], poinset[k], digitset[k], "round")
                t22 = repair_number(lowerl[k,1], poinset[k], digitset[k], "ceil")
                t23 = repair_number(lowerl[k,2], poinset[k], digitset[k], "ceil")
                t24 = repair_number(lowerl[k,3], poinset[k], digitset[k], "ceil")
                t25 = repair_number(lowerl[k,4], poinset[k], digitset[k], "ceil")
                t32 = repair_number(upperl[k,1], poinset[k], digitset[k], "floor")
                t33 = repair_number(upperl[k,2], poinset[k], digitset[k], "floor")
                t34 = repair_number(upperl[k,3], poinset[k], digitset[k], "floor")
                t35 = repair_number(upperl[k,4], poinset[k], digitset[k], "floor")
                with open('logs/'+namanama[k], 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([prevtime, t1, t2, t3, t4,
                                     t12, t13, t14, t15,
                                     t22, t23, t24, t25,
                                     t32, t33, t34, t35])
                
                print("Prev. Act. : "+str(t2))
                print("Error      : "+repair_error(galat[k], poinset[k]))

            ## train new model
            start_timer = def_timer() ## start timer
            model = train_model(close_np[:39], file_path)

            ## predict
            hasil_fore = model.get_forecast(steps = 5)   
            pred[k,:]  = hasil_fore.predicted_mean ## mean
            lowerl[k,:] = hasil_fore.conf_int(alpha = 0.05)[:,0] ## lower limit
            upperl[k,:] = hasil_fore.conf_int(alpha = 0.05)[:,1] ## upper limit
            end_timer = def_timer() ## end timer

            ## print ARIMA's parameter
            ar_param = model.specification['order'][0]
            df_param = model.specification['order'][1]
            ma_param = model.specification['order'][2]
            tr_param = model.specification['trend']

            if tr_param == 'c':
                cetak_param = f'best fit: ARIMA({ar_param},{df_param},{ma_param}) with constant'
            elif tr_param == 't':
                cetak_param = f'best fit: ARIMA({ar_param},{df_param},{ma_param}) with trend'
            elif tr_param == 'n':
                cetak_param = f'best fit: ARIMA({ar_param},{df_param},{ma_param})'

            print(file_path+' '+cetak_param)
            
##          # printing stuff
            ini_dict = {
                "Candle": [saatini[k], "1", "2", "3", "4"],
                "Lower Limit": repair_number_tab(lowerl[k,:], poinset[k], digitset[k], 'ceil'),
                "Prediction":  repair_number_tab(pred[k,:], poinset[k], digitset[k], 'round'),
                "Upper Limit": repair_number_tab(upperl[k,:], poinset[k], digitset[k], 'floor')
            }
            print(tabulate(ini_dict,
               headers=ini_dict.keys(),
               tablefmt = 'outline'))
            print(f"Elapsed time: {(end_timer - start_timer):.2f} sec")
##

