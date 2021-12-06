
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.alphavantage import AlphaVantage
import requests
import xlsxwriter




api_key='8JB4V49M6EBPR459'

#print(api_key)


url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=MSFT&apikey=8JB4V49M6EBPR459'
r = requests.get(url)
data = r.json()

#print(data)

url2 = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=MSFT&apikey=8JB4V49M6EBPR459'
r2 = requests.get(url2)
data2 = r2.json()

#print(data2)

url3 = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=MSFT&apikey=8JB4V49M6EBPR459'
r3 = requests.get(url3)
data3 = r3.json()

#print(data3)

url4 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=MSFT&apikey=8JB4V49M6EBPR459'
r4 = requests.get(url4)
data4 = r4.json()

#print(data4)

ListOfTotalSales = []
ListOfROIC = []
ListOFEPS =[]
ListOFTotalShareholderEquity = []
ListOFFreeCashFlow = []

xx = len(data2['annualReports'])


print('Company','|','Year','|','ROIC','|', 'Revenue growth YtY', '|', "EPS Growth", '|','Total Shareholders Equity', '|', 'Free Cash Flow Change' )

for i in range (xx):
    NetIncome = float((data['annualReports'][i]['netIncome']))
    CommonStockSharesOutstanding = int((data3['annualReports'][i]['commonStockSharesOutstanding']))
    EPS = NetIncome/CommonStockSharesOutstanding
    TotalShareholderEquity = float((data3['annualReports'][i]['totalShareholderEquity']))
    CapitalExpenditures = float((data2['annualReports'][i]['capitalExpenditures']))
    OperatingCashflow = float((data2['annualReports'][i]['operatingCashflow']))
    FreeCashFlow = OperatingCashflow - CapitalExpenditures
    OCF = float(data2['annualReports'][i]['operatingCashflow'])
    TotalRevenue = float((data['annualReports'][i]['totalRevenue']))
    CostOfRevenue = float((data['annualReports'][i]['costOfRevenue']))
    MyGrossProfit = TotalRevenue - CostOfRevenue
    GrossProfit = float((data['annualReports'][i]['grossProfit']))
    IncomeBeforeTax = float((data['annualReports'][i]['incomeBeforeTax']))
    OperatingIncome = float((data['annualReports'][i]['operatingIncome']))
    IncomeTaxExpense = float((data['annualReports'][i]['incomeTaxExpense']))
    Tax_Rate = IncomeTaxExpense/IncomeBeforeTax
    Tax_Rate_Percentage = "{:.0%}".format(Tax_Rate)
    NOPAT=OperatingIncome*(1-Tax_Rate)    
     
    ShortTermDebt = float((data3['annualReports'][i]['shortTermDebt']))
    LongTermDebt = float((data3['annualReports'][i]['longTermDebt']))
    TotalShareholderEquity = float((data3['annualReports'][i]['totalShareholderEquity']))
   
    InvestedCapital = ShortTermDebt + LongTermDebt + TotalShareholderEquity
    
    ROIC = NOPAT/InvestedCapital
    ROIC_percentage = "{:.0%}".format(ROIC)

    #print(data2['annualReports'][i]['fiscalDateEnding'],'IncomeTaxExpense/${0}'.format(format(IncomeTaxExpense, ',.2f')),'/','IncomeBeforeTax/${0}'.format(format(IncomeBeforeTax, ',.2f')),'OperatingIncome ${0}'.format(format(OperatingIncome, ',.2f')))
    
    #print(data2['annualReports'][i]['fiscalDateEnding'],'operatingCashflow ${0}'.format(format(OCF, ',.2f')),'totalRevenue ${0}'.format(format(TotalRevenue, ',.2f')),'CostOfRevenue ${0}'.format(format(CostOfRevenue, ',.2f')),'GrossProfit ${0}'.format(format(GrossProfit, ',.2f')),'IncomeBeforeTax ${0}'.format(format(IncomeBeforeTax, ',.2f')),'OperatingIncome ${0}'.format(format(OperatingIncome, ',.2f')),'IncomeTaxExpense ${0}'.format(format(IncomeTaxExpense, ',.2f'))) 
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
    print(data['symbol'],data2['annualReports'][i]['fiscalDateEnding'],ListOfROIC[i],TotalRevenuePercentageYtY,TotalEPSChangePercentage,TotalShareholderEquityChangePercentage,ListOFFreeCashFlowChangePercentage)
    outSheet.write(i+1,0,data['symbol'])
    outSheet.write(i+1,1,data2['annualReports'][i]['fiscalDateEnding'])
    outSheet.write(i+1,2,ListOfROIC[i])
    outSheet.write(i+1,3,TotalRevenuePercentageYtY)
    outSheet.write(i+1,4,TotalEPSChangePercentage)
    outSheet.write(i+1,5,TotalShareholderEquityChangePercentage)
    outSheet.write(i+1,6,ListOFFreeCashFlowChangePercentage)
    

outWorkbook.close()