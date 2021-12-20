import requests
import psycopg2
import xlrd
import time
from collections import Counter




#This section provides credentials for AWS Database
DB_HOST = 'ls-8ac1ef06f8c0b721d61a89b671a2e10c40a7050f.cpsgene13aqe.eu-central-1.rds.amazonaws.com'
DB_NAME =  'Stocks'
DB_USER = 'dbmasteruser'
DB_PASS = 'RH6t.8|Ssd[g0y)jSA+c,)UP,V*<7^ZV'
api_key='8JB4V49M6EBPR459'


#This variable stores path and file name of excell file with the list of 505 companies included in S&P500
loc = ("/Users/igortestoedov/DEV/InvestingWisely/InvestingWisely/S&P500.xls")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

#Adding companies' tickers to the list SandP500
SandP500 = []
for item1 in range(sheet.nrows):
    SandP500.append(sheet.cell_value(item1, 0))



#Creating connection to postgreSQL in aws
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,host=DB_HOST)
cur = conn.cursor()


def Calculate_Revenue_Growth_Rate(List_of_Symbols): 

    ListForSQLqueries = []
    itemTicker = []

    for item in List_of_Symbols:

        postgreSQL_select_Query3 = """select totalrevenue,fiscalDateEnding from income_statement where Symbol = '"""+str(item[0])+"""';"""
        ListForSQLqueries.append(postgreSQL_select_Query3)
        itemTicker.append(item[0])
        
    

    #Each iteration of the loop we calculate 4 years of growth of each company from the list "ListForSQLqueries"
    for i in range (len(ListForSQLqueries)):
        cur.execute(ListForSQLqueries[i])

        #This list stores 5 tulips which represent 5 years of revenue and fiscal years for each company
        data_to_analyzise2 = cur.fetchall()

        #We store ticker here in order to insert it into the table my_multipliers in database         
        tempTicker = itemTicker[i]

        #the revenue for each year is stored here
        VAR_TEMP2 = []
        #list for storing growth rate year to year
        YtYGrRate_List = []
        #Coresponding fiscal year is stored here
        VAR_TEMP3 = []

        #I decided that I need ецщ lists. VAR_TEMP2 is used to allow subtracting current year revenue from last year 
        for item in data_to_analyzise2:
            VAR_TEMP2.append(item[0])
            VAR_TEMP3.append(item[1])

        for i in range (len(VAR_TEMP2)):
            
            if i==len(VAR_TEMP2)-1:
                YtYGrRate_List.append(None)
            

            else:
                YtYGrRate = (VAR_TEMP2[i]-VAR_TEMP2[i+1])/VAR_TEMP2[i+1]
            #    print("{:.0%}".format(YtYGrRate))
                YtYGrRate_List.append(YtYGrRate)
            #    print()

        #print(YtYGrRate_List)
        data = YtYGrRate_List[0]
        #print(VAR_TEMP3)
        
        for i in range (len(YtYGrRate_List)):
            data = YtYGrRate_List[i]
            cur.execute("INSERT INTO my_multipliers (Symbol,YtYRevenueGrthRate,fiscalDateEnding) VALUES(%s,%s,%s)", (tempTicker, data,VAR_TEMP3[i]))
        conn.commit()







