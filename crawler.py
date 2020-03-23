import requests
import pandas as pd
import logging
from io import StringIO


def parseRequest(request):
    # parse request to dataframe
    stock_df = pd.read_csv(StringIO(request.text.replace("=", "")) ,header=["證券代號" in l for l in request.text.split("\n")].index(True)-1)
    return stock_df

def getRequest(Date):
    # get request
    requestOutput = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + Date + '&type=ALL')
    return parseRequest(requestOutput)

if __name__ == '__main__':

    
    Date = '20200316'
    stockDf = getRequest(Date)
    

    # store
    stockDf.to_csv('./data/%s.csv'%(Date) ,index = False ,encoding="utf_8_sig")


