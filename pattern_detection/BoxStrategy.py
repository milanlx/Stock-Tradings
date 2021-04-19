import numpy as np
from utils import *
import glob
from Patterns import *


"""
    - find the "1,2,3,4" patterns of breaking out of box
"""

# part I: load data
watchlist_path = "./Files/watchlist.txt"
startDate = "2020-06-01"
endDate = "2020-12-04"
folder_path = "./Data/yahoo/"
#watchlist = downloadFromYahoo(watchlist_path, startDate, endDate)
#saveYahooFiles(watchlist, folder_path)


# part II: scan for pattern
file_paths = glob.glob(folder_path+"*.pickle")

for file_path in file_paths:
    ticker = file_path.split('\\')[1].split('.')[0]
    data = loadFromPickle(file_path)
    date_str, daily_high, daily_low = extractData(data)
    signals = boxPattern(daily_high, daily_low)
    if len(signals) > 0:
        print(ticker)
        for signal in signals:
            date = [date_str[idx] for idx in signal[0]]
            print(date)
            print(np.around(signal[1], decimals=2))