def FilltheDataIntoSQL(Ticker):

    url0 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ str(Ticker)+'&apikey='+str(api_key)
    r0 = requests.get(url0)
    DataMain = r0.json()

    url1 = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ str(Ticker)+'&apikey='+str(api_key)
    r1 = requests.get(url1)
    DataIncomeStatement = r1.json()

    url2 = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol='+ str(Ticker)+'&apikey='+str(api_key)
    r2 = requests.get(url2)
    DataBalanceSheet = r2.json()

    url3 = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol='+ str(Ticker)+'&apikey='+str(api_key)
    r3 = requests.get(url3)
    DataCashFlow = r3.json()
    

    #for key, value in DataCashFlow['annualReports'][0].items():
    #    print(key)
    print('                                           ')
    print('----------',Ticker,'-----------------------')
    print('                                           ')

    i=0
    for i in range (len(DataCashFlow['annualReports'])):
        for key, value in DataCashFlow['annualReports'][i].items():
            if value == 'None':
                print('There is no data at ', key,'. The value is changed to None for year', DataCashFlow['annualReports'][i]['fiscalDateEnding'])
                DataCashFlow['annualReports'][i].update({key:None})

    #This loop provides cleaning data from 'None'. When there is no data provided alphavantage API returns None. We change all the Nones to 0
    i=0
    for i in range (len(DataIncomeStatement['annualReports'])):
        for key, value in DataIncomeStatement['annualReports'][i].items():
            if value == 'None':
                print('There is no data at ',key,' The value is changed to None for year', DataIncomeStatement['annualReports'][i]['fiscalDateEnding'])
                DataIncomeStatement['annualReports'][i].update({key:None})

    i=0
    for i in range (len(DataBalanceSheet['annualReports'])):
        for key, value in DataBalanceSheet['annualReports'][i].items():
            if value == 'None':
                print('There is no data at ', key,'The values is changed to None for year',DataBalanceSheet['annualReports'][i]['fiscalDateEnding'])
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
        cur.execute("INSERT INTO income_statement (Symbol,fiscalDateEnding,reportedCurrency,grossProfit,totalRevenue,costOfRevenue,costofGoodsAndServicesSold,operatingIncome,sellingGeneralAndAdministrative,researchAndDevelopment,operatingExpenses,investmentIncomeNet,netInterestIncome,interestIncome,interestExpense,nonInterestIncome,otherNonOperatingIncome,depreciation,depreciationAndAmortization,incomeBeforeTax,incomeTaxExpense,interestAndDebtExpense,netIncomeFromContinuingOperations,comprehensiveIncomeNetOfTax,ebit,ebitda,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(DataMain['Symbol'],DataIncomeStatement['annualReports'][i]['fiscalDateEnding'],DataIncomeStatement['annualReports'][i]['reportedCurrency'],DataIncomeStatement['annualReports'][i]['grossProfit'],DataIncomeStatement['annualReports'][i]['totalRevenue'],DataIncomeStatement['annualReports'][i]['costOfRevenue'],DataIncomeStatement['annualReports'][i]['costofGoodsAndServicesSold'],DataIncomeStatement['annualReports'][i]['operatingIncome'],DataIncomeStatement['annualReports'][i]['sellingGeneralAndAdministrative'],DataIncomeStatement['annualReports'][i]['researchAndDevelopment'],DataIncomeStatement['annualReports'][i]['operatingExpenses'],DataIncomeStatement['annualReports'][i]['investmentIncomeNet'],DataIncomeStatement['annualReports'][i]['netInterestIncome'],DataIncomeStatement['annualReports'][i]['interestIncome'],DataIncomeStatement['annualReports'][i]['interestExpense'],DataIncomeStatement['annualReports'][i]['nonInterestIncome'],DataIncomeStatement['annualReports'][i]['otherNonOperatingIncome'],DataIncomeStatement['annualReports'][i]['depreciation'],DataIncomeStatement['annualReports'][i]['depreciationAndAmortization'],DataIncomeStatement['annualReports'][i]['incomeBeforeTax'],DataIncomeStatement['annualReports'][i]['incomeTaxExpense'],DataIncomeStatement['annualReports'][i]['interestAndDebtExpense'],DataIncomeStatement['annualReports'][i]['netIncomeFromContinuingOperations'],DataIncomeStatement['annualReports'][i]['comprehensiveIncomeNetOfTax'],DataIncomeStatement['annualReports'][i]['ebit'],DataIncomeStatement['annualReports'][i]['ebitda'],DataIncomeStatement['annualReports'][i]['netIncome']))

    #This loop is for writing anual data from the company Statement of CashFlow to database table statement_of_cashflow
    i=0
    for i in range (len(DataCashFlow['annualReports'])):
        #DataCashFlow['annualReports'][i]['totalAssets']
        cur.execute("INSERT INTO statement_of_cashflow (Symbol,fiscalDateEnding,reportedCurrency,operatingCashflow,paymentsForOperatingActivities,proceedsFromOperatingActivities,changeInOperatingLiabilities,changeInOperatingAssets,depreciationDepletionAndAmortization,capitalExpenditures,changeInReceivables,changeInInventory,profitLoss,cashflowFromInvestment,cashflowFromFinancing,proceedsFromRepaymentsOfShortTermDebt,paymentsForRepurchaseOfCommonStock,paymentsForRepurchaseOfEquity,paymentsForRepurchaseOfPreferredStock,dividendPayout,dividendPayoutCommonStock,dividendPayoutPreferredStock,proceedsFromIssuanceOfCommonStock,proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet,proceedsFromIssuanceOfPreferredStock,proceedsFromRepurchaseOfEquity,proceedsFromSaleOfTreasuryStock,changeInCashAndCashEquivalents,changeInExchangeRate,netIncome) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(DataMain['Symbol'],DataCashFlow['annualReports'][i]['fiscalDateEnding'],DataCashFlow['annualReports'][i]['reportedCurrency'],DataCashFlow['annualReports'][i]['operatingCashflow'],DataCashFlow['annualReports'][i]['paymentsForOperatingActivities'],DataCashFlow['annualReports'][i]['proceedsFromOperatingActivities'],DataCashFlow['annualReports'][i]['changeInOperatingLiabilities'],DataCashFlow['annualReports'][i]['changeInOperatingAssets'],DataCashFlow['annualReports'][i]['depreciationDepletionAndAmortization'],DataCashFlow['annualReports'][i]['capitalExpenditures'],DataCashFlow['annualReports'][i]['changeInReceivables'],DataCashFlow['annualReports'][i]['changeInInventory'],DataCashFlow['annualReports'][i]['profitLoss'],DataCashFlow['annualReports'][i]['cashflowFromInvestment'],DataCashFlow['annualReports'][i]['cashflowFromFinancing'],DataCashFlow['annualReports'][i]['proceedsFromRepaymentsOfShortTermDebt'],DataCashFlow['annualReports'][i]['paymentsForRepurchaseOfCommonStock'],DataCashFlow['annualReports'][i]['paymentsForRepurchaseOfEquity'],DataCashFlow['annualReports'][i]['paymentsForRepurchaseOfPreferredStock'],DataCashFlow['annualReports'][i]['dividendPayout'],DataCashFlow['annualReports'][i]['dividendPayoutCommonStock'],DataCashFlow['annualReports'][i]['dividendPayoutPreferredStock'],DataCashFlow['annualReports'][i]['proceedsFromIssuanceOfCommonStock'],DataCashFlow['annualReports'][i]['proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet'],DataCashFlow['annualReports'][i]['proceedsFromIssuanceOfPreferredStock'],DataCashFlow['annualReports'][i]['proceedsFromRepurchaseOfEquity'],DataCashFlow['annualReports'][i]['proceedsFromSaleOfTreasuryStock'],DataCashFlow['annualReports'][i]['changeInCashAndCashEquivalents'],DataCashFlow['annualReports'][i]['changeInExchangeRate'],DataCashFlow['annualReports'][i]['netIncome']))

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



#i=0
#for i in range (10):
#    time.sleep(60)
#    Ticker = SandP500[i]
    #try: 
#    FilltheDataIntoSQL(Ticker)
    #except:
    #print('Some error occured with Ticker ',Ticker )
        

postgreSQL_select_Query2 = "select symbol from list_of_companies;"
cur.execute(postgreSQL_select_Query2)
List_of_Symbols = cur.fetchall()

Calculate_Revenue_Growth_Rate(List_of_Symbols)

#conn.commit()

conn.close()

