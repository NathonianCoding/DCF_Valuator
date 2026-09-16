from services.forecast import forecast
from services.data import financials
from services.assumptions import assumptions
from fastapi import *
from pydantic import BaseModel
app = FastAPI()

assumed = assumptions.DCFAssumptions(5, [0.1,0.2,0.1,0.3,0.2], 0.02, 0.07, 0.03,0.03)

@app.get("/{stock}")
async def getStockValue(stock:str): 
    try:
        fin = financials.Financials(stock)
    except:
        raise HTTPException(status_code = 404, detail = f"Failed to load data for {stock}")
    fin_report = fin.load() # stores dictionary of metrics for every year

    ebit_margin, da_portion, capex_portion, working_capital_portion = forecast.getMargins(fin_report.items())
    prev_year_data = list(fin_report.items())[0][1]

    fcff = forecast.getFutureFCFFs(5, assumed.revenue_growth, prev_year_data["Tax Rate For Calcs"], 
                                   prev_year_data["Total Revenue"], prev_year_data["Working Capital"], 
                                   ebit_margin, da_portion, capex_portion, working_capital_portion)

    wacc = forecast.getWACC(prev_year_data, assumed.risk_free_rate,fin.beta, 
                            assumed.equity_risk_premium, prev_year_data["Tax Rate For Calcs"], 
                            fin.share_price, fin.shares_outstanding, assumed.cost_of_debt)

    response = forecast.getInstrinsicValues(wacc, fcff, prev_year_data["Total Debt"], fin.shares_outstanding, assumed.terminal_growth_rate)
    print(list(response.values()))
    if 'nan' in list(response.values()):
        raise HTTPException(status_code = 404, detail = f"Data Missing from scraper")
    return {"valuations":response, "stock_snapshot": fin.stock_price_snapshot}

class AssumptionData(BaseModel):

    forecast_years:int
    revenue_growth:list 
    risk_free_rate:float 
    equity_risk_premium:float 
    terminal_growth_rate:float
    cost_of_debt:float

@app.post("/modify_assumption")
async def changeAssumptions(assumptions: AssumptionData):
    input = (assumptions.forecast_years, assumptions.revenue_growth, assumptions.risk_free_rate, 
             assumptions.equity_risk_premium, assumptions.terminal_growth_rate, assumptions.cost_of_debt)
    try:
        (assumed.forecast_years, assumed.revenue_growth, 
        assumed.risk_free_rate, assumed.equity_risk_premium, 
        assumed.terminal_growth_rate) = input
    except:
        HTTPException(500, detail="Server Failed")
   
