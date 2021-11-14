#imports pdblp which allows for directly pulling bloomberg api values into data frames. 
#pdblp needs to be installed using "pip install pdblp". User needs active bloomberg terminal/api access to use this feature
import pdblp
import pandas as pd
import csv
from pathlib import Path

def run_all_data():
    
    #set the start date and end date
    start_date='20191101'
    end_date='20211231'

    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Stock_Prices_20211102.csv"),start_date, end_date,"PX LAST")
    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Call_Volume_20211102.csv"),start_date, end_date,"volume_total_call")
    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Put_Volume_20211102.csv"),start_date, end_date,"volume_total_put")
    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Market_Cap_20211102.csv"),start_date, end_date,"cur_mkt_cap")
    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Open_Interest_20211102.csv"),start_date, end_date,"put_call_open_interest_total")
    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Short_Interest_20211102.csv"),start_date, end_date,"si_percent_equity_float")
    data_bdh_list(Path("./data/Tickers.csv"),Path("./data/Free_Float_20211102.csv"),start_date, end_date,"eqy_free_float_pct")
    
    data_bdh_single("SPY",Path("./data/SPY_Price_20211102.csv"),start_date, end_date,"PX LAST")
    
    data_bdp_list(Path("./data/Tickers.csv"),Path("./data/Sectors_20211102.csv"),"GICS SECTOR NAME")
    data_bdp_list(Path("./data/Tickers.csv"),Path("./data/Subsectors_20211102.csv"),"GICS INDUSTRY NAME")


    
def data_bdh_list(tickers_path, save_path, start_date, end_date, bbg_field):
    
    #initiate pdblp. debug=True will print out how we are interacting with bloomberg api in case of errors
    con = pdblp.BCon(debug=False, port=8194, timeout=5000000)    
    con.start()
    
    #pull tickers and store in a list
    with open(tickers_path, "r") as csvfile:
        ticker_list = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Read the CSV data
        for row in csvreader:
            ticker_list.append(row)

    #ticker_list is a list of lists. Remove the list from list of lists
    ticker_list = ticker_list[0]
    
    #append " US EQUITY" to bloomberg api ticker format. we create a new list that is a copy so that we can rename our headers with the original text format
    bdh_list = ticker_list.copy()

    for x in range(len(bdh_list)):
        bdh_list[x] = ticker_list[x] + " US EQUITY"
    
    #pull bloomberg data into dataframe
    data_df=con.bdh(bdh_list, bbg_field, start_date, end_date)
    
    #create empty list to populate
    new_label =[]
    
    #loop through and remove " US EQUITY" from each individual column label and add to new_label list
    for column in data_df:
        column = column[0].split()[0]
        new_label.append(column)
    
    #rename the column labels without " US EQUITY"
    data_df.set_axis(new_label,axis=1,inplace=True)
    
    #print data to csv
    data_df.to_csv(save_path)

def data_bdh_single(ticker, save_path, start_date, end_date, bbg_field):
    
    #initiate pdblp. debug=True will print out how we are interacting with bloomberg api in case of errors
    con = pdblp.BCon(debug=False, port=8194, timeout=5000000)    
    con.start()
    
    
   #place the ticker input into the list to plug bloomberg data pull
    ticker_list = []
    ticker_list.append(ticker)
    
    #append " US EQUITY" to bloomberg api ticker format. we create a new list that is a copy so that we can rename our headers with the original text format
    bdh_list = ticker_list.copy()

    for x in range(len(bdh_list)):
        bdh_list[x] = ticker_list[x] + " US EQUITY"
    
    #pull bloomberg data into dataframe
    data_df=con.bdh(bdh_list, bbg_field, start_date, end_date)
    
    #create empty list to populate
    new_label =[]
    
    #loop through and remove " US EQUITY" from each individual column label and add to new_label list
    for column in data_df:
        column = column[0].split()[0]
        new_label.append(column)
    
    #rename the column labels without " US EQUITY"
    data_df.set_axis(new_label,axis=1,inplace=True)
    
    #print data to csv
    data_df.to_csv(save_path)
    
def data_bdp_list(tickers_path, save_path, bbg_field):
    
    #initiate pdblp. debug=True will print out how we are interacting with bloomberg api in case of errors
    con = pdblp.BCon(debug=False, port=8194, timeout=5000000)    
    con.start()
    
    #pull tickers and store in a list
    with open(tickers_path, "r") as csvfile:
        ticker_list = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Read the CSV data
        for row in csvreader:
            ticker_list.append(row)

    #ticker_list is a list of lists. Remove the list from list of lists
    ticker_list = ticker_list[0]
    
    #append " US EQUITY" to bloomberg api ticker format. we create a new list that is a copy so that we can rename our headers with the original text format
    bdh_list = ticker_list.copy()

    for x in range(len(bdh_list)):
        bdh_list[x] = ticker_list[x] + " US EQUITY"
    
    #pull bloomberg data into dataframe
    data_df=con.ref(bdh_list, bbg_field)
    
    #remove extra data columns
    data_df=data_df.iloc[:,[0,2]]

    #loop through rows and remove " US EQUITY" from ticker
    for i in range(len(data_df)):
        data_df.iloc[i][0] = data_df.iloc[i][0].split()[0]
   
    #Transpose and set tickers as column headers
    #data_df=data_df.transpose()
    #data_df.columns=data_df.iloc[0]
    #data_df.drop(data_df.index[0])
    
    #print data to csv
    data_df.to_csv(save_path)