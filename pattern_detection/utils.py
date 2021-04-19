import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import pickle
import glob


"""data loader"""
def loadFile(filePath, source):
    # local data that are manually downloaded
    # header (kaggle): Date,Open,High,Low,Close,Volume,OpenInt
    # header (yahoo): Date, Open, High, Low, Close, Adjusted close, Volume
    dates, opens, highs, lows, closes, volumes = [], [], [], [], [], []
    with open(filePath) as f:
        # skip header
        next(f)
        for line in f:
            data = line.strip().split(',')
            dates.append(data[0])
            opens.append(data[1])
            highs.append(data[2])
            lows.append(data[3])
            if source == "kaggle":
                closes.append(data[4])
                volumes.append(data[5])
            elif source == "yahoo":
                closes.append(data[5])
                volumes.append(data[6])
    return [dates, opens, highs, lows, closes, volumes]


"""use yahoo API to download data"""
def downloadFromYahoo(watchlist_path, startDate, endDate, interval='1d'):
    """
    - the columns: Open, High, Low, Close, Adj Close, Volume
        - date is used as index
    :param watchlist_path: path of the txt file containing stock tickers
    :param startDate: "2020-01-01"
    :param endDate: "2020-12-03"
    :param interval: time interval, string
    :return: a dict of df for each ticker, with ticker as key
    """
    watchlist = {}
    with open(watchlist_path) as f:
        for line in f:
            ticker = line.strip().upper()
            ticker_df = yf.download(ticker, start=startDate, end=endDate,
                                    interval=interval, progress=False)
            watchlist[ticker] = ticker_df
    return watchlist


"""save each dataframe to pickle"""
def saveYahooFiles(watchlist, folder_path):
    for key in watchlist.keys():
        pickle_file = folder_path + key + '.pickle'
        saveAsPickle(watchlist[key], pickle_file)
    return 0


"""extract date (str), High, Low from dt format"""
def extractData(dt):
    # dt: DataFrame
    date = dt.index.values
    date_str = [item.astype(str)[0:10] for item in date]
    daily_high = dt['High'].values
    daily_low = dt['Low'].values
    return date_str, daily_high, daily_low


"""final local maximum/minimum"""
def findLocalExtreme(locArr, data, tp):
    # data: one dimensional np array
    # tp: max, min, default (both max and min)
    # return x,y coordinate of local max/min
    # very few overlapping of max/min on the same day
    n = len(locArr)
    idArr = np.zeros(n)
    for i, item in enumerate(locArr):
        if i==0 or i==n-1:
            continue
        if data[i]>=data[i-1] and data[i]>=data[i+1]:
            if tp == "max" or tp == "default":
                idArr[i] = 1
        if data[i]<=data[i-1] and data[i]<=data[i+1]:
            if tp == "min" or tp == "default":
                idArr[i] = 1
    return locArr[idArr==1], data[idArr==1]


"""find 1,2,3,4 signal, the box pattern"""
def findBoxPatterns(loc_mins, mins, loc_maxs, maxs):
    """
    three max, two low; or three max, three lows
    :return: list of all found signals [locs, values]
    """
    signals = []
    n_min, n_max = len(loc_mins), len(loc_maxs)
    idx_min, idx_max = 0, 0
    while idx_max < n_max:
        signal, idx_next = findConsecutiveMax(idx_max, loc_maxs, maxs)
        # if found, add to list, and start from next max
        if len(signal[0]) == 3:
            signals.append(signal)
            idx_max = idx_next
        # if not found, start from next max
        else:
            idx_max += 1
        #print(signal)
    return signals


"""helper function for findBoxPatterns"""
def findConsecutiveMax(idx_maxs, loc_maxs, maxs):
    signal = [[loc_maxs[idx_maxs]], [maxs[idx_maxs]]]
    count_max = 1
    while count_max < 3:
        idx, loc, maxv = findNextMax(idx_maxs, loc_maxs, maxs)
        if idx != -1:
            signal[0].append(loc), signal[1].append(maxv)
            # update index
            idx_maxs = idx
            count_max += 1
        else:
            break
    return signal, idx_maxs


