import numpy as np
import pandas as pd

def calc_yz(data, vol):
    N = len(data)
    window = 30
    lambda_ = 0.94
    alpha = 1 - lambda_
    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    data = data.copy()
    data['VIX'] = vol['VIX']
    data['log_ho'] = (data['High'] / data['Open']).apply(np.log)
    data['log_lo'] = (data['Low'] / data['Open']).apply(np.log)
    data['log_co'] = (data['Close'] / data['Open']).apply(np.log)
    data['log_oc'] = (data['Open'] / data['Close'].shift(1)).apply(np.log)
    data['log_oc_sq'] = data['log_oc'] ** 2
    data['log_cc'] = (data['Close'] / data['Close'].shift(1)).apply(np.log)
    data['log_cc_sq'] = data['log_cc'] ** 2
    data['rs'] = (data['log_ho'] * (data['log_ho'] - data['log_co']) 
          + data['log_lo'] * (data['log_lo'] - data['log_co']))
    data['close_vol'] = (data['log_cc_sq'].rolling(window=window, center=False).sum()
                               * (1.0 / (window - 1.0)))
    data['open_vol'] = (data['log_oc_sq'].rolling(window=window, center=False).sum()
                               * (1.0 / (window - 1.0)))
    data['window_rs'] = (data['rs'].rolling(window=window, center=False).sum()
                               * (1.0 / (window - 1.0)))
    data['result'] = (data['open_vol'] + k * data['close_vol'] +
                            (1 - k) * data['window_rs']).apply(np.sqrt) * np.sqrt(252)
    data['VRP'] = (data['VIX'] - (data['result'] * 100))
    data['rpmean'] = data['VRP'].ewm(alpha=alpha, adjust=False).mean()
    data['std'] = np.std(data['VRP'])

    return data

def calc_cc(data, vol):
    data = data.copy()
    data['VIX'] = vol['VIX']
    data['Return'] = np.log(data['Close'] / data['Close'].shift(1))
    data.dropna(inplace=True)
    data['std'] = data['Return'].rolling(window=30).std()
    data['Vol'] = data['std'] * np.sqrt(252)
    data['VRP'] = data['VIX'] - (data['Vol'] * 100)
    lambda_ = 0.94
    alpha = 1 - lambda_
    data['rpmean'] = data['VRP'].ewm(alpha=alpha, adjust=False).mean()
    data['std'] = np.std(data['VRP'])

    return data
