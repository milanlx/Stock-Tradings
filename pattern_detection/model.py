import csv
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime


class Stock:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = self.get_date(start_date)
        self.end_date = self.get_date(end_date)
        self.daily_price = {'Open':[], 'Close':[], 'High':[], 'Low':[]}
        self.hourly_price = {'Open':[], 'Close':[], 'High':[], 'Low':[]}
        self.daily_signal = None
        self.hourly_signal = None

    def get_date(self, date_str):
        # date_str: '07/16/2022'
        date_format = '%m/%d/%Y'
        d = datetime.strptime(date_str, date_format)
        return d

    def read_daily_price(self, **kwargs):
        # hard-coded duration
        price_history = yf.Ticker(self.ticker).history(period='6mo', interval='1d', actions=False)
        for key in self.daily_price.keys():
            self.daily_price[key] = np.array(price_history[key])

    def read_hourly_price(self, **kwargs):
        # hard-coded duration
        price_history = yf.Ticker(self.ticker).history(period='3mo', interval='1h', actions=False)
        for key in self.hourly_price.keys():
            self.hourly_price[key] = np.array(price_history[key])

    def write_to_csv(self, file_path):
        # date | corr
        pass

    def calculate_signal(self, scale):
        """
        (close-open)/open; (high-open)/open; (low-open)/open
        :return: np.array, n_day * (3*1, 3*8)
        """
        if scale == 'daily':
            price_dict = self.daily_price
        else:
            price_dict = self.hourly_price

        n, m = 3, price_dict['Open'].shape[0]
        signal = np.zeros((n, m))
        for i, key in enumerate(['Close', 'High', 'Low']):
            curr = (price_dict[key] - price_dict['Open'])/price_dict['Open']
            signal[i,:] = curr
        if scale == 'hourly':
            self.hourly_signal = signal.T.reshape((int(m/8), int(n*8)))
        elif scale == 'daily':
            self.daily_signal = signal.T

    # need to consider mismatch in length
    def calculate_corrcoef(self, stock, scale):
        corr = 0
        if scale == 'daily':
            if self.daily_signal is None:
                self.daily_signal = self.calculate_signal(scale)
            if stock.daily_signal is None:
                stock.daily_signal = stock.calculate_signal(scale)
            corr = self.get_corr(stock.daily_signal, scale)
        elif scale == 'hourly':
            if self.hourly_signal is None:
                self.hourly_signal = self.calculate_signal(scale)
            if stock.hourly_signal is None:
                stock.hourly_signal = stock.calculate_signal(scale)
            corr = self.get_corr(stock.hourly_signal, scale)
        return corr

    def get_corr(self, mat2, scale):
        if scale == 'daily':
            mat1 = self.daily_signal
        elif scale == 'hourly':
            mat1 = self.hourly_signal

        n = mat1.shape[0]
        corr_arr = np.zeros(n)
        for i in range(n):
            corr_temp = np.corrcoef(mat1[i,:], mat2[i,:])[0,1]
            corr_arr[i] = corr_temp
        return corr_arr



