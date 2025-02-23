## AM Stats 
Preston Fisk

prestonfisk99@gmail.com

github.com/prestonf99


## Overview
The objective for this repository was to create scripts that provide relevant information regarding the implied volatility discount/premium and the average trading range (ATR) of various futures products & a few individual large-cap U.S. Equities. These were designed with ease-of-use in mind so traders can quickly observe the volatility situation on a consistent basis. For more information regarding how to read these scripts, refer to Euan Sinclair's "Volatility Trading" (https://www.goodreads.com/book/show/138777693-volatility-trading-website-2nd-edition-by-sinclair-euan-2013-hardc). Our personal use for these scripts is to gain insight on whether a given market is "Overly hedged" or "Overly complacent". This repository is to generate insight about the boarder conditions for traders who already have an existing process for entry criteria and risk management. 

## Examples 
Before getting into the installation of the repository and the installation process, let's go through some of the visualizations. 

**_ATR_**: For active traders, knowing the average trading range for whatever product you're looking at is an important part of the preparation process. Looking at this daily in conjunction with other factors, such as the overnight volume, help lay the groundwork for what to expect from a given trading session. You can only retrieve the 20-day average.

![ATR](Vol_Examples/ATR.png)

**_Close-Close Volatility Estimator_**: This estimator calculates the realized volatility by *only* looking at the closing price of the product you're viewing.

![CC](Vol_Examples/Close_Close.png)

**_Close-Close Volatility Spread_**: Calculates realized volatility using the methodology described above. But it doesn't calculate the 'risk premium', so traders can just look at the volatility spread by itself. 

![CC Spread](Vol_Examples/CC_spread.png)

**_Yang-Zhang Volatility Estimator_**: This estimator is a weighted average of three separate variance measures. They are close to close, open to close, and intraday high-low variance. It is useful because it accounts for overnight gaps, accounts for intraday variance which improves accuracy, and improves efficiency due to its use of multiple inputs. This is our preferred estimator, especially when the asset in question tends to have overnight gaps or large intraday swings. 

![Yang Zhang](Vol_Examples/Yang_Zhang.png)

**_Yang-Zhang Spread_**: Same visualization as the Close-Close Spread, but with the Yang Zhang methodology to calculate the realized volatility. 

![YZ Spread](Vol_Examples/Yang_Zhang_Spread.png)

### Supported Tickers

* '^GSPC' - S&P 500 Index
* '^NDX' - Nasdaq 100
* '^RUT' - Russell 2000
* '^DJI' - Down Jones Industrial Average
* 'CL=F' - CME Crude Oil Futures
* 'GLD' - SPDR Gold Shares ETF
* 'AAPL' - Apple Inc. 
* 'AMZN' - Amazon.com Inc. 
* 'EEM' - iShares MSCI Emerging Markets ETF
* 'GS' - Goldman Sachs Group Inc
* 'GOOG' - Alphabet Inc Class C (Google Stock)
    
## Setting it Up

*Directions are in windows, chatgpt can be your friend here if on mac*

1. First, you'll need to install miniconda on your computer 
        
        https://docs.anaconda.com/free/miniconda/index.html

2. Open the Anaconda prompt (windows search 'miniconda') and install the packages (at this step you can look up how to create an environment, but if you're only using python to execute these files it really isn't a big deal if you just use the base environment). 

        pip install numpy pandas matplotlib yfinance jupyter fredapi

3. Go to `https://fredaccount.stlouisfed.org/apikeys`. Create an account and request an API key.  

4. After the installations are done, open jupyter lab

        (base): C:\Users\your_computer> jupyter lab

5. Navigate to the folder that contains the files in the repository and ensure that `MorningStats.py`, `calc_stats`, `helper.py` and `RunMS.ipynb` are in the same folder.

6. Open the MorningStats.py file and insert your St Louis Fed API key on the second line.  

7. Open `RunMS.ipynb` & hit shift+enter until all of the charts are loaded in (should be relatively quick).

   * The file's purpose is to showcase the broad range of tickers & functions that you can use. Feel free to make your own jupyter notebook and play around with it as you see fit! You can specify the date range & ticker however you'd like. 
   * The bands on the Volatility Risk Premium charts are as follows. The red line is the 30d exponentially weighted moving average's mean value. The yellow lines are the +1σ/-1σ of the red line. The pink lines are the +2σ/-2σ of the red line. 

8. Some of the funcitons
   * .atr() - 20d average trading range
   * .cc() - Close-Close Volatility Risk Premium & Underlying
   * .ccs() - Close-Close Premium by itself
   * .vol_spread() - CC Vol Estimator vs Vix.
   * .plot_yz() - Yang-Zhang Volatility Risk Premium(accounts for OHLC as well as overnight vol)
   * .plot_yzs() - Yang-Zhang RVOL By itself
   * .vol_spread_yz() - Yang-Zhang Vol Spread
  
9. Usage Details in the RunMS File. 

    