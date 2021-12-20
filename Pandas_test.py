import requests
import psycopg2
import xlrd
import time


#This section provides credentials for AWS Database
DB_HOST = 'ls-8ac1ef06f8c0b721d61a89b671a2e10c40a7050f.cpsgene13aqe.eu-central-1.rds.amazonaws.com'
DB_NAME =  'Stocks'
DB_USER = 'dbmasteruser'
DB_PASS = 'RH6t.8|Ssd[g0y)jSA+c,)UP,V*<7^ZV'
api_key='8JB4V49M6EBPR459'







loc = ("/Users/igortestoedov/DEV/InvestingWisely/InvestingWisely/Russell_2000.xls")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

TickersFromRussell2000 = []

for item1 in range(sheet.nrows):

    TickersFromRussell2000.append(sheet.cell_value(item1, 1))




conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,host=DB_HOST)
cur = conn.cursor()







for z in range (5):
    Ticker = TickersFromRussell2000[z]

    #Ticker = 'TSN'
    time.sleep(60)
    
    url0 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ str(Ticker)+'&apikey='+str(api_key)
    r0 = requests.get(url0)
    DataMain = r0.json()

    url1 = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ str(Ticker)+'&apikey='+str(api_key)
    r1 = requests.get(url1)
    DataIncomeStatement = r1.json()

    url2 = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol='+ str(Ticker)+'&apikey=8JB4V49M6EBPR459'
    r2 = requests.get(url2)
    DataBalanceSheet = r2.json()
    

    #This loop provides cleaning data from 'None'. When there is no data provided alphavantage API returns None. We change all the Nones to 0
    i=0
    for i in range (len(DataIncomeStatement['annualReports'])):
        for key, value in DataIncomeStatement['annualReports'][i].items():
            if value == 'None':
                print(key,'changed value to 0')
                DataIncomeStatement['annualReports'][i].update({key:None})

    i=0
    for i in range (len(DataBalanceSheet['annualReports'])):
        for key, value in DataBalanceSheet['annualReports'][i].items():
            if value == 'None':
                print(key,'changed value to actual None')
                DataBalanceSheet['annualReports'][i].update({key:None})



    #This string is for writing data from List of companies. This table must be created first before other tables. 
    cur.execute("INSERT INTO list_of_companies (Symbol,Name,Description,Sector,Industry,Country,Address) VALUES(%s,%s,%s,%s,%s,%s,%s)", (DataMain['Symbol'],DataMain['Name'],DataMain['Description'],DataMain['Sector'],DataMain['Industry'],DataMain['Country'],DataMain['Address']))

    #This loop is for writing anual data from the company Balance Sheet to database table balance_sheet
    i=0
    for i in range (len(DataBalanceSheet['annualReports'])):
        cur.execute("INSERT INTO balance_sheet (Symbol,fiscalDateEnding,reportedCurrency,totalAssets,totalCurrentAssets,cashAndCashEquivalentsAtCarryingValue,cashAndShortTermInvestments,inventory,currentNetReceivables,totalNonCurrentAssets,propertyPlantEquipment,accumulatedDepreciationAmortizationPPE,intangibleAssets,intangibleAssetsExcludingGoodwill,goodwill,investments,longTermInvestments,shortTermInvestments,otherCurrentAssets,otherNonCurrrentAssets,totalLiabilities,totalCurrentLiabilities,currentAccountsPayable,deferredRevenue,currentDebt,shortTermDebt,totalNonCurrentLiabilities,capitalLeaseObligations,longTermDebt,currentLongTermDebt,longTermDebtNoncurrent,shortLongTermDebtTotal,otherCurrentLiabilities,otherNonCurrentLiabilities,totalShareholderEquity,treasuryStock,retainedEarnings,commonStock,commonStockSharesOutstanding) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(DataMain['Symbol'],DataBalanceSheet['annualReports'][i]['fiscalDateEnding'],DataBalanceSheet['annualReports'][i]['reportedCurrency'],DataBalanceSheet['annualReports'][i]['totalAssets'],DataBalanceSheet['annualReports'][i]['totalCurrentAssets'],DataBalanceSheet['annualReports'][i]['cashAndCashEquivalentsAtCarryingValue'],DataBalanceSheet['annualReports'][i]['cashAndShortTermInvestments'],DataBalanceSheet['annualReports'][i]['inventory'],DataBalanceSheet['annualReports'][i]['currentNetReceivables'],DataBalanceSheet['annualReports'][i]['totalNonCurrentAssets'],DataBalanceSheet['annualReports'][i]['propertyPlantEquipment'],DataBalanceSheet['annualReports'][i]['accumulatedDepreciationAmortizationPPE'],DataBalanceSheet['annualReports'][i]['intangibleAssets'],DataBalanceSheet['annualReports'][i]['intangibleAssetsExcludingGoodwill'],DataBalanceSheet['annualReports'][i]['goodwill'],DataBalanceSheet['annualReports'][i]['investments'],DataBalanceSheet['annualReports'][i]['longTermInvestments'],DataBalanceSheet['annualReports'][i]['shortTermInvestments'],DataBalanceSheet['annualReports'][i]['otherCurrentAssets'],DataBalanceSheet['annualReports'][i]['otherNonCurrrentAssets'],DataBalanceSheet['annualReports'][i]['totalLiabilities'],DataBalanceSheet['annualReports'][i]['totalCurrentLiabilities'],DataBalanceSheet['annualReports'][i]['currentAccountsPayable'],DataBalanceSheet['annualReports'][i]['deferredRevenue'],DataBalanceSheet['annualReports'][i]['currentDebt'],DataBalanceSheet['annualReports'][i]['shortTermDebt'],DataBalanceSheet['annualReports'][i]['totalNonCurrentLiabilities'],DataBalanceSheet['annualReports'][i]['capitalLeaseObligations'],DataBalanceSheet['annualReports'][i]['longTermDebt'],DataBalanceSheet['annualReports'][i]['currentLongTermDebt'],DataBalanceSheet['annualReports'][i]['longTermDebtNoncurrent'],DataBalanceSheet['annualReports'][i]['shortLongTermDebtTotal'],DataBalanceSheet['annualReports'][i]['otherCurrentLiabilities'],DataBalanceSheet['annualReports'][i]['otherNonCurrentLiabilities'],DataBalanceSheet['annualReports'][i]['totalShareholderEquity'],DataBalanceSheet['annualReports'][i]['treasuryStock'],DataBalanceSheet['annualReports'][i]['retainedEarnings'],DataBalanceSheet['annualReports'][i]['commonStock'],DataBalanceSheet['annualReports'][i]['commonStockSharesOutstanding']))
    
    
    
    #This loop is for writing anual data from the company Income Statement to database table income_statement
    i=0
    for i in range (len(DataIncomeStatement['annualReports'])):
    #    cur.execute("INSERT INTO income_statement (ticker,fiscalDateEnding,reportedCurrency,grossProfit,totalRevenue,costOfRevenue,costofGoodsAndServicesSold,operatingIncome,sellingGeneralAndAdministrative,researchAndDevelopment,operatingExpenses,investmentIncomeNet,netInterestIncome,interestIncome,interestExpense,nonInterestIncome,otherNonOperatingIncome,depreciation,depreciationAndAmortization,incomeBeforeTax,incomeTaxExpense,interestAndDebtExpense,netIncomeFromContinuingOperations,comprehensiveIncomeNetOfTax,ebit,ebitda,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(DataMain['Symbol'],DataIncomeStatement['annualReports'][i]['fiscalDateEnding'],DataIncomeStatement['annualReports'][i]['reportedCurrency'],float(DataIncomeStatement['annualReports'][i]['grossProfit']),float(DataIncomeStatement['annualReports'][i]['totalRevenue']),float(DataIncomeStatement['annualReports'][i]['costOfRevenue']),float(DataIncomeStatement['annualReports'][i]['costofGoodsAndServicesSold']),float(DataIncomeStatement['annualReports'][i]['operatingIncome']),float(DataIncomeStatement['annualReports'][i]['sellingGeneralAndAdministrative']),float(DataIncomeStatement['annualReports'][i]['researchAndDevelopment']),float(DataIncomeStatement['annualReports'][i]['operatingExpenses']),float(DataIncomeStatement['annualReports'][i]['investmentIncomeNet']),float(DataIncomeStatement['annualReports'][i]['netInterestIncome']),float(DataIncomeStatement['annualReports'][i]['interestIncome']),float(DataIncomeStatement['annualReports'][i]['interestExpense']),float(DataIncomeStatement['annualReports'][i]['nonInterestIncome']),float(DataIncomeStatement['annualReports'][i]['otherNonOperatingIncome']),float(DataIncomeStatement['annualReports'][i]['depreciation']),float(DataIncomeStatement['annualReports'][i]['depreciationAndAmortization']),float(DataIncomeStatement['annualReports'][i]['incomeBeforeTax']),float(DataIncomeStatement['annualReports'][i]['incomeTaxExpense']),float(DataIncomeStatement['annualReports'][i]['interestAndDebtExpense']),float(DataIncomeStatement['annualReports'][i]['netIncomeFromContinuingOperations']),float(DataIncomeStatement['annualReports'][i]['comprehensiveIncomeNetOfTax']),float(DataIncomeStatement['annualReports'][i]['ebit']),float(DataIncomeStatement['annualReports'][i]['ebitda']),float(DataIncomeStatement['annualReports'][i]['netIncome'])))
        cur.execute("INSERT INTO income_statement (ticker,fiscalDateEnding,reportedCurrency,grossProfit,totalRevenue,costOfRevenue,costofGoodsAndServicesSold,operatingIncome,sellingGeneralAndAdministrative,researchAndDevelopment,operatingExpenses,investmentIncomeNet,netInterestIncome,interestIncome,interestExpense,nonInterestIncome,otherNonOperatingIncome,depreciation,depreciationAndAmortization,incomeBeforeTax,incomeTaxExpense,interestAndDebtExpense,netIncomeFromContinuingOperations,comprehensiveIncomeNetOfTax,ebit,ebitda,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(DataMain['Symbol'],DataIncomeStatement['annualReports'][i]['fiscalDateEnding'],DataIncomeStatement['annualReports'][i]['reportedCurrency'],DataIncomeStatement['annualReports'][i]['grossProfit'],DataIncomeStatement['annualReports'][i]['totalRevenue'],DataIncomeStatement['annualReports'][i]['costOfRevenue'],DataIncomeStatement['annualReports'][i]['costofGoodsAndServicesSold'],DataIncomeStatement['annualReports'][i]['operatingIncome'],DataIncomeStatement['annualReports'][i]['sellingGeneralAndAdministrative'],DataIncomeStatement['annualReports'][i]['researchAndDevelopment'],DataIncomeStatement['annualReports'][i]['operatingExpenses'],DataIncomeStatement['annualReports'][i]['investmentIncomeNet'],DataIncomeStatement['annualReports'][i]['netInterestIncome'],DataIncomeStatement['annualReports'][i]['interestIncome'],DataIncomeStatement['annualReports'][i]['interestExpense'],DataIncomeStatement['annualReports'][i]['nonInterestIncome'],DataIncomeStatement['annualReports'][i]['otherNonOperatingIncome'],DataIncomeStatement['annualReports'][i]['depreciation'],DataIncomeStatement['annualReports'][i]['depreciationAndAmortization'],DataIncomeStatement['annualReports'][i]['incomeBeforeTax'],DataIncomeStatement['annualReports'][i]['incomeTaxExpense'],DataIncomeStatement['annualReports'][i]['interestAndDebtExpense'],DataIncomeStatement['annualReports'][i]['netIncomeFromContinuingOperations'],DataIncomeStatement['annualReports'][i]['comprehensiveIncomeNetOfTax'],DataIncomeStatement['annualReports'][i]['ebit'],DataIncomeStatement['annualReports'][i]['ebitda'],DataIncomeStatement['annualReports'][i]['netIncome']))


    #This string is for writing data from Overvier of the company to database table General_Information
    print(Ticker,'has foloowing problems:')
    for key, value in DataMain.items():
        if value == 'None' or value =='-':
            print(key, 'changed value to None')
            DataMain.update({key:None})
        
    if DataMain['ExDividendDate'] == 0:
            DataMain['ExDividendDate'] = None
            print('ExDividendDate changed value to None')



    if DataMain['DividendDate'] == 0:
        DataMain['DividendDate'] = None    
        print('DividendDate changed value to None')
    

    cur.execute("INSERT INTO General_Information (Symbol,AssetType,Name,Description,CIK,Exchange,Currency,Country,Sector,Industry,Address,FiscalYearEnd,LatestQuarter,MarketCapitalization,EBITDA,PERatio,PEGRatio,BookValue,DividendPerShare,DividendYield,EPS,RevenuePerShareTTM,ProfitMargin,OperatingMarginTTM,ReturnOnAssetsTTM,ReturnOnEquityTTM,RevenueTTM,GrossProfitTTM,DilutedEPSTTM,QuarterlyEarningsGrowthYOY,QuarterlyRevenueGrowthYOY,AnalystTargetPrice,TrailingPE,ForwardPE,PriceToSalesRatioTTM,PriceToBookRatio,EVToRevenue,EVToEBITDA,Beta,_52WeekHigh,_52WeekLow,_50DayMovingAverage,_200DayMovingAverage,SharesOutstanding,DividendDate,ExDividendDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (DataMain['Symbol'],DataMain['AssetType'],DataMain['Name'],DataMain['Description'],DataMain['CIK'],DataMain['Exchange'],DataMain['Currency'],DataMain['Country'],DataMain['Sector'],DataMain['Industry'],DataMain['Address'],DataMain['FiscalYearEnd'],DataMain['LatestQuarter'],DataMain['MarketCapitalization'],DataMain['EBITDA'],DataMain['PERatio'],DataMain['PEGRatio'],DataMain['BookValue'],DataMain['DividendPerShare'],DataMain['DividendYield'],DataMain['EPS'],DataMain['RevenuePerShareTTM'],DataMain['ProfitMargin'],DataMain['OperatingMarginTTM'],DataMain['ReturnOnAssetsTTM'],DataMain['ReturnOnEquityTTM'],DataMain['RevenueTTM'],DataMain['GrossProfitTTM'],DataMain['DilutedEPSTTM'],DataMain['QuarterlyEarningsGrowthYOY'],DataMain['QuarterlyRevenueGrowthYOY'],DataMain['AnalystTargetPrice'],DataMain['TrailingPE'],DataMain['ForwardPE'],DataMain['PriceToSalesRatioTTM'],DataMain['PriceToBookRatio'],DataMain['EVToRevenue'],DataMain['EVToEBITDA'],DataMain['Beta'],DataMain['52WeekHigh'],DataMain['52WeekLow'],DataMain['50DayMovingAverage'],DataMain['200DayMovingAverage'],DataMain['SharesOutstanding'],DataMain['DividendDate'],DataMain['ExDividendDate']))


conn.commit()
conn.close()

