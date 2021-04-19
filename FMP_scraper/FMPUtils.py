from urllib.request import urlopen
import json
import csv
import pickle
from utils import saveAsPickle

# -------- main -------- #

def get_stock_summary(api_key, stock_ticker, selected_keys):
    """ quote stock summary
    """
    url_str = "https://financialmodelingprep.com/api/v3/profile/" + stock_ticker + \
              "?apikey=" + api_key
    response = urlopen(url_str)
    data = response.read().decode("utf-8")
    full_dict = json.loads(data)[0]
    selected_dict = dict((k, full_dict[k]) for k in selected_keys if k in full_dict)
    return selected_dict


def get_stock_summary_list(api_key, stock_ticker_list, selected_keys):
    """ quote a list of stock being queried
    """
    summary_list = []
    for stock_ticker in stock_ticker_list:
        selected_dict = get_stock_summary(api_key, stock_ticker, selected_keys)
        summary_list.append(selected_dict)
    return summary_list


def get_earnings_calendar(api_key, start_date, end_date):
    """
    - format of date: YYYY-MM-DD
    - only for premium member
    """
    url_str = "https://financialmodelingprep.com/api/v3/earning_calendar?" + "from=" + \
              start_date + "&to=" + end_date + "&apikey=" + api_key
    response = urlopen(url_str)
    data = response.read().decode("utf-8")
    full_dict = json.loads(data)[0]
    return full_dict


# -------- helper -------- #

def write_summary_to_csv(file_path, selected_keys, summary_list):
    """ write to csv file
    """
    with open(file_path, encoding="utf-8", mode="w", newline="") as csv_file:
        # header line
        writer = csv.DictWriter(csv_file, fieldnames=selected_keys)
        writer.writeheader()
        for item in summary_list:
            writer.writerow(item)
    return 0


def get_symbols_list(api_key, file_path):
    """ retrieve all symbols provided in FMP
        save as pickle
    """
    url_str = "https://financialmodelingprep.com/api/v3/stock/list?" + \
              "apikey=" + api_key
    response = urlopen(url_str)
    data = response.read().decode("utf-8")
    obj = json.loads(data)
    saveAsPickle(obj, file_path)
    return obj

"""
TODOLIST
    - stock news
    - press releases 
    - earning calendar: only for premium 
    - IPO calendar
    - institutional holders
    - mutual fund holders
    - ETF holders
    - list of S&P 500 company
    - historical S&P 500 
    - most active stock companies 
    - most gainer stock companies
    - most loser stock companies
"""