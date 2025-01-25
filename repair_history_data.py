print('loading preparations...')
import pandas as pd
##import numpy as np
##import pytz
from datetime import datetime
from timeit import default_timer as timer

'''
This code is used to repair csv obtained from MT5's History Center
(Symbol -> Bars in MT5)
and make it suitable for the code
'''
start_timer = timer()
## reading files
namafile = 'input-data.xlsx'
##tabel_acc = pd.read_excel(namafile,'Login and Settings')
tabel_pair = pd.read_excel(namafile,'Pair Table')

n_pair = len(tabel_pair) ## get numebr of pairs
nama_data = tabel_pair['train data name'] ## get training data name
timeframe = tabel_pair['timeframe']
print('preparation complete! now reading and repair data...')

## for each pair...
for kk in range(n_pair):

    ## define the file name to repair
    namanya = nama_data[kk] 

    ## read data.
    data = pd.read_csv('training data/'+namanya+'.csv', sep='\t')
    n_data = len(data) ## amount of data/bars

    ## important note
    ## date, time are str
    ## OHLC are np.float64
    ## tickvol, vol, spread are np.int64

    ## variables for dict
    out_datetime = [None]*n_data

    ## for date-time, exract data first, then make datetime object based on them
    ## NOTE: might be considering timezone, thus pytz exist

    ## if the data is daily, monthly, or weekly
    if timeframe[kk] == 'D1' or timeframe[kk] == 'W1' or timeframe[kk] == 'MN':
        col_date = data['<DATE>']

        ## for each data...
        for i in range(n_data):
            ## obtain data
            used_date = col_date[i]

            ## extract data
            used_year   = int(used_date[:4]) ## year
            used_month  = int(used_date[5:7]) ## month
            used_day    = int(used_date[8:]) ## day
            used_hour   = 0 ## hour
            used_minute = 0 ## minute

            ## create datetime
            tanggal = datetime(year = used_year,
                            month = used_month,
                            day = used_day,
                            hour = used_hour,
                            minute = used_minute)
            
            ##add this datetime to out_datetime
            out_datetime[i] = tanggal

    else: # otherwise, just add time column from the data
        col_date = data['<DATE>']
        col_time = data['<TIME>']

        ## for each data...
        for i in range(n_data):
            ## obtain data
            used_date = col_date[i]
            used_time = col_time[i]

            ## extract data
            used_year   = int(used_date[:4]) ## year
            used_month  = int(used_date[5:7]) ## month
            used_day    = int(used_date[8:]) ## day
            used_hour   = int(used_time[:2]) ## hour
            used_minute = int(used_time[3:5]) ## minute

            ## create datetime
            tanggal = datetime(year = used_year,
                            month = used_month,
                            day = used_day,
                            hour = used_hour,
                            minute = used_minute)
            
            ##add this datetime to out_datetime
            out_datetime[i] = tanggal        

    ## create output dict
    out_dict = {'time': out_datetime,
                'open': data['<OPEN>'],
                'high': data['<HIGH>'],
                'low': data['<LOW>'],
                'close': data['<CLOSE>'],
                'tick_volume': data['<TICKVOL>'],
                'spread': data['<SPREAD>'],
                'volume': data['<VOL>']}

    ## make pandas dataframe
    out_pd = pd.DataFrame.from_dict(out_dict)

    ## save it to csv
    out_pd.to_csv('training data/'+namanya+'.csv', index=False)

    ## this part for archiving
    ## prepare string for file name
    tanggal = out_pd['time'][n_data-1]
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
    out_pd.to_csv('training data/'+namanya+'_'+namadate+'.csv', index=False)

    print(f'repair {namanya+".csv"} done') # printing

end_timer = timer()
print('repair history data done')
print(f'Time elapsed: {(end_timer - start_timer):.2f} sec')
print('')
