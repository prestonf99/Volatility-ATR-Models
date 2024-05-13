
def vol_sym(underlying):
    if underlying == '^GSPC':
        return 'VIXCLS'
    if underlying == 'GLD':
        return 'GVZCLS'
    if underlying == '^RUT':
        return 'RVXCLS'
    if underlying == '^DJI':
        return 'VXDCLS'
    if underlying == 'EEM':
        return 'VXEEMCLS'
    if underlying == 'AMZN':
        return 'VXAZNCLS'
    if underlying == 'GOOG':
        return 'VXGOGCLS'
    if underlying == 'GS':
        return 'VIXCLS'
    if underlying == '^NDX':
        return 'VXNCLS'
    if underlying == 'AAPL':
        return 'VXAPLCLS'
    if underlying == 'CL=F':
        return 'OVXCLS'

def underlying_name(underlying):
    if underlying == '^GSPC':
        return 'S&P 500'
    if underlying == 'GLD':
        return 'Gold'
    if underlying == '^RUT':
        return 'Russell 2000'
    if underlying == '^DJI':
        return 'Dow Jones'
    if underlying == 'EEM':
        return 'Emerging Markets'
    if underlying == 'AMZN':
        return 'Amazon'
    if underlying == 'GOOG':
        return 'Google'
    if underlying == 'GS':
        return 'Goldman Sachs'
    if underlying == '^NDX':
        return 'Nasdaq 100'
    if underlying == 'AAPL':
        return 'Apple'
    if underlying == 'CL=F':
        return 'Crude Oil'

def volatility_label(underlying):
    if underlying == '^GSPC':
        return 'VIX'
    if underlying == 'GLD':
        return 'Gold VIX'
    if underlying == '^RUT':
        return 'Russell VIX'
    if underlying == '^DJI':
        return 'Dow Jones VIX'
    if underlying == 'EEM':
        return 'Emerging Markets VIX'
    if underlying == 'AMZN':
        return 'Amazon VIX'
    if underlying == 'GOOG':
        return 'Google VIX'
    if underlying == 'GS':
        return 'Goldman Sachs VIX'
    if underlying == '^NDX':
        return 'Nasdaq VIX'
    if underlying == 'AAPL':
        return 'Apple VIX'
    if underlying == 'CL=F':
        return 'Crude Oil VIX'
