import yfinance as yf
from collections import defaultdict
import numpy as np
from numpy import nan
class Financials:


    def __init__(self, stock):
        try:
            ticker = yf.Ticker(stock)
        except:
            raise f"{stock} couldn't be found"

        self.financials_df = ticker.financials
        

        stock_price_variations = ticker.history(period="1d", interval = "1h")
        timestamps = stock_price_variations.index.to_list()
        self.stock_price_snapshot = {timestamps[i].ctime():f"{lst[3]:.2f}" for i,lst in enumerate(stock_price_variations.to_numpy())}
        

        self.cashflow_df = ticker.cashflow
        self.balance_sheet_df = ticker.balance_sheet
        self.financials_arr = self.financials_df.to_numpy()
        self.cashflow_arr = self.cashflow_df.to_numpy()
        self.balance_sheet_arr = self.balance_sheet_df.to_numpy()

        self.beta = ticker.info['beta']
        self.share_price = ticker.info['currentPrice']
        self.shares_outstanding = ticker.info["sharesOutstanding"]
        self.financial_history=defaultdict(dict) # {timestamp:{revenue:val, ebit:ebit, taxrate:rate }}




    # returns a hashmap with the row index of each metrix in the dataframe

    def getRowIndices(self, df, index_dict):
        row_headers = df.index.to_list()
        for i in range(len(row_headers)):
            for metric in index_dict:
                if row_headers[i] == metric:
                    index_dict[metric] = i
        return index_dict

    
    # stores metrics under each timestamp in a hashmap
    def getMetrics(self,df,dataset_as_array, index_dict, history):
        # reads data between 2023 and 2026
        for i in range(len(df.columns)):
            timestamp = df.columns[i]
            for rowHeader in index_dict:

                index=index_dict[rowHeader]
                if index and dataset_as_array[index][i]!= np.float64("nan"):
                    history[timestamp][rowHeader] = dataset_as_array[index][i]
        return history

    def load(self):
        rev_index_dict = self.getRowIndices(self.financials_df, {"Total Revenue": None, "EBIT":None, "Tax Rate For Calcs":None})
        cashflow_index_dict = self.getRowIndices(self.cashflow_df, {"Depreciation And Amortization":None, "Capital Expenditure":None})
        balance_index_dict = self.getRowIndices(self.balance_sheet_df, {"Total Debt": None, "Cash And Cash Equivalents":None, "Working Capital":None})
        self.financial_history = self.getMetrics(self.financials_df,self.financials_arr, rev_index_dict, self.financial_history)
        self.financial_history = self.getMetrics(self.cashflow_df, self.cashflow_arr, cashflow_index_dict, self.financial_history)
        self.financial_history = self.getMetrics(self.balance_sheet_df, self.balance_sheet_arr, balance_index_dict, self.financial_history)

        #removes years with missing values
        yearsToRemove = []
        for key in self.financial_history:
            values = list(map(lambda x: str(x.item()), self.financial_history[key].values()))
            
            if 'nan' in values:
                yearsToRemove.append(key)
        for keyToRemove in yearsToRemove:
            self.financial_history.pop(keyToRemove)


        history_items = list(self.financial_history.items())

        for count in range(len(history_items)-1):
        
            self.financial_history[history_items[count][0]]["Change in Net Working Capital"] = history_items[count][1]["Working Capital"] - history_items[count+1][1]["Working Capital"]

        if self.financial_history:
            self.financial_history.pop(history_items[count+1][0]) # removes earliest year as it has no change in net working capital
        return self.financial_history
if __name__ == "__main__":
    x=Financials("AMZN")
    print(x.load())