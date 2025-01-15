print('loading preparations...')
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.iolib.smpickle import save_pickle
import os

## this code is to fit ARIMA for core-arima-pretrain
## models are saved in arimas/ folder.
## 2 models are saved each run: model to be applied for core-arima, and
## a copy for that model for archiving

## function for kpss test
## if kpss p-val < 0.05, not stationary
def kpss_test(timeseries):
##    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
##    print(kpss_output)
    return(kpsstest[1:3])

#function for adf test
## if adf p-val > 0.05, not stationary
def adf_test(timeseries):
##    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ],
    )
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
##    print(dfoutput)
    return(dftest[1:3])

def train_model(datanya, file_path):
    ndata = len(datanya)
    open_np   = datanya['open'].to_numpy()
    high_np   = datanya['high'].to_numpy()
    low_np    = datanya['low'].to_numpy()
    close_np  = datanya['close'].to_numpy()
##    another data might be numpied here: time, tick_volume, spread, real_volume

##    stationary test first (kpss only for now)
    useddf = close_np
    kpssres = kpss_test(useddf)
##    adfres  = adf_test(useddf)
##    print('///')
    diffing = 0
    while kpssres[0] < 0.05:
        diffing = diffing + 1
##        print('Non-stationary detected, differencing...')
        useddf = useddf[1:] - useddf[:-1]
##        print('///')
        kpssres = kpss_test(useddf)
##        adfres  = adf_test(useddf)
##        print('///')

##        if kpssres[0] >= 0.05:
##            print('Data is stationary')
##            print(diffing)
##            break
##    
    
    ## look for best ARIMA params. Algorithm roughly based on Hyndman & Khandakar, 2008
    ## DOI 10.18637/jss.v027.i03    
    useddf = close_np
    record = np.inf

    if diffing >= 2:
        ptable = [0, 2, 1, 0]
        qtable = [0, 2, 0, 1]
        ttable = ['n', 'n', 'n', 'n']
    elif diffing == 1:
        ptable = [0, 2, 1, 0, 0]
        qtable = [0, 2, 0, 1, 0]
        ttable = ['t', 't', 't', 't', 'n']
    else:
        ptable = [0, 2, 1, 0, 0]
        qtable = [0, 2, 0, 1, 0]
        ttable = ['c', 'c', 'c', 'c', 'n']
        
    for k in range(len(ptable)):
        mod = ARIMA(useddf, order=(ptable[k], diffing, qtable[k]), trend=ttable[k])
        res = mod.fit()

        if res.aic < record:
            record = res.aic ## aic
            parima = ptable[k]
            qarima = qtable[k]
            tarima = ttable[k]

    newbest = True ## to initiate seacrh process

    while newbest:
        newbest = False ## always assume we have to stop search (since no better aic found)
        ## determine the set of search range
        if parima == 0:
            ptable = [0,1]
        else:
            ptable = [parima-1, parima, parima+1]

        if qarima == 0:
            qtable = [0,1]
        else:
            qtable = [qarima-1, qarima, qarima+1]

        if diffing >= 2:
            ttable = 'n' ## what is the symbol for quadratic???
        elif diffing == 1:
            ttable = ['t', 'n']
        else:
            ttable = ['c', 'n']

##        test all possible search candidates     
        for i in ptable:
            for j in qtable:
                for k in ttable:
##                    print(i, " ", j, " ", k)
                    mod = ARIMA(useddf, order=(i, diffing, j), trend=k)
                    res = mod.fit()
                    if res.aic < record:
                        newbest = True
                        record = res.aic ## aic
                        parima = i
                        qarima = j
                        tarima = k

    ## fit ARIMA model with the best param
    finmod = ARIMA(useddf, order=(parima, diffing, qarima), trend=tarima)
    fitted = finmod.fit() ## fitted is the best model
    ## print(fitted.summary()) ## print summary if needed

    ## check if arimas folder exist, then make it if it is not
    if not os.path.isdir('arimas'):
        os.makedirs('arimas')

    ## save the model
    save_pickle(fitted, 'arimas/'+file_path+'.pkl')

    ## saving model for archving
    tanggal = datanya['time'][ndata-1]

    ## tanggal is a string, so if the string's length is more than 10, then it is YYYY-mm-dd HH:MM:SS format
    if len(tanggal) > 10:
        tanggal = datetime.strptime(tanggal, '%Y-%m-%d %H:%M:%S')
    else: # else, it is a YYYY-mm-dd format
        tanggal = datetime.strptime(tanggal, '%Y-%m-%d')

    # make new file name
    tanggal_tahun = str(tanggal.year)
    tanggal_bulan = str(tanggal.month)
    if len(tanggal_bulan) < 2:
        tanggal_bulan = '0'+tanggal_bulan
    tanggal_hari  = str(tanggal.day)
    if len(tanggal_hari) < 2:
        tanggal_hari = '0'+tanggal_hari
    tanggal_jam   = str(tanggal.hour)
    if len(tanggal_jam) < 2:
        tanggal_jam = '0'+tanggal_jam
    tanggal_menit   = str(tanggal.minute)
    if len(tanggal_menit) < 2:
        tanggal_menit = '0'+tanggal_menit
    tanggal_str   = file_path+'_'+tanggal_tahun+tanggal_bulan+tanggal_hari+tanggal_jam+tanggal_menit 
    save_pickle(fitted, 'arimas/'+tanggal_str+'.pkl')
    
    return fitted ## return fitted model

## script to train model

## read excel first
namafile = 'input-data.xlsx'
tabel_acc = pd.read_excel(namafile,'Login and Settings')
tabel_pair = pd.read_excel(namafile,'Pair Table')

## determine how many symbol/timeframe combo
n_pair = len(tabel_pair)
print('preparation complete! now training ARIMAs...')

for i in range(n_pair):
    namanya = tabel_pair["train data name"][i]
    considered = pd.read_csv(namanya+".csv")
    model = train_model(considered, namanya)

    print(f'{namanya} has fitted')

print('All data has fitted')
