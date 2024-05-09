## AM Stats 

### Setting it Up

*Directions are in windows, chatgpt can be your friend here if on mac*

1. First, you'll need to install miniconda on your computer 
        
        https://docs.anaconda.com/free/miniconda/index.html

2. Open the Anaconda prompt (windows search 'miniconda') and install the packages (at this step you can look up how to create an environment, but if you're only using python to execute these files it really isn't a big deal if you just use the base environment). 

        pip install numpy pandas matplotlib yfinance jupyter

3. After the installations are done, open jupyter lab

        (base): C:\Users\your_computer> jupyter lab

4. Navigate to the folder that contains the files in the repository and ensure that the MorningStats.py and RunMS.ipynb are in the same folder.

5. Open RunMS & hit shift+enter until all of the charts are loaded in (should be relatively quick). 

6. Some of the funcitons
   * .atr() - 20d average trading range
   * .cc() - Close-Close Volatility Risk Premium & Underlying
   * .ccs() - Close-Close Premium by itself
   * .vol_spread() - CC Vol Estimator vs Vix.
  
7. Usage Details in the RunMS File

    