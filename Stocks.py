
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.alphavantage import AlphaVantage
import requests
import xlsxwriter


Ticker = input ('Enter ticker:')


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

url4 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ str(Ticker)+'M&apikey=8JB4V49M6EBPR459'
r4 = requests.get(url4)
DataOverview = r4.json()

#print(DataOverview)

ListOfTotalSales = []
ListOfROIC = []
ListOFEPS =[]
ListOFTotalShareholderEquity = []
ListOFFreeCashFlow = []

xx = len(DataCashFlow['annualReports'])


print('Company','|','Year','|','ROIC','|', 'Revenue growth YtY', '|', "EPS Growth", '|','Total Shareholders Equity', '|', 'Free Cash Flow Change' )

for i in range (xx):
    NetIncome = float((DataIncomeStatement['annualReports'][i]['netIncome']))
    CommonStockSharesOutstanding = int((DataBalanceSheet['annualReports'][i]['commonStockSharesOutstanding']))
    EPS = NetIncome/CommonStockSharesOutstanding
    TotalShareholderEquity = float((DataBalanceSheet['annualReports'][i]['totalShareholderEquity']))
    CapitalExpenditures = float((DataCashFlow['annualReports'][i]['capitalExpenditures']))
    OperatingCashflow = float((DataCashFlow['annualReports'][i]['operatingCashflow']))
    FreeCashFlow = OperatingCashflow - CapitalExpenditures
    OCF = float(DataCashFlow['annualReports'][i]['operatingCashflow'])
    TotalRevenue = float((DataIncomeStatement['annualReports'][i]['totalRevenue']))
    CostOfRevenue = float((DataIncomeStatement['annualReports'][i]['costOfRevenue']))
    MyGrossProfit = TotalRevenue - CostOfRevenue
    GrossProfit = float((DataIncomeStatement['annualReports'][i]['grossProfit']))
    IncomeBeforeTax = float((DataIncomeStatement['annualReports'][i]['incomeBeforeTax']))
    OperatingIncome = float((DataIncomeStatement['annualReports'][i]['operatingIncome']))
    IncomeTaxExpense = float((DataIncomeStatement['annualReports'][i]['incomeTaxExpense']))
    Tax_Rate = IncomeTaxExpense/IncomeBeforeTax
    Tax_Rate_Percentage = "{:.0%}".format(Tax_Rate)
    NOPAT=OperatingIncome*(1-Tax_Rate)    
     
    ShortTermDebt = float((DataBalanceSheet['annualReports'][i]['shortTermDebt']))
    LongTermDebt = float((DataBalanceSheet['annualReports'][i]['longTermDebt']))
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
    


outWorkbook = xlsxwriter.Workbook('out.xlsx')
outSheet = outWorkbook.add_worksheet()
outSheet.write("A1", 'Company') 
outSheet.write("B1", 'Year') 
outSheet.write("C1", 'ROIC')
outSheet.write("D1", 'Revenue growth YtY')  
outSheet.write("E1", 'EPS Growth')  
outSheet.write("F1", 'Total Shareholders Equity')  
outSheet.write("G1", 'Free Cash Flow Change')  




for i in range (xx):                
    TotalRevenueChangeYtY = ((ListOfTotalSales[i]-ListOfTotalSales[i+1])/ListOfTotalSales[i+1])
    TotalRevenuePercentageYtY = "{:.0%}".format(TotalRevenueChangeYtY)
    TotalEPSChange = (ListOFEPS[i]-ListOFEPS[i+1])/ListOFEPS[i+1]
    TotalEPSChangePercentage = "{:.0%}".format(TotalEPSChange)
    TotalShareholderEquityChange = (ListOFTotalShareholderEquity[i]-ListOFTotalShareholderEquity[i+1])/ListOFTotalShareholderEquity[i+1]
    TotalShareholderEquityChangePercentage = "{:.0%}".format(TotalShareholderEquityChange)
    ListOFFreeCashFlowChange = (ListOFFreeCashFlow[i]-ListOFFreeCashFlow[i+1])/ListOFFreeCashFlow[i+1]
    ListOFFreeCashFlowChangePercentage = "{:.0%}".format(ListOFFreeCashFlowChange)
    print(DataIncomeStatement['symbol'],DataCashFlow['annualReports'][i]['fiscalDateEnding'],ListOfROIC[i],TotalRevenuePercentageYtY,TotalEPSChangePercentage,TotalShareholderEquityChangePercentage,ListOFFreeCashFlowChangePercentage)
    outSheet.write(i+1,0,DataIncomeStatement['symbol'])
    outSheet.write(i+1,1,DataCashFlow['annualReports'][i]['fiscalDateEnding'])
    outSheet.write(i+1,2,ListOfROIC[i])
    outSheet.write(i+1,3,TotalRevenuePercentageYtY)
    outSheet.write(i+1,4,TotalEPSChangePercentage)
    outSheet.write(i+1,5,TotalShareholderEquityChangePercentage)
    outSheet.write(i+1,6,ListOFFreeCashFlowChangePercentage)
    

outWorkbook.close()

