import requests
import pandas as pd
import logging
import time
import datetime
from io import StringIO
from tqdm import tqdm


def parseRequest(request):
    # parse request to dataframe
    stock_df = pd.read_csv(StringIO(request.text.replace("=", "")) ,header=["證券代號" in l for l in request.text.split("\n")].index(True)-1)
    return stock_df

def getRequest(Date):
    # get request
    requestOutput = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + Date + '&type=ALL')
    return parseRequest(requestOutput)

def getTodayDate():
    # get today date
    return time.strftime('%Y%m%d', time.localtime())
    
def getLastStockDate():
    # get last stock date from log
    logFile = open('stockLog.log')
    listOfLog = logFile.readlines()
    listOfLog.reverse()
    lastList = listOfLog[0] 
    lastDate = lastList.split(' ')
    lastDate.reverse()
    return lastDate[0]

def stringToDatetime(string):
    return datetime.datetime.strptime(string,'%Y%m%d').date()
    
def datetimeToString(datetime):
    return datetime.strftime('%Y%m%d')


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='stockLog.log', filemode='a', format=FORMAT)

if __name__ == '__main__':

    begin = stringToDatetime(getLastStockDate())
    end = stringToDatetime(getTodayDate())

    print('begin:%s'%(begin))
    print('end:  %s'%(end))

    for i in tqdm(range((end - begin).days)):
        day = begin + datetime.timedelta(days = i)
        Date = datetimeToString(day)

        try:
            stockDf = getRequest(Date)
            logging.info('stockDate %s',Date)

            # store
            stockDf.to_csv('./data/%s.csv'%(Date) ,index = False ,encoding="utf_8_sig")
        except:
            print('%s Stock rest or error'%(Date))
