from fredapi import Fred
fred = Fred(api_key='YOUR_API_KEY')
from pylab import mpl, plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '0.05'
plt.rcParams['grid.color'] = '0.15'
import helper as hp
import calc_stats as cs


class Vols():
    def __init__(self, days, underlying):
        self.days = days
        self.underlying = underlying
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=self.days)
        self.ticker = yf.Ticker(self.underlying)
        self.data = self.ticker.history(interval='1d', start=self.start_date,
                                        end=self.end_date)
        self.data = self.data.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        self.data.index = self.data.index.date
        self.vol_name = hp.vol_sym(underlying)
        self.vol_label = hp.volatility_label(underlying)
        self.name = hp.underlying_name(underlying)
        self.vol_index = fred.get_series(self.vol_name, observation_start=self.start_date)
        self.vol = pd.DataFrame(self.vol_index, columns=['VIX'])
        self.yz = cs.calc_yz(self.data, self.vol)
        self.close_close = cs.calc_cc(self.data, self.vol)
    
    def atr(self):
        atr_data = self.data.copy()
        atr_data['RNG'] = atr_data['High'] - atr_data['Low']
        atr_data['ATR'] = atr_data['RNG'].rolling(window=20).mean()
        atr_data.index = atr_data.index.astype(str)
        plt.figure(figsize=(10, 6))
        plt.grid(True, zorder=1)
        plt.bar(atr_data.index[-20:], atr_data['RNG'].tail(20), label='Range',
               color='orange', alpha = 0.8, zorder=2)
        plt.plot(atr_data['ATR'].tail(20), color='m', label='20d ATR', zorder=3)
        plt.plot(atr_data.index[-1], atr_data['ATR'].iloc[-1],
                 marker='o', markersize=5, color='m')
        plt.annotate(f"{atr_data['ATR'].iloc[-1]:.1f}",
                     (atr_data.index[-1], atr_data['ATR'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='m',
                     ha='left', fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.3", 
                               facecolor=(0, 0, 0, 0.75), edgecolor='none'))
        plt.xlabel('Date')
        plt.ylabel('Range')
        plt.title(f'{self.name} Trading Range')
        plt.legend()
        plt.gcf().autofmt_xdate();

    def cc(self):    
        plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        plt.subplot(211)
        plt.plot(self.close_close['VRP'], label='VRP')
        plt.title(f'Close-Close Volatility Risk Premium: {self.name}')
        plt.plot(self.close_close['rpmean'], color='r', alpha=0.25)
        plt.plot(self.close_close['rpmean'] + self.close_close['std'], color='y', alpha=0.25, label='1σ')
        plt.plot(self.close_close['rpmean'] - self.close_close['std'], color='y', alpha=0.25)
        plt.plot(self.close_close['rpmean'] + (self.close_close['std'] * 2), color='m', alpha=0.25, label='2σ')
        plt.plot(self.close_close['rpmean'] - (self.close_close['std'] * 2), color='m', alpha=0.25)
        plt.plot(self.close_close['VRP'].index[-1], self.close_close['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{self.close_close['VRP'].iloc[-1]:.1f}",
                     (self.close_close['VRP'].index[-1], self.close_close['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.legend()
        plt.grid(True)
        plt.subplot(212)
        plt.plot(self.close_close['Close'], color='w', label=self.name)
        plt.legend()
        plt.grid(True);

    def ccs(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.close_close['VRP'], label='VRP')
        plt.plot(self.close_close['VRP'].index[-1], self.close_close['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{self.close_close['VRP'].iloc[-1]:.1f}",
                     (self.close_close['VRP'].index[-1], self.close_close['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.title(f'Close-Close Volatility Risk Premium: {self.name}')
        plt.plot(self.close_close['rpmean'], color='r', alpha=0.25)
        plt.plot(self.close_close['rpmean'] + self.close_close['std'], color='y', alpha=0.25, label='1σ')
        plt.plot(self.close_close['rpmean'] - self.close_close['std'], color='y', alpha=0.25)
        plt.plot(self.close_close['rpmean'] + (self.close_close['std'] * 2), color='m', alpha=0.25, label='2σ')
        plt.plot(self.close_close['rpmean'] - (self.close_close['std'] * 2), color='m', alpha=0.25)
        plt.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        plt.ylabel('Discount(-)/Premium(+)')
        plt.grid(True)
        plt.legend(loc='lower left')
        plt.legend()
        plt.grid(True);

    def vol_spread(self):
        plt.figure(figsize=(10, 6))
        plt.plot((self.close_close['Vol'] * 100), lw=0.95, label=f'{self.name} CC Volatility')
        plt.plot((self.close_close['Vol']*100).index[-1], (self.close_close['Vol']*100).iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{(self.close_close['Vol']*100).iloc[-1]:.1f}",
                     ((self.close_close['Vol']*100).index[-1], (self.close_close['Vol']*100).iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.plot(self.close_close['VIX'], label=f'{self.vol_label}', color='w')
        plt.plot(self.close_close['VIX'].index[-1], self.close_close['VIX'].iloc[-1],
                 marker='o', markersize=3, color='w')
        plt.annotate(f"{self.close_close['VIX'].iloc[-1]:.1f}",
                     (self.close_close['VIX'].index[-1], self.close_close['VIX'].iloc[-1]),
                     textcoords="offset points", xytext=(0,10), color='w',
                     ha='left', fontweight='bold')
        plt.grid(True)
        plt.title(f'{self.vol_label} and {self.name} 30d Close-Close Volatility')
        plt.legend();

    def vol_spread_yz(self):
        plt.figure(figsize=(10, 6))
        plt.plot((self.yz['result'] * 100), lw=0.95, label=f'{self.name} Yang-Zhang Volatility')
        plt.plot((self.yz['result']*100).index[-1], (self.yz['result']*100).iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{(self.yz['result']*100).iloc[-1]:.1f}",
                     ((self.yz['result']*100).index[-1], (self.yz['result']*100).iloc[-1]),
                     textcoords="offset points", xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.plot(self.yz['VIX'], label=f'{self.vol_label}', color='w')
        plt.plot(self.close_close['VIX'].index[-1], self.close_close['VIX'].iloc[-1],
                 marker='o', markersize=3, color='w')
        plt.annotate(f"{self.close_close['VIX'].iloc[-1]:.1f}",
                     (self.close_close['VIX'].index[-1], self.close_close['VIX'].iloc[-1]),
                     textcoords="offset points", xytext=(0,10), color='w',
                     ha='left', fontweight='bold')
        plt.grid(True)
        plt.title(f'{self.vol_label} and {self.name} 30d Yang-Zhang Volatility')
        plt.legend();

    
    def plot_yz(self):
        plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        plt.subplot(211)
        plt.plot(self.yz['VRP'])
        plt.plot(self.yz['VRP'].index[-1], self.yz['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{self.yz['VRP'].iloc[-1]:.1f}",
                     (self.yz['VRP'].index[-1], self.yz['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.plot(self.yz['rpmean'], color='r', alpha=0.25)
        plt.plot(self.yz['rpmean'] + self.yz['std'], color='y', alpha=0.25, label='1σ')
        plt.plot(self.yz['rpmean'] - self.yz['std'], color='y', alpha=0.25)
        plt.plot(self.yz['rpmean'] + (self.yz['std'] * 2), color='m', alpha=0.25, label='2σ')
        plt.plot(self.yz['rpmean'] - (self.yz['std'] * 2), color='m', alpha=0.25)
        plt.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        plt.ylabel('Discount(-)/Premium(+)')
        plt.title(f'Yang-Zhang Volatility Risk Premium - {self.name}', loc='left', fontsize=12)
        plt.grid(True)
        plt.legend(loc='lower left')
        plt.subplot(212)
        plt.plot(self.yz['Close'], label='S&P 500', color='white')
        plt.title(f'{self.name}', loc='left', fontsize=12)
        plt.grid(True)
        plt.show()
        print(self.yz['VRP'].index[-1], self.yz['VRP'].iloc[-1]);

    def plot_yzs(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.yz['VRP'])
        plt.plot(self.yz['VRP'].index[-1], self.yz['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{self.yz['VRP'].iloc[-1]:.1f}",
                     (self.yz['VRP'].index[-1], self.yz['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.plot(self.yz['rpmean'], color='r', alpha=0.25)
        plt.plot(self.yz['rpmean'] + self.yz['std'], color='y', alpha=0.25, label='1σ')
        plt.plot(self.yz['rpmean'] - self.yz['std'], color='y', alpha=0.25)
        plt.plot(self.yz['rpmean'] + (self.yz['std'] * 2), color='m', alpha=0.25, label='2σ')
        plt.plot(self.yz['rpmean'] - (self.yz['std'] * 2), color='m', alpha=0.25)
        plt.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        plt.ylabel('Discount(-)/Premium(+)')
        plt.title(f'Yang-Zhang Volatility Risk Premium - {self.name}', loc='left', fontsize=12)
        plt.grid(True)
        plt.legend(loc='lower left');

