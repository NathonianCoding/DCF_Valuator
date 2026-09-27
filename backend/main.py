from services.forecast import forecast
from services.data import financials
from fastapi import *
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from scipy.stats import truncnorm
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class AssumptionData(BaseModel):

    forecast_years:int
    

def get_truncated_normal(mean=0, sd=1, low=float("-inf"), upp=float("inf"), size=1):
    return truncnorm.rvs(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd, size=size)

# simulate: wacc, revenue_growth, risk_free_rate, terminal_growth_rate, equity_risk_prem, cost_of_debt
@app.post("/api/valuation")
async def calcStockValue(stock:str, assumed:AssumptionData): 
    
    
    try:
        fin = financials.Financials(stock)
    except:
        raise HTTPException(status_code = 404, detail = f"Failed to load data for {stock}")
    fin_report = fin.load() # stores dictionary of metrics for every year
   
    ebit_margin, da_portion, capex_portion, working_capital_portion = forecast.getMargins(fin_report.items())
    prev_year_data = list(fin_report.items())[0][1]
    valuations = [] 
    variables = []
    value = None
    print(fin.beta)
    waccs = []
    for epoch in range(10000):
    
        risk_free_rate = get_truncated_normal(mean=0.04,sd=0.005,low=0)[0]
        terminal_growth_rate = get_truncated_normal(mean=0.02, sd=0.005, low=0, upp=0.025)[0]
        
        equity_risk_premium = get_truncated_normal(mean=0.05, sd=0.01, low=0)[0]
        cost_of_debt = get_truncated_normal(mean=0.05, sd=0.01, low=0)[0]
        revenue_growth = get_truncated_normal(0.1, sd=0.03, low=0, size=assumed.forecast_years)
        #wacc = get_truncated_normal(mean=0.054, sd=0.01)[0]
        fcff = forecast.getFutureFCFFs(assumed.forecast_years, revenue_growth, prev_year_data["Tax Rate For Calcs"], 
                                    prev_year_data["Total Revenue"], prev_year_data["Working Capital"], 
                                    ebit_margin, da_portion, capex_portion, working_capital_portion)

        wacc = forecast.getWACC(prev_year_data, risk_free_rate,fin.beta/100, 
                                 equity_risk_premium, prev_year_data["Tax Rate For Calcs"], 
                                 fin.share_price, fin.shares_outstanding, cost_of_debt)
        waccs.append(wacc)
        value = forecast.getInstrinsicValues(wacc, fcff, prev_year_data["Total Debt"], 
                                            fin.shares_outstanding, terminal_growth_rate)["Value per stock"]
        valuations.append(float(value))
        # avg revenue growth, risk_free_rate, terminal_growth_rate, equity_risk_prem, cost_of_debt, valuation
        variables.append([wacc, (sum(revenue_growth)/assumed.forecast_years).item(), risk_free_rate, 
                        terminal_growth_rate, equity_risk_premium, cost_of_debt, float(value)])
    vars = np.array(variables)
   
    df = pd.DataFrame(vars, columns = ['wacc','Growth YoY', 'risk_free_rate', 'terminal_growth_rate',
                                       'equity_risk_prem', 'cost_of_debt', 'valuation'])
    
    correlations = df.corr()['valuation']
    valuations.sort()
    print("share price", fin.share_price)
    print("wacc range", min(waccs), max(waccs))
    print("IQR", np.percentile(valuations, 25), np.percentile(valuations, 75))
    print("Undervalued", np.mean(np.array(valuations)>float(fin.share_price))*100)
    print(correlations)
    # print(np.percentile(valuations,25), np.percentile(valuations, 75))
    #print(correlations.to_numpy())
    if value == 'nan':
        raise HTTPException(status_code = 404, detail = f"Data Missing from scraper")
    return {"valuations":valuations, "price": fin.share_price}


@app.get("/api/stock_prices/{ticker}")
async def getStockPrices(ticker:str):
    try:
        fin = financials.Financials(ticker)
        return {"stock_prices": fin.stock_price_snapshot}
    except:
        raise HTTPException(status_code=404, detail=f"Failed to load data for {ticker}")





   
