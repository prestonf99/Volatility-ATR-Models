import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.patheffects as PathEffects
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '0.05'
plt.rcParams['grid.color'] = '0.15'

class MorningStats():
    def __init__(self, days, underlying):
        self.days = days
        self.underlying = underlying
        if self.underlying == '^GSPC':
            self.symbol = 'SPX'
        elif self.underlying == '^NDX':
            self.symbol = 'NDX'
        self.end_date =  datetime.now()
        self.start_date = self.end_date - timedelta(days=self.days)
        self.ticker = yf.Ticker(self.underlying)
        self.data = self.ticker.history(interval='1d', start=self.start_date,
                                        end=self.end_date)
        self.data.index = self.data.index.date
        if self.symbol == 'SPX':
            self.sym = 'S&P 500'
            self.vol_sym = 'VIX'
        elif self.symbol == 'NDX':
            self.sym = 'Nasdaq 100'
            self.vol_sym = 'VXN'
        if self.underlying == '^GSPC':
            self.vol = yf.Ticker('^VIX')
        elif self.underlying == '^NDX':
            self.vol = yf.Ticker('^VXN')
        self.vix = self.vol.history(interval='1d', start=self.start_date,
                                 end=self.end_date)
        self.vix.index = self.vix.index.date

    def get_data(self):
        data = self.data
        data = data.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        return data
    def get_vix(self):
        vix = self.vix
        vix = vix.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        return vix
    def atr(self):
        atr_data = self.data.drop(['Dividends', 'Open', 'Close', 
                                  'Volume', 'Stock Splits'], axis=1)
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
        plt.title(f'{self.sym} Trading Range')
        plt.legend()
        plt.gcf().autofmt_xdate();
    
    def cc(self):
        vix = self.vix
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
                 marker='o', markersize=3, color='paleturquoise')
        ax1.annotate(f"{close_close['VRP'].iloc[-1]:.1f}",
                     (close_close['VRP'].index[-1], close_close['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        ax1.plot(close_close['rpmean'], color='r', alpha=0.25)
        ax1.plot(close_close['rpmean'] + close_close['std'], color='y', alpha=0.25, label='1σ')
        ax1.plot(close_close['rpmean'] - close_close['std'], color='y', alpha=0.25)
        ax1.plot(close_close['rpmean'] + (close_close['std'] * 2), color='m', alpha=0.25, label='2σ')
        ax1.plot(close_close['rpmean'] - (close_close['std'] * 2), color='m', alpha=0.25)
        ax1.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        ax1.set_ylabel('Discount(-)/Premium(+)')
        ax1.set_title(f'Close-Close Volatility Risk Premium - {self.sym}', loc='left', fontsize=12)
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

    def ccs(self):
        vix = self.vix
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
        plt.plot(close_close['VRP'])
        plt.plot(close_close['VRP'].index[-1], close_close['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{close_close['VRP'].iloc[-1]:.1f}",
                     (close_close['VRP'].index[-1], close_close['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.plot(close_close['rpmean'], color='r', alpha=0.25)
        plt.plot(close_close['rpmean'] + close_close['std'], color='y', alpha=0.25, label='1σ')
        plt.plot(close_close['rpmean'] - close_close['std'], color='y', alpha=0.25)
        plt.plot(close_close['rpmean'] + (close_close['std'] * 2), color='m', alpha=0.25, label='2σ')
        plt.plot(close_close['rpmean'] - (close_close['std'] * 2), color='m', alpha=0.25)
        plt.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        plt.ylabel('Discount(-)/Premium(+)')
        plt.title(f'Close-Close Volatility Risk Premium - {self.sym}', loc='left', fontsize=12)
        plt.grid(True)
        plt.legend(loc='lower left')

    def yz(self):
        vix = self.vix
        yz = pd.DataFrame(self.data)
        yz = yz.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        N = len(yz)
        window = 30
        lambda_ = 0.94
        alpha = 1 - lambda_
        k = 0.34 / (1.34 + (window + 1) / (window-1))
        yz['VIX'] = vix['Close']
        yz['log_ho'] = (yz['High'] / yz['Open']).apply(np.log)
        yz['log_lo'] = (yz['Low'] / yz['Open']).apply(np.log)
        yz['log_co'] = (yz['Close'] / yz['Open']).apply(np.log)
        yz['log_oc'] = (yz['Open'] / yz['Close'].shift(1)).apply(np.log)
        yz['log_oc_sq'] = yz['log_oc'] ** 2
        yz['log_cc'] = (yz['Close'] / yz['Close'].shift(1)).apply(np.log)
        yz['log_cc_sq'] = (yz['log_cc'] ** 2)
        yz['rs'] = (yz['log_ho'] * (yz['log_ho'] - yz['log_co']) 
              + yz['log_lo'] * (yz['log_lo'] - yz['log_co']))
        yz['close_vol'] = (yz['log_cc_sq'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['open_vol'] = (yz['log_oc_sq'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['window_rs'] = (yz['rs'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['result'] = (yz['open_vol'] + k * yz['close_vol'] +
                                (1 - k) * yz['window_rs']).apply(np.sqrt) * np.sqrt(252)
        yz['VRP'] = (yz['VIX'] - (yz['result'] * 100) )
        yz['rpmean'] = yz['VRP'].ewm(alpha=alpha, adjust=False).mean()
        yz['std'] = np.std(yz['VRP'])
        plt.figure(figsize=(10, 6))
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        ax1.plot(yz['VRP'])
        ax1.plot(yz['VRP'].index[-1], yz['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        ax1.annotate(f"{yz['VRP'].iloc[-1]:.1f}",
                     (yz['VRP'].index[-1], yz['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        ax1.plot(yz['rpmean'], color='r', alpha=0.25)
        ax1.plot(yz['rpmean'] + yz['std'], color='y', alpha=0.25, label='1σ')
        ax1.plot(yz['rpmean'] - yz['std'], color='y', alpha=0.25)
        ax1.plot(yz['rpmean'] + (yz['std'] * 2), color='m', alpha=0.25, label='2σ')
        ax1.plot(yz['rpmean'] - (yz['std'] * 2), color='m', alpha=0.25)
        ax1.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        ax1.set_ylabel('Discount(-)/Premium(+)')
        ax1.set_title(f'Yang-Zhang Volatility Risk Premium - {self.sym}', loc='left', fontsize=12)
        ax1.grid(True)
        ax1.legend(loc='lower left')  
        ax2.plot(yz['Close'], label='S&P 500', color='white')
        ax2.set_title(f'{self.symbol}', loc='left', fontsize=12)
        ax2.grid(True)
        ax2.xaxis_date()
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.tight_layout();

    def yzs(self):
        vix = self.vix
        yz = pd.DataFrame(self.data)
        yz = yz.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        N = len(yz)
        window = 30
        lambda_ = 0.94
        alpha = 1 - lambda_
        k = 0.34 / (1.34 + (window + 1) / (window-1))
        yz['VIX'] = vix['Close']
        yz['log_ho'] = (yz['High'] / yz['Open']).apply(np.log)
        yz['log_lo'] = (yz['Low'] / yz['Open']).apply(np.log)
        yz['log_co'] = (yz['Close'] / yz['Open']).apply(np.log)
        yz['log_oc'] = (yz['Open'] / yz['Close'].shift(1)).apply(np.log)
        yz['log_oc_sq'] = yz['log_oc'] ** 2
        yz['log_cc'] = (yz['Close'] / yz['Close'].shift(1)).apply(np.log)
        yz['log_cc_sq'] = (yz['log_cc'] ** 2)
        yz['rs'] = (yz['log_ho'] * (yz['log_ho'] - yz['log_co']) 
              + yz['log_lo'] * (yz['log_lo'] - yz['log_co']))
        yz['close_vol'] = (yz['log_cc_sq'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['open_vol'] = (yz['log_oc_sq'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['window_rs'] = (yz['rs'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['result'] = (yz['open_vol'] + k * yz['close_vol'] +
                                (1 - k) * yz['window_rs']).apply(np.sqrt) * np.sqrt(252)
        yz['VRP'] = (yz['VIX'] - (yz['result'] * 100) )
        yz['rpmean'] = yz['VRP'].ewm(alpha=alpha, adjust=False).mean()
        yz['std'] = np.std(yz['VRP'])
        plt.figure(figsize=(10, 6))
        plt.plot(yz['VRP'])
        plt.plot(yz['VRP'].index[-1], yz['VRP'].iloc[-1],
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{yz['VRP'].iloc[-1]:.1f}",
                     (yz['VRP'].index[-1], yz['VRP'].iloc[-1]),
                     textcoords="offset points",
                     xytext=(0,10), color='paleturquoise',
                     ha='left', fontweight='bold')
        plt.plot(yz['rpmean'], color='r', alpha=0.25)
        plt.plot(yz['rpmean'] + yz['std'], color='y', alpha=0.25, label='1σ')
        plt.plot(yz['rpmean'] - yz['std'], color='y', alpha=0.25)
        plt.plot(yz['rpmean'] + (yz['std'] * 2), color='m', alpha=0.25, label='2σ')
        plt.plot(yz['rpmean'] - (yz['std'] * 2), color='m', alpha=0.25)
        plt.axhline(0, lw=0.5, color='grey', alpha=0.75, linestyle='--')
        plt.ylabel('Discount(-)/Premium(+)')
        plt.title(f'Yang-Zhang Volatility Risk Premium - {self.sym}', loc='left', fontsize=12)
        plt.grid(True)
        plt.legend();  


    def vol_spread(self):
        vix = self.vix['Close']
        close_close = pd.DataFrame(self.data['Close'])
        close_close['Return'] = np.log(close_close['Close'] /
                                       close_close['Close'].shift(1))
        close_close.dropna(inplace=True)
        close_close['std'] = close_close['Return'].rolling(window=30).std()
        close_close['Vol'] = close_close['std'] * np.sqrt(252)
        close_close.dropna(inplace=True)
        plt.figure(figsize=(10, 6))
        plt.plot((close_close['Vol'] * 100), lw=0.95, label=f'{self.symbol} CC Volatility')
        plt.plot(vix, label=f'{self.vol_sym}', color='w')
        plt.plot(vix.index[-1], vix.iloc[-1],
                 marker='o', markersize=3, color='w')
        plt.plot(close_close['Vol'].index[-1], (close_close['Vol'].iloc[-1]*100),
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{(close_close['Vol'].iloc[-1]*100):.1f}",
                (close_close['Vol'].index[-1], (close_close['Vol'].iloc[-1]*100)),
                textcoords="offset points",
                xytext=(0,10), color='paleturquoise',
                ha='left', fontweight='bold')
        plt.annotate(f"{vix.iloc[-1]:.1f}",
                (vix.index[-1], (vix.iloc[-1])),
                textcoords="offset points",
                xytext=(0,10), color='white',
                ha='left', fontweight='bold')
        plt.title(f'{self.vol_sym} & {self.sym} 30d Close-Close Volatility')
        plt.grid(True)
        plt.legend();

    def vol_spread_yz(self):
        vix = self.vix['Close']
        yz = pd.DataFrame(self.data)
        yz = yz.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        N = len(yz)
        window = 30
        k = 0.34 / (1.34 + (window + 1) / (window-1))
        yz['VIX'] = vix
        yz['log_ho'] = (yz['High'] / yz['Open']).apply(np.log)
        yz['log_lo'] = (yz['Low'] / yz['Open']).apply(np.log)
        yz['log_co'] = (yz['Close'] / yz['Open']).apply(np.log)
        yz['log_oc'] = (yz['Open'] / yz['Close'].shift(1)).apply(np.log)
        yz['log_oc_sq'] = yz['log_oc'] ** 2
        yz['log_cc'] = (yz['Close'] / yz['Close'].shift(1)).apply(np.log)
        yz['log_cc_sq'] = (yz['log_cc'] ** 2)
        yz['rs'] = (yz['log_ho'] * (yz['log_ho'] - yz['log_co']) 
              + yz['log_lo'] * (yz['log_lo'] - yz['log_co']))
        yz['close_vol'] = (yz['log_cc_sq'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['open_vol'] = (yz['log_oc_sq'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['window_rs'] = (yz['rs'].rolling(window=window, center=False).sum()
                                   * (1.0 / (window - 1.0)))
        yz['result'] = (yz['open_vol'] + k * yz['close_vol'] +
                                (1 - k) * yz['window_rs']).apply(np.sqrt) * np.sqrt(252)
        plt.figure(figsize=(10, 6))
        plt.plot((yz['result'] * 100), lw=0.95, label=f'{self.symbol} YZ Volatility')
        plt.plot(vix, label=f'{self.vol_sym}', color='w')
        plt.plot(vix.index[-1], vix.iloc[-1],
                 marker='o', markersize=3, color='w')
        plt.plot(yz['result'].index[-1], (yz['result'].iloc[-1]*100),
                 marker='o', markersize=3, color='paleturquoise')
        plt.annotate(f"{(yz['result'].iloc[-1]*100):.1f}",
                (yz['result'].index[-1], (yz['result'].iloc[-1]*100)),
                textcoords="offset points",
                xytext=(0,10), color='paleturquoise',
                ha='left', fontweight='bold')
        plt.annotate(f"{vix.iloc[-1]:.1f}",
                (vix.index[-1], (vix.iloc[-1])),
                textcoords="offset points",
                xytext=(0,10), color='white',
                ha='left', fontweight='bold')
        plt.title(f'{self.vol_sym} & {self.sym} 30d Yhang-Zhang Volatility')
        plt.grid(True)
        plt.legend();
