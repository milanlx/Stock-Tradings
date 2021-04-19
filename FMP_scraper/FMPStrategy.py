from Utils.FMPUtils import *
from utils import loadFromPickle, saveAsPickle
import json


# global variable
api_key = "1845e3929e19329d2be580fc65e1970d"
selected_keys = ["symbol", "price", "mktCap", "range", "description", "industry",
                 "sector", "country", "state", "city", "ipoDate"]


### test

# load from pickle
available_symbols = loadFromPickle("./Processed_Data/fmp_available_symbols.pickle")
available_symbols_list = []
for item in available_symbols:
    symbol = item["symbol"]
    available_symbols_list.append(symbol)


# get stock ticker list
ticker_file_path = "Files/Description/industrials_aerospace_and_defense.txt"
stock_ticker_list = []
with open(ticker_file_path, "r") as f:
    for line in f:
        ticker = str(line.strip())
        #if "#" not in ticker:
        #    stock_ticker_list.append(ticker)
        if ticker in available_symbols_list:
            stock_ticker_list.append(ticker)
        else:
            print("not in list:: " + ticker)

sector = ticker_file_path.split("/")[2].split(".")[0]
file_path = "./Processed_Data/"+sector+".csv"
#stock_ticker_list = ["DT", "FB", "SMAR", "WORK"]
summary_list = get_stock_summary_list(api_key, stock_ticker_list, selected_keys)
for summary in summary_list:
    print(summary)

# write to csv
write_summary_to_csv(file_path, selected_keys, summary_list)
