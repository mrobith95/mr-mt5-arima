from statsmodels.tsa.arima.model import ARIMA
from statsmodels.iolib.smpickle import load_pickle
import pandas as pd

def show_models():

    ## reading files
    namafile = 'input-data.xlsx'
    tabel_pair = pd.read_excel(namafile,'Pair Table')
    simbolset = tabel_pair['simbol'] ## symbol name
    waktuframetemp = tabel_pair['timeframe'] ##timeframe from .xlsx file
    namanyaset = tabel_pair["train data name"] ## model name, following inputs on 'train data name' column on 'Pair Table' sheet
    n_models = len(namanyaset)

    for i in range(n_models):
        simbol = simbolset[i]
        waktuframe = waktuframetemp[i]
        file_path = namanyaset[i]
        model = load_pickle('arimas/'+file_path+'.pkl')

        ## print ARIMA's parameter
        ar_param = model.specification['order'][0]
        df_param = model.specification['order'][1]
        ma_param = model.specification['order'][2]
        tr_param = model.specification['trend']

        if tr_param == 'c':
            cetak_param = f'ARIMA({ar_param},{df_param},{ma_param}) with constant'
        elif tr_param == 't':
            cetak_param = f'ARIMA({ar_param},{df_param},{ma_param}) with trend'
        elif tr_param == 'n':
            cetak_param = f'ARIMA({ar_param},{df_param},{ma_param})'

        print('')
        print('=============')
        print(f'Model summary for {simbol} {waktuframe}: {cetak_param}')
        print('')
        print(model.summary())
        print('')

show_models()