"""helper function for findBoxPatterns"""
def findNextMax(idx_max, loc_max, maxs):
    cur_max = idx_max + 1
    while cur_max < len(maxs):
        delta_T = loc_max[cur_max] - loc_max[idx_max]
        delta_S = np.abs(maxs[cur_max] - maxs[idx_max])
        if 5 <= delta_T <= 20 and delta_S <= 0.05*maxs[idx_max]:
            return [cur_max, loc_max[cur_max], maxs[cur_max]]
        else:
            cur_max += 1
    return [-1, -1, -1]


# -------------------------------------------------------------------
# ---- ARK related

"""read from ARk log csv"""
def readFromARK(filePath):
    # build two dict, one for buy, one for sell
    # key: stock ticker; value: date
    # TODOLIST: specify data range
    date_format = "%m/%d/%Y"
    buy_dict = {}
    sell_dict = {}

    with open(filePath, "rb") as f:
        for line in f:
            line = line.decode('utf8').strip()
            items = line.split(',')
            if len(items) == 8:
                try:
                    d = dt.datetime.strptime(items[0], date_format)
                    # convert date format to "yyyy-mm-dd"
                    date, action, ticker = convertDateStr(items[0]), items[1], items[2]
                    if action == "Buy":
                        if ticker in buy_dict.keys():
                            # check if duplicate
                            if date not in buy_dict[ticker]:
                                buy_dict[ticker].append(date)
                        else:
                            buy_dict[ticker] = []
                            buy_dict[ticker].append(date)
                    else:
                        if ticker in sell_dict.keys():
                            # check if duplicate
                            if date not in sell_dict[ticker]:
                                sell_dict[ticker].append(date)
                        else:
                            sell_dict[ticker] = []
                            sell_dict[ticker].append(date)
                except ValueError:
                    print("skip this line:: " + line)
    f.close()
    return buy_dict, sell_dict


"""read in daily ARK transactions from excel file"""
def dailyReadFromArk(folder_path, date):
    # date format: "yyyy-mm-dd"
    # columns: FUND, Date, Direction, Ticker, CUSIP, Name, Shares, % of ETF
    # returns: buy and sell dict: key -> Ticker; value -> Shares
    y, m, d = date.split("-")
    date_str = "".join([m,d,y])
    files = glob.glob(folder_path+"*.csv")
    for file in files:
        if date_str in file:
            print("ARk transaction found on " + date)
            # do not read stock with more than 4 letters, i.e., foreign stocks
            daily_buy_dict, daily_sell_dict = readArkCSV(file)
    return daily_buy_dict, daily_sell_dict


"""helper function: read single csv file of ARK daily transactions"""
def readArkCSV(file_path):
    buy_dict = {}
    sell_dict = {}
    with open(file_path, 'r') as f:
        # skip headers
        for _ in range(8):
            next(f)
        for line in f:
            content = line.strip().split(',')
            ticker, direction, shares = content[3], content[2], content[6]
            if len(ticker) <= 4:
                if direction == "Buy":
                    if ticker not in buy_dict.keys():
                        buy_dict[ticker] = shares
                    else:
                        buy_dict[ticker] += shares
                elif direction == "Sell":
                    if ticker not in sell_dict.keys():
                        sell_dict[ticker] = shares
                    else:
                        sell_dict[ticker] += shares
    return buy_dict, sell_dict


"""update the profile from daily ARK transaction log"""
def updateArkTransactions():
    pass

def convertDateStr(dateStr):
    # convert "mm/dd/yyyy" to "yyyy-mm-dd"
    m, d, y = dateStr.split('/')
    # append 0 if single digit in month and d
    if len(m) == 1:
        m = '0' + m
    if len(d) == 1:
        d = '0' + d
    return '-'.join([y, m, d])


def saveAsPickle(obj, pickle_file):
    with open(pickle_file, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()


def loadFromPickle(pickle_file):
    with open(pickle_file, 'rb') as handle:
        unserialized_obj = pickle.load(handle)
    handle.close()
    return unserialized_obj



"""data visualization"""
def visualization(data):
    pass