#import pandas as pd
#from pandas import DataFrame
import requests
import psycopg2


DB_HOST = 'ls-8ac1ef06f8c0b721d61a89b671a2e10c40a7050f.cpsgene13aqe.eu-central-1.rds.amazonaws.com'
DB_NAME =  'Stocks'
DB_USER = 'dbmasteruser'
DB_PASS = 'RH6t.8|Ssd[g0y)jSA+c,)UP,V*<7^ZV'

Ticker ='IBM'
date = '2017-10-15'
currency = 'usd'


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,host=DB_HOST)






api_key='8JB4V49M6EBPR459'

url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ str(Ticker)+'&apikey='+str(api_key)
#print(url)


r = requests.get(url)



DataIncomeStatement = r.json()

zz = len(DataIncomeStatement['annualReports'])

str_ =''

listOfnumbers = []

#print(type(DataIncomeStatement['annualReports'][0]))
print(len(DataIncomeStatement['annualReports'][0]))
for key, value in DataIncomeStatement['annualReports'][0].items():
#    print(key,value)
    str_ += key
    str_ +=','
    listOfnumbers.append(value)
        


str2_ =''

for i in range (len(listOfnumbers)):
    str2_ += 'listOfnumbers['+str(i)+']'
    str2_ += ','





finalString = str_[:-1]

finalString2 = str2_[:-1]

#print(finalString)
print('          ')
#print(finalString2)



cur = conn.cursor()

#cur.execute("CREATE TABLE main (id SERIAL PRIMARY KEY, title VARCHAR);")

#test = "INSERT INTO income_statement ("+finalString+") VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",()

print(DataIncomeStatement['annualReports'][0]['grossProfit'])
print(float(DataIncomeStatement['annualReports'][0]['grossProfit']))
print(int(DataIncomeStatement['annualReports'][0]['grossProfit']))

print(len(DataIncomeStatement['annualReports']))

for i in range (len(DataIncomeStatement['annualReports'])):

    print(DataIncomeStatement['annualReports'][i])

    for key, value in DataIncomeStatement['annualReports'][i].items():
        
        if value == 'None':
            print(key, value)
            DataIncomeStatement['annualReports'][i].update({key:0})

            print('Change is added to',key, value)


print(DataIncomeStatement['annualReports'][0]['investmentIncomeNet'])


#cur.execute("INSERT INTO income_statement (ticker,fiscalDateEnding,reportedCurrency,grossProfit,totalRevenue,costOfRevenue,costofGoodsAndServicesSold,operatingIncome,sellingGeneralAndAdministrative,researchAndDevelopment,operatingExpenses,investmentIncomeNet,netInterestIncome,interestIncome,nonInterestIncome,otherNonOperatingIncome,depreciation,depreciationAndAmortization,incomeBeforeTax,incomeTaxExpense,interestAndDebtExpense,netIncomeFromContinuingOperations,comprehensiveIncomeNetOfTax,ebit,ebitda,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(Ticker,DataIncomeStatement['annualReports'][0]['fiscalDateEnding'],DataIncomeStatement['annualReports'][0]['reportedCurrency'],float(DataIncomeStatement['annualReports'][0]['grossProfit'])float(DataIncomeStatement['annualReports'][0]['totalRevenue'])))

i=0
for i in range (len(DataIncomeStatement['annualReports'])):
    cur.execute("INSERT INTO income_statement (ticker,fiscalDateEnding,reportedCurrency,grossProfit,totalRevenue,costOfRevenue,costofGoodsAndServicesSold,operatingIncome,sellingGeneralAndAdministrative,researchAndDevelopment,operatingExpenses,investmentIncomeNet,netInterestIncome,interestIncome,interestExpense,nonInterestIncome,otherNonOperatingIncome,depreciation,depreciationAndAmortization,incomeBeforeTax,incomeTaxExpense,interestAndDebtExpense,netIncomeFromContinuingOperations,comprehensiveIncomeNetOfTax,ebit,ebitda,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(Ticker,DataIncomeStatement['annualReports'][i]['fiscalDateEnding'],DataIncomeStatement['annualReports'][i]['reportedCurrency'],float(DataIncomeStatement['annualReports'][i]['grossProfit']),float(DataIncomeStatement['annualReports'][i]['totalRevenue']),float(DataIncomeStatement['annualReports'][i]['costOfRevenue']),float(DataIncomeStatement['annualReports'][i]['costofGoodsAndServicesSold']),float(DataIncomeStatement['annualReports'][i]['operatingIncome']),float(DataIncomeStatement['annualReports'][i]['sellingGeneralAndAdministrative']),float(DataIncomeStatement['annualReports'][i]['researchAndDevelopment']),float(DataIncomeStatement['annualReports'][i]['operatingExpenses']),float(DataIncomeStatement['annualReports'][i]['investmentIncomeNet']),float(DataIncomeStatement['annualReports'][i]['netInterestIncome']),float(DataIncomeStatement['annualReports'][i]['interestIncome']),float(DataIncomeStatement['annualReports'][i]['interestExpense']),float(DataIncomeStatement['annualReports'][i]['nonInterestIncome']),float(DataIncomeStatement['annualReports'][i]['otherNonOperatingIncome']),float(DataIncomeStatement['annualReports'][i]['depreciation']),float(DataIncomeStatement['annualReports'][i]['depreciationAndAmortization']),float(DataIncomeStatement['annualReports'][i]['incomeBeforeTax']),float(DataIncomeStatement['annualReports'][i]['incomeTaxExpense']),float(DataIncomeStatement['annualReports'][i]['interestAndDebtExpense']),float(DataIncomeStatement['annualReports'][i]['netIncomeFromContinuingOperations']),float(DataIncomeStatement['annualReports'][i]['comprehensiveIncomeNetOfTax']),float(DataIncomeStatement['annualReports'][i]['ebit']),float(DataIncomeStatement['annualReports'][i]['ebitda']),float(DataIncomeStatement['annualReports'][i]['netIncome'])))


    

#cur.execute(test)

#cur.execute("SELECT * FROM income_statement;")

#print(cur.fetchall())

conn.commit()

conn.close()

#print(test)

#print(DataIncomeStatement['annualReports'][0]['fiscalDateEnding'])

#for item in DataIncomeStatement['annualReports']:
#    print('                 ')
#    print(len(item))
#    print('                 ')
#    for key, value in item.items():
#        print(key,value)