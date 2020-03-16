import requests
import pandas as pd
import numpy as np
from io import StringIO




# get request
Date = '20200316'
getRequest = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + Date + '&type=ALL')


# parse request to dataframe
stock_df = pd.read_csv(StringIO(getRequest.text.replace("=", "")), header=["證券代號" in l for l in getRequest.text.split("\n")].index(True)-1)

# store
stock_df.to_csv('./data/%s.csv'%(Date) , index = False)


