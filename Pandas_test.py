import requests
import psycopg2


#This section provides credentials for AWS Database
DB_HOST = 'ls-8ac1ef06f8c0b721d61a89b671a2e10c40a7050f.cpsgene13aqe.eu-central-1.rds.amazonaws.com'
DB_NAME =  'Stocks'
DB_USER = 'dbmasteruser'
DB_PASS = 'RH6t.8|Ssd[g0y)jSA+c,)UP,V*<7^ZV'

Ticker ='IBM'

api_key='8JB4V49M6EBPR459'


url0 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ str(Ticker)+'&apikey=8JB4V49M6EBPR459'
r0 = requests.get(url0)
DataMain = r0.json()
#print(type(DataMain))
#for key, value in DataMain.items():
#print(len(DataMain))


url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ str(Ticker)+'&apikey='+str(api_key)
r = requests.get(url)
DataIncomeStatement = r.json()



conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,host=DB_HOST)
cur = conn.cursor()

#This loop provides cleaning data from 'None'. When there is no data provided alphavantage API returns None. We change all the Nones to 0
for i in range (len(DataIncomeStatement['annualReports'])):
    for key, value in DataIncomeStatement['annualReports'][i].items():
        if value == 'None':
            DataIncomeStatement['annualReports'][i].update({key:0})


cur.execute("INSERT INTO list_of_companies (Symbol,Description) VALUES(%s,%s)", (DataMain['Symbol'],DataMain['Description']))

#This loop is for writing anual data from the company Income Statement to database table Income Statement
i=0
for i in range (len(DataIncomeStatement['annualReports'])):
    cur.execute("INSERT INTO income_statement (ticker,fiscalDateEnding,reportedCurrency,grossProfit,totalRevenue,costOfRevenue,costofGoodsAndServicesSold,operatingIncome,sellingGeneralAndAdministrative,researchAndDevelopment,operatingExpenses,investmentIncomeNet,netInterestIncome,interestIncome,interestExpense,nonInterestIncome,otherNonOperatingIncome,depreciation,depreciationAndAmortization,incomeBeforeTax,incomeTaxExpense,interestAndDebtExpense,netIncomeFromContinuingOperations,comprehensiveIncomeNetOfTax,ebit,ebitda,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(Ticker,DataIncomeStatement['annualReports'][i]['fiscalDateEnding'],DataIncomeStatement['annualReports'][i]['reportedCurrency'],float(DataIncomeStatement['annualReports'][i]['grossProfit']),float(DataIncomeStatement['annualReports'][i]['totalRevenue']),float(DataIncomeStatement['annualReports'][i]['costOfRevenue']),float(DataIncomeStatement['annualReports'][i]['costofGoodsAndServicesSold']),float(DataIncomeStatement['annualReports'][i]['operatingIncome']),float(DataIncomeStatement['annualReports'][i]['sellingGeneralAndAdministrative']),float(DataIncomeStatement['annualReports'][i]['researchAndDevelopment']),float(DataIncomeStatement['annualReports'][i]['operatingExpenses']),float(DataIncomeStatement['annualReports'][i]['investmentIncomeNet']),float(DataIncomeStatement['annualReports'][i]['netInterestIncome']),float(DataIncomeStatement['annualReports'][i]['interestIncome']),float(DataIncomeStatement['annualReports'][i]['interestExpense']),float(DataIncomeStatement['annualReports'][i]['nonInterestIncome']),float(DataIncomeStatement['annualReports'][i]['otherNonOperatingIncome']),float(DataIncomeStatement['annualReports'][i]['depreciation']),float(DataIncomeStatement['annualReports'][i]['depreciationAndAmortization']),float(DataIncomeStatement['annualReports'][i]['incomeBeforeTax']),float(DataIncomeStatement['annualReports'][i]['incomeTaxExpense']),float(DataIncomeStatement['annualReports'][i]['interestAndDebtExpense']),float(DataIncomeStatement['annualReports'][i]['netIncomeFromContinuingOperations']),float(DataIncomeStatement['annualReports'][i]['comprehensiveIncomeNetOfTax']),float(DataIncomeStatement['annualReports'][i]['ebit']),float(DataIncomeStatement['annualReports'][i]['ebitda']),float(DataIncomeStatement['annualReports'][i]['netIncome'])))




#This string is for writing data from Overvier of the company to database table General_Information
cur.execute("INSERT INTO General_Information (Symbol,AssetType,Name,Description,CIK,Exchange,Currency,Country,Sector,Industry,Address,FiscalYearEnd,LatestQuarter,MarketCapitalization,EBITDA,PERatio,PEGRatio,BookValue,DividendPerShare,DividendYield,EPS,RevenuePerShareTTM,ProfitMargin,OperatingMarginTTM,ReturnOnAssetsTTM,ReturnOnEquityTTM,RevenueTTM,GrossProfitTTM,DilutedEPSTTM,QuarterlyEarningsGrowthYOY,QuarterlyRevenueGrowthYOY,AnalystTargetPrice,TrailingPE,ForwardPE,PriceToSalesRatioTTM,PriceToBookRatio,EVToRevenue,EVToEBITDA,Beta,_52WeekHigh,_52WeekLow,_50DayMovingAverage,_200DayMovingAverage,SharesOutstanding,DividendDate,ExDividendDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (DataMain['Symbol'],DataMain['AssetType'],DataMain['Name'],DataMain['Description'],DataMain['CIK'],DataMain['Exchange'],DataMain['Currency'],DataMain['Country'],DataMain['Sector'],DataMain['Industry'],DataMain['Address'],DataMain['FiscalYearEnd'],DataMain['LatestQuarter'],DataMain['MarketCapitalization'],DataMain['EBITDA'],DataMain['PERatio'],DataMain['PEGRatio'],DataMain['BookValue'],DataMain['DividendPerShare'],DataMain['DividendYield'],DataMain['EPS'],DataMain['RevenuePerShareTTM'],DataMain['ProfitMargin'],DataMain['OperatingMarginTTM'],DataMain['ReturnOnAssetsTTM'],DataMain['ReturnOnEquityTTM'],DataMain['RevenueTTM'],DataMain['GrossProfitTTM'],DataMain['DilutedEPSTTM'],DataMain['QuarterlyEarningsGrowthYOY'],DataMain['QuarterlyRevenueGrowthYOY'],DataMain['AnalystTargetPrice'],DataMain['TrailingPE'],DataMain['ForwardPE'],DataMain['PriceToSalesRatioTTM'],DataMain['PriceToBookRatio'],DataMain['EVToRevenue'],DataMain['EVToEBITDA'],DataMain['Beta'],DataMain['52WeekHigh'],DataMain['52WeekLow'],DataMain['50DayMovingAverage'],DataMain['200DayMovingAverage'],DataMain['SharesOutstanding'],DataMain['DividendDate'],DataMain['ExDividendDate']))


conn.commit()
conn.close()

