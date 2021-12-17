#import pandas as pd
#from pandas import DataFrame
import requests



api_key='8JB4V49M6EBPR459'

url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ str(Ticker)+'&apikey='+str(api_key)
print(url)
r = requests.get(url)
DataIncomeStatement = r.json()



#print('test')
#print (pd.__version__)