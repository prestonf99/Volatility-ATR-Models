import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '0.05'
plt.rcParams['grid.color'] = '0.15'

class MorningStats():
    def __init__(self, days, underlying):
        self.days = days
        self.underlying = underlying
        self.data = pd.DataFrame()
        if self.underlying == '^GSPC':
            self.symbol = 'SPX'
        elif self.underlying == '^NDX':
            self.symbol = 'NDX'

    def atr(self):
        self.end_date =  datetime.now()
        self.start_date = self.end_date - timedelta(days=self.days)
        self.ticker = yf.Ticker(self.underlying)
        self.data = self.ticker.history(interval='1d', start=self.start_date,
                                        end=self.end_date)
        self.data.index = self.data.index.date
        self.atr_data = self.data.drop(['Dividends', 'Open', 'Close', 
                                  'Volume', 'Stock Splits'], axis=1)
        self.atr_data['RNG'] = self.atr_data['High'] - self.atr_data['Low']
        self.atr_data['ATR'] = self.atr_data['RNG'].rolling(window=20).mean()
        self.atr_data.index = self.atr_data.index.astype(str)
        plt.figure(figsize=(10, 6))
        plt.grid(True, zorder=1)
        plt.bar(self.atr_data.index[-20:], self.atr_data['RNG'].tail(20), label='Range',
               color='orange', alpha = 0.8, zorder=2)
        plt.plot(self.atr_data['ATR'].tail(20), color='m', label='20d ATR', zorder=3)
        plt.plot(self.atr_data.index[-1], self.atr_data['ATR'].iloc[-1],
                 marker='o', markersize=5, color='m')
        plt.annotate(f"{self.atr_data['ATR'].iloc[-1]:.2f}",
                     (self.atr_data.index[-1], self.atr_data['ATR'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='m',
                     ha='center')
        plt.xlabel('Date')
        plt.ylabel('Range')
        plt.title(f'{self.symbol} Trading Range')
        plt.legend()
        plt.gcf().autofmt_xdate();
    
    def cc(self):
        self.data = self.data
        self.end_date =  datetime.now()
        self.start_date = self.end_date - timedelta(days=self.days)
        if self.underlying == '^GSPC':
            self.vol = yf.Ticker('^VIX')
        elif self.underlying == '^NDX':
            self.vol = yf.Ticker('^VXN')
        vix = self.vol.history(interval='1d', start=self.start_date,
                                 end=self.end_date)
        vix.index = vix.index.date
        close_close = pd.DataFrame(self.data['Close'])
        close_close['Return'] = np.log(close_close['Close'] /
                                       close_close['Close'].shift(1))
        close_close.dropna(inplace=True)
        close_close['std'] = close_close['Return'].rolling(window=30).std()
        close_close['Vol'] = close_close['std'] * np.sqrt(252)
        close_close['VRP'] = vix['Close'] - (close_close['Vol'] * 100)
        close_close.dropna(inplace=True)
        lambda_ = 0.94
        alpha = 1 - lambda_
        close_close['rpmean'] = close_close['VRP'].ewm(alpha=alpha, adjust=False).mean()
        close_close['std'] = np.std(close_close['VRP'])
        plt.figure(figsize=(10, 6))
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        ax1.plot(close_close['VRP'])
        ax1.plot(close_close['VRP'].index[-1], close_close['VRP'].iloc[-1],
                 marker='o', markersize=3, color='cyan')
        ax1.annotate(f"{close_close['VRP'].iloc[-1]:.2f}",
                     (close_close['VRP'].index[-1], close_close['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='cyan',
                     ha='left')
        ax1.plot(close_close['rpmean'], color='r', alpha=0.25)
        ax1.plot(close_close['rpmean'] + close_close['std'], color='y', alpha=0.25, label='1σ')
        ax1.plot(close_close['rpmean'] - close_close['std'], color='y', alpha=0.25)
        ax1.plot(close_close['rpmean'] + (close_close['std'] * 2), color='m', alpha=0.25, label='2σ')
        ax1.plot(close_close['rpmean'] - (close_close['std'] * 2), color='m', alpha=0.25)
        ax1.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        ax1.set_ylabel('Discount(-)/Premium(+)')
        ax1.set_title('Volatility Risk Premium', loc='left', fontsize=12)
        ax1.grid(True)
        ax1.legend(loc='lower left')  
        ax2.plot(close_close['Close'], label='S&P 500', color='white')
        ax2.set_title(f'{self.symbol}', loc='left', fontsize=12)
        ax2.grid(True)
        ax2.xaxis_date()
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.tight_layout();