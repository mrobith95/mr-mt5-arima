from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.iolib.smpickle import save_pickle
import os
import warnings ## NOTE: This is for suppress WARNING!

## this code is to fit ARIMA for core-arima-online
## models are saved in arimas-online/ folder.
## 1 model are saved each run, mainly for archiving

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
##  considered data here is already a numpy array, so no need to use .to_numpy()
    ndata = len(datanya)
    close_np  = datanya

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
##    print(fitted.summary())

    ## check if arimas folder exist, then make it if it is not
    if not os.path.isdir('arimas-online'):
        os.makedirs('arimas-online')

    ## save the model
    save_pickle(fitted, 'arimas-online/'+file_path+'.pkl')
    
    return fitted
