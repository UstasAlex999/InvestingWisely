
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.alphavantage import AlphaVantage
from pandas.core.frame import DataFrame
import requests
import xlsxwriter
import time
from nltk import flatten
from pandas.core.common import flatten
import xlrd

loc = ("/Users/igortestoedov/DEV/InvestingWisely/InvestingWisely/Russell_2000.xls")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

#print("{0} {1} {2}".format(sheet.name, sheet.nrows, sheet.ncols))

OutTicker = []

TickersFromRussell2000 = []

for item1 in range(sheet.nrows):

    TickersFromRussell2000.append(sheet.cell_value(item1, 1))
    #print(sheet.cell_value(item1, 1))



#print(len(TickersFromRussell2000))








def GetAndWriteToPandas (Ticker):

    api_key='8JB4V49M6EBPR459'

    url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ str(Ticker)+'&apikey=8JB4V49M6EBPR459'
    r = requests.get(url)
    DataIncomeStatement = r.json()

    #print(DataIncomeStatement)

    url2 = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol='+ str(Ticker)+'&apikey=8JB4V49M6EBPR459'
    r2 = requests.get(url2)
    DataCashFlow = r2.json()

    #print(DataCashFlow)

    url3 = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol='+ str(Ticker)+'&apikey=8JB4V49M6EBPR459'
    r3 = requests.get(url3)
    DataBalanceSheet = r3.json()
    #print(DataBalanceSheet)

    #print(DataBalanceSheet)

    url4 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ str(Ticker)+'&apikey=8JB4V49M6EBPR459'
    r4 = requests.get(url4)
    DataOverview = r4.json()
    print(DataOverview)

    ListOfTotalSales = []
    ListOfROIC = []
    ListOFEPS =[]
    ListOFTotalShareholderEquity = []
    ListOFFreeCashFlow = []
    ListOfTickers = []
    ListOfYears = []
    ListOfTotalSalesGrowth = []
    ListOfROICGrowth = []
    ListOFEPSGrowth =[]
    ListOFTotalShareholderEquityGrowth = []
    ListOFFreeCashFlowGrowth = []
    listOFErrors = []
    ListOFErrorsTicker = []
    ListOfErrorTickerFinal = []
    ListOFSector = []
    ListOFIndustry = []
    
    xx = len(DataCashFlow['annualReports'])
    
    print(xx)

    #print('Company','|','Year','|','ROIC','|', 'Revenue growth YtY', '|', "EPS Growth", '|','Total Shareholders Equity', '|', 'Free Cash Flow Change' )
    
    # I use this loop to calculate ROIC, and add to Lists numbers which i use later to calculate growth rates

    for i in range (xx):

        NetIncome = float((DataIncomeStatement['annualReports'][i]['netIncome']))
        CommonStockSharesOutstanding = int((DataBalanceSheet['annualReports'][i]['commonStockSharesOutstanding']))
        EPS = NetIncome/CommonStockSharesOutstanding
        
        TotalShareholderEquity = float((DataBalanceSheet['annualReports'][i]['totalShareholderEquity']))
        CapitalExpenditures = float((DataCashFlow['annualReports'][i]['capitalExpenditures']))
        OperatingCashflow = float((DataCashFlow['annualReports'][i]['operatingCashflow']))
        FreeCashFlow = OperatingCashflow - CapitalExpenditures
     
        
        if DataIncomeStatement['annualReports'][i]['totalRevenue'] == 'None':
            DataIncomeStatement['annualReports'][i]['totalRevenue'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok')

        
        TotalRevenue = float((DataIncomeStatement['annualReports'][i]['totalRevenue']))
        
        if DataIncomeStatement['annualReports'][i]['costOfRevenue'] == 'None':
            DataIncomeStatement['annualReports'][i]['costOfRevenue'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok') 
        
        CostOfRevenue = float((DataIncomeStatement['annualReports'][i]['costOfRevenue']))
        
        MyGrossProfit = TotalRevenue - CostOfRevenue
        GrossProfit = float((DataIncomeStatement['annualReports'][i]['grossProfit']))
        
        if DataIncomeStatement['annualReports'][i]['incomeBeforeTax'] == 'None':
            DataIncomeStatement['annualReports'][i]['incomeBeforeTax'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok')

        
        IncomeBeforeTax = float((DataIncomeStatement['annualReports'][i]['incomeBeforeTax']))
        
        if DataIncomeStatement['annualReports'][i]['operatingIncome'] == 'None':
            DataIncomeStatement['annualReports'][i]['operatingIncome'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok')
        OperatingIncome = float((DataIncomeStatement['annualReports'][i]['operatingIncome']))
        
        if DataIncomeStatement['annualReports'][i]['incomeTaxExpense'] == 'None':
            DataIncomeStatement['annualReports'][i]['incomeTaxExpense'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok')

        IncomeTaxExpense = float((DataIncomeStatement['annualReports'][i]['incomeTaxExpense']))
        Tax_Rate = IncomeTaxExpense/IncomeBeforeTax
        Tax_Rate_Percentage = "{:.0%}".format(Tax_Rate)
        NOPAT=OperatingIncome*(1-Tax_Rate)    
     
        #print(DataBalanceSheet['annualReports'][i]['shortTermDebt'])
        if DataBalanceSheet['annualReports'][i]['shortTermDebt'] == 'None':
            DataBalanceSheet['annualReports'][i]['shortTermDebt'] = -1
            print('no data')
            listOFErrors.append('No Data')
        else:
            listOFErrors.append('ok')
            print('ok')

        ShortTermDebt = float((DataBalanceSheet['annualReports'][i]['shortTermDebt']))

        if DataBalanceSheet['annualReports'][i]['longTermDebt'] == 'None':
            DataBalanceSheet['annualReports'][i]['longTermDebt'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok')

        LongTermDebt = float((DataBalanceSheet['annualReports'][i]['longTermDebt']))

        if DataBalanceSheet['annualReports'][i]['totalShareholderEquity'] == 'None':
            DataBalanceSheet['annualReports'][i]['totalShareholderEquity'] = -1
            listOFErrors.append('No Data')
            print('no data')
        else:
            listOFErrors.append('ok')
            print('ok')

        TotalShareholderEquity = float((DataBalanceSheet['annualReports'][i]['totalShareholderEquity']))
   
        InvestedCapital = ShortTermDebt + LongTermDebt + TotalShareholderEquity
    
        ROIC = NOPAT/InvestedCapital
        ROIC_percentage = "{:.0%}".format(ROIC)

    #print(DataCashFlow['annualReports'][i]['fiscalDateEnding'],'IncomeTaxExpense/${0}'.format(format(IncomeTaxExpense, ',.2f')),'/','IncomeBeforeTax/${0}'.format(format(IncomeBeforeTax, ',.2f')),'OperatingIncome ${0}'.format(format(OperatingIncome, ',.2f')))
    
    #print(DataCashFlow['annualReports'][i]['fiscalDateEnding'],'operatingCashflow ${0}'.format(format(OCF, ',.2f')),'totalRevenue ${0}'.format(format(TotalRevenue, ',.2f')),'CostOfRevenue ${0}'.format(format(CostOfRevenue, ',.2f')),'GrossProfit ${0}'.format(format(GrossProfit, ',.2f')),'IncomeBeforeTax ${0}'.format(format(IncomeBeforeTax, ',.2f')),'OperatingIncome ${0}'.format(format(OperatingIncome, ',.2f')),'IncomeTaxExpense ${0}'.format(format(IncomeTaxExpense, ',.2f'))) 
    #print('Tax rate:', Tax_Rate_Percentage)
    #print('NOPAT$ {0}'.format(format(IncomeBeforeTax, ',.2f')))
        ListOfROIC.append(ROIC_percentage)
        ListOfTotalSales.append(TotalRevenue)
        ListOFEPS.append(EPS)
        ListOFTotalShareholderEquity.append(TotalShareholderEquity)
        ListOFFreeCashFlow.append(FreeCashFlow)
    
    
        if (i == xx-1):
            ListOfTotalSales.append(1)
            ListOfROIC.append(1)
            ListOFEPS.append(1)
            ListOFTotalShareholderEquity.append(1)
            ListOFFreeCashFlow.append(1)
            #listOFErrors.append(1)

        print(listOFErrors)
        
        result = listOFErrors.count('ok') == len(listOFErrors)
        #print(result)
        ListOFErrorsTicker.append(result)
        listOFErrors.clear()
    
    result2 =  ListOFErrorsTicker.count(True) == len(ListOFErrorsTicker)
    
    #print(result2)
    #print(len(listOFErrors))    
        
        
    


    #outWorkbook = xlsxwriter.Workbook('out.xlsx')
    #outSheet = outWorkbook.add_worksheet()
    #outSheet.write("A1", 'Company') 
    #outSheet.write("B1", 'Year') 
    #outSheet.write("C1", 'ROIC')
    #outSheet.write("D1", 'Revenue growth YtY')  
    #outSheet.write("E1", 'EPS Growth')  
    #outSheet.write("F1", 'Total Shareholders Equity Growth')  
    #outSheet.write("G1", 'Free Cash Flow Change')  




    for i in range (xx):                
        TotalRevenueChangeYtY = ((ListOfTotalSales[i]-ListOfTotalSales[i+1])/ListOfTotalSales[i+1])
        TotalRevenuePercentageYtY = "{:.0%}".format(TotalRevenueChangeYtY)
        TotalEPSChange = (ListOFEPS[i]-ListOFEPS[i+1])/ListOFEPS[i+1]
        TotalEPSChangePercentage = "{:.0%}".format(TotalEPSChange)
        TotalShareholderEquityChange = (ListOFTotalShareholderEquity[i]-ListOFTotalShareholderEquity[i+1])/ListOFTotalShareholderEquity[i+1]
        TotalShareholderEquityChangePercentage = "{:.0%}".format(TotalShareholderEquityChange)
        ListOFFreeCashFlowChange = (ListOFFreeCashFlow[i]-ListOFFreeCashFlow[i+1])/ListOFFreeCashFlow[i+1]
        ListOFFreeCashFlowChangePercentage = "{:.0%}".format(ListOFFreeCashFlowChange)
        #print(DataIncomeStatement['symbol'],DataCashFlow['annualReports'][i]['fiscalDateEnding'],ListOfROIC[i],TotalRevenuePercentageYtY,TotalEPSChangePercentage,TotalShareholderEquityChangePercentage,ListOFFreeCashFlowChangePercentage)
    
        #outSheet.write(i+1,0,DataIncomeStatement['symbol'])
        #outSheet.write(i+1,1,DataCashFlow['annualReports'][i]['fiscalDateEnding'])
        #outSheet.write(i+1,2,ListOfROIC[i])
        #outSheet.write(i+1,3,TotalRevenuePercentageYtY)
        #outSheet.write(i+1,4,TotalEPSChangePercentage)
        #outSheet.write(i+1,5,TotalShareholderEquityChangePercentage)
        #outSheet.write(i+1,6,ListOFFreeCashFlowChangePercentage)
    
        ListOfTotalSalesGrowth.append(TotalRevenuePercentageYtY)
        ListOfTickers.append(DataIncomeStatement['symbol'])
        ListOFIndustry.append(DataOverview['Industry'])
        ListOFSector.append(DataOverview['Sector'])
        ListOfYears.append(DataCashFlow['annualReports'][i]['fiscalDateEnding'])
        ListOFEPSGrowth.append(TotalEPSChangePercentage)
        ListOFTotalShareholderEquityGrowth.append(TotalShareholderEquityChangePercentage)
        ListOFFreeCashFlowGrowth.append(ListOFFreeCashFlowChangePercentage)
        ListOfErrorTickerFinal.append(result2)

    

    #outWorkbook.close()


    ListOfROIC.pop()
    ListOfROIC.pop()
    ListOfTickers.pop()
    ListOFSector.pop()
    ListOFIndustry.pop()
    ListOfTotalSalesGrowth.pop()
    ListOfYears.pop()
    ListOFEPSGrowth.pop()
    ListOFTotalShareholderEquityGrowth.pop()
    ListOFFreeCashFlowGrowth.pop()
    ListOfErrorTickerFinal.pop()
    

    

    #df = DataFrame.append({'Ticker':ListOfTickers,'Year':ListOfYears, 'TotalRevenueChangeYtY':ListOfTotalSalesGrowth,'ROIC':ListOfROIC,'EPS Growth':ListOFEPSGrowth,'Total Shareholders Equity Growth':ListOFTotalShareholderEquityGrowth, 'Free Cash Flow Change':ListOFFreeCashFlowGrowth})
    #print(df.head(5))
    
    return ListOFIndustry, ListOFSector,ListOfTickers,ListOfYears,ListOfTotalSalesGrowth,ListOfROIC,ListOFEPSGrowth,ListOFTotalShareholderEquityGrowth,ListOFFreeCashFlowGrowth, ListOfErrorTickerFinal 


 
ListOfTickersFinal = []
ListOfSectorFinal =[]
ListOFIndustryFinal =[]
ListOfYearsFinal = []
ListOfTotalSalesGrowthFinal = []
ListOfROICFinal = []
ListOFEPSGrowthFinal = []
ListOFTotalShareholderEquityGrowthFinal = []
ListOFFreeCashFlowGrowthFinal=[]
ListOFErrorsTickerFinal2 = []

OutTicker = []

for i in range (30):
    
    OutTicker.append(TickersFromRussell2000[i])



for item in OutTicker:
    
    try:
        ListOFIndustry, ListOFSector, ListOfTickers,ListOfYears,ListOfTotalSalesGrowth,ListOfROIC,ListOFEPSGrowth,ListOFTotalShareholderEquityGrowth,ListOFFreeCashFlowGrowth,result = (GetAndWriteToPandas(item))
        time.sleep(60)
        ListOFIndustryFinal.append(ListOFIndustry)
        ListOfSectorFinal.append(ListOFSector)
        ListOfTickersFinal.append(ListOfTickers)
        ListOfYearsFinal.append(ListOfYears)
        ListOfTotalSalesGrowthFinal.append(ListOfTotalSalesGrowth)
        ListOfROICFinal.append(ListOfROIC)
        ListOFEPSGrowthFinal.append(ListOFEPSGrowth)
        ListOFTotalShareholderEquityGrowthFinal.append(ListOFTotalShareholderEquityGrowth)
        ListOFFreeCashFlowGrowthFinal.append(ListOFFreeCashFlowGrowth)
        ListOFErrorsTickerFinal2.append(result)
    except:
        print('FALSE')
        ListOFIndustryFinal.append('FALSE')
        ListOfSectorFinal.append('FALSE')
        ListOfTickersFinal.append('FALSE')
        ListOfYearsFinal.append('FALSE')
        ListOfTotalSalesGrowthFinal.append('FALSE')
        ListOfROICFinal.append('FALSE')
        ListOFEPSGrowthFinal.append('FALSE')
        ListOFTotalShareholderEquityGrowthFinal.append('FALSE')
        ListOFFreeCashFlowGrowthFinal.append('FALSE')
        ListOFErrorsTickerFinal2.append('FALSE')
    

ListOFIndustryFinalFlattened = list(flatten(ListOFIndustryFinal))
ListOfSectorFinalFlattened = list(flatten(ListOfSectorFinal))
ListOfTickersFinalFlattened = list(flatten(ListOfTickersFinal))
ListOfYearsFinalFlattened = list(flatten(ListOfYearsFinal))
ListOfTotalSalesGrowthFinalFlattened = list(flatten(ListOfTotalSalesGrowthFinal))
ListOfROICFinalFlattened = list(flatten(ListOfROICFinal))
ListOFEPSGrowthFinalFlattened = list(flatten(ListOFEPSGrowthFinal))
ListOFTotalShareholderEquityGrowthFinalFlattened = list(flatten(ListOFTotalShareholderEquityGrowthFinal))
ListOFFreeCashFlowGrowthFinalFlattened = list(flatten(ListOFFreeCashFlowGrowthFinal))
ListOFErrorsTickerFinal2Flattened = list(flatten(ListOFErrorsTickerFinal2))

#print(ListOFErrorsTickerFinal,ListOfTickersFinalFlattened)



#print(ListOfTickersFinalFlattened)
#print(ListOFFreeCashFlowGrowthFinalFlattened,ListOFErrorsTickerFinal2Flattened)


df = DataFrame({'Industry':ListOFIndustryFinalFlattened, 'Sector':ListOfSectorFinalFlattened,'Ticker':ListOfTickersFinalFlattened,'Fiscal Year':ListOfYearsFinalFlattened,'SalesGrthYtY':ListOfTotalSalesGrowthFinalFlattened,'ROIC':ListOfROICFinalFlattened,'EPS GrthYtY':ListOFEPSGrowthFinalFlattened,'Equity Grth YtY':ListOFTotalShareholderEquityGrowthFinalFlattened,'FCF YtY':ListOFFreeCashFlowGrowthFinalFlattened,'Error':ListOFErrorsTickerFinal2Flattened})


df.to_excel('/Users/igortestoedov/DEV/InvestingWisely/InvestingWisely/Russell_2000_growth_rates.xls')

#print(xx)
#print(flattened_list)

print(df.head(14))

